# Douyin Creator V2 API（创作者中心 V2）

文件夹 `Douyin-Creator-V2-API` · 14 个接口 · BASE `https://api.tikhub.io`

## 获取创作者账号诊断

`POST /api/v1/douyin/creator_v2/fetch_author_diagnosis`

- 用途：获取抖音创作者账号的诊断数据和优化建议
- 返回：返回账号诊断数据，包括以下五个核心维度：
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie

## 获取作品垂类标签

`POST /api/v1/douyin/creator_v2/fetch_item_analysis_involved_vertical`

- 用途：获取指定时间段内投稿作品涉及的垂类标签
- 返回：primary_verticals: 垂类标签列表
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYYMMDD)/Start date (format YYYYMMDD)
  - `end_date` (必填,string) 结束日期(格式YYYYMMDD)/End date (format YYYYMMDD)

## 获取投稿表现数据

`POST /api/v1/douyin/creator_v2/fetch_item_analysis_item_performance`

- 用途：获取投稿作品的表现数据，包括播放量、点赞量、评论量、分享量等指标
- 返回：包含所选指标在不同体裁和垂类下的表现数据
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYYMMDD)/Start date (format YYYYMMDD)
  - `end_date` (必填,string) 结束日期(格式YYYYMMDD)/End date (format YYYYMMDD)
  - `genres` (array,默认 [1, 2, 3, 4, 5, 8]) 体裁类型列表/Genres list: 1=1min以内视频, 2=1-3min视频, 3=3-5min视频, 4=5min+视频, 5=图文, 8=长图文
  - `primary_verticals` (必填,array) 垂类标签列表/Primary verticals list (从involved_vertical接口获取)
  - `metric_type` (integer,默认 1) 指标类型/Metric type: 1=播放量(Views), 2=点赞量(Likes), 3=评论量(Comments), 4=分享量(Shares)

## 获取投稿分析概览

`POST /api/v1/douyin/creator_v2/fetch_item_analysis_overview`

- 用途：获取账号投稿作品的综合分析数据
- 返回：包含不同体裁和垂类的投稿数据分析
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYYMMDD)/Start date (format YYYYMMDD)
  - `end_date` (必填,string) 结束日期(格式YYYYMMDD)/End date (format YYYYMMDD)
  - `genres` (array,默认 [1, 2, 3, 4, 5, 8]) 体裁类型列表/Genres list: 1=1min以内视频, 2=1-3min视频, 3=3-5min视频, 4=5min+视频, 5=图文, 8=长图文
  - `primary_verticals` (必填,array) 垂类标签列表/Primary verticals list (从involved_vertical接口获取)

## 获取作品观众其他数据分析

`POST /api/v1/douyin/creator_v2/fetch_item_audience_others`

- 用途：获取抖音作品的观众其他数据分析，包括受众分布和受众关注词
- 返回：**audience_distribution (受众分布)**:
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID

## 获取作品观众数据分析

`POST /api/v1/douyin/creator_v2/fetch_item_audience_portrait`

- 用途：获取抖音作品的观众数据分析
- 返回：返回作品的观众画像数据，包括以下维度：
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID

## 获取作品弹幕分析

`POST /api/v1/douyin/creator_v2/fetch_item_danmaku_analysis`

- 用途：获取抖音作品的弹幕分析数据
- 返回：返回作品的弹幕分析数据，包括：
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID

## 获取投稿作品列表

`POST /api/v1/douyin/creator_v2/fetch_item_list`

