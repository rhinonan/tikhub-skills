# Xiaohongshu App V2 API

文件夹 `Xiaohongshu-App-V2-API` · 20 个接口
说明：小红书App V2数据接口


## 获取图文笔记详情

`GET /api/v1/xiaohongshu/app_v2/get_image_note_detail`

- 用途：获取图文笔记的完整详情数据
- 返回：图文笔记详情数据，包含笔记内容、图片列表、作者信息、互动数据等；视频笔记仅返回封面图等基础数据，不包含视频播放链接
- Query：
  - `note_id` (选填,string) 笔记ID/Note ID
  - `share_text` (选填,string) 分享链接，支持xiaohongshu.com/xhslink.com/xhslink.cn/Share link, supports xiaohongshu.com, xhslink.com, xhslink.cn
- 示例：

```
note_id="697c0eee000000000a03c308"
```

## 获取视频笔记详情

`GET /api/v1/xiaohongshu/app_v2/get_video_note_detail`

- 用途：获取视频笔记的完整详情数据
- 返回：视频笔记详情数据，包含视频播放地址、封面图、作者信息、互动数据等
- Query：
  - `note_id` (选填,string) 笔记ID/Note ID
  - `share_text` (选填,string) 分享链接，支持xiaohongshu.com/xhslink.com/xhslink.cn/Share link, supports xiaohongshu.com, xhslink.com, xhslink.cn
- 示例：

```
note_id="697c0eee000000000a03c308"
```

## 获取笔记评论列表

`GET /api/v1/xiaohongshu/app_v2/get_note_comments`

- 用途：获取指定笔记的评论列表，支持分页和多种排序方式
- 返回：评论数据对象，包含评论列表、分页游标等
- Query：
  - `note_id` (选填,string) 笔记ID/Note ID
  - `share_text` (选填,string) 分享链接，支持xiaohongshu.com/xhslink.com/xhslink.cn/Share link, supports xiaohongshu.com, xhslink.com, xhslink.cn
  - `cursor` (选填,string) 分页游标，首次请求留空/Pagination cursor, leave empty for first request
  - `index` (选填,integer) 评论索引，首次请求传0/Comment index, pass 0 for first request
  - `pageArea` (选填,string) 折叠状态: UNFOLDED(默认-展开), FOLDED(折叠)
  - `sort_strategy` (选填,string) 排序策略/Sort strategy: default, latest_v2, like_count
- 示例：

```
note_id="697c0eee000000000a03c308"
sort_strategy="latest_v2"
```

## 获取笔记二级评论列表

`GET /api/v1/xiaohongshu/app_v2/get_note_sub_comments`

- 用途：获取指定笔记某条评论下的子评论（回复）列表，使用游标分页
- 返回：子评论数据对象，包含子评论列表、分页游标等
- Query：
  - `note_id` (选填,string) 笔记ID/Note ID
  - `share_text` (选填,string) 分享链接，支持xiaohongshu.com/xhslink.com/xhslink.cn/Share link, supports xiaohongshu.com, xhslink.com, xhslink.cn
  - `comment_id` (必填,string) 父评论ID/Parent comment ID
  - `cursor` (选填,string) 分页游标，首次留空，翻页时从$.data.data.cursor中提取cursor值/Pagination cursor, leave empty for first request, extract cursor from $.data.data.cursor for next page
  - `index` (选填,integer) 分页索引，首次传1，翻页时从$.data.data.cursor中提取index值/Pagination index, pass 1 for first request, extract index from $.data.data.cursor for next page
- 示例：

```
note_id="699916e6000000001d0253da"
comment_id="699fb9930000000008030db6"
```

## 获取用户信息

`GET /api/v1/xiaohongshu/app_v2/get_user_info`

- 用途：获取指定用户的详细信息
- 返回：用户详细信息，包含昵称、头像、简介、粉丝数、关注数、笔记数等
- Query：
  - `user_id` (选填,string) 用户ID/User ID
  - `share_text` (选填,string) 分享链接，支持xiaohongshu.com/xhslink.com/xhslink.cn/Share link, supports xiaohongshu.com, xhslink.com, xhslink.cn
- 示例：

```
user_id="61b46d790000000010008153"
```

## 获取用户笔记列表

`GET /api/v1/xiaohongshu/app_v2/get_user_posted_notes`

- 用途：获取指定用户已发布的笔记列表，使用游标分页
- 返回：用户笔记列表数据，包含笔记基本信息和分页信息
- Query：
  - `user_id` (选填,string) 用户ID/User ID
  - `share_text` (选填,string) 分享链接，支持xiaohongshu.com/xhslink.com/xhslink.cn/Share link, supports xiaohongshu.com, xhslink.com, xhslink.cn
  - `cursor` (选填,string) 分页游标，首次请求留空/Pagination cursor, leave empty for first request
- 示例：

```
user_id="61b46d790000000010008153"
```
- 返回结构（实测）：
  - `data` 是对象（6 个字段）：`code`, `success`, `data`, `msg`, `debug_id`, `debug_info`
  - `data.data` 是对象（3 个字段）：`notes`, `tags`, `has_more`
  - `data.data.notes` 是数组（长度 22）；首元素字段：`has_music`, `time_desc`, `sticky`, `title`, `likes`, `create_time`, `display_title`, `guide_context`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取用户收藏笔记列表

