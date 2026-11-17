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

## 一次性准备：支付依赖

```bash
python scripts/tikhub.py ping                # 验证网关连通
```

- 不需要注册 TikHub，也不需要预充值；每次调用单独付款（标准 ¥0.10 / 高价值 ¥0.50 / 批量 ¥2.00）。也可以购买额度包：`python scripts/tikhub.py recharge`（¥9.90 / 200 credits，按接口档位约 10–200 次）。
- 买家侧需要支付依赖（`alipay-bot`，由 `npx -y @alipay/agent-payment@latest install` 安装，需要 Node.js ≥ 18）。缺了支付依赖会明确报错，不会静默失败。
- 付款由脚本自动编排：首次调用返回 402，脚本唤起支付宝付款，拿到 `Payment-Proof` 后自动重试同一请求。

## 三步工作流

```bash
# ① 找接口：中文名/英文名/路径/用途 模糊搜索（本地检索，不花钱）
python scripts/tikhub.py search 评论 分页

# ② 看参数：完整 path 或唯一关键词（本地查询，不花钱）
python scripts/tikhub.py show {{api_prefix}}/web/fetch_video_comments

# ③ 调接口（GET 用 -q，POST 用 -b）—— 这一步按次付费
python scripts/tikhub.py call {{api_prefix}}/web/fetch_video_comments \
  -q aweme_id=7372484719365098803 -q cursor=0 -q count=20 --out out/comments.json
```

首次调用会提示付款，支付宝付款完成后脚本自动重试并返回数据：

```
需要按次付款：社媒数据查询（标准）  ¥0.10
（付款完成后自动重试，无需再次执行）
```

- `search` / `show` / `list` 都是本地索引，**不产生费用**，可以放心多查。
- 大响应必须加 `--out 路径`，只把必要字段读进上下文。
- 分类浏览：`python scripts/tikhub.py list --folder {{folder_example}}`。

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

共 {{count}} 个接口。按分类查 → 打开对应参考文件；不确定用什么接口 → `python scripts/tikhub.py search <关键词>`。

{{index_table}}

导航：`references/index.md`；单行速查表：`references/api-index.md`；机器可读：`references/inventory.json`。

## 错误处理

| 状态 | 含义 | 处理 |
|---|---|---|
| 402 | 需要付款 | 脚本会自动唤起支付宝付款并重试；中断时可用 `--proof` 手动重试 |
| 403 | 接口未开放 | 联系提供方 |
| 404 | 路径错 | 用 `show` 校正 path |
| 422 | 参数缺失/类型错 | CLI 会直接列出缺哪个参数，补上再调 |
| 429 | 限流 | 并发降到 ≤2，退避重试一次 |
| 502 | 上游失败 | 本次未计费，直接重试；持续失败换同类通道 |

## 输出与合规

- 先抓 1~2 条确认字段结构，再批量；批量串行或并发 ≤3，中间结果落盘。
- 只采集公开数据用于分析/研究，不用于批量私信、骚扰、隐私挖掘。
- 按次付费，批量前先估算调用次数；`search`/`show` 不产生费用，可以先想明白再调。
- 结果默认写当前工作区（如 `报告/`、`data/`），文件名带日期+关键词。
