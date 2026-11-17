# Douyin Search API（搜索）

文件夹 `Douyin-Search-API` · 23 个接口 · BASE `https://api.tikhub.io`

## 获取话题搜索 V1

`POST /api/v1/douyin/search/fetch_challenge_search_v1`

- 用途：获取抖音 App 中的话题（挑战/标签）搜索结果。
- 返回：`cursor`: 翻页游标（用于下次请求）
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取话题搜索 V2

`POST /api/v1/douyin/search/fetch_challenge_search_v2`

- 用途：获取抖音 App 中话题(挑战/标签)搜索的结果，使用 V2 版本 API。
- 返回：`business_data`（话题搜索结果列表）
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取话题推荐搜索

`POST /api/v1/douyin/search/fetch_challenge_suggest`

- 用途：获取抖音 App 中话题(挑战/标签)的推荐搜索结果。
- 返回：`sug_list[]`: 推荐话题列表
- Body(JSON)：
  - `keyword` (string,默认 游戏) 关键词，如 '游戏' / Keyword, e.g., 'game'

## 获取讨论搜索

`POST /api/v1/douyin/search/fetch_discuss_search`

- 用途：获取抖音 App 中讨论区/问答内容的搜索结果。
- 返回：`data`: 搜索结果列表
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取经验搜索

`POST /api/v1/douyin/search/fetch_experience_search`

- 用途：获取抖音 App 中经验（知识/教程）内容的搜索结果。
- 返回：business_data: 搜索结果业务数据列表
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取综合搜索 V1

`POST /api/v1/douyin/search/fetch_general_search_v1`

- 用途：获取抖音 App 中综合搜索栏的搜索结果（非单独视频搜索）。
- 返回：`data`: 搜索结果列表
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取综合搜索 V2

`POST /api/v1/douyin/search/fetch_general_search_v2`

- 用途：获取抖音 App 中综合搜索栏的搜索结果（非单独视频搜索）。
- 返回：`data`: 搜索结果列表
- 返回结构（实测 2026-11-17）：
  - ⚠️ **`data` 为 `null`**，真实内容在顶层 `business_data[]`（实测 18 类卡片）
  - `business_data[i].type` — 卡片类型，视频/用户/直播的字段各不相同，先判类型再解析
  - `global_config` / `business_config` / `log_pb` — 透传配置与日志，一般不用
  - 入口建议：先按 `type` 过滤出视频卡片，再取内部的 `aweme_info`（结构与 `aweme_detail` 同源）
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取综合搜索 V3

`POST /api/v1/douyin/search/fetch_general_search_v3`

- 用途：获取抖音综合搜索结果（V3 版本），返回视频、用户、相关搜索词等混合卡片。
- 返回：`config`: 本次搜索的配置信息（透传）
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 搜索关键词 / Search keyword
  - `offset` (integer,默认 0) 翻页游标，从上一次响应的 data.pagination.offset 获取，首次请求传 0 / Offset cursor for pagination, obtained from data.pagination.offset of the last response, 0 for the first request
  - `page` (integer,默认 1) 页码，取值 1~200，首次请求传 1，之后每次加 1 / Page number, 1-200, start with 1 and increment by 1 each time
  - `search_id` (string) 搜索ID，从上一次响应的 data.pagination.search_id 获取，首次请求传空字符串 / Search ID, obtained from data.pagination.search_id of the last response, empty for the first request
  - `backtrace` (string) 翻页回溯标识，从上一次响应的 data.pagination.backtrace 获取，首次请求传空字符串 / Backtrace, obtained from data.pagination.backtrace of the last response, empty for the first request

## 获取图片搜索

`POST /api/v1/douyin/search/fetch_image_search`

- 用途：获取抖音 App 中图片内容搜索的结果。
- 返回：`cursor`: 下一页游标
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取图文搜索 V3

`POST /api/v1/douyin/search/fetch_image_search_v3`

- 用途：获取抖音 App 中图文内容搜索的结果。
- 返回：`status_code`: 状态码（0=成功）
- Body(JSON)：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `cursor` (integer,默认 0) 翻页游标/Pagination cursor
  - `search_id` (string) 搜索ID/Search ID for pagination

## 获取直播搜索 V2

`POST /api/v1/douyin/search/fetch_live_search_v2`

