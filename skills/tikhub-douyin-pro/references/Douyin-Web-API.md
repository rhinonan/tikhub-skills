# Douyin Web API（网页端）

文件夹 `Douyin-Web-API` · 55 个接口 · BASE `https://api.tikhub.io`

## 加密用户uid到sec_user_id

`GET /api/v1/douyin/web/encrypt_uid_to_sec_user_id`

- 返回：用户信息
- Query：
  - `uid` (必填,string) 用户uid(short_id)/User uid(short_id)

## 获取批量用户信息(最多10个)

`GET /api/v1/douyin/web/fetch_batch_user_profile_v1`

- 用途：获取批量用户信息，最多支持10个用户
- 返回：批量用户信息
- Query：
  - `sec_user_ids` (必填,string) 用户sec_user_id列表，用逗号分隔/User sec_user_id list, separated by commas

## 获取批量用户信息(最多50个)

`GET /api/v1/douyin/web/fetch_batch_user_profile_v2`

- 用途：获取批量用户信息，最多支持50个用户
- 返回：批量用户信息
- Query：
  - `sec_user_ids` (必填,string) 用户sec_user_id列表，用逗号分隔/User sec_user_id list, separated by commas

## 二次元作品推荐

`GET /api/v1/douyin/web/fetch_cartoon_aweme`

- 用途：二次元作品
- 返回：二次元作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (integer,默认 1) 翻页索引/Paging index
  - `cookie` (string) 用户自行提供的Cookie/User provided Cookie

## 话题作品

`POST /api/v1/douyin/web/fetch_challenge_posts`

- 返回：话题作品
- Body(JSON)：
  - `challenge_id` (string,默认 1608846127610893) 话题ID/Challenge ID
  - `sort_type` (integer,默认 0) 排序类型/Sort type
  - `cursor` (integer,默认 0) 游标/Cursor
  - `count` (integer,默认 20) 数量/Count
  - `cookie` (string) 用户自行提供的Cookie/User provided Cookie

## 获取抖音Web的游客Cookie

`GET /api/v1/douyin/web/fetch_douyin_web_guest_cookie`

- 返回：游客Cookie
- Query：
  - `user_agent` (必填,string) 用户浏览器代理/User browser agent

## 美食作品推荐

`GET /api/v1/douyin/web/fetch_food_aweme`

- 用途：美食作品
- 返回：美食作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (integer,默认 1) 翻页索引/Paging index
  - `cookie` (string) 用户自行提供的Cookie/User provided Cookie

## 游戏作品推荐

`GET /api/v1/douyin/web/fetch_game_aweme`

- 用途：知识作品
- 返回：游戏作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (integer,默认 1) 翻页索引/Paging index
  - `cookie` (string) 用户自行提供的Cookie/User provided Cookie

## 获取首页推荐数据

`POST /api/v1/douyin/web/fetch_home_feed`

- 返回：Feed数据
- Body(JSON)：
  - `count` (integer,默认 10) 数量/Number
  - `refresh_index` (integer,默认 0) 刷新/翻页索引：0=刷新(首页/下拉)，>0=翻页(下滑加载更多)，每次+1取下一页 / Refresh-paging index: 0=refresh, >0=load-more, increment by 1 for next page
  - `cookie` (string) 可选/Optional：用户网页版抖音登录Cookie，传入后返回该账号的个性化推荐；不传则以游客身份访问/Your web Douyin login Cookie for a personalized feed; guest access if omitted

## 获取抖音热榜数据

`GET /api/v1/douyin/web/fetch_hot_search_result`

- 返回：热榜数据

## 知识作品推荐

`GET /api/v1/douyin/web/fetch_knowledge_aweme`

- 用途：知识作品
- 返回：知识作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (integer,默认 1) 翻页索引/Paging index
  - `cookie` (string) 用户自行提供的Cookie/User provided Cookie

## 获取直播间送礼用户排行榜

`GET /api/v1/douyin/web/fetch_live_gift_ranking`

- 返回：排行榜数据
- Query：
  - `room_id` (必填,string) 直播间room_id/Room room_id
  - `rank_type` (integer,默认 30) 排行类型/Leaderboard type

## 抖音直播间弹幕参数获取

`GET /api/v1/douyin/web/fetch_live_im_fetch`

- 返回：弹幕参数数据
- Query：
  - `room_id` (必填,string) 直播间号/Live room id
  - `user_unique_id` (必填,string) 用户唯一ID/User unique ID

## 批量获取视频信息

`POST /api/v1/douyin/web/fetch_multi_video`

