# Douyin App V3 API

文件夹 `Douyin-App-V3-API` · 38 个接口
说明：抖音-App-V3数据接口（当前最新版本）


## 获取单个作品数据

`GET /api/v1/douyin/app/v3/fetch_one_video`

- 用途：获取单个作品数据，支持图文、视频等
- 返回：作品数据
- 注意：If the interface returns empty, please use the same parameters to request the Web version interface. The specific response status code refers to:
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
- 示例：

```
aweme_id = "7448118827402972455"
```

## 获取单个作品数据 V2

`GET /api/v1/douyin/app/v3/fetch_one_video_v2`

- 用途：获取单个作品数据，支持图文、视频等
- 返回：作品数据
- 注意：If the interface returns empty, please use the same parameters to request the Web version interface. The specific response status code refers to:
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
- 示例：

```
aweme_id = "7448118827402972455"
```

## 获取单个作品数据 V3 (无版权限制)

`GET /api/v1/douyin/app/v3/fetch_one_video_v3`

- 用途：获取单个作品数据，支持文章、图文、视频等；V3版本的接口，解决了版权限制问题，可以获取更多受限内容，比如 V1，V2版本返回的Reason为8的内容和部分文章或短剧等
- 返回：作品数据
- Query：
  - `aweme_id` (必填,string) 作品或文章ID/Video or Article ID
- 示例：

```
aweme_id = "7592116912205630761"
```

## 根据分享口令获取分享信息

`GET /api/v1/douyin/app/v3/fetch_share_info_by_share_code`

- 用途：根据分享口令获取分享信息，比如抖音文章的分享口令提取分享人信息和文章ID等然后再去请求单一作品数据接口获取文章内容
- 返回：分享信息，包含分享人信息和文章ID等
- Query：
  - `share_code` (必填,string) 分享口令/Share code
- 示例：

```
share_code = "8:/ h@O.kP 05/21 【生意场上，装逼就是节省沟通成本】长按复制打开抖音，即可阅读文章 ︽︽2QnCB9aIZZ29︽︽"
```

## 批量获取视频信息 V1

`POST /api/v1/douyin/app/v3/fetch_multi_video`

- 用途：批量获取视频信息，支持图文、视频等，一次性最多支持10个视频，此接口收费固定价格为0.001$ * 10 = 0.01$一次
- 返回：作品数据
- 注意：If the interface returns empty, please use the same parameters to request the Web version interface. The specific response status code refers to:
- Body(JSON)：
  - `aweme_ids` (必填,array) Aweme Ids
- 示例：

```
aweme_ids = ["7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640"]
```

## 批量获取视频信息 V2

`POST /api/v1/douyin/app/v3/fetch_multi_video_v2`

- 用途：批量获取视频信息，支持图文、视频等，一次性最多支持50个视频，此接口收费固定价格为0.001$ * 50 = 0.05$一次
- 返回：作品数据
- 注意：If the interface returns empty, please use the same parameters to request the Web version interface. The specific response status code refers to:
- Body(JSON)：
  - `aweme_ids` (必填,array) Aweme Ids
- 示例：

```
aweme_ids = ["7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640", "7448118827402972455", "7126745726494821640"]
```

## 根据分享链接获取单个作品数据

`GET /api/v1/douyin/app/v3/fetch_one_video_by_share_url`

- 用途：根据分享链接获取单个作品数据
- 返回：作品数据
- 注意：If the interface returns empty, please use the same parameters to request the Web version interface. The specific response status code refers to:
- Query：
  - `share_url` (必填,string) 分享链接/Share link
- 示例：

```
share_url = "https://v.douyin.com/e3x2fjE/"
```

## 获取视频的最高画质播放链接

`GET /api/v1/douyin/app/v3/fetch_video_high_quality_play_url`

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

## 批量获取视频的最高画质播放链接

