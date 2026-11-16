---
name: tikhub-douyin
description: 抖音（Douyin）数据接口调用与接口查询，基于 TikHub.io API，收录 332 个抖音相关接口：作品详情与分享链接解析、批量作品、无水印播放地址、弹幕、评论与回复、用户资料与主页作品、喜欢/收藏/关注/粉丝、话题与音乐、综合/视频/用户/直播搜索、热榜（热点/上升/同城/垂类/低粉爆款）、星图达人画像与商业榜、巨量算数指数、创作者中心投稿分析、DOU+ 投放、直播流。当用户要抓取抖音作品/账号/评论/搜索/热榜数据，或问"抖音某个数据怎么拿""TikHub 有没有 XX 接口"时使用。本 skill 只收抖音，不含其他平台；不提供登录、发布、点赞等写操作。
version: 1.0.0
category: data-acquisition
author: 接口索引整理；接口文档与 API 版权归 TikHub.io 所有
license: 脚本与文档结构可自由使用；接口文档内容版权归 TikHub.io，使用需遵守其服务条款
agent_created: true
---

# 抖音数据接口（TikHub）

接口来自 TikHub.io 文档站，只保留**抖音相关**（332 个，含免鉴权 Demo 与多平台解析）。清单已固化在 `references/`，不用每次翻文档。

> 本版本是**免费版**：用你自己的 TikHub API Token 直连官方接口。

## 何时使用

- 要拿抖音的作品详情与分享链接解析、批量作品、无水印播放地址、弹幕、评论与回复、用户资料与主页作品、喜欢/收藏/关注/粉丝、话题与音乐、综合/视频/用户/直播搜索、热榜（热点/上升/同城/垂类/低粉爆款）、星图达人画像与商业榜、巨量算数指数、创作者中心投稿分析、DOU+ 投放、直播流。
- 想确认"某个抖音数据有没有现成接口、参数怎么传、是 GET 还是 POST"。

**不适用**：其他平台（本 skill 只收抖音）；发内容、点赞、登录等写操作（TikHub 不提供）。

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
python scripts/tikhub.py show /api/v1/douyin/web/fetch_video_comments

# ③ 调接口（GET 用 -q，POST 用 -b）
python scripts/tikhub.py call /api/v1/douyin/web/fetch_video_comments \
  -q aweme_id=7372484719365098803 -q cursor=0 -q count=20 --out out/comments.json
