---
name: cn-social-data-pro
description: 中文社媒数据引擎（Chinese Social Media Data Engine）：下载无水印视频、解析分享链接、批量导出评论、查账号与作品数据、追热搜热榜、找达人。付费版：标准 ¥0.10/次；高价值/批量走额度包（6/30 点每次，¥9.90/200 点），无需注册上游。收录 630 个接口，覆盖抖音、微博、小红书、B站、知乎、微信、快手。当用户说"下载这个抖音视频无水印""把这个号的评论导出""今天微博热搜是什么""找几个小红书达人"时使用；只提供只读数据接口，不含登录、发布、点赞等写操作。
version: 2.0.0
category: data-acquisition
author: rhinonan
license: MIT
agent_created: true
---

# 中文社媒数据引擎（付费版）

下载抖音无水印视频、解析分享链接、批量导出评论、查账号与作品数据、追热搜热榜、找达人——用一套 CLI 查接口、调接口，覆盖抖音、微博、小红书、B站、知乎、微信、快手，收录 630 个接口。只读数据，不含登录、发布、点赞等写操作。

> **付费版 = 按次付费。** 不需要注册或充值上游，每次调用经作者网关走支付宝 AI 按量付费（A2M）。
> 已有上游账号、用量稳定？用免费版 `cn-social-data` 自带 Key 直连。

## 能帮你做什么

| 用户这样说 | 对应能力 | 第一步 |
|---|---|---|
| 下载抖音/快手/B站无水印视频、解析分享链接 | 无水印播放地址、链接解析 | `search 无水印` / `search 分享链接` |
| 导出某账号最近作品和评论 | 主页作品、一级/二级评论 | `search 评论 --platform douyin` |
| 看看这个博主/UP主/公众号的数据 | 用户资料、粉丝数、作品/文章列表 | `search 用户信息 --platform <平台>` |
| 今天微博热搜、抖音热榜是什么 | 热榜、热搜榜单 | `search 热榜` |
| 找某领域的达人，看粉丝画像 | 星图/蒲公英/花火、粉丝画像 | `search 达人` / `search 粉丝画像` |
| 导出公众号或微博文章正文 | 文章详情、互动数据 | `search 文章详情 --platform 微信` |
| 搜某个关键词在各平台的内容 | 综合/视频/用户搜索 | `search 搜索 --platform <平台>` |

绝大多数需求都走这三步：`search 关键词` → `show <候选路径>` → `call <路径> -q ...`。

## 0. 先自检

```bash
python3 scripts/social.py doctor
python3 scripts/social.py doctor --net
```

约定：

- 命令都在 **skill 根目录**下执行；在别的目录时用绝对路径 `python3 <skill目录>/scripts/social.py ...`。
- 解释器 `python3` 优先，老环境用 `python`。
- 所有命令都不写入业务系统，只读数据。

## 覆盖平台

| 平台 | 接口数 | 典型用途 |
|---|---|---|
| 抖音 | 330 | 作品详情与分享链接解析、批量作品、无水印播放地址… |
| 微博 | 56 | 用户信息与粉丝/关注、微博正文与评论/转发/点赞、用户微博时间线… |
| 小红书 | 45 | 笔记详情与评论、用户主页与笔记/收藏列表、笔记/用户/商品搜索… |
| B站 | 88 | 视频详情与播放流/字幕/弹幕、评论与回复、用户资料与投稿/收藏/动态… |
| 知乎 | 41 | 问题与回答、专栏文章、想法（Pin）… |
| 微信 | 25 | 视频号账号与主页资料、作品详情/评论/合集/直播回放、号内搜索；公众号文章详情/互动数据/评论/账号文章列表；微信搜一搜综合与视频号搜索 |
| 快手 | 38 | 作品详情与分享链接解析、一级/二级评论、用户资料与作品/收藏… |
| 通用 | 7 | 固定数据的免费演示接口（用于验证链路与字段结构）、多平台短视频混合解析 |

## 一次性准备：支付依赖

按次付款由支付宝买家侧 CLI 完成，需要 Node ≥ 18：

```bash
npx -y @alipay/agent-payment@latest install
```

装好后 `alipay-bot` 才可用；`doctor` 会提示缺失。

## 查询额度

```bash
python3 scripts/social.py balance     # 剩余 / 已购 / 已消耗
python3 scripts/social.py usage       # 最近调用与扣费
python3 scripts/social.py recharge --yes    # 购买额度包（¥9.90 / 200 点；不加 --yes 会先确认）
```

## 付费前必须确认

任何会花钱的调用，先展示预估清单给用户，确认后再执行：

```bash
# 单接口预估
python3 scripts/social.py estimate douyin/web/fetch_one_video

# 多接口任务预估（计划文件）
python3 scripts/social.py estimate --file plan.json
```

