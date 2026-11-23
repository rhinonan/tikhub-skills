# Douyin Web API

文件夹 `Douyin-Web-API` · 57 个接口
说明：抖音Web数据接口


## 获取单个作品数据

`GET /api/v1/douyin/web/fetch_one_video`

- 用途：获取单个作品数据 V1，若此接口失效，请使用 `/fetch_one_video_v2` 接口，或使用APP接口
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `need_anchor_info` (选填,boolean) 是否需要锚点信息/Whether anchor information is needed
- 示例：

```
aweme_id = "7372484719365098803"
need_anchor_info = False
```
- 返回结构（实测）：
  - `data` 是对象（3 个字段）：`aweme_detail`, `log_pb`, `status_code`
  - `data.aweme_detail` 是对象（147 个字段）：`activity_video_type`, `anchors`, `authentication_token`, `author`, `author_mask_tag`, `author_user_id`, `aweme_control`, `aweme_id`
  - `data.log_pb` 是对象（1 个字段）：`impr_id`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取单个作品数据 V2

`GET /api/v1/douyin/web/fetch_one_video_v2`

- 用途：获取单个作品数据 V2，若此接口失效，请使用 `/fetch_one_video` 接口，或使用APP接口
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
- 示例：

```
aweme_id = "7372484719365098803"
```
- 返回结构（实测）：
  - `data.aweme_detail` — 作品主体（obj，另有 `log_pb`/`status_code`）
  - `aweme_detail.aweme_id` — 作品ID（str）
  - `aweme_detail.desc` — 文案，`#话题` 原样保留（str）
  - `aweme_detail.create_time` — 发布时间的**秒级**时间戳（int）
  - `aweme_detail.duration` — 时长，单位**毫秒**（int，8010 ≈ 8.01s）
  - `aweme_detail.aweme_type` — 0=视频，68=图集（int，图片在 `images[]`）
  - `aweme_detail.share_url` — 分享链接（iesdouyin.com 短链）
  - `aweme_detail.statistics.{digg_count,comment_count,share_count,collect_count,recommend_count}` — 互动数（int）
  - `aweme_detail.author.{uid,sec_uid,unique_id,nickname,follower_count,total_favorited,signature,ip_location}` — 作者，`sec_uid` 可直接喂给资料/主页接口
  - `aweme_detail.video.{play_addr.url_list[],bit_rate[],cover.url_list[],ratio,width,height,has_watermark}` — 播放地址；`bit_rate` 有 13 档可选码率
  - `aweme_detail.music.{title,author,duration}`、`text_extra[].{hashtag_name,hashtag_id}` — 音乐与话题
  - ⚠️ web 版 **`statistics.play_count` 实测恒为 0**（312789 赞但播放量为 0），播放量要走创作者中心/数据统计接口

## 根据分享链接获取单个作品数据

`GET /api/v1/douyin/web/fetch_one_video_by_share_url`

- 用途：根据分享链接获取单个作品数据 （本质上基于 `/fetch_one_video` 接口实现，建议有能力自行获取视频ID以提升接口响应速度）；返回的视频画质比APP接口高一些，但是响应字段没有APP接口多
- 返回：作品数据
- Query：
  - `share_url` (必填,string) 分享链接/Share link
- 示例：

```
share_url = "https://v.douyin.com/e3x2fjE/"
```

## 获取视频的最高画质播放链接

`GET /api/v1/douyin/web/fetch_video_high_quality_play_url`

- 用途：价格：0.005$ 一次；获取视频的最高画质(原始上传画质)播放链接；该接口会返回最高画质的播放链接，原始上传画质是指用户上传视频时的画质，通常最高画质视频无压缩码率并且文件头包含元数据；最高画质的视频链接无法从抖音APP或网页版直接获取，需要通过此接口获取；此接口非常适合用于获取高清无水印视频链接，适用于需要高质量视频的场景，如视频编辑、存档、训练模型等；一般情况都可以在线播放，如果不行，可以尝试使用IDM或浏览器下载后播放
- 返回：video_id： 作品id；original_video_url： 最高画质(原始上传画质)播放链接；video_data： 视频数据，包含视频的元数据，如时长、大小等
- Query：
  - `aweme_id` (选填,string) 作品id/Video id
  - `share_url` (选填,string) 可选，分享链接/Optional, share link
  - `region` (选填,string) 可选，请求出口地区(ISO 国家代码，如 CN/US/HK)，国内用户传 CN 可拿到国内 CDN 域名以加快下载速度 / Optional, ISO country code (e.g. CN/US/HK). Pass CN to get China-region CDN URLs for faster download in mainland China.