```

- 大响应必须加 `--out 路径`，只把必要字段读进上下文，别把整份 JSON 塞进对话。
- 分类浏览：`python scripts/tikhub.py list --folder Douyin-Web-API`。

## 场景速查（已按实际 openapi 规格核对）

| 需求 | 方法 + 接口 | 关键参数 |
|---|---|---|
| 单个作品详情 | `GET web/fetch_one_video` | `aweme_id`（v1 失效用 `fetch_one_video_v2`） |
| 分享链接解析作品 | `GET web/fetch_one_video_by_share_url` | `share_url` |
| 批量作品（≤50 个） | `POST web/fetch_multi_video` | body `aweme_ids`；固定 $0.05/次 |
| 最高画质播放地址 | `GET web/fetch_video_high_quality_play_url` | `aweme_id` 或 `share_url` |
| 视频弹幕 | `GET web/fetch_one_video_danmaku` | `item_id`（注意不是 aweme_id） |
| 一级评论 | `GET web/fetch_video_comments` | `aweme_id`, `cursor`, `count` |
| 评论的回复 | `GET web/fetch_video_comment_replies` | `item_id`, `comment_id`, `cursor`, `count` |
| 用户资料（sec_user_id） | `GET web/handler_user_profile` | `sec_user_id` |
| 用户资料（抖音号） | `GET web/handler_user_profile_v2` | `unique_id` |
| 用户主页作品 | `GET web/fetch_user_post_videos` | `sec_user_id`, `max_cursor`, `count` |
| 用户喜欢作品 | `POST web/fetch_user_like_videos` | body `sec_user_id`, `max_cursor`, `counts` |
| 用户收藏作品 | `POST web/fetch_user_collection_videos` | body `cookie`, `max_cursor`, `counts` |
| 粉丝 / 关注列表 | `GET web/fetch_user_fans_list`、`fetch_user_following_list` | `sec_user_id`, `max_time`, `count` |
| 话题下作品 | `POST web/fetch_challenge_posts` | body `challenge_id`, `cursor`, `count` |
| 综合搜索 | `POST search/fetch_general_search_v3` | body `keyword`, `offset`, `page`, `search_id`, `backtrace` |
| 视频搜索 | `POST search/fetch_video_search_v5` | 同上 |
| 用户搜索 | `POST search/fetch_user_search_v2` | body `keyword`, `cursor` |
| 抖音热榜 | `GET web/fetch_hot_search_result`（无参）或 `GET app/v3/fetch_hot_search_list`（`board_type`） | — |
| 热点总榜 / 上升 / 同城 | `GET billboard/fetch_hot_total_list`、`fetch_hot_rise_list`、`fetch_hot_city_list` | **必填** `page`, `page_size`, `type`（`snapshot` 或 `range`） |
| 垂类标签 | `GET billboard/fetch_content_tag` | 无参，取 `tags` 供榜单筛选 |
| 低粉爆款 / 高涨粉率 | `POST billboard/fetch_hot_total_low_fan_list`、`fetch_hot_total_high_fan_list` | body `page`, `page_size`, `date_window`, `tags` |
| 星图达人基本信息 | `GET xingtu_v2/get_author_base_info` | `o_author_id`（星图达人ID） |
| 星图达人受众画像 | `GET xingtu_v2/get_author_audience_distribution` | `o_author_id` |
| sec_user_id → 星图达人ID | `GET xingtu_v2/get_xingtu_kolid_by_sec_user_id` | `sec_user_id` |
| 星图达人搜索 | `GET xingtu_v2/search_creator` | `keyword`, `page`, `fans_min/max`, `price_min/max`…（参数名 `seach_type` 官方原文如此） |
| 星图商业榜 | `GET xingtu_v2/get_ranking_list_data` | `code`, `qualifier`, `period`, `date` |
| 巨量算数关键词热度 | `POST index/fetch_multi_keyword_hot_trend` | **query**：`keyword_list`, `start_date`, `end_date` |
| 视频指数趋势 | `POST index/fetch_item_index` | **query**：`item_id`, `start_date`, `end_date` |
| 创作者投稿总览 | `POST creator_v2/fetch_item_overview_data` | body `cookie`, `ids`, `fields` |
| 直播流地址 | `GET web/fetch_user_live_videos_by_sec_uid` | `sec_uid`（拼写就是 sec_uid） |
| DOU+ 视频详情 | `POST douplus/fetch_video_detail` | body `cookie`, `video` |
| 从文本批量提作品ID | `POST web/get_all_aweme_id` | body `url` |
| 从文本提单个作品ID | `GET web/get_aweme_id` | `url` |
| 短链还原 | `GET web/handler_shorten_url` | `target_url` |
| 取游客 Cookie | `GET web/fetch_douyin_web_guest_cookie` | `user_agent` |

上表路径省略前缀 `/api/v1/douyin/`。完整参数用 `show` 看，或翻 `references/<分类>.md`。

## ID 与分页要点

- **用户 ID 四种**：`uid`（数字）/ `sec_user_id`（MS4wLjAB…）/ `unique_id`（抖音号）/ `short_id`。互转用 `web/encrypt_uid_to_sec_user_id`、`web/fetch_query_user`（POST，body cookie）、`handler_user_profile_v2/v3`。
- **作品 ID（aweme_id）**：从分享文本提取用 `web/get_all_aweme_id`（POST）或 `web/get_aweme_id`（GET）；短链还原 `web/handler_shorten_url`。
- **分页三种范式**，别混用：
  1. `cursor` / `max_cursor`（首页传 `0`）+ `count`（多为 ≤20）→ 作品、评论；看返回 `has_more`。
  2. `offset` + `page` + `search_id` + `backtrace` → 搜索接口，后两个从上一次响应的 `data.pagination` 里取，首次传空串。
  3. `page` + `page_size` → 榜单/指数类。
- **参数位置不统一**：多数 POST 走 JSON body；但 `index/*` 虽是 POST，参数放在 **query**（如 `keyword_list`、`item_id`、`start_date`）。拿不准就先 `show`。
- 部分 web 接口有可选 `cookie`：可先用 `web/fetch_douyin_web_guest_cookie` 取游客 Cookie 提升成功率。

## 同类通道降级顺序

`web` → `app/v3` → `v2/v1` 老版 → `douplus`。官方明确 `fetch_one_video` 失效时改 `fetch_one_video_v2` 或 APP 接口。

## 已知坑

- **榜单 `type=snapshot` 会静默返回空**：`snapshot_time` 没精确命中已存快照时，`data.objs` 是 `[]` 但 `data.page.total` 有值，HTTP 仍 200、照常计费。要稳就用 `type=range` + `start_date/end_date`（实测 total 1029、返回真实热点）。
- 参数名有历史遗留拼写：直播接口是 `sec_uid`、星图搜索是 `seach_type`、收藏/喜欢接口是 `counts`，照抄别"纠正"。
- 已删除/受限作品仍返回 HTTP 200 + `filter_detail`，**照样计费**，批量前先抽样。
- **Git Bash 路径转换**：`/api/v1/...` 会被 MSYS 改写成 `C:/.../api/v1/...`。脚本已兼容；裸 curl 时用 `MSYS_NO_PATHCONV=1 curl ...`。
- 文档站把同一接口拆过多份页面，清单已按 `method+path` 去重（332 条）。

## 实测记录（2026-11-10）

以下结构均为真实调用核对过，比文档里"返回：作品数据"这类描述更可用：

| 接口 | data 结构 |
|---|---|
| `web/fetch_one_video_v2` | `data.aweme_detail`（作品）+ `log_pb` + `status_code`；正文 `desc`、`author.nickname/follower_count`、`statistics.digg_count/comment_count/share_count/collect_count`、`duration`(ms)、`create_time`(秒) |
| `search/fetch_video_search_v5` | `data.items`（10 条/页，卡片结构：`type`/`aweme_info`/`card_info`，**视频数据在 `items[].aweme_info`**）+ `data.config` + `data.pagination`（`search_id`/`offset`/`cursor`/`backtrace`/`has_more`），翻页把这四个回传 |
| `billboard/fetch_hot_total_list` | `data.objs[]`（`rank`/`sentence`/`hot_score`/`video_count`/`sentence_tag_name`/`trends[]`）+ `data.page.total` |

单次成本很低（个位数请求≈$0.01 量级），但每次调用都会计费，批量前务必先看余额。

查用量：`GET /api/v1/tikhub/user/get_user_daily_usage`；查余额：`GET /api/v1/tikhub/user/get_user_info`（`data.user_data.balance`）。


## 分类索引

共 332 个接口。按分类查 → 打开对应参考文件；不确定用什么接口 → `python scripts/tikhub.py search <关键词>`。

| 分类 | 接口数 | 参考文件 |
|---|---|---|
| Douyin-Web-API | 55 | `references/Douyin-Web-API.md` |
| Douyin-Index-API | 51 | `references/Douyin-Index-API.md` |
| Douyin-Xingtu-V2-API | 50 | `references/Douyin-Xingtu-V2-API.md` |
| Douyin-App-V3-API | 38 | `references/Douyin-App-V3-API.md` |
| Douyin-Xingtu-API | 32 | `references/Douyin-Xingtu-API.md` |
| Douyin-Billboard-API | 31 | `references/Douyin-Billboard-API.md` |
| Douyin-Search-API | 23 | `references/Douyin-Search-API.md` |
| Douyin-Creator-API | 17 | `references/Douyin-Creator-API.md` |
| Douyin-DouPlus-API | 17 | `references/Douyin-DouPlus-API.md` |
| Douyin-Creator-V2-API | 14 | `references/Douyin-Creator-V2-API.md` |
| Demo-API | 3 | `references/Demo-API.md` |
| Hybrid-Parsing | 1 | `references/Hybrid-Parsing.md` |

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
