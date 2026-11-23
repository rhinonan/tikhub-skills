# Zhihu Web API

文件夹 `Zhihu-Web-API` · 41 个接口
说明：知乎Web数据接口


## 获取知乎专栏文章列表

`GET /api/v1/zhihu/web/fetch_column_articles`

- 用途：获取知乎专栏文章列表
- 返回：知乎专栏文章列表
- Query：
  - `column_id` (必填,string) 专栏ID/Column ID
  - `limit` (选填,string) 每页文章数量/Number of articles per page
  - `offset` (选填,string) 偏移量/Offset
- 示例：

```
column_id = "zhangjiawei"
limit = "10"
offset = "0"
```
- 返回结构（实测）：
  - `data` 是对象（3 个字段）：`paging`, `data`, `need_force_login`
  - `data.paging` 是对象（5 个字段）：`is_end`, `totals`, `previous`, `is_start`, `next`
  - `data.data` 是数组（长度 10）；首元素字段：`updated`, `is_labeled`, `copyright_permission`, `settings`, `excerpt`, `admin_closed_comment`, `voting`, `article_type`
  - `data.data` 是数组（长度 10）；首元素字段：`updated`, `is_labeled`, `copyright_permission`, `settings`, `excerpt`, `admin_closed_comment`, `voting`, `article_type`, `reason`, `force_login_when_click_read_more`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取知乎专栏文章详情

`GET /api/v1/zhihu/web/fetch_column_article_detail`

- 用途：获取知乎专栏文章详情
- 返回：知乎专栏文章详情
- Query：
  - `article_id` (必填,string) 文章ID/Article ID
- 示例：

```
article_id = "669214677"
```
- 返回结构（实测）：
  - `data` 是对象（70 个字段）：`id`, `title`, `type`, `article_type`, `excerpt_title`, `url`, `image_url`, `title_image`, `excerpt`, `created`, `updated`, `author`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取知乎相似专栏推荐

`GET /api/v1/zhihu/web/fetch_column_recommend`

- 用途：获取知乎相似专栏推荐
- 返回：知乎相似专栏推荐
- Query：
  - `article_id` (必填,string) 文章ID/Article ID
  - `limit` (选填,string) 每页专栏数量/Number of columns per page
  - `offset` (选填,string) 偏移量/Offset
- 示例：

```
article_id = "669214677"
limit = "12"
offset = "0"
```

## 获取知乎专栏文章互动关系

`GET /api/v1/zhihu/web/fetch_column_relationship`

- 用途：获取知乎专栏文章互动关系
- 返回：知乎专栏互动关系
- Query：
  - `article_id` (必填,string) 文章ID/Article ID
- 示例：

```
article_id = "669214677"
```

## 获取知乎专栏评论区配置

`GET /api/v1/zhihu/web/fetch_column_comment_config`

- 用途：获取知乎专栏评论区配置
- 返回：知乎专栏评论区配置
- Query：
  - `article_id` (必填,string) 文章ID/Article ID
- 示例：

```
article_id = "669214677"
```

## 获取知乎首页推荐

`GET /api/v1/zhihu/web/fetch_hot_recommend`

- 用途：获取知乎首页推荐
- 返回：知乎首页推荐
- Query：
  - `offset` (选填,string) 偏移量/Offset
  - `page_number` (选填,string) 页码/Page Number
  - `session_token` (选填,string) 会话令牌/Session Token
- 示例：

```
offset = "0"
page_number = "1"
session_token = ""
```

## 获取知乎首页热榜

`GET /api/v1/zhihu/web/fetch_hot_list`

- 用途：获取知乎首页热榜
- 返回：知乎首页热榜
- Query：
  - `limit` (选填,string) 每页文章数量/Number of articles per page
  - `desktop` (选填,string) 是否为桌面端/Is it a desktop
- 示例：

```
limit = "50"
desktop = "true"
```
- 返回结构（实测）：
  - `data` 是对象（10 个字段）：`data`, `paging`, `kanshan`, `fresh_text`, `display_num`, `display_first`, `fb_bill_main_rise`, `head_zone`, `head_zones`, `prefer_hot_topics_top_card`
  - `data.data` 是数组（长度 30）；首元素字段：`type`, `style_type`, `id`, `card_id`, `target`, `attached_info`, `detail_text`, `trend`
  - `data.paging` 是对象（5 个字段）：`is_end`, `is_start`, `next`, `previous`, `totals`
  - `data.kanshan` 是对象（3 个字段）：`image_url`, `guide_text`, `query`
  - `data.data` 是数组（长度 30）；首元素字段：`type`, `style_type`, `id`, `card_id`, `target`, `attached_info`, `detail_text`, `trend`, `debut`, `children`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取知乎首页视频榜

`GET /api/v1/zhihu/web/fetch_video_list`

