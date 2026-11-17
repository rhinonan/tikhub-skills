---
name: {{name}}
description: {{description}}
version: {{version}}
category: data-acquisition
author: 接口索引整理；接口文档与 API 版权归 TikHub.io 所有
license: 脚本与文档结构可自由使用；接口文档内容版权归 TikHub.io
agent_created: true
---

# {{platform_zh}}数据接口（TikHub · 付费版）

接口来自 TikHub.io，只保留**{{platform_zh}}相关**（{{count}} 个）。清单已固化在 `references/`，不用每次翻文档。

> 本版本是**付费版**：**不需要注册 TikHub，也不需要充 $5**。按次付费：标准档 **¥0.10/次**、高价值档 **¥0.50/次**、批量档 **¥2.00/次**；任务包 ¥1.99，额度包 ¥9.90。调用时脚本会自动处理 402 付款，付款完成后自动重试并返回数据。

## 何时使用

- 要拿{{platform_zh}}的{{scope}}，但不想为一次调用去注册 TikHub 并充值。
- 想确认"某个{{platform_zh}}数据有没有现成接口、参数怎么传、是 GET 还是 POST"。

**不适用**：其他平台（本 skill 只收{{platform_zh}}）；发内容、点赞、登录等写操作（TikHub 不提供）。

## 0. 先自检（30 秒，强烈建议）

```bash
python3 scripts/tikhub.py doctor          # 环境/清单/文档/凭证一次看完
python3 scripts/tikhub.py doctor --net    # 连网络（网关连通性）一起测
```

看到 `[OK] 环境、清单、文档都齐` 再往下做；有 `[FAIL]` 按提示修（多数是包没解压全）。

**运行环境三条约定**：

1. **解释器**：优先 `python3`，老环境用 `python`（脚本兼容 3.8+）。
2. **工作目录**：脚本用自身路径定位清单，任意目录都能跑；不确定 cwd 时用**绝对路径**调用，
   如 `python3 /path/to/{{name}}/scripts/tikhub.py search 评论`。
3. **清单坏了也能干活**：`references/inventory.json` 缺失/损坏时，`search`/`show` 自动降级扫
   `references/*.md`；`call` 给完整 path 仍可调用。

## 一次性准备：支付依赖

```bash
python3 scripts/tikhub.py ping                # 验证网关连通
```

- 不需要注册 TikHub，也不需要预充值；每次调用单独付款（标准 ¥0.10 / 高价值 ¥0.50 / 批量 ¥2.00）。也可以购买额度包：`python3 scripts/tikhub.py recharge`（¥9.90 / 200 credits，按接口档位约 10–200 次）。
- 买家侧需要支付依赖（`alipay-bot`，由 `npx -y @alipay/agent-payment@latest install` 安装，需要 Node.js ≥ 18）。缺了支付依赖会明确报错，不会静默失败。
- 付款由脚本自动编排：首次调用返回 402，脚本唤起支付宝付款，拿到 `Payment-Proof` 后自动重试同一请求。

## 查询额度

```bash
python3 scripts/tikhub.py balance              # 剩余 credits、累计购买/消耗/退款
python3 scripts/tikhub.py usage --limit 20     # 最近调用明细（档位、扣减、状态、路径）
```

- 两个命令都是只读，不产生费用。
- 只有购买过额度包并保存了账户 token 后才能查询。

## 三步工作流

```bash
# ① 找接口：中文名/英文名/路径/用途 模糊搜索（本地检索，不花钱）
python3 scripts/tikhub.py search 评论 回复

# ② 看参数：完整 path 或唯一关键词（本地查询，不花钱）
python3 scripts/tikhub.py show {{api_prefix}}/web/fetch_video_comments

# ③ 调接口（GET 用 -q，POST 用 -b）—— 这一步按次付费
python3 scripts/tikhub.py call {{api_prefix}}/web/fetch_video_comments \
  -q aweme_id=7372484719365098803 -q cursor=0 -q count=20 --out out/comments.json
```

