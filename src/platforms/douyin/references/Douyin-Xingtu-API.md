# Douyin Xingtu API（星图 V1）

文件夹 `Douyin-Xingtu-API` · 32 个接口 · BASE `https://api.tikhub.io`

## 获取达人商业种草基础信息V1

`GET /api/v1/douyin/xingtu/author_commerce_seed_base_info_v1`

- 用途：获取达人商业种草的基础信息
- 返回：达人商业种草基础信息
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `_range` (string) 时间范围(可选)/Time Range (optional)

## 获取kol热词分析内容V1

`GET /api/v1/douyin/xingtu/author_content_hot_comment_keywords_v1`

- 返回：kol热词分析内容
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## 获取达人合同基础信息V1

`GET /api/v1/douyin/xingtu/author_contract_base_info_v1`

- 用途：获取达人合同的基础信息
- 返回：达人合同基础信息
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `_range` (string) 时间范围(可选)/Time Range (optional)

## 获取达人可见性状态V1

`GET /api/v1/douyin/xingtu/author_display_status_v1`

- 用途：查询达人在星图平台上的可见性状态（是否可被检索、可被下单等）
- 返回：达人可见性状态
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `platformChannel` (string,默认 _1) 平台渠道/Platform Channel

## 获取达人主页视频列表V1

`GET /api/v1/douyin/xingtu/author_homepage_videos_v1`

- 用途：获取星图达人主页的视频列表
- 返回：视频列表数据，包含:
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu author ID
  - `page` (integer,默认 1) 页码，从1开始，每页20条/Page number, starts from 1, 20 items per page
  - `videoType` (string,默认 ALL) 流量类型：ALL/PERSONAL/XINGTU / Traffic type: ALL/PERSONAL/XINGTU
  - `onlyAssign` (boolean,默认 False) 是否仅返回指派视频/Only return assigned videos
  - `keyword` (string) 视频标题关键词筛选(可选)/Filter by video title keyword (optional)
  - `startDate` (string) 起始日期(可选), 格式 yyyyMMdd/Start date (optional), format yyyyMMdd
  - `endDate` (string) 结束日期(可选), 格式 yyyyMMdd/End date (optional), format yyyyMMdd

## 获取kol热词分析评论V1

`GET /api/v1/douyin/xingtu/author_hot_comment_tokens_v1`

- 返回：kol热词分析评论
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## 获取达人直播统计V1

`GET /api/v1/douyin/xingtu/author_live_statistics_v1`

- 用途：获取达人的直播统计数据
- 返回：达人直播统计数据
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `liveType` (string) 直播类型(可选)/Live Type (optional)
  - `period` (string) 时间范围(可选)/Time Period (optional)
  - `onlyStarOrder` (string) 是否仅星图订单(可选)/Only Xingtu orders (optional)
  - `flowType` (string) 流量类型(可选)/Flow Type (optional)

## 获取达人直播观看分布V1

`GET /api/v1/douyin/xingtu/author_live_watch_distribution_v1`

- 用途：获取达人直播的观看人群分布
- 返回：达人直播观看人群分布
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `liveCrowdType` (string) 人群类型(可选)/Live Crowd Type (optional)
  - `liveType` (string) 直播类型(可选)/Live Type (optional)

## 获取达人接单经验V1

`GET /api/v1/douyin/xingtu/author_order_experience_v1`

- 用途：获取达人在星图平台的接单经验数据（合作品牌、接单量等）
- 返回：达人接单经验
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `period` (string,默认 DAY_30) 时间范围/Time Period

## 获取达人渠道指标V1

`GET /api/v1/douyin/xingtu/author_platform_channel_info_v1`

- 用途：获取达人在指定平台渠道下的指标概况
- 返回：达人渠道指标
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `platformChannel` (string,默认 _1) 平台渠道/Platform Channel

## 获取达人侧基础信息V1

`GET /api/v1/douyin/xingtu/author_side_base_info_v1`

- 用途：获取达人侧的基础信息
- 返回：达人侧基础信息
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID

## 获取达人标签V1

`GET /api/v1/douyin/xingtu/author_tags_v1`

- 用途：获取达人的标签信息（内容标签、人设标签等）
- 返回：达人标签
- Query：
  - `starAuthorId` (必填,string) 星图达人ID/Xingtu Author ID

## 获取加密图片解析

`GET /api/v1/douyin/xingtu/get_sign_image`

- 用途：解析星图加密图片，获取可访问的图片URL
- 返回：解析后的图片数据，包含可访问的图片URL
- Query：
  - `uri` (必填,string) 图片的uri/Image URI
  - `durationTS` (integer,默认 86400) 有效期时长（秒）/Duration in seconds
  - `format` (string,默认 webp) 图片格式/Image format

## 根据抖音sec_user_id获取游客星图kolid

`GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_sec_user_id`

- 用途：通过抖音sec_user_id获取游客星图kolid
- 返回：游客星图kolid
- Query：
  - `sec_user_id` (必填,string) 抖音用户sec_user_id/Douyin User sec_user_id

## 根据抖音用户ID获取游客星图kolid

`GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_uid`

- 用途：通过抖音用户ID获取游客星图kolid
- 返回：游客星图kolid
- Query：
  - `uid` (必填,string) 抖音用户ID/Douyin User ID

## 根据抖音号获取游客星图kolid

`GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_unique_id`

- 用途：通过抖音号获取游客星图kolid
- 返回：游客星图kolid
- Query：
  - `unique_id` (必填,string) 抖音号/Douyin User unique_id

## 获取kol观众画像V1

`GET /api/v1/douyin/xingtu/kol_audience_portrait_v1`

- 返回：kol观众画像
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## 获取kol基本信息V1

