# Douyin App V3 API（APP 端）

文件夹 `Douyin-App-V3-API` · 38 个接口 · BASE `https://api.tikhub.io`

## 获取抖音品牌热榜分类数据

`GET /api/v1/douyin/app/v3/fetch_brand_hot_search_list`

- 返回：品牌热搜榜分类数据

## 获取抖音品牌热榜具体分类数据

`GET /api/v1/douyin/app/v3/fetch_brand_hot_search_list_detail`

- 返回：品牌热搜榜具体分类数据
- Query：
  - `category_id` (必填,integer) 分类id/Category id

## 获取指定话题的详情数据

`GET /api/v1/douyin/app/v3/fetch_hashtag_detail`

- 返回：话题详情数据
- Query：
  - `ch_id` (必填,integer) 话题id/Hashtag id

## 获取指定话题的作品数据

`GET /api/v1/douyin/app/v3/fetch_hashtag_video_list`

- 返回：话题作品数据
- Query：
  - `ch_id` (必填,string) 话题id/Hashtag id
  - `cursor` (integer,默认 0) 游标/Cursor
  - `sort_type` (integer,默认 0) 排序类型/Sort type
  - `count` (integer,默认 10) 数量/Number

## 获取抖音热搜榜数据

`GET /api/v1/douyin/app/v3/fetch_hot_search_list`

- 用途：获取抖音热榜数据，包括：
- 返回：热搜榜数据
- Query：
  - `board_type` (string,默认 0) 榜单类型/Board type
  - `board_sub_type` (string) 榜单子类型/Board sub type

## 获取抖音直播热搜榜数据

`GET /api/v1/douyin/app/v3/fetch_live_hot_search_list`

- 返回：直播热搜榜数据

## 批量获取视频信息 V1

`POST /api/v1/douyin/app/v3/fetch_multi_video`

- 用途：批量获取视频信息，支持图文、视频等，一次性最多支持10个视频，此接口收费固定价格为0.001$ * 10 = 0.01$一次。
- 返回：作品数据
- Body(JSON)：
  - `aweme_ids` 作品id列表，最多支持10个作品id。

## 批量获取视频的最高画质播放链接

`POST /api/v1/douyin/app/v3/fetch_multi_video_high_quality_play_url`

- 用途：此接口目前优惠活动价为$0.25，活动结束后恢复原价$0.5。不足50个视频按50个视频收费。
- 返回：total: 总数
- Body(JSON)：
  - `aweme_ids` (string,默认 7512756548356492544,7448118827402972455,7126745726494821640) 作品id列表，用逗号分隔，最多50个/Video id list, separated by commas, up to 50
  - `region` 可选，请求出口地区(ISO 国家代码，如 CN/US/HK)。抖音根据请求 IP 返回对应区域 CDN，国内用户传 'CN' 可获得国内 CDN 链接以加快下载速度 / Optional, ISO country code (e.g. CN). Pass 'CN' for users in mainland China to get China-region CDN URLs for faster download.

## 根据视频ID批量获取作品的统计数据（点赞数、下载数、播放数、分享数）

`GET /api/v1/douyin/app/v3/fetch_multi_video_statistics`

- 用途：根据视频ID获取作品的统计数据，支持多个视频id，一次性最多支持50个视频。
- 返回：作品统计数据
- Query：
  - `aweme_ids` (必填,string) 作品id/Video id

## 批量获取视频信息 V2

`POST /api/v1/douyin/app/v3/fetch_multi_video_v2`

- 用途：批量获取视频信息，支持图文、视频等，一次性最多支持50个视频，此接口收费固定价格为0.001$ * 50 = 0.05$一次。
- 返回：作品数据
- Body(JSON)：
  - `aweme_ids` 作品id列表，最多支持50个作品id。

## 获取指定音乐的详情数据

`GET /api/v1/douyin/app/v3/fetch_music_detail`

- 返回：音乐详情数据
- Query：
  - `music_id` (必填,string) 音乐id/Music id

## 获取抖音音乐榜数据

`GET /api/v1/douyin/app/v3/fetch_music_hot_search_list`