- 用途：获取知乎首页视频榜
- 返回：知乎首页视频榜
- Query：
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页视频数量/Number of videos per page
- 示例：

```
offset = ""
limit = "12"
```

## 获取知乎文章搜索V3

`GET /api/v1/zhihu/web/fetch_article_search_v3`

- 用途：获取知乎文章搜索V3
- 返回：知乎文章搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页文章数量/Number of articles per page
  - `show_all_topics` (选填,integer) 显示所有主题/Show all topics
  - `search_source` (选填,string) 搜索来源/Search Source
  - `search_hash_id` (选填,string) 搜索哈希ID/Search Hash ID
  - `vertical` (选填,string) 垂类/Vertical Type
  - `sort` (选填,string) 排序/Sort
  - `time_interval` (选填,string) 时间间隔/Time Interval
  - `vertical_info` (选填,string) 垂类信息/Vertical Info
- 示例：

```
# 默认搜索，综合排序，不限时间
keyword = "deepseek"
offset = "0"
limit = "20"
show_all_topics = 0
search_source = "Normal"
search_hash_id = ""
vertical = ""
sort = ""
time_interval = ""
vertical_info = ""

# 只看回答，最多赞同，三月内
keyword = "deepseek"
offset = "0"
limit = "20"
show_all_topics = 0
search_source = "Filter"
search_hash_id = ""
vertical = "answer"
sort = "upvoted_count"
time_interval = "three_months"
vertical_info = "0,0,0,0,0,0,0,0,0,0,0,0"
```

## 获取知乎用户搜索V3

`GET /api/v1/zhihu/web/fetch_user_search_v3`

- 用途：获取知乎用户搜索V3
- 返回：知乎用户搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页用户数量/Number of users per page
- 示例：

```
keyword = "deepseek"
offset = "0"
limit = "25"
```

## 获取知乎话题搜索V3

`GET /api/v1/zhihu/web/fetch_topic_search_v3`

- 用途：获取知乎话题搜索V3
- 返回：知乎话题搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页话题数量/Number of topics per page
- 示例：

```
keyword = "deepseek"
offset = "0"
limit = "25"
```

## 获取知乎论文搜索V3

`POST /api/v1/zhihu/web/fetch_scholar_search_v3`

- 用途：获取知乎论文搜索V3
- 返回：知乎论文搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页论文数量/Number of papers per page
- 示例：

```
keyword = "人工智能"
offset = "0"
limit = "25"
```

## 获取知乎视频搜索V3

`GET /api/v1/zhihu/web/fetch_video_search_v3`

- 用途：获取知乎视频搜索V3
- 返回：知乎视频搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `limit` (选填,string) 每页视频数量/Number of videos per page
  - `offset` (选填,string) 偏移量/Offset
  - `search_hash_id` (选填,string) 搜索哈希ID/Search Hash ID
- 示例：

```
keyword = "deepseek"
limit = "20"
offset = "0"
search_hash_id = ""
```

## 获取知乎专栏搜索V3

`GET /api/v1/zhihu/web/fetch_column_search_v3`

- 用途：获取知乎专栏搜索V3
- 返回：知乎专栏搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页专栏数量/Number of columns per page
  - `search_hash_id` (选填,string) 搜索哈希ID/Search Hash ID
- 示例：

```
keyword = "deepseek"
limit = "20"
offset = "0"
search_hash_id = ""
```

## 获取知乎盐选内容搜索V3

`GET /api/v1/zhihu/web/fetch_salt_search_v3`

- 用途：获取知乎盐选内容搜索V3
- 返回：知乎盐选内容搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页内容数量/Number of contents per page
  - `search_hash_id` (选填,string) 搜索哈希ID/Search Hash ID
- 示例：

```
keyword = "deepseek"
limit = "20"
offset = "0"
search_hash_id = ""
```

## 获取知乎电子书搜索V3

`GET /api/v1/zhihu/web/fetch_ebook_search_v3`

- 用途：获取知乎电子书搜索V3
- 返回：知乎电子书搜索V3
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页电子书数量/Number of ebooks per page
  - `search_hash_id` (选填,string) 搜索哈希ID/Search Hash ID
- 示例：

```
keyword = "deepseek"
limit = "20"
offset = "0"
search_hash_id = ""
```

## 获取知乎搜索预设词

`GET /api/v1/zhihu/web/fetch_preset_search`

- 用途：获取知乎搜索预设词
- 返回：知乎搜索预设词

## 获取知乎搜索发现

`GET /api/v1/zhihu/web/fetch_search_recommend`

- 用途：获取知乎搜索发现
- 返回：知乎搜索发现

## 知乎搜索预测词

`GET /api/v1/zhihu/web/fetch_search_suggest`

