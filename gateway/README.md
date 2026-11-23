# gateway

付费版的收款与转发后端。**独立部署，不进 skill 包**——skill 包里只有调用方代码，没有任何密钥。

零第三方依赖，Python 3.9+ 直接跑。真实接入支付宝时再加 `alipay-sdk-python` + `pycryptodome`。

## 为什么必须有这一层

三样东西不能出现在 skill 里（skill 是用户本机明文文件）：

| 不能进 skill | 后果 |
|---|---|
| TikHub 主 Key | 一个人买 = 全网公开 |
| 支付宝应用私钥 | 官方明确要求服务端保存 |
| 订单与验付逻辑 | 官方明确要求后端独立部署 |

用户机器上只留自己的支付宝账号，主 Key 和私钥留在服务器。

## 接口

| 端点 | 用途 | 计费 |
|---|---|---|
| `POST /v1/task` | 任务包，一次付费内部调 N 次上游 | 按任务定价 |
| `POST /v1/recharge` | 额度包，付费换账户 token | 按包定价 |
| `POST /v1/call` | 按次调用；有 token 扣额度，无 token 直接 402 按次收款 | 按端点档位 |
| `GET /v1/balance` | 查询剩余额度、累计购买/消耗/退款（Bearer token） | — |
| `GET /v1/usage` | 查询最近调用明细（Bearer token，`?limit=` 最多 100） | — |
| `GET /healthz` | 健康检查 | — |

`/v1/task` 与 `/v1/recharge` 是标准 A2M 流程：不带 `Payment-Proof` 就返回 402 + `Payment-Needed`，付款后带凭证重试同一请求。

`/v1/call` 有 token 且余额足够时扣额度；没有 token 或余额不足时直接对本次调用返回 402，按档位收款。`/v1/balance` 和 `/v1/usage` 只读，不产生费用。

## 计费档位

TikHub 端点成本差 10 倍以上，不能一个价。网关**优先按上游真实成本**归档，没标价的接口再退回路径正则：

| 档位 | 定价规则 | 计费 | 扣额度 |
|---|---|---|---|
| standard | 成本 ≤ $0.01，或未标价且不命中下方规则 | ¥0.10/次（可单次付款） | 1 |
| premium | $0.01 < 成本 < $0.05，或未标价且路径含 `/index/`、`_index`、`/xingtu`、`billboard`、`huahuo`、`/pgy/`、热榜/榜单词 | 只走额度包（约 ¥0.30） | 6 |
| batch | 成本 ≥ $0.05，或未标价且路径含 `multi_`、`/batch`、`_batch`、`bulk` | 只走额度包（约 ¥1.49） | 30 |

- 标准档额度不足时返回 402 单次账单（¥0.10）；高价值/批量额度不足时返回 402 `CREDITS_REQUIRED`，CLI 会自动购买额度包（¥9.90 / 200 点）后重试，不按次收款。
- 一个额度包 200 点：标准 200 次、高价值 33 次、批量 6 次。

- 成本数据来自 `endpoint_costs.json`：`tools/collect_inventory.py` 以 `pricing/tikhub_pricing_2026-11-23.csv` 为准写入，当前 623 条（7 个平台 630 个接口中仅 7 个无标价）。
- 成本高于 $0.25 的接口现有档位覆盖不了，网关直接返回 503 `ENDPOINT_NOT_AVAILABLE`，避免卖一次亏一次（当前清单里没有这种接口，保留为保护）。
- 一个档位对应一个支付宝 `serviceId`。规则和任务定义都在 `pricing.py`，改价改那里。

**注意：支付宝是一个 serviceId 一个登记价**，所以「任务包 ¥1.99」和「额度包 ¥9.90」不能复用 ¥0.10 的那个服务。网关按**金额**反查 serviceId（`alipay_a2m.SERVICE_ENV_BY_AMOUNT`）。现在实际只会出 3 种账单：0.10（标准按次）/ 1.99（任务包）/ 9.90（额度包）；0.50 / 2.00 作为历史档位保留在映射里，但高价值/批量已改为只走额度包。

## 本地联调

```bash
cd gateway
MOCK_UPSTREAM=1 python tests/mock_server.py
# 另开一个终端
python smoke_test.py
```

全绿输出应该是 `55 通过 / 0 失败`。覆盖了：402 出单、付款后交付、同凭证幂等重试、充值建户与已有账户合并、额度/按次计费（标准 1 点、高价值 6 点、批量 30 点）、成本优先定价（含 CSV 覆盖描述里的错误价格）、高价值/批量不按次出账单、平台白名单（微博放行 / TikTok 拒绝）、余额耗尽回到 402、凭证不能跨资源重放。假验付只存在于 `tests/mock_server.py`，生产 `server.py` 没有 mock 分支。

想手动走一遍：