`POST /api/v1/douyin/app/v3/fetch_multi_video_high_quality_play_url`

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

## 根据视频ID获取作品的统计数据（点赞数、下载数、播放数、分享数）

`GET /api/v1/douyin/app/v3/fetch_video_statistics`

- 用途：根据视频ID获取作品的统计数据；抖音大多数接口已经不再返回作品的播放数，只能通过此接口获取；可以获取到的统计有：
- 返回：作品统计数据
- Query：
  - `aweme_ids` (必填,string) 作品id/Video id
- 示例：

```
aweme_ids = "7448118827402972455,7126745726494821640"
```

## 根据视频ID批量获取作品的统计数据（点赞数、下载数、播放数、分享数）

`GET /api/v1/douyin/app/v3/fetch_multi_video_statistics`

- 用途：根据视频ID获取作品的统计数据，支持多个视频id，一次性最多支持50个视频；抖音大多数接口已经不再返回作品的播放数，只能通过此接口获取；价格为：0.025$一次；可以获取到的统计有：
- 返回：作品统计数据
- Query：
  - `aweme_ids` (必填,string) 作品id/Video id
- 示例：

```
aweme_ids = "7448118827402972455,7126745726494821640"
```

## 获取指定用户的信息

`GET /api/v1/douyin/app/v3/handler_user_profile`

- 用途：获取指定用户的信息
- 返回：用户信息
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
- 示例：

```
sec_user_id = "MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"
```

## 获取用户粉丝列表

`GET /api/v1/douyin/app/v3/fetch_user_fans_list`

- 用途：获取用户粉丝列表
- 返回：粉丝列表
- Query：
  - `sec_user_id` (选填,string) 用户sec_user_id/User sec_user_id
  - `max_time` (选填,string) 最大时间戳/Maximum timestamp
  - `count` (选填,integer) 数量/Number
- 示例：

```
sec_user = "MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70"
max_time = "0"
count = 20
```

## 获取用户主页作品数据

`GET /api/v1/douyin/app/v3/fetch_user_post_videos`

- 用途：获取用户主页作品数据
- 返回：用户作品数据
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (选填,integer) 最大游标/Maximum cursor
  - `count` (选填,integer) 每页数量/Number per page
  - `sort_type` (选填,integer) 排序类型/Sort type
  - `channel` (选填,string) 抖音渠道版本/Douyin channel: normal(正常版-默认), lite(极速版)
- 示例：

```
sec_user_id = "MS4wLjABAAAANXSltcLCzDGmdNFI2Q_QixVTr67NiYzjKOIP5s03CAE"
max_cursor = 0
counts = 20
sort_type = 0
channel = "normal"
```

## 获取用户喜欢作品数据

`GET /api/v1/douyin/app/v3/fetch_user_like_videos`

- 用途：获取用户喜欢作品数据
- 返回：用户作品数据
- Query：
  - `sec_user_id` (必填,string) 用户sec_user_id/User sec_user_id
  - `max_cursor` (选填,integer) 最大游标/Maximum cursor
  - `counts` (选填,integer) 每页数量/Number per page
- 示例：

```
sec_user_id = "MS4wLjABAAAAW9FWcqS7RdQAWPd2AA5fL_ilmqsIFUCQ_Iym6Yh9_cUa6ZRqVLjVQSUjlHrfXY1Y"
max_cursor = 0
counts = 20
```

## 获取单个视频评论数据

`GET /api/v1/douyin/app/v3/fetch_video_comments`

- 用途：获取单个视频评论数据
- 返回：评论数据
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
  - `cursor` (选填,integer) 游标/Cursor
  - `count` (选填,integer) 数量/Number
- 示例：

```
aweme_id = "7448118827402972455"
cursor = 0
count = 20
```

## 获取指定视频的评论回复数据

`GET /api/v1/douyin/app/v3/fetch_video_comment_replies`

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

## 获取抖音视频合集详情数据

