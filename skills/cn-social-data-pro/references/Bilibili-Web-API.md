# Bilibili Web API

文件夹 `Bilibili-Web-API` · 32 个接口
说明：哔哩哔哩Web数据接口


## 获取单个视频详情信息

`GET /api/v1/bilibili/web/fetch_one_video`

- 用途：获取单个视频详情信息
- 返回：视频详情信息
- Query：
  - `bv_id` (必填,string) 作品id/Video id
- 示例：

```
bv_id = "BV1M1421t7hT"
```
- 返回结构（实测）：
  - `data` 是对象（4 个字段）：`code`, `message`, `ttl`, `data`
  - `data.data` 是对象（46 个字段）：`bvid`, `aid`, `videos`, `tid`, `tid_v2`, `tname`, `tname_v2`, `copyright`
  - `data.data` 是对象（46 个字段）：`bvid`, `aid`, `videos`, `tid`, `tid_v2`, `tname`, `tname_v2`, `copyright`, `pic`, `title`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取单个视频详情信息V2

`GET /api/v1/bilibili/web/fetch_one_video_v2`

- 用途：获取单个视频详情信息V2
- 返回：视频详情信息V2
- Query：
  - `a_id` (必填,string) 作品id/Video id
  - `c_id` (必填,string) 作品cid/Video cid
- 示例：

```
a_id = "114006081739452"
c_id = "28400484458"
```

## 获取单个视频详情信息V3

`GET /api/v1/bilibili/web/fetch_one_video_v3`

- 用途：获取单个视频详情信息V3
- 返回：视频详情信息V3
- Query：
  - `url` (必填,string) 视频链接/Video URL
- 示例：

```
url = "https://www.bilibili.com/video/BV1S5uKzzE4r"
```

## 获取单个视频详情

`GET /api/v1/bilibili/web/fetch_video_detail`

- 用途：获取单个视频详情
- 返回：视频详情
- Query：
  - `aid` (必填,string) 作品id/Video id
- 示例：

```
aid = "114902186396822"
```

## 获取单个视频播放信息

`GET /api/v1/bilibili/web/fetch_video_play_info`

- 用途：获取单个视频播放信息
- 返回：视频播放信息
- Query：
  - `url` (必填,string) 视频链接/Video URL
- 示例：

```
url = "https://www.bilibili.com/video/BV1S5uKzzE4r"
```

## 获取视频字幕信息

`GET /api/v1/bilibili/web/fetch_video_subtitle`

- 用途：获取视频字幕信息
- 返回：视频字幕信息
- Query：
  - `a_id` (必填,string) 作品id/Video id
  - `c_id` (必填,string) 作品cid/Video cid
- 示例：

```
a_id = "114006081739452"
c_id = "28400484458"
```

## 获取热门搜索信息

`GET /api/v1/bilibili/web/fetch_hot_search`

- 用途：获取热门搜索信息
- 返回：热门搜索信息
- 注意：limit default is 10, maximum is 50
- Query：
  - `limit` (必填) 返回数量/Return number
- 示例：

```
limit = 10
```

## 获取综合搜索信息

`GET /api/v1/bilibili/web/fetch_general_search`

- 用途：获取综合搜索信息
- 返回：综合搜索信息
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `order` (必填,string) 排序方式/Order method
  - `page` (必填,integer) 页码/Page number
  - `page_size` (必填,integer) 每页数量/Number per page
  - `duration` (选填,integer) 时长筛选/Duration filter
  - `pubtime_begin_s` (选填,integer) 开始日期/Start date (10-digit timestamp)
  - `pubtime_end_s` (选填,integer) 结束日期/End date (10-digit timestamp)
- 示例：

```
keyword = "火影忍者"
order = "totalrank"
page = 1
page_size = 42
duration = 0
pubtime_begin_s = 0
pubtime_end_s = 0
```

## 获取视频流地址

`GET /api/v1/bilibili/web/fetch_video_playurl`

- 用途：获取视频流地址
- 返回：视频流地址
- Query：
  - `bv_id` (必填,string) 作品id/Video id
  - `cid` (必填,string) 作品cid/Video cid
- 示例：

```
bv_id = "BV1y7411Q7Eq"
cid = "171776208"
```

## 获取大会员清晰度视频流地址

`POST /api/v1/bilibili/web/fetch_vip_video_playurl`

- 用途：获取大会员清晰度视频流地址
- 返回：大会员清晰度视频流地址
- Body(JSON)：
  - `bv_id` (必填,string) 作品id/Video id
  - `cid` (必填,string) 作品cid/Video cid
  - `cookie` (必填,string) 大会员用户Cookie/VIP User Cookie
- 示例：

```
bv_id = "BV1y7411Q7Eq"
cid = "171776208"
cookie = "your_vip_bilibili_cookie"
```

