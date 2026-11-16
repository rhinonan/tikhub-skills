# Douyin Billboard API（榜单/热点）

文件夹 `Douyin-Billboard-API` · 31 个接口 · BASE `https://api.tikhub.io`

## 获取中国城市列表

`GET /api/v1/douyin/billboard/fetch_city_list`

- 用途：获取城市列表
- 返回：中国城市列表

## 获取垂类内容标签

`GET /api/v1/douyin/billboard/fetch_content_tag`

- 返回：垂类内容标签

## 获取粉丝兴趣作者 20个用户

`GET /api/v1/douyin/billboard/fetch_hot_account_fans_interest_account_list`

- 返回：粉丝兴趣作者 20个用户
- Query：
  - `sec_uid` (必填,string) 用户sec_id

## 获取粉丝近3天搜索词 10个搜索词

`GET /api/v1/douyin/billboard/fetch_hot_account_fans_interest_search_list`

- 返回：粉丝近3天搜索词 10个搜索词
- Query：
  - `sec_uid` (必填,string) 用户sec_id

## 获取粉丝近3天感兴趣的话题 10个话题

`GET /api/v1/douyin/billboard/fetch_hot_account_fans_interest_topic_list`

- 返回：粉丝近3天感兴趣的话题 10个话题
- Query：
  - `sec_uid` (必填,string) 用户sec_id

## 获取粉丝画像

`GET /api/v1/douyin/billboard/fetch_hot_account_fans_portrait_list`

- 返回：粉丝画像
- Query：
  - `sec_uid` (必填,string) 用户sec_id
  - `option` (integer,默认 1) 选项，1 手机价格分布 2 性别分布 3 年龄分布 4 地域分布-省份 5 地域分布-城市 6 城市等级 7 手机品牌分布 8 兴趣标签分析 百分比

## 获取账号作品分析-上周

`GET /api/v1/douyin/billboard/fetch_hot_account_item_analysis_list`

- 用途：获取账号作品分析
- 返回：账号作品分析
- Query：
  - `sec_uid` (必填,string) 用户sec_id

## 获取热门账号

`POST /api/v1/douyin/billboard/fetch_hot_account_list`