- 用途：批量获取视频信息，支持图文、视频等，一次性最多支持50个视频，此接口收费固定价格为0.001$ * 50 = 0.05$一次。
- 返回：作品数据
- Body(JSON)：
  - `aweme_ids` 作品id列表，最多支持50个作品id。

## 批量获取视频的最高画质播放链接

`POST /api/v1/douyin/web/fetch_multi_video_high_quality_play_url`

- 用途：此接口目前优惠活动价为$0.25，活动结束后恢复原价$0.5。不足50个视频按50个视频收费。
- 返回：total: 总数
- Body(JSON)：
  - `aweme_ids` (string,默认 7512756548356492544,7448118827402972455,7126745726494821640) 作品id列表，用逗号分隔，最多50个/Video id list, separated by commas, up to 50
  - `region` 可选，请求出口地区(ISO 国家代码，如 CN/US/HK)。抖音根据请求 IP 返回对应区域 CDN，国内用户传 'CN' 可获得国内 CDN 链接以加快下载速度 / Optional, ISO country code (e.g. CN). Pass 'CN' for users in mainland China to get China-region CDN URLs for faster download.

## 音乐作品推荐

`GET /api/v1/douyin/web/fetch_music_aweme`

- 用途：音乐作品
- 返回：音乐作品数据
- Query：
  - `count` (必填,integer) 每页数量/Number per page
  - `refresh_index` (integer,默认 1) 翻页索引/Paging index
  - `cookie` (string) 用户自行提供的Cookie/User provided Cookie

## 获取单个作品数据

`GET /api/v1/douyin/web/fetch_one_video`

- 用途：获取单个作品数据 V1，若此接口失效，请使用 `/fetch_one_video_v2` 接口，或使用APP接口。
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `need_anchor_info` (boolean,默认 False) 是否需要锚点信息/Whether anchor information is needed

## 根据分享链接获取单个作品数据

`GET /api/v1/douyin/web/fetch_one_video_by_share_url`

- 用途：根据分享链接获取单个作品数据 （本质上基于 `/fetch_one_video` 接口实现，建议有能力自行获取视频ID以提升接口响应速度）
- 返回：作品数据
- Query：
  - `share_url` (必填,string) 分享链接/Share link

## 获取单个作品视频弹幕数据

`GET /api/v1/douyin/web/fetch_one_video_danmaku`

- 返回：视频弹幕数据
- Query：
  - `item_id` (必填,string) 作品id/Video id
  - `duration` (必填,integer) 视频总时长/Video total duration
  - `end_time` (必填,integer) 结束时间/End time
  - `start_time` (必填,integer) 开始时间/Start time

## 获取单个作品数据 V2

`GET /api/v1/douyin/web/fetch_one_video_v2`

- 用途：获取单个作品数据 V2，若此接口失效，请使用 `/fetch_one_video` 接口，或使用APP接口。
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id

## 查询抖音用户基本信息

`POST /api/v1/douyin/web/fetch_query_user`

- 返回：用户基本信息
- Body(JSON)：
  - `cookie` 用户ttwid Cookie，获取方式：调用`/api/v1/douyin/web/generate_ttwid`接口获取。

## 获取相关作品推荐数据

`GET /api/v1/douyin/web/fetch_related_posts`

- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `refresh_index` (integer,默认 1) 翻页索引/Paging index
  - `count` (integer,默认 20) 数量/Number

## 短剧作品

`GET /api/v1/douyin/web/fetch_series_aweme`

- 返回：短剧作品数据
- Query：
  - `offset` (必填,integer) 页码/Page number
  - `count` (必填,integer) 每页数量/Number per page
  - `content_type` (必填,integer) 短剧类型/Subtype
  - `cookie` (string) 用户自行提供的Cookie/User provided Cookie

## 获取用户收藏作品数据

`POST /api/v1/douyin/web/fetch_user_collection_videos`

- 返回：用户作品数据
- Body(JSON)：
  - `cookie` (必填,string) 用户网页版抖音Cookie/Your web version of Douyin Cookie
  - `max_cursor` (integer,默认 0) 最大游标/Maximum cursor
  - `counts` (integer,默认 20) 每页数量/Number per page

## 获取用户收藏夹

`POST /api/v1/douyin/web/fetch_user_collects`

- 返回：用户收藏夹数据
- Body(JSON)：
  - `max_cursor` (integer,默认 0) 最大游标/Maximum cursor
  - `counts` (integer,默认 20) 每页数量/Number per page
  - `cookie` (必填,string) 用户网页版抖音Cookie/Your web version of Douyin Cookie