- 示例：

```
aweme_id = "7512756548356492544"
share_url = "https://www.douyin.com/video/7512756548356492544"
region = "CN"
```
- 返回结构（实测）：
  - 顶层即结果，无 `data` 包装：`video_id`/`original_video_url`/`file_size`/`file_size_in_mb`/`content_type`
  - `original_video_url` — 无水印 mp4 直链（带时效签名，落盘后尽快下载）
  - `file_size` 是**字符串**字节数，`file_size_in_mb` 是 float——别把前者当数字直接算

## 批量获取视频的最高画质播放链接

`POST /api/v1/douyin/web/fetch_multi_video_high_quality_play_url`

- 用途：此接口目前优惠活动价为$0.25，活动结束后恢复原价$0.5。不足50个视频按50个视频收费；批量获取视频的最高画质(原始上传画质)播放链接；该接口会返回最高画质的播放链接，原始上传画质是指用户上传视频时的画质，通常最高画质视频无压缩码率并且文件头包含元数据；最高画质的视频链接无法从抖音APP或网页版直接获取，需要通过此接口获取；此接口非常适合用于批量获取高清无水印视频链接，适用于需要高质量视频的场景，如视频编辑、存档、训练模型等；使用并发请求，提高批量获取效率；最多支持50个视频ID
- 返回：total: 总数；success_count: 成功数量；failed_count: 失败数量；videos: 视频列表，每个视频包含以下字段：
- 注意：Due to the large number, the processing time may be slightly longer, please increase the waiting time
- Body(JSON)：
  - `aweme_ids` (选填,string) 作品id列表，用逗号分隔，最多50个/Video id list, separated by commas, up to 50
  - `region` (选填) 可选，请求出口地区(ISO 国家代码，如 CN/US/HK)。抖音根据请求 IP 返回对应区域 CDN，国内用户传 'CN' 可获得国内 CDN 链接以加快下载速度 / Optional, ISO country code (e.g. CN). Pass 'CN' for users in mainland China to get China-region CDN URLs for faster download.
- 示例：

```
aweme_ids = "7512756548356492544,7448118827402972455,7126745726494821640"
```

## 获取单个作品播放量

`GET /api/v1/douyin/web/fetch_video_play_count`

- 用途：获取单个作品的公开播放量，无需 Cookie
- 返回：aweme_id: 作品id；is_available: 是否可获取播放量；作品不存在、已删除、私密，以及图文、实况作品均为 false；play_count: 播放量（is_available 为 false 时为 0）；digg_count: 点赞数（is_available 为 false 时为 0）；publish_time: 发布时间戳（秒，is_available 为 false 时为 0）
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
- 示例：

```
aweme_id = "7512756548356492544"
```

## 批量获取作品播放量

`GET /api/v1/douyin/web/fetch_multi_video_play_count`

- 用途：批量获取作品的公开播放量，无需 Cookie，单个作品失败不影响其他结果
- 返回：total / success_count / failed_count: 总数 / 成功数量 / 失败数量；videos: 作品列表，每项包含：
- Query：
  - `aweme_ids` (必填,string) 作品id列表，逗号分隔，最多20个/Comma-separated video ids, up to 20
- 示例：

```
aweme_ids = "7512756548356492544,7695699449444816817"
```

## 批量获取视频信息

`POST /api/v1/douyin/web/fetch_multi_video`

- 用途：批量获取视频信息，支持图文、视频等，一次性最多支持50个视频，此接口收费固定价格为0.001$ * 50 = 0.05$一次；若此接口失效，请使用APP接口替代
- 返回：作品数据
- Body(JSON)：
  - `aweme_ids` (必填,array) Aweme Ids
- 示例：

```
aweme_ids = ["7372484719365098803", "7126745726494821640", "7372484719365098803", "7126745726494821640", "7372484719365098803", "7126745726494821640", "7372484719365098803", "7126745726494821640", "7372484719365098803", "7126745726494821640"]
```

## 获取单个作品视频弹幕数据

`GET /api/v1/douyin/web/fetch_one_video_danmaku`