清单包含：**预计请求多少个接口、每个接口的档位、扣多少点、当前额度、需要补多少、推荐套餐**。

- `call` 默认也会先打印这份清单。
- 终端交互会提示输入 `y` 确认；非交互环境（agent 调用）必须加 `--yes` 才会真正发出请求，否则只打印清单并退出。
- 计划文件格式：

```json
{"title": "抖音账号分析", "endpoints": [
  {"path": "douyin/web/handler_user_profile", "repeat": 1},
  {"path": "douyin/web/fetch_user_post_videos", "repeat": 3},
  {"path": "douyin/web/fetch_video_comments", "repeat": 3}
]}
```

多接口任务的推荐流程：`estimate` → 把清单给用户确认 → 逐条 `call <path> --yes`；额度不足时 CLI 会自动购买额度包（`--no-auto-recharge` 可关闭）。单独 `recharge` 也会先打印商品与价格，输入 `y` 或加 `--yes` 才发起支付。

## 三步工作流

```bash
# 1) 搜
python3 scripts/social.py search 评论 --platform weibo

# 2) 看
python3 scripts/social.py show weibo/web_v2/fetch_post_comments

# 3) 调（先打印付费清单；用户确认后加 --yes 执行）
python3 scripts/social.py call weibo/web_v2/fetch_post_comments \
  -q id=5283919831764022 --out out/comments.json --yes
```

标准接口每次 ¥0.10（有额度时扣 1 点）；高价值/批量扣 6/30 点，不做单次收款。上游失败不计费。

## 计费规则

| 档位 | 计费 | 适用 |
|---|---|---|
| 标准 | ¥0.10 / 次，可单次付款 | 常规详情、评论、用户、搜索 |
| 高价值 | 6 点 / 次（约 ¥0.30） | 指数、星图/花火/蒲公英、榜单类 |
| 批量 | 30 点 / 次（约 ¥1.49） | 批量作品、批量查询 |
| 额度包 | ¥9.90 / 200 点 | 高价值与批量只能走额度；标准也可用 |
| 任务包 | ¥1.99 起 | 组合任务（如账号分析） |

**高价值与批量接口不支持单次付款**：额度不足时 CLI 会提示并自动购买额度包，然后重试本次调用；不想自动付款可加 `--no-auto-recharge`，先手动 `recharge`。标准接口在没有额度时才会单次收款。

## 平台速查

## 抖音

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 作品详情 | `GET douyin/web/fetch_one_video` | `aweme_id` |
| 下载无水印视频 | `GET douyin/web/fetch_video_high_quality_play_url` | `aweme_id` 或 `share_url` |
| 分享链接解析 | `GET douyin/web/fetch_one_video_by_share_url` | `share_url` |
| 用户主页作品 | `GET douyin/web/fetch_user_post_videos` | `sec_user_id`, `max_cursor` |
| 热榜 | `GET douyin/web/fetch_hot_search_result` | — |

- 用户 ID 有 `uid` / `short_id` / `sec_uid` / `sec_user_id` 四种，接口要求各不相同；列表翻页常见 `cursor` 或毫秒时间戳 `max_cursor`。
- 网页端 `play_count` 常为 0，用 `douyin/app/v3` 兜底；同类通道按 `web` → `app/v3` → `v2` 降级。

## 微博

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 用户信息 | `GET weibo/web_v2/fetch_user_info` | `uid` |
| 导出微博正文 | `GET weibo/web_v2/fetch_post_detail` | `id` |
| 用户微博时间线 | `GET weibo/web_v2/fetch_user_posts` | `uid`, `page`, `since_id` |
| 微博评论 | `GET weibo/web_v2/fetch_post_comments` | `id`, `count`, `max_id` |
| 完整热搜榜 | `GET weibo/web_v2/fetch_hot_search_summary` | — |

- 用户 ID 是数字 `uid`，微博正文主键叫 `id`；时间线翻页用 `page` + `since_id`，评论用 `max_id` 游标。
- Web V2 与 App 两套通道返回结构不同，Web 失败时用 App 接口兜底。

## 小红书

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 笔记详情 | `GET xiaohongshu/web_v3/fetch_note_detail` | `note_id`, `xsec_token` |
| 用户笔记列表 | `GET xiaohongshu/app_v2/get_user_posted_notes` | `user_id` 或 `share_text` |
| 笔记评论 | `GET xiaohongshu/app_v2/get_note_comments` | `note_id`, `cursor` |
| 搜索笔记 | `GET xiaohongshu/app_v2/search_notes` | `keyword`, `page` |