- 用途：知乎搜索预测词
- 返回：知乎搜索预测词
- Query：
  - `keyword` (必填,string) 搜索关键词/Search Keywords
- 示例：

```
keyword = "deepseek"
```

## 获取知乎评论区V5

`GET /api/v1/zhihu/web/fetch_comment_v5`

- 用途：获取知乎评论区V5
- 返回：知乎评论区V5
- Query：
  - `answer_id` (必填,string) 回答ID/Answer ID
  - `order_by` (选填,string) 排序/Sort
  - `limit` (选填,string) 每页评论数量/Number of comments per page
  - `offset` (选填,string) 偏移量/Offset
- 示例：

```
answer_id = "89226347214"
order_by = "score"
limit = "20"
offset = "" # 1739257701_11108372663_0
```

## 获取知乎子评论区V5

`GET /api/v1/zhihu/web/fetch_sub_comment_v5`

- 用途：获取知乎子评论区V5
- 返回：知乎子评论区V5
- Query：
  - `comment_id` (必填,string) 评论ID/Comment ID
  - `order_by` (选填,string) 排序/Sort
  - `limit` (选填,string) 每页评论数量/Number of comments per page
  - `offset` (选填,string) 偏移量/Offset
- 示例：

```
comment_id = "11100789728"
order_by = "score"
limit = "20"
offset = ""
```

## 获取知乎用户信息

`GET /api/v1/zhihu/web/fetch_user_info`

- 用途：获取知乎用户信息
- 返回：知乎用户信息
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
- 示例：

```
user_url_token = "ming-he-43-93"
```

## 获取知乎用户关注列表

`GET /api/v1/zhihu/web/fetch_user_followees`

- 用途：获取知乎用户关注列表
- 返回：知乎用户关注列表
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页用户数量/Number of users per page
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
```

## 获取知乎用户粉丝列表

`GET /api/v1/zhihu/web/fetch_user_followers`

- 用途：获取知乎用户粉丝列表
- 返回：知乎用户粉丝列表
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页用户数量/Number of users per page
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
```

## 获取知乎用户的文章列表

`GET /api/v1/zhihu/web/fetch_user_articles`

- 用途：获取知乎用户的文章列表
- 返回：知乎用户的文章列表
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页文章数量/Number of articles per page
  - `sort_type` (选填,string) 排序类型/Sort Type
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
sort_type = "created"
```

## 获取知乎用户的被收录文章列表

`GET /api/v1/zhihu/web/fetch_user_included_articles`

- 用途：获取知乎用户的被收录文章列表
- 返回：知乎用户的被收录文章列表
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页文章数量/Number of articles per page
- 示例：

```
user_url_token = "jzwa"
offset = "0"
limit = "20"
```

## 获取知乎用户订阅的专栏

`GET /api/v1/zhihu/web/fetch_user_follow_columns`

- 用途：获取知乎用户订阅的专栏
- 返回：知乎用户订阅的专栏
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页专栏数量/Number of columns per page
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
```

## 获取知乎用户关注的问题

`GET /api/v1/zhihu/web/fetch_user_follow_questions`

- 用途：获取知乎用户关注的问题
- 返回：知乎用户关注的问题
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页问题数量/Number of questions per page
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
```

## 获取知乎用户关注的收藏

`GET /api/v1/zhihu/web/fetch_user_follow_collections`

- 用途：获取知乎用户关注的收藏
- 返回：知乎用户关注的收藏
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页收藏数量/Number of collections per page
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
```

## 获取知乎用户关注的话题

`GET /api/v1/zhihu/web/fetch_user_follow_topics`

- 用途：获取知乎用户关注的话题
- 返回：知乎用户关注的话题
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页话题数量/Number of topics per page
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
```

## 获取知乎推荐关注列表

`GET /api/v1/zhihu/web/fetch_recommend_followees`

- 用途：获取知乎推荐关注列表
- 返回：知乎推荐关注列表

## 获取知乎问题回答列表

`GET /api/v1/zhihu/web/fetch_question_answers`

- 用途：获取知乎问题的回答列表
- 返回：知乎问题回答列表数据。分页会话绑定首次成功请求的账号，由服务自动保持；机构号可用性取决于当前权限和限频状态；`data.paging.is_end=true` 或 next 缺失时停止。解析 next 的 cursor、offset、session_id、limit、order 原样传回；offset 不要自行加 limit。切换问题或排序时从首页重新开始。分页状态在成功获取后续游标时续期 15 分钟；会话过期或账号不可用需重新请求首页，暂时繁忙可使用相同游标重试
- Query：
  - `question_id` (必填,string) 问题ID/Question ID
  - `cursor` (选填,string) 从 data.paging.next URL 提取/Pagination cursor from data.paging.next URL
  - `limit` (选填,integer) 每页回答数量/Number of answers per page
  - `offset` (选填,integer) 从 data.paging.next 原样提取，勿自行加 limit/Use next URL offset unchanged
  - `order` (选填,string) 排序方式：default=默认排序，updated=按时间排序/Sort order: default=default sort, updated=sort by time
  - `session_id` (选填,string) 从 data.paging.next URL 提取/Session ID from data.paging.next URL
- 示例：

```
question_id = "37811449"
cursor = ""
limit = 5
offset = 0
order = "default"  # 或 "updated" 按时间排序
session_id = ""