- 用途：获取单个作品视频弹幕数据
- 返回：视频弹幕数据
- Query：
  - `item_id` (必填,string) 作品id/Video id
  - `duration` (必填,integer) 视频总时长/Video total duration
  - `end_time` (必填,integer) 结束时间/End time
  - `start_time` (必填,integer) 开始时间/Start time
- 示例：

```
item_id = "7355433624046472498"
duration = 15134
end_time = 15133
start_time = 0
```

## 获取首页推荐数据

`POST /api/v1/douyin/web/fetch_home_feed`

- 用途：获取首页推荐数据
- 返回：Feed数据
- Body(JSON)：
  - `count` (选填,integer) 数量/Number
  - `refresh_index` (选填,integer) 刷新/翻页索引：0=刷新(首页/下拉)，>0=翻页(下滑加载更多)，每次+1取下一页 / Refresh-paging index: 0=refresh, >0=load-more, increment by 1 for next page
  - `cookie` (选填,string) 可选/Optional：用户网页版抖音登录Cookie，传入后返回该账号的个性化推荐；不传则以游客身份访问/Your web Douyin login Cookie for a personalized feed; guest access if omitted
- 示例：

```
count = 10
refresh_index = 0
cookie = ""
```

## 获取相关作品推荐数据

`GET /api/v1/douyin/web/fetch_related_posts`

- 用途：获取相关作品推荐数据
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `refresh_index` (选填,integer) 翻页索引/Paging index
  - `count` (选填,integer) 数量/Number
- 示例：

```
aweme_id = "7393365489105358132"
refresh_index = 1
count = 20
```

## 获取用户主页作品数据

`GET /api/v1/douyin/web/fetch_user_post_videos`

- 用途：获取用户主页作品数据；注意：请尽量使用APP的接口而不是WEB的接口，因为WEB的接口可能会被不稳定
- 返回：用户作品数据
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (选填,string) 最大游标/Maximum cursor
  - `count` (选填,integer) 每页数量/Number per page
  - `filter_type` (选填,string) 过滤类型/Filter type
  - `cookie` (选填,string) 用户网页版抖音Cookie/Your web version of Douyin Cookie
- 示例：

```
sec_user_id = "MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE"
max_cursor = "0"
counts = 20
filter_type = "0"
```
- 返回结构（实测）：
  - `aweme_list[]` — 作品列表，单条结构基本同 `fetch_one_video_v2` 的 `aweme_detail`（字段有裁剪）
  - `max_cursor` — 下一页游标，**实测是毫秒时间戳**（如 1794557654000），不是 0 起算的序号
  - `has_more`（1/0）、`min_cursor`、`time_list[]` — 翻页控制与时间轴
  - ⚠️ `count` 只是建议值：传 `count=2` 实测返回 4 条，**按 `aweme_list` 长度判断**，别按 count 算页数

## 获取用户喜欢作品数据

`POST /api/v1/douyin/web/fetch_user_like_videos`

- 用途：获取用户喜欢作品数据
- 返回：用户作品数据
- Body(JSON)：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (选填,integer) 最大游标/Maximum cursor
  - `counts` (选填,integer) 每页数量/Number per page
  - `cookie` (选填) 可选：本人有效的抖音网页版登录Cookie；提供后使用该登录身份访问，不传则以游客身份访问/Optional: your valid Douyin web login Cookie; uses that signed-in identity when provided, otherwise guest access
- 示例：

```
sec_user_id = "USER_SEC_ID"
max_cursor = 0
counts = 20
cookie = "YOUR_COOKIE"
```

## 获取用户收藏作品数据

`POST /api/v1/douyin/web/fetch_user_collection_videos`

- 用途：获取用户收藏作品数据
- 返回：用户作品数据
- Body(JSON)：
  - `cookie` (必填,string) 用户网页版抖音Cookie/Your web version of Douyin Cookie
  - `max_cursor` (选填,integer) 最大游标/Maximum cursor
  - `counts` (选填,integer) 每页数量/Number per page
- 示例：

```
cookie = "YOUR_COOKIE"
max_cursor = 0
counts = 20
```

## 获取用户收藏夹

`POST /api/v1/douyin/web/fetch_user_collects`

- 用途：获取用户收藏夹
- 返回：用户收藏夹数据
- Body(JSON)：
  - `max_cursor` (选填,integer) 最大游标/Maximum cursor
  - `counts` (选填,integer) 每页数量/Number per page
  - `cookie` (必填,string) 用户网页版抖音Cookie/Your web version of Douyin Cookie
