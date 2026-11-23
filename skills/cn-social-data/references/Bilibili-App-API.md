# Bilibili App API

文件夹 `Bilibili-App-API` · 11 个接口
说明：哔哩哔哩App数据接口


## 获取单个视频详情信息

`GET /api/v1/bilibili/app/fetch_one_video`

- 用途：获取单个视频详情信息（APP接口）
- 返回：视频详情信息
- Query：
  - `av_id` (选填,string) AV号/AV ID
  - `bv_id` (选填,string) BV号/BV ID
- 示例：

```
av_id = "115568241811221"
bv_id = "BV18SCrBGE9E"
```

## 获取视频评论列表

`GET /api/v1/bilibili/app/fetch_video_comments`

- 用途：获取视频评论列表
- 返回：评论列表数据
- Query：
  - `av_id` (选填,string) AV号/AV ID
  - `bv_id` (选填,string) BV号/BV ID
  - `mode` (选填,integer) 排序模式/Sort mode (3=热门/hot, 2=时间/time)
  - `next_offset` (选填,integer) 分页游标/Pagination cursor
- 示例：

```
bv_id = "BV18SCrBGE9E"
mode = 3
next_offset = 1
```

## 获取二级评论回复

`GET /api/v1/bilibili/app/fetch_reply_detail`

- 用途：获取二级评论回复
- 返回：二级评论列表数据
- Query：
  - `root` (必填,string) 一级评论ID/Root comment ID
  - `av_id` (选填,string) AV号/AV ID
  - `bv_id` (选填,string) BV号/BV ID
  - `next_offset` (选填,integer) 下一页游标/Next page cursor
  - `ps` (选填,integer) 每页数量/Page size
- 示例：

```
root = "241743663521"
av_id = "113100682434775"
```

## 获取用户投稿视频

`GET /api/v1/bilibili/app/fetch_user_videos`

- 用途：获取用户投稿视频列表
- 返回：用户投稿视频列表
- Query：
  - `user_id` (必填,string) 用户ID/User ID
  - `post_filter` (选填,string) 过滤类型/Filter type (archive/season/contribute)
  - `page` (选填,integer) 页码/Page number
  - `ps` (选填,integer) 每页数量/Page size
- 示例：

```
user_id = "203680252"
post_filter = "archive"
```

## 获取用户信息

`GET /api/v1/bilibili/app/fetch_user_info`

- 用途：获取用户信息
- 返回：用户信息（包含粉丝数、关注数、投稿数等）
- Query：
  - `user_id` (必填,string) 用户ID/User ID
- 示例：

```
user_id = "203680252"
```

## 获取主页推荐视频流

`GET /api/v1/bilibili/app/fetch_home_feed`

- 用途：获取主页推荐视频流
- 返回：推荐视频流数据
- Query：
  - `idx` (选填,integer) 页面索引/Page index
  - `flush` (选填,integer) 刷新标记/Flush flag (0=普通加载, 1=刷新)
  - `pull` (选填,boolean) 是否下拉刷新/Pull to refresh

## 获取热门推荐

`GET /api/v1/bilibili/app/fetch_popular_feed`

- 用途：获取热门推荐视频
- 返回：热门推荐视频数据
- Query：
  - `idx` (选填,integer) 页面索引/Page index
  - `last_param` (选填,string) 上一页最后一个视频ID/Last video ID
- 示例：

```
idx = 1
```

## 综合搜索

`GET /api/v1/bilibili/app/fetch_search_all`

- 用途：综合搜索（返回所有类型的搜索结果）
- 返回：搜索结果，包含nav（分类导航）、item（搜索结果）、pagination（分页信息）等；下一页游标：`$.data.data.pagination.next`，把它作为下一次请求的 `cursor` 传回
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `cursor` (选填,string) 翻页游标，首页留空；翻页时传回上一页响应的 data.pagination.next/Pagination cursor, leave empty for the first page; for the next page pass back data.pagination.next from the previous response
  - `page_size` (选填,integer) 每页数量/Page size
  - `order` (选填,integer) 排序方式/Sort order (0=综合排序)
- 示例：

```
keyword = "原神"
cursor = ""
page_size = 20
```

## 分类搜索

`GET /api/v1/bilibili/app/fetch_search_by_type`

- 用途：分类搜索（按类型搜索）
- 返回：搜索结果；下一页游标：`$.data.data.pagination.next`，把它作为下一次请求的 `cursor` 传回
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `search_type` (选填,string) 搜索类型/Search type (video/bangumi/pgc/live/article/user)
  - `cursor` (选填,string) 翻页游标，首页留空；翻页时传回上一页响应的 data.pagination.next/Pagination cursor, leave empty for the first page; for the next page pass back data.pagination.next from the previous response
  - `page_size` (选填,integer) 每页数量/Page size
  - `order` (选填,integer) 排序方式/Sort order (0=综合, 1=最新, 2=播放量, 3=弹幕数)
- 示例：

```
keyword = "原神"
search_type = "video"
cursor = ""
```

## 获取影视推荐

`GET /api/v1/bilibili/app/fetch_cinema_tab`

- 用途：获取主页影视推荐
- 返回：影视推荐数据

## 获取番剧推荐

`GET /api/v1/bilibili/app/fetch_bangumi_tab`

- 用途：获取主页番剧推荐
- 返回：番剧推荐数据