`GET /api/v1/xiaohongshu/app_v2/get_user_faved_notes`

- 用途：获取指定用户公开收藏的笔记列表，使用游标分页
- 返回：用户收藏笔记列表数据，包含笔记基本信息和分页信息
- Query：
  - `user_id` (选填,string) 用户ID/User ID
  - `share_text` (选填,string) 分享链接，支持xiaohongshu.com/xhslink.com/xhslink.cn/Share link, supports xiaohongshu.com, xhslink.com, xhslink.cn
  - `cursor` (选填,string) 分页游标，首次请求留空，翻页时传入上一页最后一条笔记的note_id/Pagination cursor, leave empty for first request, pass last note_id from previous page for next page
- 示例：

```
user_id="5a8cf39111be10466d285d6b"
```

## 搜索笔记

`GET /api/v1/xiaohongshu/app_v2/search_notes`

- 用途：根据关键词搜索小红书笔记，支持多种排序方式、笔记类型筛选和发布时间筛选
- 返回：搜索结果数据，包含笔记列表和分页信息
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页码，从1开始/Page number, start from 1
  - `sort_type` (选填,string) 排序方式/Sort type
  - `note_type` (选填,string) 笔记类型/Note type: 不限, 视频笔记, 普通笔记, 直播笔记
  - `time_filter` (选填,string) 发布时间筛选/Time filter: 不限, 一天内, 一周内, 半年内
  - `search_id` (选填,string) 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `search_session_id` (选填,string) 搜索会话ID，翻页时传入首次搜索返回的值/Search session ID for pagination
  - `source` (选填,string) 来源/Source
  - `ai_mode` (选填,integer) AI模式：0=关闭, 1=开启/AI mode: 0=off, 1=on
- 示例：

```
keyword="美食推荐"
page=1
sort_type="general"
```
- 返回结构（实测）：
  - `data` 是对象（10 个字段）：`code`, `success`, `data`, `msg`, `search_id`, `search_session_id`, `page`, `next_page`, `debug_id`, `debug_info`
  - `data.data` 是对象（20 个字段）：`request_dqa_instant`, `ai_mode_enable`, `items`, `search_dqa_new_page_exp`, `can_cut`, `strategy_info`, `cur_cut_number`, `request_dqa`
  - `data.data` 是对象（20 个字段）：`request_dqa_instant`, `ai_mode_enable`, `items`, `search_dqa_new_page_exp`, `can_cut`, `strategy_info`, `cur_cut_number`, `request_dqa`, `query_type`, `taxonomy1`
  - `data.data.items` 是数组（长度 20）；首元素字段：`mix_track_id`, `new_help_style`, `model_type`, `note`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 搜索用户

`GET /api/v1/xiaohongshu/app_v2/search_users`

- 用途：根据关键词搜索小红书用户，每页返回 20 条结果，支持分页
- 返回：搜索结果数据，包含用户列表和分页信息
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页码，从1开始/Page number, start from 1
  - `search_id` (选填,string) 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `source` (选填,string) 来源/Source
- 示例：

```
keyword="美食博主"
page=1
```

## 搜索图片

`GET /api/v1/xiaohongshu/app_v2/search_images`

- 用途：根据关键词搜索小红书图片，每页返回 20 条结果，支持分页
- 返回：搜索结果数据，包含图片列表和分页信息
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页码，从1开始/Page number, start from 1
  - `search_id` (选填,string) 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `search_session_id` (选填,string) 搜索会话ID，翻页时传入首次搜索返回的值/Search session ID for pagination
  - `word_request_id` (选填,string) 词请求ID，翻页时传入首次搜索返回的值/Word request ID for pagination
  - `source` (选填,string) 来源/Source
- 示例：

```
keyword="壁纸"
page=1
```

## 搜索商品

`GET /api/v1/xiaohongshu/app_v2/search_products`

- 用途：根据关键词搜索小红书商品，每页返回 20 条结果，支持分页
- 返回：搜索结果数据，包含商品列表和分页信息
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页码，从1开始/Page number, start from 1
  - `search_id` (选填,string) 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `source` (选填,string) 来源/Source
- 示例：

```
keyword="手机壳"
page=1
```

## 搜索群聊

`GET /api/v1/xiaohongshu/app_v2/search_groups`

- 用途：根据关键词搜索小红书群聊列表，支持分页
- 返回：搜索结果数据，包含群聊列表和分页信息
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `page_no` (选填,integer) 页码，从0开始/Page number, start from 0
  - `search_id` (选填,string) 搜索ID，翻页时传入首次搜索返回的值/Search ID for pagination
  - `source` (选填,string) 来源/Source
  - `is_recommend` (选填,integer) 是否推荐：0=否, 1=是/Is recommend: 0=no, 1=yes
- 示例：

```
keyword="上海"
page_no=0
```

## 获取商品详情