- 用途：获取抖音音乐热榜数据
- 返回：音乐热搜榜数据
- Query：
  - `chart_type` (string,默认 hot) 榜单类型/Chart type
  - `cursor` (string,默认 0) 游标/Cursor

## 获取指定音乐的视频列表数据

`GET /api/v1/douyin/app/v3/fetch_music_video_list`

- 返回：音乐视频列表数据
- Query：
  - `music_id` (必填,string) 音乐id/Music id
  - `cursor` (integer,默认 0) 游标/Cursor
  - `count` (integer,默认 10) 数量/Number

## 获取单个作品数据

`GET /api/v1/douyin/app/v3/fetch_one_video`

- 用途：获取单个作品数据，支持图文、视频等。
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id

## 根据分享链接获取单个作品数据

`GET /api/v1/douyin/app/v3/fetch_one_video_by_share_url`

- 返回：作品数据
- Query：
  - `share_url` (必填,string) 分享链接/Share link

## 获取单个作品数据 V2

`GET /api/v1/douyin/app/v3/fetch_one_video_v2`

- 用途：获取单个作品数据，支持图文、视频等。
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id

## 获取单个作品数据 V3 (无版权限制)

`GET /api/v1/douyin/app/v3/fetch_one_video_v3`

- 用途：获取单个作品数据，支持文章、图文、视频等。
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品或文章ID/Video or Article ID

## 获取短剧详情信息

`GET /api/v1/douyin/app/v3/fetch_series_detail`

- 返回：短剧详情数据
- Query：
  - `series_id` (必填,string) 短剧id/Series id

## 获取短剧视频列表

`GET /api/v1/douyin/app/v3/fetch_series_video_list`

- 返回：短剧视频列表数据
- Query：
  - `series_id` (必填,string) 短剧id/Series id
  - `cursor` (integer,默认 0) 游标/Cursor

## 根据分享口令获取分享信息

`GET /api/v1/douyin/app/v3/fetch_share_info_by_share_code`

- 用途：根据分享口令获取分享信息，比如抖音文章的分享口令提取分享人信息和文章ID等然后再去请求单一作品数据接口获取文章内容。
- 返回：分享信息，包含分享人信息和文章ID等
- Query：
  - `share_code` (必填,string) 分享口令/Share code

## 获取用户粉丝列表

`GET /api/v1/douyin/app/v3/fetch_user_fans_list`

- 返回：粉丝列表
- Query：
  - `sec_user_id` (string,默认 MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70) 用户sec_user_id/User sec_user_id
  - `max_time` (string,默认 0) 最大时间戳/Maximum timestamp
  - `count` (integer,默认 20) 数量/Number

## 获取用户喜欢作品数据

`GET /api/v1/douyin/app/v3/fetch_user_like_videos`

- 返回：用户作品数据
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (integer,默认 0) 最大游标/Maximum cursor
  - `counts` (integer,默认 20) 每页数量/Number per page

## 获取用户主页作品数据

`GET /api/v1/douyin/app/v3/fetch_user_post_videos`

- 返回：用户作品数据
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (integer,默认 0) 最大游标/Maximum cursor
  - `count` (integer,默认 20) 每页数量/Number per page
  - `sort_type` (integer,默认 0) 排序类型/Sort type
  - `channel` (string,默认 normal) 抖音渠道版本/Douyin channel: normal(正常版-默认), lite(极速版)

## 获取用户短剧合集列表

`GET /api/v1/douyin/app/v3/fetch_user_series_list`

- 用途：获取用户的短剧合集列表
- 返回：用户短剧合集列表数据
- Query：
  - `user_id` (string) 用户id/User id
  - `sec_user_id` (string) 用户加密id/User sec id
  - `cursor` (integer,默认 0) 游标/Cursor

## 获取指定视频的评论回复数据

`GET /api/v1/douyin/app/v3/fetch_video_comment_replies`

- 返回：评论回复数据
- Query：
  - `item_id` (必填,string) 作品id/Video id
  - `comment_id` (必填,string) 评论id/Comment id
  - `cursor` (integer,默认 0) 游标/Cursor
  - `count` (integer,默认 20) 数量/Number

## 获取单个视频评论数据

