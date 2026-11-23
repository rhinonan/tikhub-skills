# Weibo App API

文件夹 `Weibo-App-API` · 23 个接口
说明：新浪微博APP数据接口


## 获取用户信息

`GET /api/v1/weibo/app/fetch_user_info`

- 用途：获取微博用户的基本信息，包括昵称、头像、简介、关注数、粉丝数等
- 返回：用户基本信息数据
- 注意：如果用户设置了隐私保护，部分信息可能无法获取
- Query：
  - `uid` (必填,string) 用户ID
- 示例：

```
uid = "7648703289"
```
- 返回结构（实测）：
  - `data` 是对象（7 个字段）：`channelInfo`, `config`, `header`, `headerBack`, `profileSkin`, `footer`, `navigationBar`
  - `data.channelInfo` 是对象（2 个字段）：`channelConfig`, `channels`
  - `data.header` 是对象（2 个字段）：`config`, `data`
  - `data.headerBack` 是对象（2 个字段）：`config`, `default`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取用户详细信息

`GET /api/v1/weibo/app/fetch_user_info_detail`

- 用途：获取微博用户的详细信息，比基本信息更加完整，包括认证信息、标签、等级等
- 返回：用户详细信息数据
- 注意：如果用户设置了隐私保护，部分信息可能无法获取
- Query：
  - `uid` (必填,string) 用户ID
- 示例：

```
uid = "7648703289"
```

## 获取用户发布的微博

`GET /api/v1/weibo/app/fetch_user_timeline`

- 用途：获取指定用户发布的微博列表，支持分页和多种内容筛选
- 返回：微博列表数据，包含微博内容、图片、视频等信息
- 注意：如果用户设置了隐私保护，可能无法获取微博列表；每页返回数量约为20条微博；使用时间筛选时必须同时指定filter_type=month和month参数
- Query：
  - `uid` (必填,string) 用户ID
  - `page` (选填,integer) 页码
  - `filter_type` (选填,string) 筛选类型
  - `month` (选填) 时间筛选(YYYYMMDD格式)
- 示例：

```
uid = "7648703289"
page = 1
filter_type = "all"
# or filter_type = "video" for videos only
# or filter_type = "month" with month = "20251010" for time filter
```

## 获取用户视频列表

`GET /api/v1/weibo/app/fetch_user_videos`

- 用途：获取指定用户发布的视频列表（瀑布流展示）
- 返回：视频列表数据，包含视频标题、封面、播放量等信息；包含 moreInfo.params.since_id 字段用于翻页
- 注意：只返回包含视频的微博；使用游标翻页（since_id），不使用页码翻页
- Query：
  - `uid` (必填,string) 用户ID
  - `since_id` (选填) 翻页游标
- 示例：

```
# First page
uid = "7648703289"
since_id = None

# Next page (use since_id from previous response)
# since_id = "4763250669650541"
```

## 获取用户参与的超话列表

`GET /api/v1/weibo/app/fetch_user_super_topics`

- 用途：获取指定用户参与的超话列表
- 返回：用户参与的超话列表数据
- 注意：如果用户设置了隐私保护，可能无法获取超话列表
- Query：
  - `uid` (必填,string) 用户ID
  - `page` (选填,integer) 页码
- 示例：

```
uid = "7648703289"
page = 1
```

## 获取用户相册

`GET /api/v1/weibo/app/fetch_user_album`

- 用途：获取指定用户的相册内容
- 返回：用户相册数据，包含图片列表等信息
- 注意：如果用户设置了隐私保护，可能无法获取相册；使用游标翻页（since_id），不使用页码翻页
- Query：
  - `uid` (必填,string) 用户ID
  - `since_id` (选填) 翻页游标
- 示例：

```
uid = "7648703289"
since_id = None  # First page
# since_id = "5012154263666753_4990205358511630|1034:4990204960768042_20240328_-1"  # Next page
```

## 获取用户文章列表

`GET /api/v1/weibo/app/fetch_user_articles`

- 用途：获取指定用户发布的文章列表
- 返回：用户文章列表数据
- 注意：如果用户没有发布过文章，返回空列表；使用游标翻页（since_id），不使用页码翻页
- Query：
  - `uid` (必填,string) 用户ID
  - `since_id` (选填) 翻页游标
- 示例：

```
uid = "1725941200"
since_id = None  # First page
```

## 获取用户音频列表

`GET /api/v1/weibo/app/fetch_user_audios`

- 用途：获取指定用户发布的音频列表
- 返回：用户音频列表数据
- 注意：如果用户没有发布过音频，返回空列表；使用游标翻页（since_id），不使用页码翻页
- Query：
  - `uid` (必填,string) 用户ID
  - `since_id` (选填) 翻页游标
- 示例：

```
uid = "1725941200"
since_id = None  # First page
```

## 获取用户主页动态

`GET /api/v1/weibo/app/fetch_user_profile_feed`