`GET /api/v1/xiaohongshu/app_v2/get_product_detail`

- 用途：通过 SKU ID 获取商品的详细信息，包括价格、规格、库存、商品描述等
- 返回：商品详情数据，包含价格、规格、库存、商品描述等
- Query：
  - `sku_id` (必填,string) 商品SKU ID/Product SKU ID
  - `source` (选填,string) 来源/Source
  - `pre_page` (选填,string) 前置页面/Previous page
- 示例：

```
sku_id="669ddd44e05f3700011067ed"
```

## 获取商品评论总览

`GET /api/v1/xiaohongshu/app_v2/get_product_review_overview`

- 用途：获取商品的评论统计信息，包括评分分布、好评率、评论标签等
- 返回：商品评论总览数据，包含评分分布、好评率、评论标签等
- Query：
  - `sku_id` (必填,string) 商品SKU ID/Product SKU ID
  - `tab` (选填,integer) 标签类型/Tab type
- 示例：

```
sku_id="669ddd44e05f3700011067ed"
```

## 获取商品评论列表

`GET /api/v1/xiaohongshu/app_v2/get_product_reviews`

- 用途：获取商品的用户评论列表，支持分页、排序和筛选有图评论
- 返回：商品评论列表数据
- Query：
  - `sku_id` (必填,string) 商品SKU ID/Product SKU ID
  - `page` (选填,integer) 页码，从0开始/Page number, start from 0
  - `sort_strategy_type` (选填,integer) 排序策略：0=综合排序, 1=最新排序/Sort strategy: 0=general, 1=latest
  - `share_pics_only` (选填,integer) 仅看有图评论：0=否, 1=是/Show reviews with images only: 0=no, 1=yes
  - `from_page` (选填,string) 来源页面/From page
- 示例：

```
sku_id="669ddd44e05f3700011067ed"
page=0
```

## 获取商品推荐列表

`GET /api/v1/xiaohongshu/app_v2/get_product_recommendations`

- 用途：根据商品 SKU ID 获取相关推荐商品列表，使用游标分页
- 返回：推荐商品列表数据
- Query：
  - `sku_id` (必填,string) 商品SKU ID/Product SKU ID
  - `cursor_score` (选填,string) 分页游标，首次请求留空/Pagination cursor, leave empty for first request
  - `region` (选填,string) 地区/Region
- 示例：

```
sku_id="669ddd44e05f3700011067ed"
```

## 获取话题详情

`GET /api/v1/xiaohongshu/app_v2/get_topic_info`

- 用途：获取指定话题的详细信息，包括话题名称、浏览量、讨论数、分享信息等
- 返回：话题详情数据，包含 page_info（名称/浏览量/讨论数）、tabs、share_info 等
- Query：
  - `page_id` (必填,string) 话题页面ID/Topic page ID
  - `source` (选填,string) 来源/Source
  - `note_id` (选填,string) 来源笔记ID，从笔记跳转到话题时传入/Source note ID, pass when jumping from note to topic
- 示例：

```
page_id="5c1cc866febed9000184b7c1"
```

## 获取话题笔记列表

`GET /api/v1/xiaohongshu/app_v2/get_topic_feed`

- 用途：获取指定话题下的笔记列表，支持按最热或最新排序，使用游标分页
- 返回：话题笔记列表数据
- Query：
  - `page_id` (必填,string) 话题页面ID/Topic page ID
  - `sort` (选填,string) 排序方式/Sort: trend(最热), time(最新)
  - `cursor_score` (选填,string) 分页游标分数，翻页时传入/Pagination cursor score for next page
  - `last_note_id` (选填,string) 上一页最后一条笔记ID，翻页时传入/Last note ID from previous page
  - `last_note_ct` (选填,string) 上一页最后一条笔记创建时间，翻页时传入/Last note create time from previous page
  - `session_id` (选填,string) 会话ID，翻页时保持一致/Session ID, keep consistent for pagination
  - `first_load_time` (选填,string) 首次加载时间戳，翻页时保持一致/First load timestamp, keep consistent for pagination
  - `source` (选填,string) 来源/Source
- 示例：

```
page_id="5c1cc866febed9000184b7c1"
sort="trend"
```

## 获取创作者推荐灵感列表

`GET /api/v1/xiaohongshu/app_v2/get_creator_inspiration_feed`

- 用途：获取创作者中心的推荐创作灵感流，使用游标分页
- 返回：推荐灵感列表数据
- Query：
  - `cursor` (选填,string) 分页游标，首次请求留空/Pagination cursor, leave empty for first request
  - `tab` (选填,integer) 标签类型/Tab type
  - `source` (选填,string) 来源/Source
- 示例：

```
cursor=""
```

## 获取创作者热点灵感列表

`GET /api/v1/xiaohongshu/app_v2/get_creator_hot_inspiration_feed`

- 用途：获取创作者中心的热点创作灵感流，使用游标分页
- 返回：热点灵感列表数据
- Query：
  - `cursor` (选填,string) 分页游标，首次请求留空/Pagination cursor, leave empty for first request
- 示例：

```
cursor=""
```