`GET /api/v1/douyin/app/v3/fetch_video_comments`

- 返回：评论数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `cursor` (integer,默认 0) 游标/Cursor
  - `count` (integer,默认 20) 数量/Number

## 获取视频的最高画质播放链接

`GET /api/v1/douyin/app/v3/fetch_video_high_quality_play_url`

- 用途：价格：0.005$ 一次。
- 返回：video_id： 作品id
- Query：
  - `aweme_id` (string) 作品id/Video id
  - `share_url` (string) 可选，分享链接/Optional, share link
  - `region` (string) 可选，请求出口地区(ISO 国家代码，如 CN/US/HK)，国内用户传 CN 可拿到国内 CDN 域名以加快下载速度 / Optional, ISO country code (e.g. CN/US/HK). Pass CN to get China-region CDN URLs for faster download in mainland China.

## 获取抖音视频合集详情数据

`GET /api/v1/douyin/app/v3/fetch_video_mix_detail`

- 返回：视频合集详情数据
- Query：
  - `mix_id` (必填,string) 合集id/Mix id

## 获取抖音视频合集作品列表数据

`GET /api/v1/douyin/app/v3/fetch_video_mix_post_list`

- 返回：视频合集作品列表数据
- Query：
  - `mix_id` (必填,string) 合集id/Mix id
  - `cursor` (integer,默认 0) 游标/Cursor
  - `count` (integer,默认 20) 数量/Number

## 根据视频ID获取作品的统计数据（点赞数、下载数、播放数、分享数）

`GET /api/v1/douyin/app/v3/fetch_video_statistics`

- 用途：根据视频ID获取作品的统计数据
- 返回：作品统计数据
- Query：
  - `aweme_ids` (必填,string) 作品id/Video id

## 生成抖音短链接

`GET /api/v1/douyin/app/v3/generate_douyin_short_url`

- 返回：短链接数据
- Query：
  - `url` (必填,string) 抖音链接/Douyin link

## 生成抖音视频分享二维码

`GET /api/v1/douyin/app/v3/generate_douyin_video_share_qrcode`

- 返回：二维码数据
- Query：
  - `object_id` (必填,string) 作品id/Video id

## 获取指定用户的信息

`GET /api/v1/douyin/app/v3/handler_user_profile`

- 返回：用户信息
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id

## 生成抖音分享链接，唤起抖音APP，跳转指定关键词搜索结果

`GET /api/v1/douyin/app/v3/open_douyin_app_to_keyword_search`

- 用途：生成抖音分享链接，唤起抖音APP，跳转指定关键词搜索结果。
- 返回：分享链接
- Query：
  - `keyword` (必填,string) 关键词/Keyword

## 生成抖音分享链接，唤起抖音APP，给指定用户发送私信

`GET /api/v1/douyin/app/v3/open_douyin_app_to_send_private_message`

- 用途：生成抖音分享链接，唤起抖音APP，给指定用户发送私信。
- 返回：分享链接
- Query：
  - `uid` (必填,string) 用户id/User id
  - `sec_uid` (必填,string) 用户sec_uid/User sec_uid

## 生成抖音分享链接，唤起抖音APP，跳转指定用户主页

`GET /api/v1/douyin/app/v3/open_douyin_app_to_user_profile`

- 用途：生成抖音分享链接，唤起抖音APP，跳转指定用户主页。
- 返回：分享链接
- Query：
  - `uid` (必填,string) 用户id/User id
  - `sec_uid` (必填,string) 用户sec_uid/User sec_uid

## 生成抖音分享链接，唤起抖音APP，跳转指定作品详情页

`GET /api/v1/douyin/app/v3/open_douyin_app_to_video_detail`

- 用途：生成抖音分享链接，唤起抖音APP，跳转指定作品详情页。
- 返回：分享链接
- Query：
  - `aweme_id` (必填,string) 作品id/Video id

## 抖音APP注册设备

`GET /api/v1/douyin/app/v3/register_device`

- 用途：抖音APP注册设备，获取设备信息以及设备的Cookie信息。
- 返回：设备信息以及设备的Cookie信息。
- Query：
  - `proxy` (string) 代理/Proxy
