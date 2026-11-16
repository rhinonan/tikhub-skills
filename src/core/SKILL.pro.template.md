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

> 本版本是**付费版**：**不需要注册 TikHub，也不需要充 $5**。按次扣额度，几毛钱一次，用完再充。

## 何时使用

- 要拿{{platform_zh}}的{{scope}}，但不想为一次调用去注册 TikHub 并充值。
- 想确认"某个{{platform_zh}}数据有没有现成接口、参数怎么传、是 GET 还是 POST"。

**不适用**：其他平台（本 skill 只收{{platform_zh}}）；发内容、点赞、登录等写操作（TikHub 不提供）。

## 一次性准备：额度

```bash
python scripts/tikhub.py recharge            # 支付宝扫码充值，成功后自动保存账户 token
python scripts/tikhub.py token               # 查看是否已配置
python scripts/tikhub.py ping                # 验证网关连通
```

- 充值走支付宝扫码，**每次调用单独计费**，额度用完再充，没有订阅、没有最低充值门槛。
- 账户 token 存在 `~/.workbuddy/tikhub_gateway_token`，换机器要重新充值。
- 买家侧需要支付依赖（`alipay-bot`，由 `npx -y @alipay/agent-payment@latest install` 安装，需要 Node.js ≥ 18）。缺了 `recharge` 会明确报错，不会静默失败。

## 三步工作流

```bash
# ① 找接口：中文名/英文名/路径/用途 模糊搜索（本地检索，不花钱）
python scripts/tikhub.py search 评论 分页

# ② 看参数：完整 path 或唯一关键词（本地查询，不花钱）
python scripts/tikhub.py show {{api_prefix}}/web/fetch_video_comments

# ③ 调接口（GET 用 -q，POST 用 -b）—— 这一步按次扣额度
python scripts/tikhub.py call {{api_prefix}}/web/fetch_video_comments \
  -q aweme_id=7372484719365098803 -q cursor=0 -q count=20 --out out/comments.json
```

每次成功调用会打印本次消耗与剩余额度：

```
[quota] standard 档，本次扣 1，剩余 199
```

- `search` / `show` / `list` 都是本地索引，**不消耗额度**，可以放心多查。
- 大响应必须加 `--out 路径`，只把必要字段读进上下文。
- 分类浏览：`python scripts/tikhub.py list --folder {{folder_example}}`。

## 计费规则

| 端点类型 | 每次消耗 | 说明 |
|---|---|---|
| 普通查询（详情/用户/搜索） | 1 | 绝大多数接口 |
| 高价值端点（算数指数/星图/榜单） | 5 | 计算与数据成本更高 |
| 批量端点（如 `fetch_multi_video`） | 20 | 一次调用取多条 |

- 额度包与单价以 `recharge` 返回为准。
- **上游失败不扣额度**：网关返回 502 时会自动退回本次消耗，可直接重试。
- 同一个请求重复重试不会重复扣费。

{{platform_body}}

## 分类索引

共 {{count}} 个接口。按分类查 → 打开对应参考文件；不确定用什么接口 → `python scripts/tikhub.py search <关键词>`。

{{index_table}}

导航：`references/index.md`；单行速查表：`references/api-index.md`；机器可读：`references/inventory.json`。

## 错误处理

| 状态 | 含义 | 处理 |
|---|---|---|
| 401 | 账户 token 无效 | 运行 `python scripts/tikhub.py recharge` |
| 402 | 额度不足 | 运行 `python scripts/tikhub.py recharge`，不要盲目重试 |
| 403 | 账户停用/接口未开放 | 联系提供方 |
| 404 | 路径错 | 用 `show` 校正 path |
| 422 | 参数缺失/类型错 | CLI 会直接列出缺哪个参数，补上再调 |
| 429 | 限流 | 并发降到 ≤2，退避重试一次 |
| 502 | 上游失败 | 本次未扣额度，直接重试；持续失败换同类通道 |

## 输出与合规

- 先抓 1~2 条确认字段结构，再批量；批量串行或并发 ≤3，中间结果落盘。
- 只采集公开数据用于分析/研究，不用于批量私信、骚扰、隐私挖掘。
- 按次扣额度，批量前先算清楚要调用多少次；`search`/`show` 不花钱，可以先想明白再调。
- 结果默认写当前工作区（如 `报告/`、`data/`），文件名带日期+关键词。