`GET /api/v1/douyin/app/v3/fetch_video_mix_detail`

- 用途：获取抖音视频合集详情数据
- 返回：视频合集详情数据
- Query：
  - `mix_id` (必填,string) 合集id/Mix id
- 示例：

```
mix_id = "7302011174286002217"
```

## 获取抖音视频合集作品列表数据

`GET /api/v1/douyin/app/v3/fetch_video_mix_post_list`

- 用途：获取抖音视频合集作品列表数据
- 返回：视频合集作品列表数据
- Query：
  - `mix_id` (必填,string) 合集id/Mix id
  - `cursor` (选填,integer) 游标/Cursor
  - `count` (选填,integer) 数量/Number
- 示例：

```
mix_id = "7302011174286002217"
cursor = 0
count = 20
```

## 获取用户短剧合集列表

`GET /api/v1/douyin/app/v3/fetch_user_series_list`

- 用途：获取用户的短剧合集列表
- 返回：用户短剧合集列表数据
- 注意：This interface returns all series collections published by the user; The series_id in the response can be used to get series details and video list
- Query：
  - `user_id` (选填,string) 用户id/User id
  - `sec_user_id` (选填,string) 用户加密id/User sec id
  - `cursor` (选填,integer) 游标/Cursor
- 示例：

```
user_id = "3010877781453635"
sec_user_id = "MS4wLjABAAAAfAU5kMk-W4569G1z2iRsy8t6-kOxO17Eaz6yte4NQokeUeOpeqTGEc480e34O8lK"
cursor = 0
```

## 获取短剧视频列表

`GET /api/v1/douyin/app/v3/fetch_series_video_list`

- 用途：获取短剧视频列表
- 返回：短剧视频列表数据
- 注意：This interface returns all video list in the series; The aweme_list in the response contains video information of each episode; The has_more field indicates whether there is more data
- Query：
  - `series_id` (必填,string) 短剧id/Series id
  - `cursor` (选填,integer) 游标/Cursor
- 示例：

```
series_id = "7592054624643713067"
cursor = 0
```

## 获取短剧详情信息

`GET /api/v1/douyin/app/v3/fetch_series_detail`

- 用途：获取短剧详情信息
- 返回：短剧详情数据
- 注意：This interface returns detailed information of the series, including:
- Query：
  - `series_id` (必填,string) 短剧id/Series id
- 示例：

```
series_id = "7592054624643713067"
```

## 获取指定音乐的详情数据

`GET /api/v1/douyin/app/v3/fetch_music_detail`

- 用途：获取指定音乐的详情数据
- 返回：音乐详情数据
- Query：
  - `music_id` (必填,string) 音乐id/Music id
- 示例：

```
music_id = "7136850194742315016"
```

## 获取指定音乐的视频列表数据

`GET /api/v1/douyin/app/v3/fetch_music_video_list`

- 用途：获取指定音乐的视频列表数据
- 返回：音乐视频列表数据
- Query：
  - `music_id` (必填,string) 音乐id/Music id
  - `cursor` (选填,integer) 游标/Cursor
  - `count` (选填,integer) 数量/Number
- 示例：

```
music_id = "7136850194742315016"
cursor = 0
count = 10
```

## 获取指定话题的详情数据

`GET /api/v1/douyin/app/v3/fetch_hashtag_detail`

- 用途：获取指定话题的详情数据
- 返回：话题详情数据
- Query：
  - `ch_id` (必填,integer) 话题id/Hashtag id
- 示例：

```
ch_id = 1575791821492238
```

## 获取指定话题的作品数据

`GET /api/v1/douyin/app/v3/fetch_hashtag_video_list`

- 用途：获取指定话题的作品数据
- 返回：话题作品数据
- Query：
  - `ch_id` (必填,string) 话题id/Hashtag id
  - `cursor` (选填,integer) 游标/Cursor
  - `sort_type` (选填,integer) 排序类型/Sort type
  - `count` (选填,integer) 数量/Number