`GET /api/v1/douyin/xingtu/kol_base_info_v1`

- 返回：kol基本信息
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `platformChannel` (必填,string) 平台渠道/Platform Channel

## 获取kol转化能力分析V1

`GET /api/v1/douyin/xingtu/kol_conversion_ability_analysis_v1`

- 返回：kol转化能力分析
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `_range` (必填,string) 时间范围/Time Range

## 获取kol转化视频展示V1

`GET /api/v1/douyin/xingtu/kol_convert_video_display_v1`

- 返回：kol转化视频展示
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `detailType` (必填,string) 详情类型/Detail Type
  - `page` (必填,integer) 页码/Page

## 获取kol性价比能力分析V1

`GET /api/v1/douyin/xingtu/kol_cp_info_v1`

- 返回：kol性价比能力分析
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## 获取kol粉丝趋势V1

`GET /api/v1/douyin/xingtu/kol_daily_fans_v1`

- 返回：kol粉丝趋势
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `startDate` (必填,string) 开始日期/Start Date
  - `endDate` (必填,string) 结束日期/End Date

## 获取kol数据概览V1

`GET /api/v1/douyin/xingtu/kol_data_overview_v1`

- 返回：kol数据概览
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `_type` (必填,string) 类型/Type
  - `_range` (必填,string) 范围/Range
  - `flowType` (必填,integer) 流量类型/Flow Type
  - `onlyAssign` (boolean) 是否指派/Whether assigned (optional)

## 获取kol粉丝画像V1

`GET /api/v1/douyin/xingtu/kol_fans_portrait_v1`

- 返回：kol粉丝画像
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `fansType` (string,默认 _1) 粉丝类型/Fans Type

## 获取kol连接用户V1

`GET /api/v1/douyin/xingtu/kol_link_struct_v1`

- 返回：kol连接用户
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## 获取kol内容表现V1

`GET /api/v1/douyin/xingtu/kol_rec_videos_v1`

- 返回：kol内容表现
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## 获取kol服务报价V1

`GET /api/v1/douyin/xingtu/kol_service_price_v1`

- 返回：kol服务报价
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `platformChannel` (必填,string) 平台渠道/Platform Channel

## 获取kol连接用户来源V1

`GET /api/v1/douyin/xingtu/kol_touch_distribution_v1`

- 返回：kol连接用户来源
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## 获取kol视频表现V1

`GET /api/v1/douyin/xingtu/kol_video_performance_v1`

- 返回：kol视频表现
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `onlyAssign` (必填,boolean) 是否只显示分配作品/Whether to display only assigned works

## 获取kol星图指数V1

`GET /api/v1/douyin/xingtu/kol_xingtu_index_v1`

- 返回：kol星图指数
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId

## [已废弃]关键词搜索kol V1

`GET /api/v1/douyin/xingtu/search_kol_v1`

- 用途：关键词搜索kol V1
- 返回：kol列表
- Query：
  - `keyword` (必填,string) 关键词/Keyword
  - `platformSource` (必填,string) 平台来源/Platform Source
  - `page` (必填,integer) 页码/Page

## 高级搜索kol V2

`GET /api/v1/douyin/xingtu/search_kol_v2`

- 用途：高级搜索kol V2，支持粉丝范围和内容标签筛选
- 返回：kol列表（支持高级筛选）
- Query：
  - `keyword` (必填,string) 关键词/Keyword
  - `followerRange` (string) 粉丝范围(可选)/Follower Range (optional), 例如 10-100 表示10万-100万粉丝
  - `contentTag` (string) 内容标签(可选)/Content Tag (optional), 例如 tag-1 或 tag_level_two-7
  - `page` (string) 页码(可选)/Page (optional)
  - `sort` (string) 排序方式(可选)/Sort order (optional)
  - `searchType` (string) 搜索类型(可选)/Search type (optional)
  - `marketingTarget` (string) 营销目标(可选)/Marketing target (optional)
  - `industry` (string) 所属行业(可选)/Industry (optional)
  - `isSuperstar` (string) 是否明星(可选)/Whether superstar (optional)
  - `kolPriceType` (string) 报价类型(可选)/KOL price type (optional)
  - `kolPriceRange` (string) 报价区间(可选)/KOL price range (optional)
  - `contentTheme` (string) 内容主题(可选)/Content theme (optional)
  - `personaTag` (string) 人设标签(可选)/Persona tag (optional)
  - `gender` (string) 达人性别(可选)/Author gender (optional)
  - `location` (string) 达人地域(可选)/Author location (optional)
  - `tonalityTag` (string) 内容调性标签(可选)/Tonality tag (optional)
  - `connectedUserRange` (string) 连接人数区间(可选)/Connected user range (optional)
  - `audienceImage` (string) 观众画像筛选(可选)/Audience image (optional)
  - `fansImage` (string) 粉丝画像筛选(可选)/Fans image (optional)
  - `expectedPlayRange` (string) 预期播放区间(可选)/Expected play range (optional)
  - `expectedCpmRange` (string) 预期CPM区间(可选)/Expected CPM range (optional)
  - `expectedCpeRange` (string) 预期CPE区间(可选)/Expected CPE range (optional)
  - `interactionRateRange` (string) 互动率区间(可选)/Interaction rate range (optional)
  - `completionRateRange` (string) 完播率区间(可选)/Completion rate range (optional)
  - `viralRateRange` (string) 爆款率区间(可选)/Viral rate range (optional)
  - `progressTaskRange` (string) 在途任务数区间(可选)/In-progress task range (optional)
  - `isCuratedAuthor` (string) 是否精选达人(可选)/Whether curated author (optional)
  - `authorList` (string) 指定达人列表(可选)/Specific author list (optional)