## 获取用户收藏夹作品（自带Cookie）

`POST /api/v1/douyin/web/fetch_user_collects_videos`

- 用途：获取本人收藏夹内的作品列表，所有参数通过 JSON 请求体传入。
- 返回：作品列表 aweme_list、分页游标 cursor 和是否有下一页 has_more。
- Body(JSON)：
  - `collects_id` (必填,string) 收藏夹id/Collection id
  - `max_cursor` (integer,默认 0) 最大游标/Maximum cursor
  - `counts` (integer,默认 20) 每页数量/Number per page
  - `cookie` (必填,string) 收藏夹所属账号的抖音网页版登录Cookie/Web Douyin login Cookie of the collection owner

## 获取用户粉丝列表

`GET /api/v1/douyin/web/fetch_user_fans_list`

- 返回：粉丝列表
- Query：
  - `sec_user_id` (string,默认 MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70) 用户sec_user_id/User sec_user_id
  - `max_time` (string,默认 0) 最大时间戳/Maximum timestamp
  - `count` (integer,默认 20) 数量/Number
  - `source_type` (integer,默认 1) 来源类型/Source type

## 获取用户关注列表

`GET /api/v1/douyin/web/fetch_user_following_list`

- 返回：关注列表
- Query：
  - `sec_user_id` (string,默认 MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70) 用户sec_user_id/User sec_user_id
  - `max_time` (string,默认 0) 最大时间戳/Maximum timestamp
  - `count` (integer,默认 20) 数量/Number
  - `source_type` (integer,默认 1) 来源类型/Source type

## 获取用户喜欢作品数据

`POST /api/v1/douyin/web/fetch_user_like_videos`

- 返回：用户作品数据
- Body(JSON)：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (integer,默认 0) 最大游标/Maximum cursor
  - `counts` (integer,默认 20) 每页数量/Number per page
  - `cookie` 可选：本人有效的抖音网页版登录Cookie；提供后使用该登录身份访问，不传则以游客身份访问/Optional: your valid Douyin web login Cookie; uses that signed-in identity when provided, otherwise guest access

## 使用UID获取用户开播信息

`GET /api/v1/douyin/web/fetch_user_live_info_by_uid`

- 返回：用户开播信息，包含room_id与live_status
- Query：
  - `uid` (必填,string) 用户UID/User UID

## 获取用户直播流数据

`GET /api/v1/douyin/web/fetch_user_live_videos`

- 返回：直播流数据
- Query：
  - `webcast_id` (必填,string) 直播间webcast_id/Room webcast_id

## 通过room_id获取指定用户的直播流数据 V2

`GET /api/v1/douyin/web/fetch_user_live_videos_by_room_id_v2`

- 用途：获取指定用户的直播流数据V2
- 返回：直播流数据
- Query：
  - `room_id` (必填,string) 直播间room_id/Room room_id

## 通过sec_uid获取指定用户的直播流数据

`GET /api/v1/douyin/web/fetch_user_live_videos_by_sec_uid`

- 返回：直播流数据
- Query：
  - `sec_uid` (必填,string) 用户sec_uid/User sec_uid

## 获取用户合辑作品数据

`GET /api/v1/douyin/web/fetch_user_mix_videos`

- 返回：用户作品数据
- Query：
  - `mix_id` (必填,string) 合辑id/Mix id
  - `max_cursor` (integer,默认 0) 最大游标/Maximum cursor
  - `counts` (integer,默认 20) 每页数量/Number per page

## 获取用户主页作品数据

`GET /api/v1/douyin/web/fetch_user_post_videos`

- 返回：用户作品数据
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (string,默认 0) 最大游标/Maximum cursor
  - `count` (integer,默认 20) 每页数量/Number per page
  - `filter_type` (string,默认 0) 过滤类型/Filter type
  - `cookie` (string) 用户网页版抖音Cookie/Your web version of Douyin Cookie

## 使用Short ID获取用户信息

`GET /api/v1/douyin/web/fetch_user_profile_by_short_id`

- 返回：用户信息
- Query：
  - `short_id` (必填,string) 用户Short ID/User Short ID

## 使用UID获取用户信息

`GET /api/v1/douyin/web/fetch_user_profile_by_uid`

- 返回：用户信息
- Query：
  - `uid` (必填,string) 用户UID/User UID

## 抖音视频频道数据

`GET /api/v1/douyin/web/fetch_video_channel_result`