- 示例：

```
cookie = "YOUR_COOKIE"
max_cursor = 0
counts = 20
```

## 获取用户收藏夹作品（自带Cookie）

`POST /api/v1/douyin/web/fetch_user_collects_videos`

- 用途：获取本人收藏夹内的作品列表，所有参数通过 JSON 请求体传入
- 返回：作品列表 aweme_list、分页游标 cursor 和是否有下一页 has_more
- Body(JSON)：
  - `collects_id` (必填,string) 收藏夹id/Collection id
  - `max_cursor` (选填,integer) 最大游标/Maximum cursor
  - `counts` (选填,integer) 每页数量/Number per page
  - `cookie` (必填,string) 收藏夹所属账号的抖音网页版登录Cookie/Web Douyin login Cookie of the collection owner
- 示例：

```
```json
{
    "collects_id": "",
    "cookie": "YOUR_COOKIE",
    "max_cursor": 0,
    "counts": 20
}
```
```

## 获取用户合辑作品数据

`GET /api/v1/douyin/web/fetch_user_mix_videos`

- 用途：获取用户合辑作品数据
- 返回：用户作品数据
- Query：
  - `mix_id` (必填,string) 合辑id/Mix id
  - `max_cursor` (选填,integer) 最大游标/Maximum cursor
  - `counts` (选填,integer) 每页数量/Number per page
- 示例：

```
url = https://www.douyin.com/collection/7348687990509553679
mix_id = "7348687990509553679"
max_cursor = 0
counts = 20
```

## 获取用户直播流数据

`GET /api/v1/douyin/web/fetch_user_live_videos`

- 用途：获取用户直播流数据
- 返回：直播流数据
- Query：
  - `webcast_id` (必填,string) 直播间webcast_id/Room webcast_id
- 示例：

```
webcast_id = "376034101029"
```

## 通过sec_uid获取指定用户的直播流数据

`GET /api/v1/douyin/web/fetch_user_live_videos_by_sec_uid`

- 用途：通过sec_uid获取指定用户的直播流数据
- 返回：直播流数据
- Query：
  - `sec_uid` (必填,string) 用户sec_uid/User sec_uid
- 示例：

```
sec_uid = "MS4wLjABAAAAAIKOBr_x6p2fPVKOAhqG8LrC1lwwdWChifKEsl-TXFS-kGSGqpMBRexJdzoAfvUF"
```

## 通过room_id获取指定用户的直播流数据 V2

`GET /api/v1/douyin/web/fetch_user_live_videos_by_room_id_v2`

- 用途：获取指定用户的直播流数据V2
- 返回：直播流数据
- Query：
  - `room_id` (必填,string) 直播间room_id/Room room_id
- 示例：

```
room_id = "7462723839303093032"
```

## 获取直播间送礼用户排行榜

`GET /api/v1/douyin/web/fetch_live_gift_ranking`

- 用途：获取直播间送礼用户排行榜
- 返回：排行榜数据
- Query：
  - `room_id` (必填,string) 直播间room_id/Room room_id
  - `rank_type` (选填,integer) 排行类型/Leaderboard type
- 示例：

```
room_id = "7356585666190461731"
rank_type = 30
```

## 使用UID获取用户信息

`GET /api/v1/douyin/web/fetch_user_profile_by_uid`

- 用途：使用UID获取用户信息
- 返回：用户信息
- Query：
  - `uid` (必填,string) 用户UID/User UID
- 示例：

```
uid = "68141954464"
```

## 获取批量用户信息(最多10个)

`GET /api/v1/douyin/web/fetch_batch_user_profile_v1`

- 用途：获取批量用户信息，最多支持10个用户
- 返回：批量用户信息
- Query：
  - `sec_user_ids` (必填,string) 用户sec_user_id列表，用逗号分隔/User sec_user_id list, separated by commas
- 示例：

```
sec_user_ids = "MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE,MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"
```

## 获取批量用户信息(最多50个)

`GET /api/v1/douyin/web/fetch_batch_user_profile_v2`

- 用途：获取批量用户信息，最多支持50个用户
- 返回：批量用户信息
- Query：
  - `sec_user_ids` (必填,string) 用户sec_user_id列表，用逗号分隔/User sec_user_id list, separated by commas