- 示例：

```
ch_id = 1575791821492238
cursor = 0
sort_type = 0
count = 10
```

## 获取抖音热搜榜数据

`GET /api/v1/douyin/app/v3/fetch_hot_search_list`

- 用途：获取抖音热榜数据，包括：
- 返回：热搜榜数据
- Query：
  - `board_type` (选填,string) 榜单类型/Board type
  - `board_sub_type` (选填,string) 榜单子类型/Board sub type
- 示例：

```
- 获取热点榜数据
    - board_type = 0
    - board_sub_type = ""
- 获取种草榜数据
    - board_type = 2
    - board_sub_type = "seeding"
```

## 获取抖音直播热搜榜数据

`GET /api/v1/douyin/app/v3/fetch_live_hot_search_list`

- 用途：获取抖音直播热搜榜数据
- 返回：直播热搜榜数据
- 示例：

```
pass
```

## 获取抖音音乐榜数据

`GET /api/v1/douyin/app/v3/fetch_music_hot_search_list`

- 用途：获取抖音音乐热榜数据
- 返回：音乐热搜榜数据
- Query：
  - `chart_type` (选填,string) 榜单类型/Chart type
  - `cursor` (选填,string) 游标/Cursor
- 示例：

```
chart_type = "hot"
cursor = "0"
```

## 获取抖音品牌热榜分类数据

`GET /api/v1/douyin/app/v3/fetch_brand_hot_search_list`

- 用途：获取抖音品牌热榜分类数据
- 返回：品牌热搜榜分类数据
- 示例：

```
pass
```

## 获取抖音品牌热榜具体分类数据

`GET /api/v1/douyin/app/v3/fetch_brand_hot_search_list_detail`

- 用途：获取抖音品牌热榜具体分类数据
- 返回：品牌热搜榜具体分类数据
- Query：
  - `category_id` (必填,integer) 分类id/Category id
- 示例：

```
category_id = 10
```

## 生成抖音短链接

`GET /api/v1/douyin/app/v3/generate_douyin_short_url`

- 用途：生成抖音短链接
- 返回：短链接数据
- Query：
  - `url` (必填,string) 抖音链接/Douyin link
- 示例：

```
url = "https://www.douyin.com/passport/web/logout/"
```

## 生成抖音视频分享二维码

`GET /api/v1/douyin/app/v3/generate_douyin_video_share_qrcode`

- 用途：生成抖音视频分享二维码
- 返回：二维码数据
- Query：
  - `object_id` (必填,string) 作品id/Video id
- 示例：

```
object_id = "7348044435755846962"
```

## 抖音APP注册设备

`GET /api/v1/douyin/app/v3/register_device`

- 用途：抖音APP注册设备，获取设备信息以及设备的Cookie信息
- 返回：设备信息以及设备的Cookie信息
- Query：
  - `proxy` (选填,string) 代理/Proxy
- 示例：