- 返回：视频频道数据
- Query：
  - `tag_id` (必填,integer) 标签id/Tag id
  - `count` (integer,默认 10) 数量/Number
  - `refresh_index` (integer,默认 1) 刷新索引/Refresh index

## 获取指定视频的评论回复数据

`GET /api/v1/douyin/web/fetch_video_comment_replies`

- 返回：评论回复数据
- Query：
  - `item_id` (必填,string) 作品id/Video id
  - `comment_id` (必填,string) 评论id/Comment id
  - `cursor` (integer,默认 0) 游标/Cursor
  - `count` (integer,默认 20) 数量/Number

## 获取单个视频评论数据

`GET /api/v1/douyin/web/fetch_video_comments`

- 返回：评论数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `cursor` (integer,默认 0) 游标/Cursor
  - `count` (integer,默认 20) 数量/Number

## 获取视频的最高画质播放链接

`GET /api/v1/douyin/web/fetch_video_high_quality_play_url`

- 用途：价格：0.005$ 一次。
- 返回：video_id： 作品id
- Query：
  - `aweme_id` (string) 作品id/Video id
  - `share_url` (string) 可选，分享链接/Optional, share link
  - `region` (string) 可选，请求出口地区(ISO 国家代码，如 CN/US/HK)，国内用户传 CN 可拿到国内 CDN 域名以加快下载速度 / Optional, ISO country code (e.g. CN/US/HK). Pass CN to get China-region CDN URLs for faster download in mainland China.

## 生成ttwid

`GET /api/v1/douyin/web/generate_ttwid`

- 返回：ttwid
- Query：
  - `user_agent` (string,默认 Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0)

## 生成弹幕xb签名

`GET /api/v1/douyin/web/generate_wss_xb_signature`

- 返回：弹幕xb签名
- Query：
  - `user_agent` (必填,string) 用户浏览器代理/User browser agent
  - `room_id` (必填,string) 房间号/Room ID
  - `user_unique_id` (必填,string) 用户唯一ID/User unique ID

## 提取列表作品id

`POST /api/v1/douyin/web/get_all_aweme_id`

- 用途：提取列表作品id（最多支持20个链接）
- 返回：作品id列表
- Body(JSON)：
  - `url` 作品链接列表

## 提取列表用户id

`POST /api/v1/douyin/web/get_all_sec_user_id`

- 返回：如果链接成功获取到sec_user_id，则返回sec_user_id，否则返回原始的输入链接，后续可以手动校验链接无法获取sec_user_id的原因。
- Body(JSON)：
  - `url` 用户主页链接列表（最多支持10个链接）

## 提取列表直播间号

`POST /api/v1/douyin/web/get_all_webcast_id`

- 返回：直播间号列表
- Body(JSON)：
  - `url` 直播间链接列表（最多支持20个链接）

## 提取单个作品id

`GET /api/v1/douyin/web/get_aweme_id`

- 返回：作品id
- Query：
  - `url` (必填,string)

## 提取单个用户id

`GET /api/v1/douyin/web/get_sec_user_id`

- 返回：用户sec_user_id
- Query：
  - `url` (必填,string)

## 提取直播间号

`GET /api/v1/douyin/web/get_webcast_id`

- 用途：提取列表直播间号
- 返回：直播间号
- Query：
  - `url` (必填,string)

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

## 使用unique_id（抖音号）获取指定用户的信息

`GET /api/v1/douyin/web/handler_user_profile_v2`

- 用途：根据抖音号获取指定用户的信息
- 返回：用户信息
- Query：
  - `unique_id` (必填,string) 用户抖音号，不是昵称、uid 或 sec_user_id/User Douyin ID, not a nickname, uid, or sec_user_id

## 根据抖音uid获取指定用户的信息

`GET /api/v1/douyin/web/handler_user_profile_v3`

- 返回：用户信息
- Query：
  - `uid` (必填,string) 用户数字 uid，不是抖音号或 short_id/User numeric uid, not the Douyin ID or short_id

## 根据sec_user_id获取指定用户的信息（性别，年龄，直播等级、牌子）

`GET /api/v1/douyin/web/handler_user_profile_v4`

- 用途：获取指定用户的信息
- 返回：用户信息，包含性别，年龄，直播等级，直播间牌子
- Query：
  - `sec_user_id` (必填,string) 用户主页链接中 /user/ 后的 sec_user_id/User sec_user_id after /user/ in the profile URL

## 直播间号转房间号

`GET /api/v1/douyin/web/webcast_id_2_room_id`

- 返回：房间号
- Query：
  - `webcast_id` (必填,string) 直播间号/Webcast id