- 用途：获取指定用户主页的动态流
- 返回：用户主页动态数据
- 注意：如果用户设置了隐私保护，可能无法获取动态；使用游标翻页（since_id），不使用页码翻页
- Query：
  - `uid` (必填,string) 用户ID
  - `since_id` (选填) 翻页游标
- 示例：

```
uid = "6580994757"
since_id = None  # First page
# since_id = "2|1769360821762|5258923930289595,,,,,,1768788000,,,,,-1,-1"  # Next page
```

## 获取用户粉丝列表

`GET /api/v1/weibo/app/fetch_user_followers`

- 用途：获取指定用户的粉丝列表，返回粉丝的用户信息（昵称、头像、简介、粉丝数、最新微博等）
- 返回：粉丝列表数据
- 注意：该接口走微博移动端(m.weibo.cn)H5接口，依赖服务端缓存的已登录Cookie，Cookie失效时会返回错误；使用 `page` 递增翻页，翻到 `data.list.next_page` 为空或0时表示没有更多数据；每页固定返回20条，微博会过滤部分账号（触发博主自保护策略），因此单页实际返回数量可能不足20条；微博限制粉丝列表的可翻页深度（实测约1000条后 `users` 返回空数组、`next_page` 为0）
- Query：
  - `uid` (必填,string) 用户ID
  - `page` (选填,integer) 页码，从1开始
- 示例：

```
uid = "1856404484"
page = 1  # First page
# page = 2  # Next page
```

## 获取用户关注列表

`GET /api/v1/weibo/app/fetch_user_following`

- 用途：获取指定用户的关注列表，返回被关注用户的信息（昵称、头像、简介、粉丝数、最新微博等）
- 返回：关注列表数据
- 注意：该接口走微博移动端(m.weibo.cn)H5接口，依赖服务端缓存的已登录Cookie，Cookie失效时会返回错误；每页返回约20条，使用 since_id 游标翻页，不使用页码翻页；响应中不再返回 since_id 即表示已翻到底，此时 users 可能仍有不足20条的最后一批数据；用户信息嵌套在 data.users[].user 中，与粉丝列表接口的结构不同
- Query：
  - `uid` (必填,string) 用户ID
  - `since_id` (选填) 翻页游标，格式为"时间戳|偏移量"，首次请求不传，后续请求使用返回的since_id值
  - `sort_type` (选填,integer) 排序类型: 1=按最新微博时间排序, 2=按关注时间排序（默认）
- 示例：

```
uid = "1856404484"
since_id = None  # First page
# since_id = "1787913903|40"  # Next page
sort_type = 2
```

## 获取微博详情

`GET /api/v1/weibo/app/fetch_status_detail`

- 用途：获取指定微博的详细信息
- 返回：微博详细数据，包含完整文本、图片、视频、点赞数、评论数、转发数等
- 注意：如果微博已被删除或设置为私密，可能无法获取
- Query：
  - `status_id` (必填,string) 微博ID
- 示例：

```
status_id = "5016922058656962"
```

## 获取微博评论

`GET /api/v1/weibo/app/fetch_status_comments`

- 用途：获取指定微博的一级评论列表（也适用于视频评论）
- 返回：评论列表数据，包含评论内容、评论者信息、点赞数等；包含 max_id 字段用于翻页
- 注意：每次返回约20条评论；当没有更多评论时，max_id 为空或相同
- Query：
  - `status_id` (必填,string) 微博ID
  - `max_id` (选填) 翻页游标
  - `sort_type` (选填,string) 排序类型: 0=按热度排序, 1=按时间排序
- 示例：

```
status_id = "5258708168476831"
max_id = None  # First page
sort_type = "0"  # Sort by popularity
```

## 获取微博转发列表

`GET /api/v1/weibo/app/fetch_status_reposts`

- 用途：获取指定微博的转发列表（也适用于视频转发）
- 返回：转发列表数据，包含转发内容、转发者信息等；包含 max_id 字段用于翻页
- 注意：每次返回约20条转发；当没有更多转发时，max_id 为空或相同
- Query：
  - `status_id` (必填,string) 微博ID
  - `max_id` (选填) 翻页游标
- 示例：

```
status_id = "5016922058656962"
max_id = None  # First page
```

## 获取微博点赞列表

`GET /api/v1/weibo/app/fetch_status_likes`

- 用途：获取指定微博的点赞列表（也适用于视频点赞）
- 返回：点赞列表数据，包含点赞者信息、点赞类型等
- 注意：每次返回约50条点赞记录
- Query：
  - `status_id` (必填,string) 微博ID
  - `attitude_type` (选填,string) 点赞类型: 0=全部, 1=点赞, 2=开心, 3=惊讶, 4=伤心, 5=愤怒, 6=打赏, 8=抱抱
- 示例：

```
status_id = "5016922058656962"
attitude_type = "0"  # All types
```

## 获取视频详情

`GET /api/v1/weibo/app/fetch_video_detail`