首次调用会提示付款，支付宝付款完成后脚本自动重试并返回数据：

```
需要按次付款：社媒数据查询（标准）  ¥0.10
（付款完成后自动重试，无需再次执行）
```

- `search` / `show` / `list` 都是本地索引，**不产生费用**，可以放心多查。
- 大响应必须加 `--out 路径`（目录不存在会自动创建），只把必要字段读进上下文。
- 分类浏览：`python3 scripts/tikhub.py list --folder {{folder_example}}`。

**省钱三件套**（付费版尤其重要）：

| 开关 | 作用 |
|---|---|
| `--dry-run` | 打印最终请求（URL/headers/body），**不发送、不扣费**——付款前先核一遍参数 |
| `--retry N` | 网络错误 / 429 / 5xx 自动退避重试（默认 2，`0` 关闭） |
| `--force` | 必填参数缺失时仍然发送（默认本地拦截，避免花钱买 422） |

分页类参数（`cursor`/`page`/`count`/`page_size`/`offset`）没传时会自动补默认值并打印 `[autofill]`。

## 计费规则

| 档位 | 每次价格 | 当前状态 |
|---|---|---|
| 标准档（详情/用户/搜索等普通查询） | ¥0.10 | 已开放 |
| 高价值端点（算数指数/星图/榜单） | ¥0.50 | 已开放 |
| 批量端点 | ¥2.00 | 已开放 |
| 任务包（账号数据分析） | ¥1.99 | 已开放 |
| 额度包（10–200 次） | ¥9.90 | 已开放 |

- 每次调用单独付款，无订阅、无最低充值门槛。
- **上游失败不产生费用**：网关返回 502 时未完成履约，可直接重试。
- 付款后带 `Payment-Proof` 重试同一请求不会重复扣费。

{{platform_body}}

## 分类索引

共 {{count}} 个接口。按分类查 → 打开对应参考文件；不确定用什么接口 → `python3 scripts/tikhub.py search <关键词>`。

{{index_table}}

导航：`references/index.md`；单行速查表：`references/api-index.md`；机器可读：`references/inventory.json`。
清单校准至 2026-11-10（接口数 {{count}}）；若与线上文档有出入，以 `show` 的参数表和实际返回为准。

## 错误处理

| 现象 | 含义 | 处理 |
|---|---|---|
| `python: command not found` | 环境只有 python3 | 换成 `python3 scripts/tikhub.py` |
| `scripts/tikhub.py: No such file` | cwd 不对 | 用绝对路径调用，或先 `cd` 到 skill 根目录 |
| 清单/目录读不到 | 包不完整 | 跑 `doctor` 看缺什么；`search/show` 可降级扫 md，`call` 用完整 path 仍可用 |
| 402 | 需要付款 | 脚本会自动唤起支付宝付款并重试；中断时可用 `--proof` 手动重试 |
| 403 | 接口未开放 | 联系提供方 |
| 404 | 路径错 | CLI 会自动给相近 path；用 `show` 校正 |
| 422 | 参数缺失/类型错 | CLI 会直接列出缺哪个参数，补上再调 |
| 429 | 限流 | 并发降到 ≤2；`--retry` 已自动退避 |
| 502 | 上游失败 | 本次未计费，直接重试；持续失败换同类通道 |
| 网络超时 | 本地网络/代理 | `doctor --net` 自检；调大 `--timeout`，`--retry 3` |

## 输出与合规

- 先抓 1~2 条确认字段结构，再批量；批量串行或并发 ≤3，中间结果落盘。
- 只采集公开数据用于分析/研究，不用于批量私信、骚扰、隐私挖掘。
- 按次付费，批量前先估算调用次数；`search`/`show` 不产生费用，可以先想明白再调。
- 结果默认写当前工作区（如 `报告/`、`data/`），文件名带日期+关键词。
