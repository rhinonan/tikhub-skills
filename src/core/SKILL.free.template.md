---
name: {{name}}
description: {{description}}
version: {{version}}
category: data-acquisition
author: 接口索引整理；接口文档与 API 版权归 TikHub.io 所有
license: 脚本与文档结构可自由使用；接口文档内容版权归 TikHub.io，使用需遵守其服务条款
agent_created: true
---

# {{platform_zh}}数据接口（TikHub）

接口来自 TikHub.io 文档站，只保留**{{platform_zh}}相关**（{{count}} 个，含免鉴权 Demo 与多平台解析）。清单已固化在 `references/`，不用每次翻文档。

> 本版本**自备 API Key**：用你自己的 TikHub API Token 直连官方接口，本 skill 不代收任何费用。TikHub 的起充额度为 **5 美元**；不想充值可使用同平台的 Pro 版（`{{name}}-pro`），按次付费、无需自备 Token。

## 0. 先自检（30 秒，强烈建议）

```bash
python3 scripts/tikhub.py doctor          # 环境/清单/文档/凭证一次看完
python3 scripts/tikhub.py doctor --net    # 连网络一起测
```

看到 `[OK] 环境、清单、文档都齐` 再往下做；有 `[FAIL]` 就按提示修（多数是清单缺失或包没解压全）。

**运行环境三条约定**，按这个来能省掉绝大多数"命令直接报错"：

1. **解释器**：优先 `python3`，老环境用 `python`（脚本兼容 3.8+，版本太低会自己报错退出）。
2. **工作目录**：脚本用自身路径定位清单，任意目录都能跑；但不确定 cwd 时请用**绝对路径**调用，
   如 `python3 /path/to/{{name}}/scripts/tikhub.py search 评论`，避免 `scripts/tikhub.py: No such file`。
3. **清单坏了也能干活**：`references/inventory.json` 缺失/损坏时，`search`/`show` 会自动降级扫
   `references/*.md`；`call` 只要给完整 path 依旧能直连。所以"目录报错"不等于整个 skill 不可用。

## 何时使用

- 要拿{{platform_zh}}的{{scope}}。
- 想确认"某个{{platform_zh}}数据有没有现成接口、参数怎么传、是 GET 还是 POST"。

**不适用**：其他平台（本 skill 只收{{platform_zh}}）；发内容、点赞、登录等写操作（TikHub 不提供）。

## 一次性准备：Token

```bash
python3 scripts/tikhub.py token <你的token>   # 存到 ~/.workbuddy/tikhub_token
python3 scripts/tikhub.py token              # 查看是否已配置
python3 scripts/tikhub.py ping               # 验证 token 是否可用
```

- Token 在 https://user.tikhub.io 的 API token 菜单生成，请求头 `Authorization: Bearer <token>`。
- 也读环境变量 `TIKHUB_API_KEY`（优先级最高）。
- **没 token 也能先跑通链路**：`Demo-API` 的 `/api/v1/demo/...` 接口免鉴权、返回固定数据、1 小时缓存。

## 三步工作流

```bash
# ① 找接口：中文名/英文名/路径/用途 模糊搜索（多关键词按 AND，搜不到会自动放宽并给相近项）
python3 scripts/tikhub.py search 评论 回复

# ② 看参数：完整 path 最好；只给 web/fetch_video_comments 这种后缀也能唯一命中
python3 scripts/tikhub.py show {{api_prefix}}/web/fetch_video_comments

# ③ 调接口（GET 用 -q，POST 用 -b）
python3 scripts/tikhub.py call {{api_prefix}}/web/fetch_video_comments \
  -q aweme_id=7372484719365098803 --out out/comments.json
```

三条实用开关，能省掉大部分调试和冤枉钱：

| 开关 | 作用 | 什么时候用 |
|---|---|---|
| `--dry-run` | 只打印最终 URL / headers / body，**不发请求不计费** | 参数没把握、POST 接口、批量前核对 |
| `--retry N` | 网络错误 / 429 / 5xx 自动退避重试（默认 2，`0` 关闭） | 网络不稳、限流 |
| `--force` | 必填参数缺失时仍然发送（默认**本地拦截**） | 确认文档的必填标记有误时 |

- **自动补全**：分页类参数（`cursor`/`max_cursor`/`page`/`count`/`page_size`/`offset`）没传时，
  CLI 会按接口默认值补上并打印 `[autofill]`，不用一个个手填。