## 获取用户主页作品数据

`GET /api/v1/bilibili/web/fetch_user_post_videos`

- 用途：获取用户发布的视频数据
- 返回：用户发布的视频数据
- Query：
  - `uid` (必填,string) 用户UID
  - `pn` (选填,integer) 页码，最大100/Page number, max 100
  - `ps` (选填,integer) 每页数量，最大50/Page size, max 50
  - `order` (选填,string) 排序方式/Order method
- 示例：

```
uid = "178360345"
pn = 1
ps = 25
order = "pubdate"
```

## 获取用户主页作品数据V2

`GET /api/v1/bilibili/web/fetch_user_post_videos_v2`

- 用途：获取用户发布的视频数据，并可按关键词在该用户的作品内搜索；与 `/fetch_user_post_videos` 的区别见下方「与V1的区别」
- 返回：用户发布的视频数据，作品列表在 `data.archives`，总数在 `data.page.total`
- Query：
  - `uid` (必填,string) 用户UID
  - `pn` (选填,integer) 页码，无上限/Page number, no cap
  - `ps` (选填,integer) 每页数量，最大100/Page size, max 100
  - `keyword` (选填,string) 关键词，留空返回全部/Keyword, empty returns all
- 示例：

```
uid = "178360345"
pn = 1
ps = 30
keyword = ""
```

## 获取用户所有收藏夹信息

`GET /api/v1/bilibili/web/fetch_collect_folders`

- 用途：获取用户收藏作品数据
- 返回：用户收藏夹信息
- Query：
  - `uid` (必填,string) 用户UID
- 示例：

```
uid = "178360345"
```

## 获取指定收藏夹内视频数据

`GET /api/v1/bilibili/web/fetch_user_collection_videos`

- 用途：获取指定收藏夹内视频数据
- 返回：指定收藏夹内视频数据
- Query：
  - `folder_id` (必填,string) 收藏夹id/collection folder id
  - `pn` (选填,integer) 页码/Page number
- 示例：

```
folder_id = "1756059545"
pn = 1
```

## 获取指定用户的信息

`GET /api/v1/bilibili/web/fetch_user_profile`

- 用途：获取指定用户的信息
- 返回：指定用户的个人信息
- Query：
  - `uid` (必填,string) 用户UID
- 示例：

```
uid = "178360345"
```

## 获取UP主状态统计

`GET /api/v1/bilibili/web/fetch_user_up_stat`

- 用途：获取UP主状态统计信息（总播放数、总获赞数）
- 返回：UP主状态统计数据
- Query：
  - `uid` (必填,string) 用户UID/User UID
- 示例：

```
uid = "178360345"
```

## 获取用户关系状态统计

`GET /api/v1/bilibili/web/fetch_user_relation_stat`

- 用途：获取用户关系状态统计信息（关注数、粉丝数）
- 返回：用户关系状态统计数据
- Query：
  - `uid` (必填,string) 用户UID/User UID
- 示例：

```
uid = "178360345"
```

## 获取综合热门视频信息

`GET /api/v1/bilibili/web/fetch_com_popular`

- 用途：获取综合热门视频信息
- 返回：综合热门视频信息
- Query：
  - `pn` (选填,integer) 页码/Page number
- 示例：

```
pn = 1
```
- 返回结构（实测）：
  - `data` 是对象（4 个字段）：`code`, `message`, `ttl`, `data`
  - `data.data` 是对象（2 个字段）：`list`, `no_more`
  - `data.data.list` 是数组（长度 20）；首元素字段：`aid`, `videos`, `tid`, `tname`, `copyright`, `pic`, `title`, `pubdate`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取指定视频的评论

`GET /api/v1/bilibili/web/fetch_video_comments`

- 用途：获取指定视频的评论
- 返回：指定视频的评论数据
- Query：
  - `bv_id` (必填,string) 作品id/Video id
  - `pn` (选填,integer) 页码/Page number
- 示例：

```
bv_id = "BV1M1421t7hT"
pn = 1
```
- 返回结构（实测）：
  - `data` 是对象（4 个字段）：`code`, `message`, `ttl`, `data`
  - `data.data` 是对象（12 个字段）：`page`, `config`, `replies`, `upper`, `top`, `vote`, `blacklist`, `assist`
  - `data.data` 是对象（12 个字段）：`page`, `config`, `replies`, `upper`, `top`, `vote`, `blacklist`, `assist`, `mode`, `support_mode`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取视频下指定评论的回复

`GET /api/v1/bilibili/web/fetch_comment_reply`

- 用途：获取视频下指定评论的回复
- 返回：指定评论的回复数据
- Query：
  - `bv_id` (必填,string) 作品id/Video id
  - `pn` (选填,integer) 页码/Page number
  - `rpid` (必填,string) 回复id/Reply id