```
proxy = "http://username:password@ip:port"

# [响应/Response]
```json
{
    "code": 200,
    "router": "/api/v1/douyin/app/v3/register_device",
    "params": {
        "proxy": "username:password@ip:port"
    },
    "data": {
        "iid": "3631064037200330",
        "device_id": "3631064037196234",
        "mssdk_token": "",
        "device_platform": "android",
        "channel": "xiaomi_64_1775",
        "version_code": 240900,
        "version_name": "24.9.0",
        "manifest_version_code": 240901,
        "update_version_code": 24909900,
        "device_type": "V1963A",
        "device_brand": "vivo",
        "device_model": "V1963A",
        "openudid": "5d736335afc17aab",
        "os_api": 29,
        "os_version": "10",
        "resolution": "2400x1080",
        "dpi": 480,
        "host_abi": "arm64-v8a",
        "ua": "com.ss.android.ugc.aweme/240901 (Linux; U; Android 10; zh_CN; V1963A; Build/compiler10301842;tt-ok/3.12.13.4-tiktok)",
        "cookies": {
            "install_id": "3631064037200330",
            "odin_tt": "5ef413aaa319b3a4077814a1da3d3e1bcec3e8640ddc3ad30945a8518f59d1563d24c3b7a3c59d97fbd5344f13208a25cf143312acf4462b028e56cd0b611cc3fc2a64318f7375470d6db86440f92841",
            "d_ticket": "42186c5b0c54ea1a2a9e02d4e62bf6ab",
            "store-region": "cn-js",
            "store-region-src": "did",
            "multi_sids": "462868309327184:38167255076198698951907954929873",
            "passport_csrf_token": "6f75287240634ad1f51f3b3bdcdb5424",
            "passport_csrf_token_default": "6f75287240634ad1f51f3b3bdcdb5424",
            "ttreq": "1$7f616210b41fc044b1f164542ac4e064288b5163"
        },
        "lanusk": "",
        "device_manufacturer": "vivo",
        "uuid": "357125675341697",
        "cdid": "f64372bf-4d1d-4883-bc8a-d3d6fa87a9e3",
        "first_launch_timestamp": 1726970498636,
        "x_tt_dt": "AAA2FGV24A2GAOHJJ3D3XCJ32IZDZ26XXKMQAOTDNUDWTB644ISU5YA3GBYVX2Y3XVOQ3ISDH3UA4JXGGNFXBLJ6AAZU7QTIBKHFYJLDJMDG5K36LVPBRCKLHW2XM",
        "BootTime": 1726980411,
        "MbTime": 1726780411,
        "server_time": 1726980500,
        "mc": "2A:66:7A:2D:8B:29",
        "rom": "compiler10301842",
        "rom_version": "PD1963-user 10 QP1A.190711.020 compiler10301842 release-keys"
    }
}
```
```

## 生成抖音分享链接，唤起抖音APP，跳转指定作品详情页

`GET /api/v1/douyin/app/v3/open_douyin_app_to_video_detail`

- 用途：生成抖音分享链接，唤起抖音APP，跳转指定作品详情页
- 返回：分享链接
- Query：
  - `aweme_id` (必填,string) 作品id/Video id
- 示例：

```
aweme_id = "7197598285882789120"
```

## 生成抖音分享链接，唤起抖音APP，跳转指定用户主页

`GET /api/v1/douyin/app/v3/open_douyin_app_to_user_profile`

- 用途：生成抖音分享链接，唤起抖音APP，跳转指定用户主页
- 返回：分享链接
- Query：
  - `uid` (必填,string) 用户id/User id
  - `sec_uid` (必填,string) 用户sec_uid/User sec_uid
- 示例：

```
uid = "96874812426"
sec_uid = "MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70"
```

## 生成抖音分享链接，唤起抖音APP，跳转指定关键词搜索结果

`GET /api/v1/douyin/app/v3/open_douyin_app_to_keyword_search`

- 用途：生成抖音分享链接，唤起抖音APP，跳转指定关键词搜索结果
- 返回：分享链接
- Query：
  - `keyword` (必填,string) 关键词/Keyword
- 示例：

```
keyword = "雷军"
```

## 生成抖音分享链接，唤起抖音APP，给指定用户发送私信

`GET /api/v1/douyin/app/v3/open_douyin_app_to_send_private_message`

- 用途：生成抖音分享链接，唤起抖音APP，给指定用户发送私信
- 返回：分享链接
- Query：
  - `uid` (必填,string) 用户id/User id
  - `sec_uid` (必填,string) 用户sec_uid/User sec_uid
- 示例：

```
uid = "96874812426"
sec_uid = "MS4wLjABAAAA9y04iBlVdeMQqTJbqsQZKb-tqWqWW29jPVJqideHT70"
```
