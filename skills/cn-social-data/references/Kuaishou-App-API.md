# Kuaishou App API

文件夹 `Kuaishou-App-API` · 26 个接口
说明：快手App数据接口


## 视频详情V1

`GET /api/v1/kuaishou/app/fetch_one_video`

- 用途：获取单个作品数据接口 V1
- 返回：视频数据
- Query：
  - `photo_id` (必填,string)
- 示例：

```
photo_id = "3xhpk3xcf6e4iac"
photo_id = "5246975215478907538"
```
- 返回结构（实测）：
  - `data` 是对象（3 个字段）：`result`, `photos`, `host-name`
  - `data.photos` 是数组（长度 1）；首元素字段：`longVideo`, `supportType`, `coronaVipInfo`, `enableCoronaViewLater`, `canShowQuickCommentGuide`, `showSpecialFollowIcon`, `danmakuInfo`, `inputPromptGuide`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 快手批量视频查询接口

`GET /api/v1/kuaishou/app/fetch_videos_batch`

- 用途：批量获取多个作品数据，单次请求最多支持40个视频ID；如果此接口连续请求失败，可以尝试使用价格更昂贵的V2接口进行冗余请求；此接口收费标准默认为：40 * 0.001 = 0.04 美元/次
- 返回：视频数据列表
- Query：
  - `photo_ids` (必填,string) 多个作品ID用逗号分隔，单次最多40个/Multiple photo IDs separated by commas, max 40 per request
- 示例：

```
photo_ids = "5228960823332207296,5196309727975443273,5222486898325987583"
```

## 根据链接获取单个作品数据

`GET /api/v1/kuaishou/app/fetch_one_video_by_url`

- 用途：根据链接获取单个作品数据
- 返回：视频数据
- Query：
  - `share_text` (必填,string)
- 示例：

```
share_text = "https://v.kuaishou.com/cNYP0Z"
```

## 精选/推荐Feed流

`GET /api/v1/kuaishou/app/fetch_selection_feed`

- 用途：获取 App 首页「精选 / 推荐」频道的推荐作品流；推荐流无游标翻页，想要更多内容直接再次调用即可（结果随推荐策略变化，不保证顺序与去重）
- 返回：推荐作品流数据

## 生成快手分享链接

`GET /api/v1/kuaishou/app/generate_kuaishou_share_link`

- 用途：生成快手分享链接
- 返回：分享链接
- Query：
  - `shareObjectId` (必填,string)
- 示例：

```
shareObjectId = "3xg5wjqdtekbb3u"
```

## 获取单个作品评论数据

`GET /api/v1/kuaishou/app/fetch_video_comment`

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

## 评论二级回复

`GET /api/v1/kuaishou/app/fetch_video_sub_comments`

- 用途：获取某条一级评论（楼主评论）下的二级回复列表，使用游标分页
- 返回：二级回复列表数据
- Query：
  - `photo_id` (必填,string)
  - `root_comment_id` (必填,string)
  - `pcursor` (选填,string) 首页留空，翻页传上一页响应的 pcursor
  - `count` (选填,integer) 默认 8，范围 1-20

## 获取单个用户数据V2

`GET /api/v1/kuaishou/app/fetch_one_user_v2`

- 用途：获取单个用户数据 V2；此接口收费较贵，但稳定性更高，具体价格请在用户后台查看价格表
- 返回：用户数据
- Query：
  - `user_id` (必填,string)
- 示例：

```
user_id = "3xz63mn6fngqtiq"
```

## 用户视频列表V2

`GET /api/v1/kuaishou/app/fetch_user_post_v2`

- 用途：用户视频列表 V2；此接口收费较贵，但稳定性更高，具体价格请在用户后台查看价格表
- 返回：视频数据
- Query：
  - `user_id` (必填,string)
  - `pcursor` (选填,string) 第一次请求留空，后续传上一页响应的 pcursor
  - `sort` (选填,string) latest(最新, 默认) / hot(热门)
- 示例：

```
user_id = "903511772"
pcursor = ""
sort = "latest"
```

## 获取用户热门作品数据

`GET /api/v1/kuaishou/app/fetch_user_hot_post`

- 用途：获取用户热门作品数据
- 返回：作品数据
- Query：
  - `user_id` (必填,string)
  - `pcursor` (选填,string)
- 示例：

```
user_id = "228905802"
pcursor = None
```

## 获取用户直播信息

`GET /api/v1/kuaishou/app/fetch_user_live_info`

- 用途：获取用户直播信息
- 返回：直播信息
- Query：
  - `user_id` (必填,string)
- 示例：

```
user_id = "1377082950"
```

## 综合搜索

`GET /api/v1/kuaishou/app/search_comprehensive`

- 用途：快手综合搜索接口，支持搜索视频、用户等内容，并提供多维度筛选功能
- 返回：搜索结果数据
- Query：
  - `keyword` (必填,string)
  - `pcursor` (选填,string)
  - `sort_type` (选填,string) 可选值: all(综合排序), newest(最新发布), most_likes(最多点赞)
  - `publish_time` (选填,string) 可选值: all(全部), one_day(近一日), one_week(近一周), one_month(近一月)
  - `duration` (选填,string) 可选值: all(全部), under_1_min(1分钟以内), 1_to_5_min(1-5分钟), over_5_min(5分钟以上)
- 示例：

```
keyword = "汽车之家"
sort_type = "most_likes"
publish_time = "one_week"
```

## 搜索视频V2

`GET /api/v1/kuaishou/app/search_video_v2`