- 示例：

```
sec_user_ids = "MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE,MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"
```

## 使用UID获取用户开播信息

`GET /api/v1/douyin/web/fetch_user_live_info_by_uid`

- 用途：使用UID获取用户开播信息
- 返回：用户开播信息，包含room_id与live_status
- Query：
  - `uid` (必填,string) 用户UID/User UID
- 示例：

```
uid = "3081254195702747"
```

## 使用Short ID获取用户信息

`GET /api/v1/douyin/web/fetch_user_profile_by_short_id`

- 用途：使用Short ID获取用户信息
- 返回：用户信息
- Query：
  - `short_id` (必填,string) 用户Short ID/User Short ID
- 示例：

```
short_id = "114131058"
```

## 生成短链接

`GET /api/v1/douyin/web/handler_shorten_url`

- Query：
  - `target_url` (必填,string) 待转换的短链接/Target URL to be converted

## 使用sec_user_id获取指定用户的信息

`GET /api/v1/douyin/web/handler_user_profile`

- 用途：获取指定用户的信息
- 返回：用户信息
- Query：
  - `sec_user_id` (必填,string) 必填：用户主页链接中 /user/ 后的 sec_user_id，不是抖音号或 uid/Required: sec_user_id after /user/ in the profile URL, not the Douyin ID or uid
- 示例：

```
sec_user_id = "MS4wLjABAAAAGA9bHrExvrQmowuVfRZxjG4s07M7EUjf1PlaHRHqdls"
```
- 返回结构（实测）：
  - `user.{uid,sec_uid,unique_id,short_id,nickname,signature}` — 四种 ID 与昵称签名
  - `user.{follower_count,following_count,total_favorited,aweme_count,favoriting_count}` — 粉丝/关注/获赞/作品数/喜欢数（int）
  - `user.ip_location` — 形如 `IP属地：浙江`，**带前缀**，取值需截断
  - `user.avatar_{thumb,168x168,300x300,larger}.url_list[]` — 多尺寸头像
  - `user.{city,country,custom_verify,commerce_user_level}` — 地域/认证/商业等级
  - ⚠️ 只有静态快照，没有粉丝增量；要做增量就自己按时间落盘对比

## 使用unique_id（抖音号）获取指定用户的信息

`GET /api/v1/douyin/web/handler_user_profile_v2`

- 用途：根据抖音号获取指定用户的信息
- 返回：用户信息；上游明确返回抖音号参数不合法时，返回 HTTP 200，并在 message 中提示传入合法抖音号；该请求正常计费。网络或服务故障仍按失败处理
- Query：
  - `unique_id` (必填,string) 用户抖音号，不是昵称、uid 或 sec_user_id/User Douyin ID, not a nickname, uid, or sec_user_id
- 示例：

```
unique_id = "TheChief"
```

## 加密用户uid到sec_user_id

`GET /api/v1/douyin/web/encrypt_uid_to_sec_user_id`

- 用途：加密用户uid到sec_user_id
- 返回：用户信息
- Query：
  - `uid` (必填,string) 用户uid(short_id)/User uid(short_id)
- 示例：

```
uid = "1673937488185292"
```

## 根据抖音uid获取指定用户的信息

`GET /api/v1/douyin/web/handler_user_profile_v3`

- 用途：根据抖音uid获取指定用户的信息
- 返回：用户信息
- Query：
  - `uid` (必填,string) 用户数字 uid，不是抖音号或 short_id/User numeric uid, not the Douyin ID or short_id
- 示例：

```
uid = "6796248446"
```

## 根据sec_user_id获取指定用户的信息（性别，年龄，直播等级、牌子）

`GET /api/v1/douyin/web/handler_user_profile_v4`

- 用途：获取指定用户的信息
- 返回：用户信息，包含性别，年龄，直播等级，直播间牌子
- Query：
  - `sec_user_id` (必填,string) 用户主页链接中 /user/ 后的 sec_user_id/User sec_user_id after /user/ in the profile URL
- 示例：

```
sec_user_id = "MS4wLjABAAAAGA9bHrExvrQmowuVfRZxjG4s07M7EUjf1PlaHRHqdls"
```

## 获取用户粉丝列表

`GET /api/v1/douyin/web/fetch_user_fans_list`