```bash
# 1. 拿账单
curl -i -X POST localhost:3006/v1/task \
  -H 'Content-Type: application/json' \
  -d '{"task":"douyin_account_analysis","params":{"unique_id":"test"}}'
# 从响应头里取 Payment-Needed 的值

# 2. 模拟支付（真实环境这一步由 alipay-bot 完成）
python mock_pay.py '<Payment-Needed 的值>'

# 3. 带凭证重试
curl -X POST localhost:3006/v1/task \
  -H 'Content-Type: application/json' \
  -H 'Payment-Proof: <上一步输出的值>' \
  -d '{"task":"douyin_account_analysis","params":{"unique_id":"test"}}'
```

## Docker 镜像（GitHub Actions 自动构建）

推到 `main` 或打 `v*` tag 时，`.github/workflows/gateway-docker.yml` 会自动构建并推送到 GHCR：

| 触发 | 镜像 tag |
|---|---|
| push `main` | `latest`、`main`、`sha-<commit>` |
| tag `v1.2.3` | `1.2.3`、`1.2`、`sha-<commit>` |
| PR | 只构建，不推送 |

镜像名：`ghcr.io/<owner>/<repo>-gateway`。首次推送后，在 GitHub 仓库的 Packages 里把包设为 Public，否则部署机需要先 `docker login ghcr.io`。

```bash
docker run -d --name cn-social-data-gateway \
  -p 3006:3006 \
  -v gateway-data:/data \
  --env-file gateway/.env \
  ghcr.io/<owner>/<repo>-gateway:latest
```

**`.env` 里有两项必须按容器改**，否则端口映射不生效 / 数据库不持久：

```bash
HOST=0.0.0.0
DB_PATH=/data/gateway.db
```

密钥建议继续用文件挂载（`ALIPAY_PRIVATE_KEY=/run/secrets/app_private_key.txt`），不要把私钥写进镜像或 `--env`。

## 上线前必须做的替换

| 检查项 | 从 | 到 |
|---|---|---|
| `MOCK_UPSTREAM` | 1 | 0 |
| `ALIPAY_GATEWAY` | 沙箱网关 | `https://openapi.alipay.com/gateway.do` |
| `SERVICE_ID_*` | `api_mock_service_id` | 三个真实 serviceId |
| `ALIPAY_PRIVATE_KEY` | 空 | 生产应用私钥（PKCS#1） |
| 服务地址 | localhost | 公网 HTTPS，**与支付宝登记的完全一致** |
| 三处价格 | 模板价 | 支付宝登记价 = 服务端账单 = SkillHub 展示价 |

少一样都不行。价格不一致是最常见的退单原因。

## 自己实现时最容易踩的坑

这几条是写代码时真踩到的，不是抄来的注意事项：

1. **凭证必须绑定到"当前请求的资源"**。只比较"凭证里的 resource_id"和"订单里的 resource_id"是无效校验——两者天生相等，结果拿 ¥1.99 的任务凭证能白刷 ¥9.9 的额度包。
2. **履约状态会永久卡死**。先提交 `PENDING_CONFIRM` 再生成资源，如果生成过程抛错（包括结果无法序列化），订单会停在"已认领但没有结果"，用户付了钱永远拿不到货。必须保证任何失败都能回退到 `UNFULFILLED`，并且进程崩溃后重试能重新执行。
3. **执行要用订单里存档的参数**，不能用客户端重试时传的。否则付 A 的钱可以取 B 的数据。
4. **上游失败不能算用户头上**。TikHub 429/5xx 时不履约确认、按次调用要退回额度，允许同一凭证重试。
5. **金额校验在生产环境缺失即拒绝**。只有沙箱精确模式下才允许用本地订单金额兜底。
6. **别在长事务里调上游**。SQLite 一次上游调用最长 60 秒，占着写锁会把所有请求堵住。认领和生成要分两段提交。
7. **serviceId 必须按金额查，不能按档位名查**。支付宝一个 serviceId 只有一个登记价，任务包（¥1.99）和额度包（¥9.90）如果复用 ¥0.10 的服务标识，验付时金额对不上，用户付了钱也拿不到东西。

## 已知边界

- SQLite 单机，够用到日均几千单；再往上换 Postgres（`store.py` 是唯一改动点）
- 没有退款接口，`mark_refunded` 只改状态，实际退款要走支付宝商家后台
- 任务定义是声明式的，步骤间靠字段路径引用；上游返回结构一变，引用会失配，需要在 `pricing.py` 里维护
- 验付没有 mock 开关；本地假验付只在 `tests/mock_server.py`，生产镜像不含测试目录
- **订单会留存返回结果**（`result_json`）。这是幂等的代价：不存结果，重试就会重复扣上游额度。当前没有清理机制，建议加一个按 TTL 置空的任务（履约 24 小时后清 `result_json`，保留订单行用于对账）