- Web V3 详情必须同时给 `note_id` 和 `xsec_token`，token 失效时改走 App V2 详情接口。
- 蒲公英（PGY）接口全部是 POST + JSON body，和常规 query 风格不同。

## B站

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 视频详情 | `GET bilibili/web/fetch_one_video` | `bv_id` |
| 下载视频/播放流地址 | `GET bilibili/web/fetch_video_playurl` | `bv_id`, `cid` |
| 视频评论 | `GET bilibili/web/fetch_video_comments` | `bv_id`, `pn` |
| UP 主投稿 | `GET bilibili/web/fetch_user_post_videos` | `uid`, `pn`, `ps` |

- 视频主键是 `bv_id`，只有 `aid` 时先用 `bv_to_aid` 互转；播放流还要 `cid`（视频详情里取）。
- 列表分页用 `pn` + `ps`；大会员清晰度单独调 `fetch_vip_video_playurl`。

## 知乎

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 问题下的回答 | `GET zhihu/web/fetch_question_answers` | `question_id`, `cursor` |
| 回答详情/导出正文 | `GET zhihu/web/fetch_answer_detail` | `answer_id` |
| 用户回答列表 | `GET zhihu/web/fetch_user_answers` | `user_url_token`, `offset` |
| 首页热榜 | `GET zhihu/web/fetch_hot_list` | `limit` |

- 用户标识是 `user_url_token`（URL 里的英文串），不是数字 ID 或昵称。
- 知乎基本只有 Web 通道，没有 App 兜底；ID 类型（问题/回答/专栏/想法）不能混用。

## 微信

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 视频号账号信息 | `POST wechat_channels/v2/fetch_channel_info` | body `username` |
| 视频号作品详情 | `POST wechat_channels/v2/fetch_video_detail` | body `object_id` 或 `share_url` |
| 导出公众号文章正文 | `POST wechat_mp/v2/fetch_article_detail_h5` | body `url` |
| 搜一搜 | `POST wechat_search/v2/fetch_search` | body `keyword`, `business_type` |

- 微信接口几乎全部是 **POST + JSON body**，参数用 `-b` 传，不要用 `-q`。
- 视频号账号是 `v2_...@finder` 长串，公众号是 `gh_` 开头；文章优先用 H5 版本接口。

## 快手

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 作品详情/下载地址（App） | `GET kuaishou/app/fetch_one_video` | `photo_id` |
| 分享链接解析 | `GET kuaishou/app/fetch_one_video_by_url` | `share_text` |
| 作品评论 | `GET kuaishou/app/fetch_video_comment` | `photo_id`, `pcursor` |
| 视频搜索 | `GET kuaishou/app/search_video_v2` | `keyword`, `pcursor` |

- 作品主键是 `photo_id`（短字符串），用户标识是 `user_id`；列表统一用 `pcursor`，返回空串即到底。
- Web 端 `fetch_one_video` 只接受分享链接，传 `photo_id` 要走 App 端。

## 通用

### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 验证链路（免费） | `GET demo/douyin/web/fetch_one_video` | — |
| 抖音演示搜索 | `GET demo/douyin_search/app/general_search` | — |
| 混合解析视频链接 | `GET hybrid/video_data` | `url` |

- Demo 接口返回固定数据并缓存 1 小时，不扣额度，适合在配置 token 前验证 CLI。
- `hybrid/video_data` 支持多个平台的分享链接；传 `minimal=true` 只返回核心字段。

## 分类导航

完整的分类清单在 `references/index.md`（约 630 个接口分成若干类，每个平台一组）。**不要一次把所有分类文档读进上下文**：

- 用 `search` / `list` / `show` 按需定位；
- 机器可读清单是 `references/inventory.json`；
- 每个分类的详细参数在 `references/<分类>.md`，只在确认要用某一类时打开。

## 常见问题

| 问题 | 处理 |
|---|---|
| 401 | 账户 token 无效，运行 `recharge` 重新获取 |
| 402 | 标准接口：CLI 自动唤起支付宝按次付款；高价值/批量：自动购买额度包后重试 |
| 422 | 必填参数漏了，`show <path>` 看参数表 |
| 429 | 限流，降低并发或等 30s |
| 404 | 路径写错，用 `search`/`show` 重新确认 |
| 502 | 上游失败，本次未计费，可直接重试 |
| data 为 null | 有些接口内容在 `business_data` 等顶层字段，用 `--raw` 看完整响应 |

## 输出与合规

- `--out` 把 `data` 落盘；`--raw` 输出完整响应；`--preview N` 控制终端预览长度。
- 数据来源：TikHub。只采集公开数据；不要高频轰炸上游，不要用于侵犯隐私或绕过平台风控。
- 数据版权归原平台与内容作者，遵守目标平台的用户协议与当地法规（含个人信息保护要求）。
