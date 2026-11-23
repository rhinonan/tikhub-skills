# Kuaishou Web API

文件夹 `Kuaishou-Web-API` · 12 个接口
说明：快手Web数据接口


## 获取单个作品数据 V1

`GET /api/v1/kuaishou/web/fetch_one_video`

- 用途：获取单个作品数据，此接口不支持图文作品
- 返回：视频数据
- Query：
  - `share_text` (必填,string)
- 示例：

```
share_text = "https://www.kuaishou.com/f/X-f2k5KJpiXN1SY"
```

## 获取单个作品数据 V2

`GET /api/v1/kuaishou/web/fetch_one_video_v2`

- 用途：快手单一视频查询接口V2
- 返回：视频数据
- Query：
  - `photo_id` (必填,string)
- 示例：

```
photo_id = "3xtdqvdnqd3psuc"
```

## 链接获取作品数据

`GET /api/v1/kuaishou/web/fetch_one_video_by_url`

- 用途：根据链接获取单个作品数据
- 返回：视频数据
- Query：
  - `url` (必填,string)
- 示例：

```
url = "https://v.kuaishou.com/GKTpYm"
```

## 获取作品一级评论

`GET /api/v1/kuaishou/web/fetch_one_video_comment`

- 用途：获取单个作品评论数据
- 返回：评论数据
- Query：
  - `photo_id` (必填,string)
  - `pcursor` (选填,string)
- 示例：

```
photo_id = "3x7gxp2zhgjv832"
pcursor = None
```

## 获取作品二级评论

`GET /api/v1/kuaishou/web/fetch_one_video_sub_comment`

- 用途：获取单个作品二级评论数据
- 返回：评论数据
- Query：
  - `photo_id` (必填,string)
  - `pcursor` (选填,string)
  - `root_comment_id` (必填,string)
- 示例：

```
photo_id = "3xgarycnydawq3g"
pcursor = "909377053156"
root_comment_id = "908850553827"
```

## 生成分享短连接

`GET /api/v1/kuaishou/web/generate_share_short_url`

- 用途：生成分享短连接
- 返回：短连接
- Query：
  - `photo_id` (必填,string)
- 示例：

```
body = {
    "photo_id": "3xtdqvdnqd3psuc"
}

# [返回示例/Example Response]
```json
{
  "code": 200,
  "request_id": "3fe5f6dc-e88c-4915-a6fa-2a63a2743342",
  "router": "/api/v1/kuaishou/web/generate_share_short_url",
  "params": {
    "photo_id": "3xtdqvdnqd3psuc"
  },
  "data": {
    "result": 1,
    "hostName": "public-bjzey-rs6-kce-node1155.idchb1az3.hb1.kwaidc.com",
    "cache-scope": "nocache",
    "error_msg": null,
    "max-age": 0,
    "share": {
      "shareMethod": "TOKEN",
      "shareMethodType": null,
      "shareChannel": "COPY_LINK",
      "shareMode": "APP",
      "kpn": "KUAISHOU",
      "subBiz": "BROWSE_SLIDE_PHOTO",
      "appName": "as",
      "appIconUrl": "https://static.yximgs.com/udata/pkg/ks-share-sdk/cardlogonew.png",
      "shareObject": {
        "copylinkSuccessTips": "链接复制成功，快去分享给朋友吧",
        "shareMessage": "https://v.kuaishou.com/KDh1s1j1 上一秒他是市民，下一秒他是市长 大哥突如其来的专业，让人笑不活了。"搞笑 "非物质文化遗产 "...更多",
        "kwaiToken": "X8hIM7myjQen2bi",
        "shareId": "18546252276277",
        "shareObjectId": "3xtdqvdnqd3psuc",
        "shareResourceType": "PHOTO_OTHER",
        "shortLink": "https://v.kuaishou.com/KDh1s1j1"
      },
      "extParams": {
        "shareMode": "app",
        "tokenExtParams": "{}",
        "expTag": "1_i/0_unknown0",
        "shareMethod": "token",
        "useMmuTitle": false,
        "logExt": "{"expTag":"1_i/0_unknown0","trendingType":""}",
        "templateStyle": "",
        "shareInfoWrap": "{"shareTitleInfo":{"title":"分享一个作品给你","subTitle":"推荐你看这个视频"},"shareId":"18546252276277","docId":9,"groupName":"","shareType":"PHOTO_OTHER","coverUrlKey":null,"coverUrl":null,"tagType":null,"webShareVerifyData":null}",
        "battleTemplateId": "",
        "templateGenerationType": ""
      }
    },
    "host-name": "public-bjzey-rs6-kce-node1155.idchb1az3.hb1.kwaidc.com"
  }
}
```
```