- 示例：

```
bv_id = "BV1M1421t7hT"
pn = 1
rpid = "237109455120"
```

## 获取指定用户动态

`GET /api/v1/bilibili/web/fetch_user_dynamic`

- 用途：获取指定用户动态
- 返回：指定用户动态数据
- Query：
  - `uid` (必填,string) 用户UID
  - `offset` (选填,string) 开始索引/offset
- 示例：

```
uid = "178360345"
offset = "953154282154098691"
```

## 获取动态详情

`GET /api/v1/bilibili/web/fetch_dynamic_detail`

- 用途：获取指定动态的详情信息（v1接口）；适用于图文 / 文字 / 专栏类动态，返回完整 module_stat（含 favorite / coin）；视频类动态（DYNAMIC_TYPE_AV）请改用 v2 接口
- 返回：动态详情数据
- Query：
  - `dynamic_id` (必填,string) 动态id/Dynamic id
- 示例：

```
dynamic_id = "1172584638000922630"
```

## 获取动态详情v2

`GET /api/v1/bilibili/web/fetch_dynamic_detail_v2`

- 用途：获取指定动态的详情信息（v2接口）；视频类动态（DYNAMIC_TYPE_AV）请使用本接口；module_stat 只含 comment / forward / like；如需 favorite / coin 且为图文 / 文字 / 专栏类动态请用 v1 接口
- 返回：动态详情数据
- Query：
  - `dynamic_id` (必填,string) 动态id/Dynamic id
- 示例：

```
dynamic_id = "1172584638000922630"
```

## 获取动态评论

`GET /api/v1/bilibili/web/fetch_dynamic_comments`

- 用途：获取图文、文字动态的评论列表
- Query：
  - `dynamic_id` (选填) 动态ID，与oid二选一/Dynamic ID; provide either dynamic_id or oid
  - `oid` (选填) 评论区ID，与dynamic_id二选一/Comment-section ID; provide either oid or dynamic_id
  - `comment_type` (选填) 仅配合oid使用，默认11（图文）/Only with oid; defaults to 11 (image posts)
  - `mode` (选填,integer) 排序：3热门，2时间/Sort: 3 hot, 2 time
  - `pagination_str` (选填,string) 翻页JSON，首页留空/Pagination JSON; leave empty for the first page
- 示例：

```
dynamic_id = "DYNAMIC_ID"
mode = 3
pagination_str = ""
```

## 获取视频实时弹幕

`GET /api/v1/bilibili/web/fetch_video_danmaku`

- 用途：获取视频实时弹幕
- 返回：视频实时弹幕
- Query：
  - `cid` (必填,string) 作品cid/Video cid
- 示例：

```
cid = "1639235405"
```

## 获取指定直播间信息

`GET /api/v1/bilibili/web/fetch_live_room_detail`

- 用途：获取指定直播间信息
- 返回：指定直播间信息
- Query：
  - `room_id` (必填,string) 直播间ID/Live room ID
- 示例：

```
room_id = "22816111"
```

## 获取直播间视频流

`GET /api/v1/bilibili/web/fetch_live_videos`

- 用途：获取指定直播间视频流
- 返回：指定直播间视频流
- Query：
  - `room_id` (必填,string) 直播间ID/Live room ID
- 示例：

```
room_id = "1815229528"
```

## 获取指定分区正在直播的主播

`GET /api/v1/bilibili/web/fetch_live_streamers`

- 用途：获取指定分区正在直播的主播
- 返回：指定分区正在直播的主播
- Query：
  - `area_id` (必填,string) 直播分区id/Live area ID
  - `pn` (选填,integer) 页码/Page number
- 示例：

```
area_id = "9"
pn = 1
```

## 获取所有直播分区列表

`GET /api/v1/bilibili/web/fetch_all_live_areas`

- 用途：获取所有直播分区列表
- 返回：所有直播分区列表

## 通过bv号获得视频aid号

`GET /api/v1/bilibili/web/bv_to_aid`

- 用途：通过bv号获得视频aid号
- 返回：视频aid号
- Query：
  - `bv_id` (必填,string) 作品id/Video id
- 示例：

```
bv_id = "BV1M1421t7hT"
```

## 通过bv号获得视频分p信息

`GET /api/v1/bilibili/web/fetch_video_parts`

- 用途：通过bv号获得视频分p信息
- 返回：视频分p信息
- Query：
  - `bv_id` (必填,string) 作品id/Video id
- 示例：

```
bv_id = "BV1M1421t7hT"
```

## 提取用户ID

`GET /api/v1/bilibili/web/fetch_get_user_id`

- 用途：提取用户ID
- 返回：用户ID
- Query：
  - `share_link` (必填,string) 用户分享链接/User share link