- 用途：获取指定时间范围内发布的所有投稿作品列表
- 返回：投稿作品列表数据，包含作品的详细指标信息
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `count` (integer,默认 10) 每页数量/Count per page (最多100条)
  - `order_by` (integer,默认 1) 排序方式/Order by (1-26): 1=发布时间↓(新到旧), 2=发布时间↑(旧到新), 3=播放量↓, 4=播放量↑, 5=点赞量↓, 6=点赞量↑, 7=评论量↓, 8=评论量↑, 9=分享量↓, 10=分享量↑, 11=收藏量↓, 12=收藏量↑, 13=2s跳出率↓, 14=2s跳出率↑, 15=5s完播率↓, 16=5s完播率↑, 17=完播率↓, 18=完播率↑, 19=封面点击率↓, 20=封面点击率↑, 21=平均播放时长↓, 22=平均播放时长↑, 23=主页访问量↓, 24=主页访问量↑, 25=粉丝增量↓, 26=粉丝增量↑
  - `fields` (string,默认 metrics,review,visibility) 需要返回的字段/Fields to return
  - `need_cooperation` (boolean,默认 True) 是否需要合作信息/Need cooperation info
  - `start_time` (必填,integer) 开始时间戳(毫秒)/Start time timestamp (milliseconds)
  - `end_time` (必填,integer) 结束时间戳(毫秒)/End time timestamp (milliseconds)
  - `need_long_article` (boolean,默认 True) 是否包含长图文/Include long articles
  - `cursor` 分页游标/Pagination cursor (可选)

## 导出投稿作品列表

`POST /api/v1/douyin/creator_v2/fetch_item_list_download`

- 用途：导出指定时间范围内前1000条投稿作品的详细数据
- 返回：**直接返回Excel文件流**，浏览器会自动下载
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `min_cursor` (必填,integer) 最小游标(开始时间戳,毫秒)/Min cursor (start timestamp in milliseconds)
  - `max_cursor` (必填,integer) 最大游标(结束时间戳,毫秒)/Max cursor (end timestamp in milliseconds)
  - `type_filters` (array,默认 [1, 2, 3, 4, 5, 8]) 体裁类型过滤/Type filters: 1=1min以内视频, 2=1-3min视频, 3=3-5min视频, 4=5min+视频, 5=图文, 8=长图文
  - `need_long_article` (boolean,默认 True) 是否包含长图文/Include long articles

## 获取作品总览数据

`POST /api/v1/douyin/creator_v2/fetch_item_overview_data`

- 用途：获取抖音作品总览数据，包括流量指标、审核状态、播放信息等
- 返回：作品总览数据，根据 fields 参数返回对应的字段内容
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `ids` (必填,string) 作品ID列表,多个ID用逗号分隔/Item IDs, separated by comma
  - `fields` (默认 metrics,review,play_info,dou_plus,integrated_incentive,incentive_life,content_analysis) 需要返回的字段,多个字段用逗号分隔/Fields to return, separated by comma. 可选值: metrics(指标),review(审核),play_info(播放信息),dou_plus(抖+),integrated_incentive(综合激励),incentive_life(激励生命周期),content_analysis(内容分析)

## 获取作品流量来源统计

`POST /api/v1/douyin/creator_v2/fetch_item_play_source`

- 用途：获取抖音作品的流量来源统计数据
- 返回：play_source: 流量来源列表，包含各渠道的播放占比
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID

## 获取作品搜索关键词统计

`POST /api/v1/douyin/creator_v2/fetch_item_search_keyword`

- 用途：获取抖音作品的搜索关键词统计数据
- 返回：返回用户搜索该作品时使用的关键词列表，包括：
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID

## 获取作品观看趋势分析

`POST /api/v1/douyin/creator_v2/fetch_item_watch_trend`

- 用途：获取抖音作品的观看趋势分析数据
- 返回：analysis_trend: 趋势分析数据
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID
  - `analysis_type` (integer,默认 1) 分析类型/Analysis type: 1=留存分析(Retention), 2=点赞分析(Like), 7=跳出分析(Bounce)

## 获取直播场次历史记录

`POST /api/v1/douyin/creator_v2/fetch_live_room_history_list`

- 用途：获取抖音创作者的直播场次历史记录
- 返回：返回直播场次历史记录列表，数据位于 `data.data.series` 数组中，每个场次包含以下信息：
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYY-MM-DD)/Start date (format YYYY-MM-DD)
  - `end_date` (必填,string) 结束日期(格式YYYY-MM-DD)/End date (format YYYY-MM-DD)
  - `limit` (integer,默认 400) 每页数量限制/Limit per page (最多400条)
  - `need_living` (integer,默认 1) 是否包含正在直播的场次/Include living rooms: 0=不包含, 1=包含
  - `download` (integer,默认 0) 是否下载/Download: 0=不下载, 1=下载