## 获取用户信息

`GET /api/v1/kuaishou/web/fetch_user_info`

- Query：
  - `user_id` (必填,string)
- 示例：

```
user_id = "3xz63mn6fngqtiq"

    # [返回示例/Example Response]
    ```json
    {
        "code": 200,
        "request_id": "782e6fa2-4c8e-4fac-b151-78db03c10b8d",
        "router": "/api/v1/kuaishou/web/fetch_user_info",
        "params": {
            "user_id": "3xz63mn6fngqtiq"
        },
        "data": {
            "result": 1,
            "userProfile": {
                "profile": {
                    "user_profile_bg_url": "//s2-10623.kwimgs.com/kos/nlav10623/vision_images/profile_background.5bc08b1bf4fba1f4.svg",
                    "user_id": "3xz63mn6fngqtiq",
                    "user_name": "权少爱吃小汉堡🍔",
                    "headurl": "https://p66-pro.a.yximgs.com/uhead/AB/2025/08/11/21/BMjAyNTA4MTEyMTEyNDlfMjI4OTA1ODAyXzFfaGQ5ODdfODg4_s.jpg",
                    "user_text": "感谢你的关注木木哒 我玩得游戏叫:Gmod

禁止冒充搬运视频 违者必究"
                },
                "gender": "M",
                "showCollectTab": false,
                "livingInfo": {
                    "living": false,
                    "livingId": null,
                    "iconType": 0
                },
                "ownerCount": {
                    "fan": 4300985,
                    "like": 37676016,
                    "follow": 198,
                    "photo_public": 237
                },
                "userDefineId": "quanshaogmod",
                "isFollowing": false,
                "isUserIsolated": false
            },
            "host-name": "public-bjzey-c3-kce-node67.idchb1az3.hb1.kwaidc.com"
        }
    }
    ```
```

## 获取用户直播回放

`GET /api/v1/kuaishou/web/fetch_user_live_replay`

- 用途：获取用户直播回放列表
- 返回：用户直播回放列表
- Query：
  - `user_id` (必填,string)
  - `pcursor` (选填,string)
- 示例：

```
user_id = "3xz63mn6fngqtiq"
pcursor = None

# [返回示例/Example Response]
```json

```
```

## 获取用户收藏作品

`GET /api/v1/kuaishou/web/fetch_user_collect`

- 用途：获取用户收藏作品
- 返回：用户收藏作品列表
- Query：
  - `user_id` (必填,string)
  - `pcursor` (选填,string)
- 示例：

```
user_id = "3xz63mn6fngqtiq"
pcursor = None

# [返回示例/Example Response]
```json

```
```

## 获取快手热榜 V1

`GET /api/v1/kuaishou/web/fetch_kuaishou_hot_list_v1`

- 用途：获取快手热榜 V1
- 返回：快手热榜 V1 列表
- 示例：

```
# [返回示例/Example Response]
```json

```
```
- 返回结构（实测）：
  - ⚠️ 实测失败：HTTP 400（None）

## 获取快手热榜 V2

`GET /api/v1/kuaishou/web/fetch_kuaishou_hot_list_v2`

- 用途：获取快手热榜 V2
- 返回：快手热榜 V2 列表
- Query：
  - `board_type` (选填,string)
- 示例：

```
# [返回示例/Example Response]
```json

```
```

## 获取用户ID

`GET /api/v1/kuaishou/web/fetch_get_user_id`

- 用途：通过用户分享链接获取用户ID
- 返回：用户ID
- Query：
  - `share_link` (必填,string)
- 示例：

```
share_link = "https://v.kuaishou.com/KcdKDwFp"

share_link = "https://c.kuaishou.com/fw/user/3xcuu5habgc8z29"

share_link = "https://live.kuaishou.com/profile/3xcuu5habgc8z29?fid=2357689552&cc=share_copylink"

# [返回示例/Example Response]
```json
```
```