- 返回：热门账号
- Body(JSON)：
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 24/72/168，代表近1天/近3天/近7天，默认24
  - `page_num` (integer,默认 1) 页码，默认1
  - `page_size` (integer,默认 10) 每页数量，默认10
  - `query_tag` 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"date_window": 24, "page_num": 1, "page_size": 10, "query_tag": {"value": 628, "children": [{"value": 62808}, {"value": 62804}]}}`

## 搜索用户名或抖音号

`GET /api/v1/douyin/billboard/fetch_hot_account_search_list`

- 用途：获取搜索用户名或抖音号
- 返回：搜索结果
- Query：
  - `keyword` (必填,string) 搜索的用户名或抖音号
  - `cursor` (必填,integer) 游标，默认空

## 获取账号粉丝数据趋势

`GET /api/v1/douyin/billboard/fetch_hot_account_trends_list`

- 返回：账号粉丝数据趋势
- Query：
  - `sec_uid` (必填,string) 用户sec_id
  - `option` (integer,默认 2) 选项，2 新增点赞量 3 新增作品量 4 新增评论量 5 新增分享量
  - `date_window` (integer,默认 24) 数据点粒度(小时)，可选 1/24，代表每小时一个点/每天一个点，默认24

## 获取活动日历详情

`GET /api/v1/douyin/billboard/fetch_hot_calendar_detail`

- 返回：活动日历详情
- Query：
  - `calendar_id` (必填,string) 活动id

## 获取活动日历

`POST /api/v1/douyin/billboard/fetch_hot_calendar_list`

- 返回：活动日历
- Body(JSON)：
  - `city_code` (string) 城市编码，从城市列表获取，空为全部
  - `category_code` (string) 热点榜分类编码，从热点榜分类获取，空为全部
  - `end_date` (integer,默认 1735488000) 快照结束时间 格式10位时间戳
  - `start_date` (integer,默认 1734902400) 快照开始时间 格式10位时间戳

## 获取热点榜分类

`GET /api/v1/douyin/billboard/fetch_hot_category_list`

- 用途：获取热点榜分类的id与热度
- 返回：热点榜分类
- Query：
  - `billboard_type` (必填,string) 榜单类型
  - `snapshot_time` (string,默认 20250106151500) 快照时间 格式yyyyMMddHHmmss
  - `start_date` (string) 快照开始时间 格式yyyyMMdd
  - `end_date` (string) 快照结束时间 格式yyyyMMdd
  - `keyword` (string) 热点搜索词

## 获取挑战热榜

`GET /api/v1/douyin/billboard/fetch_hot_challenge_list`

- 用途：获取挑战榜
- 返回：挑战榜
- Query：
  - `page` (必填,integer) 页码
  - `page_size` (必填,integer) 每页数量
  - `keyword` (string) 热点搜索词

## 获取同城热点榜

`GET /api/v1/douyin/billboard/fetch_hot_city_list`

- 返回：同城热点榜
- Query：
  - `page` (必填,integer) 页码
  - `page_size` (必填,integer) 每页数量
  - `order` (必填,string) 排序方式
  - `city_code` (string) 城市编码，从城市列表获取，空为全部
  - `sentence_tag` (string) 热点分类标签，从热点榜分类获取，多个分类用逗号分隔，空为全部
  - `keyword` (string) 热点搜索词

## 获取作品评论分析-词云权重

`GET /api/v1/douyin/billboard/fetch_hot_comment_word_list`

- 返回：作品评论分析-词云权重
- Query：
  - `aweme_id` (必填,string) 作品id

## 获取作品数据趋势

`GET /api/v1/douyin/billboard/fetch_hot_item_trends_list`

- 返回：作品数据趋势
- Query：
  - `aweme_id` (string) 作品id
  - `option` (integer,默认 7) 选项，7 点赞量 8 分享量 9 评论量
  - `date_window` (integer,默认 1) 数据点粒度，可选 1/2，代表按小时/按天，默认1

## 获取上升热点榜

`GET /api/v1/douyin/billboard/fetch_hot_rise_list`

- 返回：上升热点榜
- Query：
  - `page` (必填,integer) 页码
  - `page_size` (必填,integer) 每页数量
  - `order` (必填,string) 排序方式
  - `sentence_tag` (string) 热点分类标签，从热点榜分类获取，多个分类用逗号分隔，空为全部
  - `keyword` (string) 热点搜索词

## 获取高涨粉率榜

`POST /api/v1/douyin/billboard/fetch_hot_total_high_fan_list`

- 返回：高涨粉率榜
- Body(JSON)：
  - `page` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string) 搜索关键词，对榜单按关键词过滤，空为全部
  - `tags` (array) 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"page": 1, "page_size": 10, "date_window": 24, "keyword": "", "tags": [{"value": 628, "children": [{"value": 62808}, {"value": 62804}]}]}`

## 获取高点赞率榜

`POST /api/v1/douyin/billboard/fetch_hot_total_high_like_list`

- 返回：高点赞率榜
- Body(JSON)：
  - `page` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string) 搜索关键词，对榜单按关键词过滤，空为全部
  - `tags` (array) 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"page": 1, "page_size": 10, "date_window": 24, "keyword": "", "tags": [{"value": 628, "children": [{"value": 62808}, {"value": 62804}]}]}`

## 获取高完播率榜

`POST /api/v1/douyin/billboard/fetch_hot_total_high_play_list`

- 返回：高完播率榜
- Body(JSON)：
  - `page` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string) 搜索关键词，对榜单按关键词过滤，空为全部
  - `tags` (array) 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"page": 1, "page_size": 10, "date_window": 24, "keyword": "", "tags": [{"value": 628, "children": [{"value": 62808}, {"value": 62804}]}]}`

## 获取热度飙升的搜索榜

`POST /api/v1/douyin/billboard/fetch_hot_total_high_search_list`

- 返回：热度飙升的搜索榜
- Body(JSON)：
  - `page_num` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string,默认 抖音) 搜索关键字
- 示例：`{"page_num": 1, "page_size": 10, "date_window": 24, "keyword": "抖音"}`

## 获取热度飙升的话题榜

`POST /api/v1/douyin/billboard/fetch_hot_total_high_topic_list`