- 用途：按抖音号或抖音昵称搜索直播间（V2 版本），支持游标翻页。
- 返回：匹配的直播间列表，每项包含主播昵称、抖音号、头像、直播间ID及开播状态等
- Body(JSON)：
  - `keyword` (string,默认 小耳朵) 抖音号 或 抖音昵称 / Douyin ID or nickname
  - `cursor` (integer,默认 0) 翻页游标，首次请求传 0，之后传上一页响应里的 cursor / Pagination cursor, 0 for the first request, then the cursor from the last response

## 获取多重搜索

`POST /api/v1/douyin/search/fetch_multi_search`

- 用途：获取抖音 App 中多种类型（视频、用户、音乐、话题等）的综合搜索结果。
- 返回：`cursor`: 下一页翻页游标
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取音乐搜索

`POST /api/v1/douyin/search/fetch_music_search`

- 用途：获取抖音 App 中音乐内容的搜索结果。
- 返回：`music`: 音乐结果列表
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取学校搜索

`POST /api/v1/douyin/search/fetch_school_search`

- 用途：获取抖音 App 中学校信息的搜索结果。
- 返回：`schools[]`: 学校列表
- Body(JSON)：
  - `keyword` (string,默认 北京) 关键词，如学校名称或所在地区 / Keyword, such as school name or location

## 获取搜索关键词推荐

`POST /api/v1/douyin/search/fetch_search_suggest`

- 用途：获取抖音 App 中搜索关键词的联想推荐结果。
- 返回：`status_code`: 状态码（0 表示成功）
- Body(JSON)：
  - `keyword` (string,默认 人工智能) 需要联想的关键词/The keyword to be suggested

## 获取搜索关键词推荐 V2

`POST /api/v1/douyin/search/fetch_search_suggest_v2`

- 用途：获取抖音搜索关键词的联想推荐结果（V2 版本）。
- 返回：`words[]`: 联想词字符串列表（多数场景只需要这个）
- Body(JSON)：
  - `keyword` (string,默认 人工智能) 需要联想的关键词/The keyword to be suggested
  - `history_words` (string) 可选，用户的历史搜索词（英文逗号分隔），会影响联想词的排序/Optional, the user's history search words (comma separated), affects the ranking of suggestions

## 获取用户搜索

`POST /api/v1/douyin/search/fetch_user_search`

- 用途：获取抖音 App 中根据关键词搜索到的用户列表。
- 返回：`cursor`: 下一页游标
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `douyin_user_fans` (string) 粉丝数过滤：空=不限 0_1k=1千以下 1k_5k=1千到5千 5k_10k=5千到1万 10k_100k=1万到10万 100k_1M=10万到100万 1M_=100万以上 / Fans filter: empty=No limit, 0_1k=Under 1k, etc.
  - `douyin_user_type` (string) 用户类型过滤：空=不限 300=创作者 900=小店 700=音乐人 800=明星 / User type filter: empty=No limit, 300=Creator, 900=Shop, 700=Musician, 800=Celebrity
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response

## 获取用户搜索 V2

`POST /api/v1/douyin/search/fetch_user_search_v2`

- 用途：获取抖音 App 中根据关键词搜索到的用户列表。
- 返回：`cursor`: 下一页游标
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response

## 获取视频搜索 V1

`POST /api/v1/douyin/search/fetch_video_search_v1`

- 用途：获取抖音 App 中通过关键词搜索到的视频内容。
- 返回：`status_code`: 响应状态码（0表示成功）
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取视频搜索 V2

`POST /api/v1/douyin/search/fetch_video_search_v2`