- 用途：获取用户粉丝列表；第一次请求时，max_time传`0`，source_type传`2`，然后会返回一个空的粉丝列表，里面包含了max_time，然后再次请求时，max_time传上一次请求返回的max_time，source_type传`1`，即可获取到粉丝列表；如果不按照上述方式请求，可能会导致返回数据包含重复数据
- 返回：粉丝列表
- Query：
  - `sec_user_id` (选填,string) 用户sec_user_id/User sec_user_id
  - `max_time` (选填,string) 最大时间戳/Maximum timestamp
  - `count` (选填,integer) 数量/Number
  - `source_type` (选填,integer) 来源类型/Source type
- 示例：

```
sec_user = "MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70"
max_time = "0"
count = 20
source_type = 2
```

## 获取用户关注列表

`GET /api/v1/douyin/web/fetch_user_following_list`

- 用途：获取用户关注列表；第一次请求时，max_time传`0`，source_type传`2`，然后会返回一个空的粉丝列表，里面包含了max_time，然后再次请求时，max_time传上一次请求返回的max_time，source_type传`1`，即可获取到粉丝列表；如果不按照上述方式请求，可能会导致返回数据包含重复数据
- 返回：关注列表
- Query：
  - `sec_user_id` (选填,string) 用户sec_user_id/User sec_user_id
  - `max_time` (选填,string) 最大时间戳/Maximum timestamp
  - `count` (选填,integer) 数量/Number
  - `source_type` (选填,integer) 来源类型/Source type
- 示例：

```
sec_user = "MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70"
max_time = "0"
count = 20
source_type = 2
```

## 获取单个视频评论数据

`GET /api/v1/douyin/web/fetch_video_comments`

- 用途：获取单个视频评论数据
- 返回：评论数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `cursor` (选填,integer) 游标/Cursor
  - `count` (选填,integer) 数量/Number
- 示例：

```
aweme_id = "7372484719365098803"
cursor = 0
count = 20
```
- 返回结构（实测）：
  - `data` 是对象（17 个字段）：`status_code`, `comments`, `cursor`, `has_more`, `reply_style`, `total`, `extra`, `log_pb`, `hotsoon_filtered_count`, `user_commented`, `fast_response_comment`, `comment_config`
  - `data.comments` 是数组（长度 5）；首元素字段：`cid`, `text`, `aweme_id`, `create_time`, `digg_count`, `status`, `user`, `reply_id`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取指定视频的评论回复数据

`GET /api/v1/douyin/web/fetch_video_comment_replies`

- 用途：获取指定视频的评论回复数据
- 返回：评论回复数据
- Query：
  - `item_id` (必填,string) 作品id/Video id
  - `comment_id` (必填,string) 评论id/Comment id
  - `cursor` (选填,integer) 游标/Cursor
  - `count` (选填,integer) 数量/Number
- 示例：

```
aweme_id = "7354666303006723354"
comment_id = "7354669356632638218"
cursor = 0
count = 20
```

## 话题作品

`POST /api/v1/douyin/web/fetch_challenge_posts`

- 用途：话题作品
- 返回：话题作品
- Body(JSON)：
  - `challenge_id` (选填,string) 话题ID/Challenge ID
  - `sort_type` (选填,integer) 排序类型/Sort type
  - `cursor` (选填,integer) 游标/Cursor
  - `count` (选填,integer) 数量/Count
  - `cookie` (选填,string) 用户自行提供的Cookie/User provided Cookie
- 示例：

```
challenge_id = "1750525814851611"
sort_type = 0
offset = 0
cursor = 0
count = 20
```

## 获取抖音热榜数据

`GET /api/v1/douyin/web/fetch_hot_search_result`

- 用途：获取抖音热榜数据
- 返回：热榜数据
- 返回结构（实测）：
  - `data` 是对象（6 个字段）：`banner_dark`, `banner_light`, `data`, `extra`, `log_pb`, `status_code`
  - `data.banner_dark` 是对象（2 个字段）：`uri`, `url_list`
  - `data.banner_light` 是对象（2 个字段）：`uri`, `url_list`
  - `data.data` 是对象（7 个字段）：`active_time`, `banner_display`, `display_style`, `share_info`, `trending_desc`, `trending_list`, `word_list`
  - `data.extra` 是对象（3 个字段）：`logid`, `now`, `time_cost`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 抖音视频频道数据