- 用途：获取单个视频的详细信息，包括视频播放地址；**重要**: 从微博视频链接（如 https://weibo.com/tv/show/1034:5232127105761312）获取真实视频ID的必需步骤
- 返回：视频详细数据，包含视频播放地址、封面、时长、标题等；**items[0].data.idstr**: 真实的视频微博ID，可用于获取评论等操作
- 注意：返回的视频地址可能有时效性；支持获取高清视频地址；**获取评论前必须先调用此接口**: 链接中的ID不能直接用于获取评论，需要先通过此接口获取 items[0].data.idstr 中的真实ID
- Query：
  - `mid` (必填,string) 视频微博ID
- 示例：

```
mid = "5242977759006596"
```

## 获取短视频精选Feed流

`GET /api/v1/weibo/app/fetch_video_featured_feed`

- 用途：获取微博短视频精选页的Feed流
- 返回：短视频精选Feed流数据，包含视频列表等
- 注意：每页返回约20条视频
- Query：
  - `page` (选填) 页码，首页不传，第二页传2
- 示例：

```
page = None  # First page
# page = "2"  # Second page
```

## 综合搜索

`GET /api/v1/weibo/app/fetch_search_all`

- 用途：在微博中进行综合搜索，返回相关内容。支持多种搜索类型
- 返回：搜索结果列表，包含微博内容、作者信息、图片、视频等
- 注意：搜索结果按相关度排序；仅使用 page 参数进行翻页
- Query：
  - `query` (必填,string) 搜索关键词
  - `page` (选填,integer) 页码
  - `search_type` (选填,integer) 搜索类型: 1=综合, 61=实时, 3=用户, 64=视频, 63=图片, 62=关注, 60=热门, 21=全网, 38=话题, 98=超话, 92=地点, 97=商品
- 示例：

```
query = "NVIDIA"
page = 1
search_type = 1  # General search
# search_type = 3  # Search users
# search_type = 64  # Search videos
```

## AI智搜

`GET /api/v1/weibo/app/fetch_ai_smart_search`

- 用途：使用微博AI智搜功能进行搜索，返回AI增强的搜索结果
- 返回：AI智搜结果，包含AI增强的搜索内容
- 注意：此接口为AI增强搜索，返回结果经过AI处理
- Query：
  - `query` (必填,string) 搜索关键词
  - `page` (选填,integer) 页码
- 示例：

```
query = "人工智能"
page = 1
```

## 获取首页推荐Feed流

`GET /api/v1/weibo/app/fetch_home_recommend_feed`

- 用途：获取微博首页推荐Feed流
- 返回：首页推荐Feed流数据
- 注意：推荐内容基于热门话题和热点事件
- Query：
  - `page` (选填) 页码，首页不传，第二页传2
  - `count` (选填,integer) 每页数量
- 示例：

```
page = None  # First page
count = 15
```

## 获取热搜榜

`GET /api/v1/weibo/app/fetch_hot_search`

- 用途：获取微博热搜榜，支持多个分类
- 返回：热搜榜数据，包含热搜词条、热度等
- 注意：热搜榜实时更新
- Query：
  - `category` (选填,string) 热搜分类: mineband=我的, realtimehot=热搜, social=社会, fun=文娱, technologynav=科技, lifenav=生活, region=同城, sportnav=体育, gamenav=ACG
  - `page` (选填,integer) 页码
  - `count` (选填,integer) 每页数量
  - `region_name` (选填,string) 同城热搜城市名称，仅 category=region 时有效，支持: 北京/上海/广州/深圳/杭州/成都/重庆/武汉/南京/天津/西安/长沙/郑州/苏州/东莞/青岛/沈阳/合肥等，默认北京
- 示例：

```
category = "realtimehot"
page = 1
count = 20
```

## 获取热搜分类列表

`GET /api/v1/weibo/app/fetch_hot_search_categories`

- 用途：获取微博热搜榜的所有可用分类列表
- 返回：热搜分类列表数据，包含各分类名称和标识
- 注意：返回的分类可用于 fetch_hot_search 接口的 category 参数
- 示例：

```
# No parameters required
```

## 获取热搜简报

`GET /api/v1/weibo/app/fetch_hot_search_brief`

- 用途：获取微博热搜简报（今日热点事件纪要），返回当日热点事件的AI摘要，
- 返回：热搜简报数据（微博原始响应），简报内容嵌套在AI智搜卡片中，取值路径为:
- 注意：简报由微博智搜（AI）生成，内容每隔一段时间更新一次，更新时间见 slogan_info.dynamic_wenan；单次返回当日约20条热点事件，该接口不支持翻页；简报内容为多层嵌套的JSON字符串，调用方需要逐层反序列化后才能取到事件列表；简报由AI边生成边返回，命中生成中的响应时服务端会自动重试；极端情况下仍可能返回生成中的响应，
- 示例：

```
# 无需参数 / No parameters required
```