- 用途：获取抖音 App 中通过关键词搜索到的视频内容（V2版本接口）。
- 返回：`business_data[]`: 搜索返回的数据列表
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 关键词 / Keyword
  - `cursor` (integer,默认 0) 偏移游标，用于翻页，从上一次请求返回的响应中获取 / Offset cursor for pagination, obtained from the last response
  - `sort_type` (string,默认 0) 排序方式：0=综合排序 1=最多点赞 2=最新发布 / Sort type: 0=Comprehensive, 1=Most Likes, 2=Latest
  - `publish_time` (string,默认 0) 发布时间筛选：0=不限 1=最近一天 7=最近一周 180=最近半年 / Publish time filter: 0=Unlimited, 1=Last day, 7=Last week, 180=Last half year
  - `filter_duration` (string,默认 0) 视频时长过滤：0=不限 0-1=一分钟以内 1-5=一到五分钟 5-10000=五分钟以上 / Video duration filter: 0=Unlimited, 0-1=Within 1 minute, 1-5=1 to 5 minutes, 5-10000=More than 5 minutes
  - `content_type` (string,默认 0) 内容类型：0=不限 1=视频 2=图片 3=文章 / Content type: 0=All, 1=Video, 2=Picture, 3=Article
  - `search_id` (string) 搜索ID，用于翻页，从上一次请求返回的响应中获取 / Search ID for pagination, obtained from the last response
  - `backtrace` (string) 翻页回溯标识，用于翻页，从上一次请求返回的响应中获取 / Backtrace for pagination, obtained from the last response

## 获取视频搜索 V3

`POST /api/v1/douyin/search/fetch_video_search_v3`

- 用途：按关键词搜索视频（V3 版本），支持发布时间、视频类型、时长三维筛选。
- 返回：视频列表，每项包含：
- Body(JSON)：
  - `query` (string,默认 美食) 搜索关键词/Search keyword
  - `date_type` (integer,默认 0) 发布时间筛选：0=不限, 3=近3天, 7=近7天, 30=近一个月/Publish date filter: 0=any, 3=last 3 days, 7=last 7 days, 30=last 30 days
  - `label_type` (integer,默认 0) 视频类型筛选：0=不限, 1=低粉爆款, 2=高完播率, 3=高涨粉率, 4=高点赞率/Video type filter: 0=any, 1=low-follower hit, 2=high completion rate, 3=high follower growth, 4=high like rate
  - `duration_type` (integer,默认 0) 时长筛选：0=不限, 1=0-15秒, 6=15-60秒, 7=60-120秒, 8=120-180秒, 9=大于180秒/Duration filter: 0=any, 1=0-15s, 6=15-60s, 7=60-120s, 8=120-180s, 9=over 180s

## 获取视频搜索 V4

`POST /api/v1/douyin/search/fetch_video_search_v4`

- 用途：按视频标题/关键词搜索视频（V4 版本），支持游标翻页。
- 返回：匹配的视频列表，每项包含视频ID、标题、封面、时长、发布时间及互动数据等
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 视频标题/关键词 / Video title or keyword
  - `cursor` (integer,默认 0) 翻页游标，首次请求传 0，之后传上一页响应里的 cursor / Pagination cursor, 0 for the first request, then the cursor from the last response

## 获取视频搜索 V5

`POST /api/v1/douyin/search/fetch_video_search_v5`

- 用途：按关键词搜索视频（V5 版本），只返回视频内容。
- 返回：`config`: 本次搜索的配置信息（透传）
- 返回结构（实测 2026-11-17）：
  - ⚠️ 2026-11-17 实测：参数按文档传（`keyword`/`offset`/`page`/`search_id`/`backtrace`）连续两次返回 **HTTP 400**（官方提示 Please retry，未计费）
  - 当前可用替代：`search/fetch_general_search_v2`（综合搜索，能用）或 `app/v3` 的视频搜索
  - 恢复后返回结构为 `data.items[]`（10 条/页，视频在 `items[].aweme_info`）+ `data.pagination`（`search_id`/`offset`/`cursor`/`backtrace`/`has_more`）
- Body(JSON)：
  - `keyword` (string,默认 猫咪) 搜索关键词 / Search keyword
  - `offset` (integer,默认 0) 翻页游标，从上一次响应的 data.pagination.offset 获取，首次请求传 0 / Offset cursor for pagination, obtained from data.pagination.offset of the last response, 0 for the first request
  - `page` (integer,默认 1) 页码，取值 1~200，首次请求传 1，之后每次加 1 / Page number, 1-200, start with 1 and increment by 1 each time
  - `search_id` (string) 搜索ID，从上一次响应的 data.pagination.search_id 获取，首次请求传空字符串 / Search ID, obtained from data.pagination.search_id of the last response, empty for the first request
  - `backtrace` (string) 翻页回溯标识，从上一次响应的 data.pagination.backtrace 获取，首次请求传空字符串 / Backtrace, obtained from data.pagination.backtrace of the last response, empty for the first request