`GET /api/v1/douyin/web/fetch_video_channel_result`

- 用途：抖音视频频道数据；https://www.douyin.com/channel/300205
- 返回：视频频道数据
- Query：
  - `tag_id` (必填,integer) 标签id/Tag id
  - `count` (选填,integer) 数量/Number
  - `refresh_index` (选填,integer) 刷新索引/Refresh index
- 示例：

```
tag_id = 300203
count = 10
refresh_index = 1
```

## 获取抖音Web的游客Cookie

`GET /api/v1/douyin/web/fetch_douyin_web_guest_cookie`

- 用途：获取抖音Web的游客Cookie；可以用于爬取抖音Web的数据，如用户作品、合辑作品等；可以固定身份避免部分接口重复数据；请注意：游客Cookie无法爬取所有数据，有一定的限制；可以配合开源项目使用此接口实现抖音Web的数据爬取
- 返回：游客Cookie
- Query：
  - `user_agent` (必填,string) 用户浏览器代理/User browser agent
- 示例：

```
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
```

## 生成ttwid

`GET /api/v1/douyin/web/generate_ttwid`

- 用途：生成ttwid
- 返回：ttwid
- Query：
  - `user_agent` (选填,string)

## 查询抖音用户基本信息

`POST /api/v1/douyin/web/fetch_query_user`

- 用途：查询抖音用户基本信息
- 返回：用户基本信息
- 示例：

```
cookie = "ttwid=xxx;"
```

## 生成弹幕xb签名

`GET /api/v1/douyin/web/generate_wss_xb_signature`

- 用途：生成弹幕xb签名
- 返回：弹幕xb签名
- Query：
  - `user_agent` (必填,string) 用户浏览器代理/User browser agent
  - `room_id` (必填,string) 房间号/Room ID
  - `user_unique_id` (必填,string) 用户唯一ID/User unique ID
- 示例：

```
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
room_id = "7382517534467115826"
user_unique_id = "7382524529011246630"
```

## 提取单个用户id

`GET /api/v1/douyin/web/get_sec_user_id`

- 用途：提取单个用户id
- 返回：用户sec_user_id
- Query：
  - `url` (必填,string)
- 示例：

```
url = "https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE"
```

## 提取列表用户id

`POST /api/v1/douyin/web/get_all_sec_user_id`

- Body(JSON)：
  - `url` (必填,array) 用户主页链接列表/User homepage link list
- 示例：

```
```json
 {
"urls":[
   "https://www.douyin.com/user/MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE?vid=7285950278132616463",
   "https://www.douyin.com/user/MS4wLjABAAAAVsneOf144eGDFf8Xp9QNb1VW6ovXnNT5SqJBhJfe8KQBKWKDTWK5Hh-_i9mJzb8C",
   "长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/idFqvUms/",
   "https://v.douyin.com/idFqvUms/"
    ]
 }
 ```
```

## 提取单个作品id

`GET /api/v1/douyin/web/get_aweme_id`

- 用途：提取单个作品id
- 返回：作品id
- Query：
  - `url` (必填,string)
- 示例：

```
url = "https://www.douyin.com/video/7298145681699622182"
```

## 提取列表作品id

`POST /api/v1/douyin/web/get_all_aweme_id`

- Body(JSON)：
  - `url` (必填,array) 作品链接列表/Video link list
- 示例：

```
```json
 {
"urls":[
    "0.53 02/26 I@v.sE Fus:/ 你别太帅了郑润泽# 现场版live # 音乐节 # 郑润泽  https://v.douyin.com/iRNBho6u/ 复制此链接，打开Dou音搜索，直接观看视频!",
    "https://v.douyin.com/iRNBho6u/",
    "https://www.iesdouyin.com/share/video/7298145681699622182/?region=CN&mid=7298145762238565171&u_code=l1j9bkbd&did=MS4wLjABAAAAtqpCx0hpOERbdSzQdjRZw-wFPxaqdbAzsKDmbJMUI3KWlMGQHC-n6dXAqa-dM2EP&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ&with_sec_did=1&titleType=title&share_sign=05kGlqGmR4_IwCX.ZGk6xuL0osNA..5ur7b0jbOx6cc-&share_version=170400&ts=1699262937&from_aid=6383&from_ssr=1&from=web_code_link",
    "https://www.douyin.com/video/7298145681699622182?previous_page=web_code_link",
    "https://www.douyin.com/video/7298145681699622182",
 ]
 }
 ```
```

