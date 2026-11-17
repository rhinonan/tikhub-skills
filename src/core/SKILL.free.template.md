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

> 本版本是**免费版**：用你自己的 TikHub API Token 直连官方接口。TikHub 的起充额度为 **5 美元**；不想充值可使用同平台的 Pro 版（`{{name}}-pro`），按次付费、无需自备 Token。

## 何时使用

- 要拿{{platform_zh}}的{{scope}}。
- 想确认"某个{{platform_zh}}数据有没有现成接口、参数怎么传、是 GET 还是 POST"。

**不适用**：其他平台（本 skill 只收{{platform_zh}}）；发内容、点赞、登录等写操作（TikHub 不提供）。

## 一次性准备：Token

```bash
python scripts/tikhub.py token <你的token>   # 存到 ~/.workbuddy/tikhub_token
python scripts/tikhub.py token              # 查看是否已配置
python scripts/tikhub.py ping               # 验证 token 是否可用
```

- Token 在 https://user.tikhub.io 的 API token 菜单生成，请求头 `Authorization: Bearer <token>`。
- 也读环境变量 `TIKHUB_API_KEY`（优先级最高）。
- **没 token 也能先跑通链路**：`Demo-API` 的 `/api/v1/demo/...` 接口免鉴权、返回固定数据、1 小时缓存。

## 三步工作流

```bash
# ① 找接口：中文名/英文名/路径/用途 模糊搜索
python scripts/tikhub.py search 评论 分页

# ② 看参数：完整 path 或唯一关键词
python scripts/tikhub.py show {{api_prefix}}/web/fetch_video_comments

# ③ 调接口（GET 用 -q，POST 用 -b）
python scripts/tikhub.py call {{api_prefix}}/web/fetch_video_comments \
  -q aweme_id=7372484719365098803 -q cursor=0 -q count=20 --out out/comments.json
```

- 大响应必须加 `--out 路径`，只把必要字段读进上下文，别把整份 JSON 塞进对话。
- 分类浏览：`python scripts/tikhub.py list --folder {{folder_example}}`。

{{platform_body}}

## 分类索引

共 {{count}} 个接口。按分类查 → 打开对应参考文件；不确定用什么接口 → `python scripts/tikhub.py search <关键词>`。

{{index_table}}

导航：`references/index.md`；单行速查表：`references/api-index.md`；机器可读：`references/inventory.json`。

## 错误处理

| 状态 | 含义 | 处理 |
|---|---|---|
| 401 | token 无效/缺失 | 提示用户配 token，不要重试 |
| 402 | TikHub 余额不足 | 换免费 Demo，或告知用户充值 |
| 403 | 权限/账号异常 | 账号停用或邮箱未验证 |
| 404 | 路径错 | 用 `show` 校正 path |
| 422 | 参数缺失/类型错 | CLI 会直接列出缺哪个参数，补上再调 |
| 429 | 限流 | 并发降到 ≤2，退避重试一次 |
| 500 | 服务端错误 | 重试一次；仍失败换同类通道 |

## 输出与合规

- 先抓 1~2 条确认字段结构，再批量；批量串行或并发 ≤3，中间结果落盘。
- 只采集公开数据用于分析/研究，不用于批量私信、骚扰、隐私挖掘；遵守 TikHub 与各平台条款。
- 按次计费：响应里 `cache_url` 是 24h 免费缓存链接；已删除/受限作品仍返回 HTTP 200 + `filter_detail`，**照样计费**，批量前先抽样。
- 结果默认写当前工作区（如 `报告/`、`data/`），文件名带日期+关键词。
- 查用量：`GET /api/v1/tikhub/user/get_user_daily_usage`；查余额：`GET /api/v1/tikhub/user/get_user_info`。
