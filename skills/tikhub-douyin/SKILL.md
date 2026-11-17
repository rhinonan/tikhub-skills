---
name: tikhub-douyin
description: 抖音（Douyin）数据接口调用与接口查询，基于 TikHub.io API，收录 332 个抖音相关接口：作品详情与分享链接解析、批量作品、无水印播放地址、弹幕、评论与回复、用户资料与主页作品、喜欢/收藏/关注/粉丝、话题与音乐、综合/视频/用户/直播搜索、热榜（热点/上升/同城/垂类/低粉爆款）、星图达人画像与商业榜、巨量算数指数、创作者中心投稿分析、DOU+ 投放、直播流。当用户要抓取抖音作品/账号/评论/搜索/热榜数据，或问"抖音某个数据怎么拿""TikHub 有没有 XX 接口"时使用。本 skill 只收抖音，不含其他平台；不提供登录、发布、点赞等写操作。
version: 1.2.0
category: data-acquisition
author: 接口索引整理；接口文档与 API 版权归 TikHub.io 所有
license: 脚本与文档结构可自由使用；接口文档内容版权归 TikHub.io，使用需遵守其服务条款
agent_created: true
---

# 抖音数据接口（TikHub）

接口来自 TikHub.io 文档站，只保留**抖音相关**（332 个，含免鉴权 Demo 与多平台解析）。清单已固化在 `references/`，不用每次翻文档。

> 本版本**自备 API Key**：用你自己的 TikHub API Token 直连官方接口，本 skill 不代收任何费用。TikHub 的起充额度为 **5 美元**；不想充值可使用同平台的 Pro 版（`tikhub-douyin-pro`），按次付费、无需自备 Token。

## 0. 先自检（30 秒，强烈建议）

```bash
python3 scripts/tikhub.py doctor          # 环境/清单/文档/凭证一次看完
python3 scripts/tikhub.py doctor --net    # 连网络一起测
```

看到 `[OK] 环境、清单、文档都齐` 再往下做；有 `[FAIL]` 就按提示修（多数是清单缺失或包没解压全）。

**运行环境三条约定**，按这个来能省掉绝大多数"命令直接报错"：

1. **解释器**：优先 `python3`，老环境用 `python`（脚本兼容 3.8+，版本太低会自己报错退出）。
2. **工作目录**：脚本用自身路径定位清单，任意目录都能跑；但不确定 cwd 时请用**绝对路径**调用，
   如 `python3 /path/to/tikhub-douyin/scripts/tikhub.py search 评论`，避免 `scripts/tikhub.py: No such file`。
3. **清单坏了也能干活**：`references/inventory.json` 缺失/损坏时，`search`/`show` 会自动降级扫
   `references/*.md`；`call` 只要给完整 path 依旧能直连。所以"目录报错"不等于整个 skill 不可用。

## 何时使用

- 要拿抖音的作品详情与分享链接解析、批量作品、无水印播放地址、弹幕、评论与回复、用户资料与主页作品、喜欢/收藏/关注/粉丝、话题与音乐、综合/视频/用户/直播搜索、热榜（热点/上升/同城/垂类/低粉爆款）、星图达人画像与商业榜、巨量算数指数、创作者中心投稿分析、DOU+ 投放、直播流。
- 想确认"某个抖音数据有没有现成接口、参数怎么传、是 GET 还是 POST"。

**不适用**：其他平台（本 skill 只收抖音）；发内容、点赞、登录等写操作（TikHub 不提供）。

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
python3 scripts/tikhub.py show /api/v1/douyin/web/fetch_video_comments

# ③ 调接口（GET 用 -q，POST 用 -b）
python3 scripts/tikhub.py call /api/v1/douyin/web/fetch_video_comments \
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
- 分类浏览：`python3 scripts/tikhub.py list --folder Douyin-Web-API`。

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
- **web 版作品的 `statistics.play_count` 恒为 0**：实测某条 31.2 万赞的作品 `play_count` 仍是 `0`，播放量得走创作者中心/数据统计接口，别拿它算播放。
- **`fetch_user_post_videos` 的 `count` 只是建议值**：传 `count=2` 实测回 4 条；按 `aweme_list` 长度判断，别用 count 算页数。它的 `max_cursor` 是**毫秒时间戳**（如 `1794557654000`），不是 0 起算的序号。
- **`search/fetch_general_search_v2` 的 `data` 是 `null`**：真实内容在顶层 `business_data[]`（实测 18 类卡片，按 `business_data[i].type` 区分视频/用户/直播）。
- **`search/fetch_video_search_v5` 2026-11-17 实测连续 400**（未计费）；期间用 `search/fetch_general_search_v2` 或 `app/v3` 的视频搜索替代。
- 参数名有历史遗留拼写：直播接口是 `sec_uid`、星图搜索是 `seach_type`、收藏/喜欢接口是 `counts`，照抄别"纠正"。
- 已删除/受限作品仍返回 HTTP 200 + `filter_detail`，**照样计费**，批量前先抽样。
- **Git Bash 路径转换**：`/api/v1/...` 会被 MSYS 改写成 `C:/.../api/v1/...`。脚本已兼容；裸 curl 时用 `MSYS_NO_PATHCONV=1 curl ...`。
- 文档站把同一接口拆过多份页面，清单已按 `method+path` 去重（332 条）。

## 实测记录（2026-11-17 复核）

以下结构均为真实调用核对过，比文档里"返回：作品数据"这类描述更可用；每个接口的完整字段表已写进
`references/<分类>.md` 的「返回结构」段，`show <path>` 也会直接打印：

| 接口 | data 结构 |
|---|---|
| `web/fetch_one_video_v2` | `data.aweme_detail`（作品）+ `log_pb` + `status_code`；正文 `desc`、`author.nickname/follower_count`、`statistics.digg_count/comment_count/share_count/collect_count`、`duration`(ms)、`create_time`(秒) |
| `web/fetch_video_comments` | `comments[]`（`cid`/`text`/`digg_count`/`reply_comment_total`/`ip_label`/`user`）+ `total`（总数）+ `cursor`/`has_more`；约 20 条/页 |
| `web/handler_user_profile` | `user.{uid,sec_uid,unique_id,short_id,nickname,signature,follower_count,following_count,total_favorited,aweme_count,favoriting_count,ip_location}` |
| `web/fetch_user_post_videos` | `aweme_list[]`（同 `aweme_detail` 裁剪版）+ `max_cursor`（**毫秒时间戳**）+ `has_more`/`min_cursor`/`time_list` |
| `web/fetch_hot_search_result` | `data.word_list[]`（`word`/`hot_value`/`sentence_id`/`label`/`view_count`/`discuss_video_count`）+ `trending_list` |
| `web/fetch_video_high_quality_play_url` | 无 `data` 包装：`video_id`/`original_video_url`/`file_size`(str)/`file_size_in_mb`(float)/`content_type` |
| `search/fetch_general_search_v2` | `data` 为 null；内容在 `business_data[]`（18 类卡片，按 `type` 区分） |
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
清单校准至 2026-11-10（接口数 332）；若与线上文档有出入，以 `show` 的参数表和实际返回为准。

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