## 提取直播间号

`GET /api/v1/douyin/web/get_webcast_id`

- 用途：提取列表直播间号
- 返回：直播间号
- Query：
  - `url` (必填,string)
- 示例：

```
url = "https://live.douyin.com/775841227732"
```

## 提取列表直播间号

`POST /api/v1/douyin/web/get_all_webcast_id`

- 用途：提取列表直播间号
- 返回：直播间号列表
- Body(JSON)：
  - `url` (必填,array) 直播间链接列表/Room link list
- 示例：

```
```json
{
  "urls": [
        "https://live.douyin.com/775841227732",
        "https://live.douyin.com/775841227732?room_id=7318296342189919011&enter_from_merge=web_share_link&enter_method=web_share_link&previous_page=app_code_link",
        'https://webcast.amemv.com/douyin/webcast/reflow/7318296342189919011?u_code=l1j9bkbd&did=MS4wLjABAAAAEs86TBQPNwAo-RGrcxWyCdwKhI66AK3Pqf3ieo6HaxI&iid=MS4wLjABAAAA0ptpM-zzoliLEeyvWOCUt-_dQza4uSjlIvbtIazXnCY&with_sec_did=1&use_link_command=1&ecom_share_track_params=&extra_params={"from_request_id":"20231230162057EC005772A8EAA0199906","im_channel_invite_id":"0"}&user_id=3644207898042206&liveId=7318296342189919011&from=share&style=share&enter_method=click_share&roomId=7318296342189919011&activity_info={}',
        "6i- Q@x.Sl 03/23 【醒子8ke的直播间】  点击打开👉https://v.douyin.com/i8tBR7hX/  或长按复制此条消息，打开抖音，看TA直播",
        "https://v.douyin.com/i8tBR7hX/",
        ]
}
```
```

## 直播间号转房间号

`GET /api/v1/douyin/web/webcast_id_2_room_id`

- 用途：直播间号转房间号
- 返回：房间号
- Query：
  - `webcast_id` (必填,string) 直播间号/Webcast id
- 示例：

```
"webcast_id = "775841227732"
```

## 抖音直播间弹幕参数获取

`GET /api/v1/douyin/web/fetch_live_im_fetch`

- 用途：抖音直播间弹幕参数获取
- 返回：弹幕参数数据
- Query：
  - `room_id` (必填,string) 直播间号/Live room id
  - `user_unique_id` (必填,string) 用户唯一ID/User unique ID

## 短剧作品

`GET /api/v1/douyin/web/fetch_series_aweme`

- 用途：短剧作品
- 返回：短剧作品数据
- Query：
  - `offset` (必填,integer) 页码/Page number
  - `count` (必填,integer) 每页数量/Number per page
  - `content_type` (必填,integer) 短剧类型/Subtype
  - `cookie` (选填,string) 用户自行提供的Cookie/User provided Cookie

## 知识作品推荐

`GET /api/v1/douyin/web/fetch_knowledge_aweme`

- 用途：知识作品
- 返回：知识作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (选填,integer) 翻页索引/Paging index
  - `cookie` (选填,string) 用户自行提供的Cookie/User provided Cookie

## 游戏作品推荐

`GET /api/v1/douyin/web/fetch_game_aweme`

- 用途：知识作品
- 返回：游戏作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (选填,integer) 翻页索引/Paging index
  - `cookie` (选填,string) 用户自行提供的Cookie/User provided Cookie

## 二次元作品推荐

`GET /api/v1/douyin/web/fetch_cartoon_aweme`

- 用途：二次元作品
- 返回：二次元作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (选填,integer) 翻页索引/Paging index
  - `cookie` (选填,string) 用户自行提供的Cookie/User provided Cookie

## 音乐作品推荐

`GET /api/v1/douyin/web/fetch_music_aweme`

- 用途：音乐作品
- 返回：音乐作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (选填,integer) 翻页索引/Paging index
  - `cookie` (选填,string) 用户自行提供的Cookie/User provided Cookie

## 美食作品推荐

`GET /api/v1/douyin/web/fetch_food_aweme`

- 用途：美食作品
- 返回：美食作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (选填,integer) 翻页索引/Paging index
  - `cookie` (选填,string) 用户自行提供的Cookie/User provided Cookie
