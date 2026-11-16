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