# 获取下一页 (Get next page):
# 从本次响应 data.paging.next URL 提取参数，不复用文档中的固定游标
# Extract the next URL parameters from this response; never reuse a static cursor.

# 按时间排序 (Sort by time):
order = "updated"
```

## 获取知乎问题详情

`GET /api/v1/zhihu/web/fetch_question_detail`

- 用途：获取知乎问题详情 (标题/描述/统计/话题等)
- 返回：知乎问题详情
- Query：
  - `question_id` (必填,string) 问题ID/Question ID
- 示例：

```
question_id = "37811449"
```

## 获取知乎回答详情

`GET /api/v1/zhihu/web/fetch_answer_detail`

- 用途：获取知乎单个回答的详情 (正文/统计/作者/所属问题等)
- 返回：知乎回答详情
- Query：
  - `answer_id` (必填,string) 回答ID/Answer ID
- 示例：

```
answer_id = "2054145988235880002"
```

## 获取知乎用户的回答列表

`GET /api/v1/zhihu/web/fetch_user_answers`

- 用途：获取知乎用户的回答列表
- 返回：知乎用户的回答列表
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页回答数量/Number of answers per page
  - `sort_type` (选填,string) 排序类型/Sort Type
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
sort_type = "created"
```

## 获取知乎用户创建的收藏夹列表

`GET /api/v1/zhihu/web/fetch_user_collections`

- 用途：获取知乎用户**创建**的收藏夹列表 (区别于"关注的收藏夹")
- 返回：知乎用户创建的收藏夹列表
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页收藏夹数量/Number of collections per page
- 示例：

```
user_url_token = "ming-he-43-93"
offset = "0"
limit = "20"
```

## 获取知乎用户的划线列表

`GET /api/v1/zhihu/web/fetch_user_segments`

- 用途：获取知乎用户的划线列表 (lineComments)
- 返回：知乎用户的划线列表
- Query：
  - `user_url_token` (必填,string) 用户 member hash id (非 url_token)/User member hash id (not url_token)
  - `content_type` (选填,string) 内容类型/Content type
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页数量/Number per page
- 示例：

```
user_url_token = "c72367b43730a490687966ceb87e9305"
content_type = "all"
offset = "0"
limit = "20"
```

## 获取知乎用户的想法列表

`GET /api/v1/zhihu/web/fetch_user_pins`

- 用途：获取知乎用户的想法 (pins / moments) 列表
- 返回：知乎用户的想法列表
- Query：
  - `user_url_token` (必填,string) 用户ID/User ID
  - `offset` (选填,string) 偏移量/Offset
  - `limit` (选填,string) 每页想法数量/Number of pins per page
- 示例：

```
user_url_token = "persistence-66-66"
offset = "0"
limit = "20"
```

## 获取知乎想法详情

`GET /api/v1/zhihu/web/fetch_pin_detail`

- 用途：获取单条知乎想法 (pin) 的详情
- 返回：知乎想法详情
- Query：
  - `pin_id` (必填,string) 想法ID/Pin ID
- 示例：

```
pin_id = "2050290260991534603"
```

## 获取知乎想法评论区

`GET /api/v1/zhihu/web/fetch_pin_comments`

- 用途：获取知乎想法 (pin) 的评论区列表
- 返回：知乎想法评论列表
- Query：
  - `pin_id` (必填,string) 想法ID/Pin ID
  - `order_by` (选填,string) 排序方式：score=默认，ts=最新/Sort: score=default, ts=newest
  - `limit` (选填,string) 每页评论数量/Number of comments per page
  - `offset` (选填,string) 偏移量，翻页用返回里的游标/Offset from response cursor
- 示例：

```
pin_id = "2050290260991534603"
order_by = "score"
limit = "20"
offset = ""
```

## 获取知乎AI搜索(新版)

`GET /api/v1/zhihu/web/fetch_ai_search_stream`

- 用途：获取知乎 AI 搜索结果 (新版接口)
- 返回：知乎 AI 搜索结果, 数据为事件列表 {"events": [...]}
- Query：
  - `message_content` (必填,string) 搜索内容/Search Content
  - `chat_mode` (选填,string) 对话模式/Chat mode
  - `session_id` (选填,string) 会话ID/Session ID
- 示例：

```
message_content = "deepseek"
chat_mode = "FAST"
session_id = ""
```