- 用途：搜索视频 V2；此接口收费较贵，但稳定性更高，具体价格请在用户后台查看价格表
- 返回：视频数据
- Query：
  - `keyword` (必填,string)
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor / Empty for first page, pass pcursor from previous response
- 示例：

```
keyword = "人工智能"
pcursor = ""
```
- 返回结构（实测）：
  - `data` 是对象（14 个字段）：`portalFlag`, `recoPcursor`, `host-name`, `jumpToSlideMode`, `ussid`, `mixFeeds`, `extParams`, `pcursor`, `recoInterestFlag`, `result`, `responseCode`, `llsid`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 搜索用户V2

`GET /api/v1/kuaishou/app/search_user_v2`

- 用途：搜索用户 V2；此接口收费较贵，但稳定性更高，具体价格请在用户后台查看价格表
- 返回：用户数据
- Query：
  - `keyword` (必填,string)
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor / Empty for first page
  - `user_relation` (选填,string) all / same_city / verified / live / following
  - `user_gender` (选填,string) all / male / female
  - `fans_sort` (选填,string) default / most_to_least / least_to_most
- 示例：

```
keyword = "人工智能"
pcursor = ""
```

## 搜索图片作品

`GET /api/v1/kuaishou/app/search_image`

- 用途：关键词搜索图片作品，使用游标分页
- 返回：图片作品搜索结果
- Query：
  - `keyword` (必填,string)
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor

## 搜索直播间

`GET /api/v1/kuaishou/app/search_live`

- 用途：关键词搜索正在直播的直播间，使用游标分页
- 返回：直播间搜索结果
- Query：
  - `keyword` (必填,string)
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor

## 搜索音乐

`GET /api/v1/kuaishou/app/search_music`

- 用途：关键词搜索音乐（歌曲名 / 歌手 / 关键词），使用游标分页
- 返回：音乐搜索结果
- Query：
  - `keyword` (必填,string)
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor

## 搜索话题标签

`GET /api/v1/kuaishou/app/search_tag`

- 用途：关键词搜索话题标签（hashtag），结果在 tags[] 中。可配合 /fetch_tag_feed 翻该标签内容流
- 返回：话题标签搜索结果
- Query：
  - `keyword` (必填,string)
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor

## 话题标签聚合页

`GET /api/v1/kuaishou/app/fetch_tag_feed`

- 用途：话题标签聚合页：给定标签，返回标签信息(tagInfo) + 关联作品流(mixFeeds[])。hashtag 页有 4 个子 tab
- 返回：标签信息 + 作品流数据
- Query：
  - `general_tag_id` (必填,string) 话题标签传标签名或 search_tag 的数字 id；声音标签传编码串
  - `tab` (选填,string) hot(最热门) / latest(最新发布) / image(图片) / live(直播)
  - `tag_name` (选填,string) 话题标签建议传，等于标签名
  - `tag_type` (选填,integer) 1=话题标签，29=声音/音乐标签
  - `tag_source` (选填,integer) 2=搜索进入话题页，3=作品页声音标签
  - `from_photo_id` (选填,string) 进入标签页的源作品 photoId（可选）
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor

## 快手直播榜单

`GET /api/v1/kuaishou/app/fetch_live_top_list`

- 用途：快手直播榜单
- 返回：榜单数据
- Query：
  - `subTabId` (选填,integer)
  - `subTabName` (选填,string)
- 示例：

```
subTabId = 0
subTabName = None
```

## 快手热榜分类

`GET /api/v1/kuaishou/app/fetch_hot_board_categories`

- 用途：快手热榜分类
- 返回：分类数据
- 返回结构（实测）：
  - `data` 是对象（4 个字段）：`result`, `boards`, `location`, `host-name`
  - `data.boards` 是数组（长度 5）；首元素字段：`type`, `boardId`, `boardName`, `bannerIconUrl`, `bannerLinkUrl`, `backgroundUrl`, `darkBackgroundUrl`, `shareTitle`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 快手热榜详情

`GET /api/v1/kuaishou/app/fetch_hot_board_detail`

- 用途：快手热榜详情
- 返回：详情数据
- Query：
  - `boardType` (选填,integer)
  - `boardId` (选填,integer)
- 示例：

```
boardType = 1
boardId = 1
```

## 快手热搜人物榜单

`GET /api/v1/kuaishou/app/fetch_hot_search_person`

- 用途：快手热搜人物榜单
- 返回：榜单数据

## 快手购物榜单

`GET /api/v1/kuaishou/app/fetch_shopping_top_list`

- 用途：快手购物榜单
- 返回：榜单数据
- Query：
  - `subTabId` (选填,integer)
  - `subTabName` (选填,string)
- 示例：

```
subTabId = 0
subTabName = None
```

## 快手品牌榜单

`GET /api/v1/kuaishou/app/fetch_brand_top_list`

- 用途：快手品牌榜单
- 返回：榜单数据
- Query：
  - `subTabId` (选填,integer)
  - `subTabName` (选填,string)
- 示例：

```
subTabId = 0
subTabName = None
```

## 音乐榜单

`GET /api/v1/kuaishou/app/fetch_music_ranking`

- 用途：获取音乐榜单（歌曲列表，结果在 musics[]），使用游标分页
- 返回：音乐榜单数据
- Query：
  - `tab_id` (选填,integer) 100002=热歌榜（默认），100063=π计划推荐榜
  - `count` (选填,integer) 默认 20，范围 1-50
  - `pcursor` (选填,string) 首次留空，翻页传上一页响应的 pcursor