- 返回：热度飙升的话题榜
- Body(JSON)：
  - `page` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string) 搜索关键词，对榜单按关键词过滤，空为全部
  - `tags` (array) 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"page": 1, "page_size": 10, "date_window": 24, "keyword": "", "tags": [{"value": 628, "children": [{"value": 62808}, {"value": 62804}]}]}`

## 获取内容词详情

`GET /api/v1/douyin/billboard/fetch_hot_total_hot_word_detail_list`

- 返回：内容词详情
- Query：
  - `keyword` (必填,string) 搜索关键字
  - `word_id` (必填,string) 内容词id
  - `query_day` (必填,integer) 查询日期，格式为YYYYMMDD，需为当日

## 获取全部热门内容词

`POST /api/v1/douyin/billboard/fetch_hot_total_hot_word_list`

- 用途：获取全部内容词
- 返回：全部内容词
- Body(JSON)：
  - `page_num` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 24/72/168，代表近1天/近3天/近7天，默认24
  - `keyword` (string,默认 抖音) 搜索关键字
- 示例：`{"page_num": 1, "page_size": 10, "date_window": 24, "keyword": "抖音"}`

## 获取热点总榜

`GET /api/v1/douyin/billboard/fetch_hot_total_list`

- 返回：热点总榜
- Query：
  - `page` (必填,integer) 页码
  - `page_size` (必填,integer) 每页数量
  - `type` (必填,string) 快照类型 snapshot 按时刻查看 range 按时间范围
  - `snapshot_time` (string,默认 20250106151500) 快照时间 格式yyyyMMddHHmmss
  - `start_date` (string) 快照开始时间 格式yyyyMMdd
  - `end_date` (string) 快照结束时间 格式yyyyMMdd
  - `sentence_tag` (string) 热点分类标签，从热点榜分类获取，多个分类用逗号分隔，空为全部
  - `keyword` (string) 热点搜索词

## 获取低粉爆款榜

`POST /api/v1/douyin/billboard/fetch_hot_total_low_fan_list`

- 返回：低粉爆款榜
- Body(JSON)：
  - `page` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string) 搜索关键词，对榜单按关键词过滤，空为全部
  - `tags` (array) 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"page": 1, "page_size": 10, "date_window": 24, "keyword": "", "tags": [{"value": 628, "children": [{"value": 62808}, {"value": 62804}]}]}`

## 获取搜索热榜

`POST /api/v1/douyin/billboard/fetch_hot_total_search_list`

- 用途：获取搜索榜
- 返回：搜索榜
- Body(JSON)：
  - `page_num` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string,默认 抖音) 搜索关键字
- 示例：`{"page_num": 1, "page_size": 10, "date_window": 24, "keyword": "抖音"}`

## 获取话题热榜

`POST /api/v1/douyin/billboard/fetch_hot_total_topic_list`

- 用途：获取话题榜
- 返回：话题榜
- Body(JSON)：
  - `page` (integer,默认 1) 页码
  - `page_size` (integer,默认 10) 每页数量
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `keyword` (string) 搜索关键词，对榜单按关键词过滤，空为全部
  - `tags` (array) 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"page": 1, "page_size": 10, "date_window": 24, "keyword": "", "tags": [{"value": 628, "children": [{"value": 62808}, {"value": 62804}]}]}`

## 获取视频热榜

`POST /api/v1/douyin/billboard/fetch_hot_total_video_list`

- 用途：获取视频榜
- 返回：视频榜
- Body(JSON)：
  - `page` (integer,默认 1) 页码，默认1
  - `page_size` (integer,默认 10) 每页数量，默认10
  - `date_window` (integer,默认 24) 时间窗口(小时)，可选 1/24/72/168，代表近1小时/近1天/近3天/近7天，默认24
  - `sub_type` (integer,默认 1001) 榜单分类，1001 视频总榜 1002 低粉爆款 1003 高完播率 1004 高涨粉率 1005 高点赞率
  - `keyword` (string) 搜索关键词，对榜单按关键词过滤，空为全部
  - `tags` (array) 垂类标签筛选，空则为全部，标签id从 fetch_content_tag 接口获取
- 示例：`{"page": 1, "page_size": 10, "date_window": 24, "sub_type": 1001, "keyword": "", "tags": [{"value": 628, "children": [{"value": 62808}, {"value": 62804}]}]}`

## 获取作品点赞观众画像-仅限热门榜

`GET /api/v1/douyin/billboard/fetch_hot_user_portrait_list`

- 用途：获取作品点赞观众画像
- 返回：作品点赞观众画像
- Query：
  - `aweme_id` (必填,string) 作品id
  - `option` (integer,默认 4) 选项，1 手机价格分布 2 性别分布 3 年龄分布 4 地域分布-省份 5 地域分布-城市 6 城市等级 7 手机品牌分布
