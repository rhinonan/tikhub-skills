# Xiaohongshu Web V3 API

文件夹 `Xiaohongshu-Web-V3-API` · 5 个接口
说明：小红书网页版 V3 数据接口


## 获取笔记详情

`GET /api/v1/xiaohongshu/web_v3/fetch_note_detail`

- 用途：获取笔记详情（图文/视频通用）
- 返回：笔记详情数据
- Query：
  - `note_id` (必填,string) 笔记ID/Note ID
  - `xsec_token` (必填,string) 安全令牌，可以从小红书的分享链接中获取/Security token, can be obtained from the sharing link of Xiaohongshu
- 示例：

```
note_id = "6a2f423d000000001003cb36"
xsec_token = "ABtexB6bX5HgLD42SFrK1scGUmSO8YV5_isaLrDy9sLxQ="
```

## 获取搜索联想词

`GET /api/v1/xiaohongshu/web_v3/fetch_search_suggest`

- 用途：获取搜索联想词，keyword 为空时返回热门推荐
- 返回：联想词列表
- Query：
  - `keyword` (选填,string) 关键词 (可为空)/Keyword (optional)
- 示例：

```
keyword = "口红"
```

## 获取首页推荐

`GET /api/v1/xiaohongshu/web_v3/fetch_homefeed`

- 用途：获取首页推荐笔记列表
- 返回：推荐笔记列表
- Query：
  - `num` (选填,integer) 返回数量，最大40/Number of results, max 40
  - `cursor_score` (选填,string) 翻页游标/Pagination cursor
  - `category` (选填,string) 分类频道ID/Category channel ID
  - `need_filter_image` (选填,boolean) 仅图文/Image notes only
- 示例：

```
num = 20
category = "homefeed_recommend"
```

## 获取首页分类列表

`GET /api/v1/xiaohongshu/web_v3/fetch_homefeed_categories`

- 用途：获取首页频道分类列表
- 返回：分类列表

## 获取用户信息

`GET /api/v1/xiaohongshu/web_v3/fetch_user_info`

- 用途：获取用户公开资料
- 返回：用户信息
- Query：
  - `user_id` (必填,string) 用户ID/User ID
- 示例：

```
user_id = "5e3a8ee700000000010070c6"
```
- 返回结构（实测）：
  - `data` 是对象（6 个字段）：`ok`, `status`, `code`, `success`, `msg`, `data`
  - `data.data` 是对象（9 个字段）：`liked`, `result`, `basic_info`, `interactions`, `collected`, `tags`, `tab_public`, `extra_info`, `posted`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23