- **调用前预检**：必填参数缺失会在本地拦住（不消耗额度），直接列出该补哪个参数。
- 大响应必须加 `--out 路径`（目录不存在会自动创建），只把必要字段读进上下文，别把整份 JSON 塞进对话。
- 分类浏览：`python3 scripts/tikhub.py list --folder {{folder_example}}`。

{{platform_body}}

## 分类索引

共 {{count}} 个接口。按分类查 → 打开对应参考文件；不确定用什么接口 → `python scripts/tikhub.py search <关键词>`。

{{index_table}}

导航：`references/index.md`；单行速查表：`references/api-index.md`；机器可读：`references/inventory.json`。
清单校准至 2026-11-10（接口数 {{count}}）；若与线上文档有出入，以 `show` 的参数表和实际返回为准。

## 常见问题（FAQ）

**Q1：`python scripts/tikhub.py` 报"找不到文件 / No such file"？**
A：要么 cwd 不在 skill 根目录，要么环境里只有 `python3`。用绝对路径 + `python3`：
`python3 <skill目录>/scripts/tikhub.py doctor`。

**Q2：报"接口清单无法读取 / 找不到 inventory.json"？**
A：skill 包没解压全。`references/` 里应有 `inventory.json`（约 400KB）+ 12 个分类 md。
此时 `search`/`show` 已自动降级扫 md，`call` 给完整 path 仍可用；彻底修就重新解压或 `build.py` 重建。

**Q3：`show` 出来一堆候选、看不到参数？**
A：说明关键词太宽。用完整 path，或给更长的后缀（`web/fetch_video_comments`）。
现在 `show` 即使命中多条，也会先打印最匹配那条的完整参数，其余作为候选列出。

**Q4：`call` 报 422？**
A：必填参数没传或类型不对。CLI 会打印字段级原因；`show <path>` 能看到完整参数表。
分页类参数已自动补默认值，仍 422 多半是 id/cookie 这类必须自己给的值。

**Q5：没 token 能不能先试用？**
A：能。`Demo-API` 三个 `/api/v1/demo/...` 接口免鉴权、返回固定样例数据，
拿来验证 CLI、字段结构和下游解析都够用。

**Q6：怎么确认"这次调用花了多少 / 还剩多少"？**
A：`GET /api/v1/tikhub/user/get_user_daily_usage`（当日用量）、
`GET /api/v1/tikhub/user/get_user_info`（`data.user_data.balance` 余额）。
批量前先 `--dry-run` 核参，再串行跑，别一上来就并发。

**Q7：返回 200 但 `data` 是空的？**
A：先看 `filter_detail`（作品已删/受限）和榜单的 `type=snapshot` 命中问题，见上文"已知坑"。

## 错误处理

| 现象 | 含义 | 处理 |
|---|---|---|
| `python: command not found` | 环境只有 python3 | 换成 `python3 scripts/tikhub.py` |
| `scripts/tikhub.py: No such file` | cwd 不对 | 用绝对路径调用，或先 `cd` 到 skill 根目录 |
| 清单/目录读不到 | 包不完整 | 跑 `doctor` 看缺什么；`search/show` 已可降级，`call` 用完整 path |
| 401 | token 无效/缺失 | 提示用户配 token，不要重试 |
| 402 | TikHub 余额不足 | 换免费 Demo，或告知用户充值 |
| 403 | 权限/账号异常 | 账号停用或邮箱未验证 |
| 404 | 路径错 | CLI 会自动给相近 path；用 `show` 校正 |
| 422 | 参数缺失/类型错 | CLI 列出缺哪个参数，补上再调 |
| 429 | 限流 | 并发降到 ≤2；`--retry` 已自动退避，仍失败等 30s |
| 5xx | 服务端错误 | 已自动重试；持续失败换同类通道（Web → App V3） |
| 网络超时 | 本地网络/代理 | `doctor --net` 自检；调大 `--timeout`，`--retry 3` |

## 输出与合规

- 先抓 1~2 条确认字段结构，再批量；批量串行或并发 ≤3，中间结果落盘。
- 只采集公开数据用于分析/研究，不用于批量私信、骚扰、隐私挖掘；遵守 TikHub 与各平台条款。
- 按次计费：响应里 `cache_url` 是 24h 免费缓存链接；已删除/受限作品仍返回 HTTP 200 + `filter_detail`，**照样计费**，批量前先抽样。
- 结果默认写当前工作区（如 `报告/`、`data/`），文件名带日期+关键词。
- 查用量：`GET /api/v1/tikhub/user/get_user_daily_usage`；查余额：`GET /api/v1/tikhub/user/get_user_info`。
