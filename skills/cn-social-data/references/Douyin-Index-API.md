# Douyin Index API

文件夹 `Douyin-Index-API` · 51 个接口
说明：抖音指数数据接口（关键词指数、达人分析、品牌分析、话题分析、视频搜索等）


## 获取所有有效日期

`GET /api/v1/douyin/index/fetch_all_valid_date`

- 用途：获取抖音指数各类型数据的最新有效日期
- 返回：包含关键词、品牌、话题等维度的日/周/月最新可用日期

## 获取关联分析有效日期

`GET /api/v1/douyin/index/fetch_valid_date_for_relation`

- 用途：获取抖音指数关联分析功能的有效日期范围
- 返回：关联分析的起止可用日期

## 获取所有地区列表

`GET /api/v1/douyin/index/fetch_all_area`

- 用途：获取抖音指数支持的所有地区列表
- 返回：省份和城市的层级结构列表，可用于关键词指数的地区筛选参数

## 获取实时热点排行

`GET /api/v1/douyin/index/fetch_current_hot_topic`

- 用途：获取抖音实时热点和飙升热点排行榜
- 返回：热点名称、热点指数、排名变化等信息

## 获取热点详情分析

`GET /api/v1/douyin/index/fetch_hot_detail`

- 用途：获取单个热点的完整分析数据，一次请求覆盖热点详情页的全部模块
- 返回：trend_item: 热点指数趋势（按时间点的指数值）；content_item: 热门内容列表（视频标题、链接、封面、作者、点赞/评论数等）；play_rank_author_item: 相关达人榜（按播放量排序）；digg_rank_author_item: 相关达人榜（按点赞数排序）；fans_rank_author_item: 相关达人榜（按粉丝数排序）；comment_rank_author_item: 相关达人榜（按评论数排序）；portrait: 人群画像，包含地域分布(province)、城市(city)、性别(gender)、
- Query：
  - `topic_name` (必填,string) 热点名称/Hot topic name
- 示例：

```
topic_name = "詹姆斯宣布加盟76人"
```

## 获取热门关键词

`GET /api/v1/douyin/index/fetch_hot_words`

- 用途：获取当前热门搜索关键词列表
- 返回：关键词名称、搜索指数、增长率等
- Query：
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)

## 获取热门推荐词

`GET /api/v1/douyin/index/fetch_hot_trend_word`

- 用途：获取关键词指数搜索框的热门推荐词，用作关键词指数分析的输入建议；注意: 这不是实时热点榜，实时热点和飙升热点请用 fetch_current_hot_topic
- 返回：update_time: 数据更新日期（按天更新，非实时）；trend_words: 推荐词列表，含 id 和 word
- Query：
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
  - `type` (选填,integer) 推荐词类型/Word type: 0(搜索热词/Search words), 1(内容热词/Content words)
- 示例：

```
app_name = "aweme"; type = 0
```

## 获取关键词有效日期

`POST /api/v1/douyin/index/fetch_keyword_valid_date`

- 用途：获取指定关键词在抖音指数中的有效日期范围
- 返回：各关键词可查询的起止日期
- Query：
  - `keyword_list` (必填,string) 关键词列表，逗号分隔/Keyword list, comma separated
- 示例：

```
keyword_list = "美食"
```

## 获取多关键词热度趋势

`POST /api/v1/douyin/index/fetch_multi_keyword_hot_trend`

- 用途：获取多个关键词在指定时间范围内的热度趋势数据；可对比多个关键词的热度变化
- 返回：每日热度趋势数据
- Query：
  - `keyword_list` (必填,string) 关键词列表，逗号分隔/Keyword list, comma separated
  - `start_date` (必填,string) 开始日期/Start date, YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date, YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
  - `region` (选填,string) 地区列表，逗号分隔/Region list, comma separated
- 示例：

```
keyword_list = "美食"
start_date = "20260312"
end_date = "20260412"
```

## 获取多关键词解读

`POST /api/v1/douyin/index/fetch_multi_keyword_interpretation`

- 用途：获取多个关键词的指数解读数据（综合指数、搜索指数、内容指数等）；建议配合 fetch_multi_keyword_hot_trend 一起使用
- 返回：关键词综合指数、搜索指数、内容指数解读
- Query：
  - `keyword_list` (必填,string) 关键词列表，逗号分隔/Keyword list, comma separated
  - `start_date` (必填,string) 开始日期/Start date, YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date, YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
  - `region` (选填,string) 地区列表，逗号分隔/Region list, comma separated
- 示例：

```
keyword_list = "便利贴"
start_date = "20251015"
end_date = "20260412"
```

## 获取关联词分析

`POST /api/v1/douyin/index/fetch_relation_word`

- 用途：获取关键词的关联词分析，包含搜索关联词和内容关联词；展示关联词图谱和关联词排名
- 返回：搜索关联词列表、内容关联词列表、关联词图谱数据
- 注意：**关联分析的日期范围必须以周日为终止日期**，例如 start_date=20260330, end_date=20260405（周日）；如果 end_date 不是周日，接口可能返回空数据
- Query：
  - `keyword` (必填,string) 关键词/Keyword
  - `start_date` (必填,string) 开始日期（周一）/Start date (Monday) YYYYMMDD
  - `end_date` (必填,string) 结束日期（必须为周日）/End date (must be Sunday) YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
- 示例：

```
keyword = "美食"
start_date = "20260330"
end_date = "20260405"
```

## 获取人群画像

`POST /api/v1/douyin/index/fetch_portrait`

- 用途：获取关键词的人群画像分析数据
- 返回：性别分布、年龄分布、地域分布、兴趣分布等人群画像数据
- Query：
  - `keyword` (必填,string) 关键词/Keyword
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
- 示例：

```
keyword = "美食"
start_date = "20260406"
end_date = "20260412"
```

## 获取用户订阅关键词

`POST /api/v1/douyin/index/fetch_get_user_sub_word`

- 用途：获取当前登录用户在抖音指数中订阅的关键词列表
- 返回：用户已订阅的关键词列表

## 抖音 uid 转加密 user_id

`GET /api/v1/douyin/index/fetch_encrypt_user_id`

- 用途：将抖音 uid（纯数字）转换为抖音指数 API 内部使用的加密 user_id；达人相关接口（如 fetch_daren_similar_users、fetch_daren_great_item_mile_info 等）
- 返回：uid: 原始输入的抖音 uid；user_id: 加密后的 user_id
- Query：
  - `uid` (必填,string) 抖音 uid (纯数字) / Douyin uid (numeric). Example: 3100268042915212
- 示例：

```
uid = "3100268042915212"
```

## 达人搜索建议

`POST /api/v1/douyin/index/fetch_daren_sug_great_user_list`

- 用途：搜索达人，获取达人列表建议
- 返回：匹配的达人列表（包含达人ID、昵称、头像、粉丝数等）
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `total` (选填,string) 返回数量/Return count
- 示例：

```
keyword = "小野"
total = "20"
```

## 达人趋势对比

`POST /api/v1/douyin/index/fetch_daren_compare_users_stable`

- 用途：对比多个达人的趋势数据（粉丝增长、互动量等）
- 返回：每个达人在指定天数内的趋势数据对比
- Query：
  - `user_list` (必填,string) 达人抖音 uid 列表，逗号分隔，最多5个 / Daren uid list, comma separated, max 5
  - `days` (选填,string) 天数/Days: 7 or 30
- 示例：

```
user_list = "3100268042915212,2190670988842736"
days = "7"
```

## 获取相似达人

`POST /api/v1/douyin/index/fetch_daren_similar_users`

- 用途：获取与指定达人相似的达人列表
- 返回：相似达人列表
- Query：
  - `user_id` (必填,string) 达人抖音 uid (纯数字) / Douyin uid (numeric). Example: 3100268042915212
- 示例：

```
user_id = "3100268042915212"
```

## 获取达人视频

`POST /api/v1/douyin/index/fetch_daren_great_user_top_video`

- 用途：获取达人在指定时间范围内的热门视频列表
- 返回：达人热门视频列表（播放量、点赞数等）
- 注意：**日期范围不能超过30天**，否则接口会报错
- Query：
  - `user_id` (必填,string) 达人抖音 uid (纯数字) / Douyin uid (numeric). Example: 3100268042915212
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
user_id = "3100268042915212"
start_date = "20260316"
end_date = "20260414"
```

## 获取达人核心指标

`POST /api/v1/douyin/index/fetch_daren_great_item_mile_info`

- 用途：获取达人核心指标数据
- 返回：粉丝数、获赞数、作品数、互动率等核心指标
- Query：
  - `user_id` (必填,string) 达人抖音 uid (纯数字) / Douyin uid (numeric). Example: 3100268042915212
- 示例：

```
user_id = "3100268042915212"
```

## 获取达人粉丝分析

`POST /api/v1/douyin/index/fetch_daren_great_user_fans_info`

- 用途：获取达人粉丝分析数据
- 返回：粉丝性别分布、年龄分布、地域分布、活跃时间等
- Query：
  - `user_id` (必填,string) 达人抖音 uid (纯数字) / Douyin uid (numeric). Example: 3100268042915212
- 示例：

```
user_id = "3100268042915212"
```

## 获取视频搜索筛选选项

`GET /api/v1/douyin/index/fetch_item_filter_options`

- 用途：获取视频搜索 `fetch_item_query` 接口支持的所有筛选选项取值；包含：垂类(categories)、时长(duration_types)、类型(label_types)、发布时间(date_types)；调用 `fetch_item_query` 前可先查询本接口获取所需的 ID
- 返回：categories: 垂类列表，每项包含 id / name / name_en，id 用于 category_id 参数；duration_types: 时长列表，每项包含 id / name / name_en，id 用于 duration_type 参数；label_types: 视频类型列表，每项包含 id / name / name_en，id 用于 label_type 参数；date_types: 发布时间列表，每项包含 id / name / name_en，id 用于 date_type 参数

## 视频搜索建议

`POST /api/v1/douyin/index/fetch_item_sug`

- 用途：获取视频搜索的关键词自动补全建议
- 返回：匹配的关键词建议列表
- Query：
  - `query` (必填,string) 搜索关键词/Search keyword
- 示例：

```
query = "打瓦"
```

## 视频搜索结果

`POST /api/v1/douyin/index/fetch_item_query`

- 用途：搜索抖音指数视频库，支持垂类、时长、类型、发布时间四维筛选；结果包含视频基础信息、播放/点赞/粉丝等核心数据
- 返回：视频列表，每项包含：itemId、itemTitle、视频封面、时长、发布时间、
- 注意：所有筛选参数的完整合法取值可通过 `GET /fetch_item_filter_options` 动态获取，
- Query：
  - `query` (必填,string) 搜索关键词/Search keyword
  - `category_id` (选填,string) 垂类ID（可通过 fetch_item_filter_options 获取）/Category ID (get from fetch_item_filter_options), 0=全部/all
  - `date_type` (选填,integer) 发布时间类型（可通过 fetch_item_filter_options 获取）/Date type (get from fetch_item_filter_options), 0=不限/unlimited
  - `label_type` (选填,integer) 视频类型（可通过 fetch_item_filter_options 获取）/Label type (get from fetch_item_filter_options), 0=不限/unlimited
  - `duration_type` (选填,integer) 时长类型（可通过 fetch_item_filter_options 获取）/Duration type (get from fetch_item_filter_options), 0=不限/unlimited
- 示例：

```
# 搜索全部美食视频
query = "美食"
category_id = "0"

# 只搜美食垂类下近7天发布的15-60秒高完播率视频
query = "美食"
category_id = "628"
date_type = 7
duration_type = 6
label_type = 2
```

## 获取视频详情

`POST /api/v1/douyin/index/fetch_item_base`

- 用途：获取指定视频在抖音指数「视频分析」中的基础详情
- 返回：视频标题、封面、时长、发布时间、作者信息及基础数据等
- Query：
  - `item_id` (必填,string) 视频ID（抖音 aweme id，纯数字）/Video ID (Douyin aweme id, numeric). Example: 7660090930283744575
- 示例：

```
item_id = "7660090930283744575"
```

## 获取视频指数趋势

`POST /api/v1/douyin/index/fetch_item_index`

- 用途：获取指定视频在时间范围内的视频指数趋势数据
- 返回：视频指数（综合/传播/互动等）随时间变化的趋势数据
- Query：
  - `item_id` (必填,string) 视频ID（抖音 aweme id，纯数字）/Video ID (Douyin aweme id, numeric). Example: 7660090930283744575
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
item_id = "7660090930283744575"
start_date = "20260704"
end_date = "20260710"
```

## 获取视频指数解读

`POST /api/v1/douyin/index/fetch_item_index_interpret`

- 用途：获取指定视频的视频指数解读（各分项指数的说明与归因）；建议配合 fetch_item_index 一起使用
- 返回：视频综合指数、传播指数、互动指数等分项解读
- Query：
  - `item_id` (必填,string) 视频ID（抖音 aweme id，纯数字）/Video ID (Douyin aweme id, numeric). Example: 7660090930283744575
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
item_id = "7660090930283744575"
start_date = "20260704"
end_date = "20260710"
```

## 获取视频对比分析

`POST /api/v1/douyin/index/fetch_item_analysis`

- 用途：获取指定视频的对比分析数据（与同类视频/大盘的表现对比）
- 返回：视频在各维度上与参照对象的对比分析结果
- Query：
  - `item_id` (必填,string) 视频ID（抖音 aweme id，纯数字）/Video ID (Douyin aweme id, numeric). Example: 7660090930283744575
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
item_id = "7660090930283744575"
start_date = "20260704"
end_date = "20260710"
```

## 获取视频观众分析

`POST /api/v1/douyin/index/fetch_item_user_profile`

- 用途：获取指定视频的观众人群画像
- 返回：观众性别分布、年龄分布、地域分布、兴趣分布等画像数据
- Query：
  - `item_id` (必填,string) 视频ID（抖音 aweme id，纯数字）/Video ID (Douyin aweme id, numeric). Example: 7660090930283744575
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
item_id = "7660090930283744575"
start_date = "20260704"
end_date = "20260710"
```

## 品牌搜索建议

`POST /api/v1/douyin/index/fetch_brand_suggest`

- 用途：获取品牌搜索的自动补全建议列表
- 返回：匹配的品牌列表（品牌名称、分类ID等）
- Query：
  - `keyword` (必填,string) 品牌名称关键词/Brand keyword
- 示例：

```
keyword = "泡泡玛特"
```

## 获取品牌指数

`POST /api/v1/douyin/index/fetch_brand_valid_info`

- 用途：获取品牌的有效信息和品牌指数数据
- 返回：品牌指数、可用日期范围等
- Query：
  - `keyword_list` (必填,string) 品牌名称列表逗号分隔/Brand list comma separated
- 示例：

```
keyword_list = "泡泡玛特"
```

## 获取品牌雷达图

`POST /api/v1/douyin/index/fetch_brand_radar_chart`

- 用途：获取品牌的雷达图数据（多维度评分）
- 返回：品牌多维度评分雷达图数据
- Query：
  - `brand_name` (必填,string) 品牌名称/Brand name
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
- 示例：

```
brand_name = "泡泡玛特"
start_date = "20251015"
end_date = "20260412"
```

## 获取品牌趋势线

`POST /api/v1/douyin/index/fetch_brand_lines`

- 用途：获取品牌的趋势线数据（热度随时间变化）
- 返回：品牌热度趋势线数据
- Query：
  - `brand_name` (必填,string) 品牌名称/Brand name
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)

## 获取品牌周期数据

`POST /api/v1/douyin/index/fetch_brand_cycles`

- 用途：获取品牌的周期数据（周期性热度分析）
- 返回：品牌周期性热度数据
- Query：
  - `brand_name` (必填,string) 品牌名称/Brand name
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)

## 获取品牌主动排行周榜

`POST /api/v1/douyin/index/fetch_brand_initiative_rank_weekly`

- 用途：获取品牌主动排行周榜数据
- 返回：品牌在该周的主动排行数据
- Query：
  - `brand_name` (必填,string) 品牌名称/Brand name
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)

## 话题搜索建议

`POST /api/v1/douyin/index/fetch_topic_suggest`

- 用途：获取话题搜索的自动补全建议列表
- 返回：匹配的话题列表
- Query：
  - `keyword` (必填,string) 话题关键词/Topic keyword
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
- 示例：

```
keyword = "特朗普"
```

## 话题搜索结果

`POST /api/v1/douyin/index/fetch_topic_query`

- 用途：搜索话题，获取话题详情和相关数据
- 返回：话题详情、话题热度、相关视频数等
- Query：
  - `keyword` (必填,string) 话题关键词/Topic keyword
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
  - `app_name` (选填,string) 平台/Platform: aweme(抖音), toutiao(头条)
- 示例：

```
keyword = "特朗普"
start_date = "20260406"
end_date = "20260412"
```

## 创作指南有效日期

`GET /api/v1/douyin/index/fetch_content_valid_date`

- 用途：获取创作指南各类型数据的有效日期范围
- 返回：创作指南可查询的起止日期

## 热门视频时间范围

`POST /api/v1/douyin/index/fetch_brand_hot_videos_time_scope`

- 用途：获取品牌热门视频功能可查询的时间范围；用于在请求其他品牌相关接口前确定合法的日期边界
- 返回：时间范围信息（起止日期、周期单位等）

## 创作热门关键词

`POST /api/v1/douyin/index/fetch_content_creative_keywords`

- 用途：获取指定垂类下创作热门关键词
- 返回：该垂类下热门关键词列表
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部**（同 fetch_item_query 的 category_id 但不接受 0）/Category ID, **required, does NOT support 0=all**. Get full list via fetch_item_filter_options (excluding id=0)
  - `period` (选填,string) 时间周期/Period: 1=近1天, 3=近3天, 7=近7天
  - `end_date` (必填,string) 结束日期 YYYYMMDD（**仅当 period=7 时必须为周日**，period=1/3 时可为任意日期）/End date YYYYMMDD (**must be a Sunday only when period=7**; any day for period=1/3)
- 示例：

```
tag_id = "601"
period = "7"
end_date = "20260412"
```

## 关键词相关视频

`POST /api/v1/douyin/index/fetch_content_creative_keyword_items`

- 用途：获取指定垂类下、指定热门关键词的相关视频列表；用于查看某个热门关键词具体由哪些视频贡献
- 返回：与该关键词相关的视频列表
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部** / Category ID, **required, does NOT support 0=all**
  - `period` (选填,string) 时间周期/Period: 1, 3, 7
  - `end_date` (必填,string) 结束日期 YYYYMMDD（**仅当 period=7 时必须为周日**，period=1/3 时可为任意日期）/End date YYYYMMDD (**must be a Sunday only when period=7**; any day for period=1/3)
  - `keyword` (必填,string) 关键词（从 fetch_content_creative_keywords 获取）/Keyword (get from fetch_content_creative_keywords)
- 示例：

```
tag_id = "601"
period = "1"
end_date = "20260414"
keyword = "视频"
```

## 创作热门话题

`POST /api/v1/douyin/index/fetch_content_creative_topic`

- 用途：获取指定垂类下创作热门话题
- 返回：该垂类下热门话题列表
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部** / Category ID, **required, does NOT support 0=all**
  - `period` (选填,string) 时间周期/Period: 1, 3, 7
  - `end_date` (必填,string) 结束日期 YYYYMMDD（**仅当 period=7 时必须为周日**，period=1/3 时可为任意日期）/End date YYYYMMDD (**must be a Sunday only when period=7**; any day for period=1/3)
  - `rank_type` (选填,string) 排序类型/Rank type: index=指数排序, rise=飙升排序
- 示例：

```
tag_id = "601"
period = "7"
end_date = "20260405"
rank_type = "index"
```

## 内容发布趋势

`GET /api/v1/douyin/index/fetch_content_publish_trend`

- 用途：获取指定垂类的视频发布数量随时间变化趋势；用于了解某垂类的内容供给热度变化
- 返回：按日聚合的发布量数据（日期 + 当日发布作品数）
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部**（同 fetch_item_query 的 category_id 但不接受 0）/Category ID, **required, does NOT support 0=all**. Get full list via fetch_item_filter_options (excluding id=0)
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
tag_id = "601"
start_date = "20260314"
end_date = "20260414"
```

## 创作时长分布

`POST /api/v1/douyin/index/fetch_content_creative_duration`

- 用途：获取指定垂类下视频时长分布数据；用于了解该垂类创作者偏好的视频时长结构
- 返回：各时长区间（如 0-15 秒/15-60 秒/60-180 秒/大于 180 秒）的视频数量与占比
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部**（同 fetch_item_query 的 category_id 但不接受 0）/Category ID, **required, does NOT support 0=all**. Get full list via fetch_item_filter_options (excluding id=0)
  - `period` (选填,string) 时间粒度/Period: week=周, month=月
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
tag_id = "601"
period = "week"
end_date = "20260412"
```

## 创作者画像

`POST /api/v1/douyin/index/fetch_content_author_portrait`

- 用途：获取指定垂类下**创作者**人群画像（即"发布该垂类视频的作者"画像）；用于了解某垂类创作者的性别、年龄、地域、活跃时段等特征
- 返回：创作者画像数据：性别分布、年龄段分布、地域分布、设备分布、活跃时段等
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部**（同 fetch_item_query 的 category_id 但不接受 0）/Category ID, **required, does NOT support 0=all**. Get full list via fetch_item_filter_options (excluding id=0)
  - `period` (选填,string) 时间粒度/Period: week or month
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
tag_id = "601"
period = "month"
end_date = "20260331"
```

## 消费者画像

`POST /api/v1/douyin/index/fetch_content_consumer_portrait`

- 用途：获取指定垂类下**消费者**人群画像（即"观看该垂类视频的用户"画像）；与 fetch_content_author_portrait 互为补充：一个看作者，一个看观众
- 返回：消费者画像数据：性别分布、年龄段分布、地域分布、兴趣偏好、设备分布等
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部**（同 fetch_item_query 的 category_id 但不接受 0）/Category ID, **required, does NOT support 0=all**. Get full list via fetch_item_filter_options (excluding id=0)
  - `period` (选填,string) 时间粒度/Period: week or month
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
tag_id = "601"
period = "month"
end_date = "20260331"
```

## 互动趋势

`POST /api/v1/douyin/index/fetch_content_interact_trend`

- 用途：获取指定垂类的互动数据（点赞/评论/分享/收藏等）随时间变化趋势；衡量该垂类内容引发用户互动的活跃程度
- 返回：按日聚合的互动数据：每日点赞总数、评论总数、分享总数、收藏总数等
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部**（同 fetch_item_query 的 category_id 但不接受 0）/Category ID, **required, does NOT support 0=all**. Get full list via fetch_item_filter_options (excluding id=0)
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
tag_id = "601"
start_date = "20260314"
end_date = "20260414"
```

## 消费趋势

`POST /api/v1/douyin/index/fetch_content_consume_trend`

- 用途：获取指定垂类的消费数据（播放量、观看时长等）随时间变化趋势；衡量该垂类内容被用户实际消费（观看）的热度变化
- 返回：按日聚合的消费数据：每日播放总量、观看时长、独立观看人数等
- Query：
  - `tag_id` (必填,string) 垂类ID，**必填，不支持 0=全部**（同 fetch_item_query 的 category_id 但不接受 0）/Category ID, **required, does NOT support 0=all**. Get full list via fetch_item_filter_options (excluding id=0)
  - `start_date` (必填,string) 开始日期/Start date YYYYMMDD
  - `end_date` (必填,string) 结束日期/End date YYYYMMDD
- 示例：

```
tag_id = "601"
start_date = "20260314"
end_date = "20260414"
```

## 获取推荐报告

`GET /api/v1/douyin/index/fetch_insight_recommend`

- 用途：获取首页推荐的趋势报告列表
- 返回：推荐报告列表（含报告ID、标题、封面、发布时间等）

## 搜索趋势报告

`POST /api/v1/douyin/index/fetch_report_search`

- 用途：搜索抖音指数下的趋势报告，支持类型/产品/年份/关键词四维筛选
- 返回：报告列表（标题、封面、发布时间、产品标签、报告ID 等）
- Query：
  - `current_page` (选填,string) 页码/Page number
  - `page_size` (选填,string) 每页数量/Page size
  - `type` (选填,string) 报告类型/Report type: 空=全部, 行业洞察=Industry, 产品洞察=Product, 用户洞察=User, 趋势洞察=Trend
  - `business` (选填,string) 所属产品列表，逗号分隔/Business list, comma separated. Options: 巨量引擎, 今日头条, 抖音, 西瓜视频, 抖音电商, 仕小禄, 其他
  - `report_time` (选填,string) 发布年份列表，逗号分隔/Year list, comma separated. e.g. 2024,2023
  - `search` (选填,string) 报告关键词搜索/Search keyword
  - `category` (选填,string) 顶层分类ID（默认 6 表示抖音指数趋势报告）/Top category ID (default 6 = Douyin Index trend reports)
- 示例：

```
type = "行业洞察"
business = "巨量引擎"
report_time = "2024"
search = "公路"
```

## 获取报告详情

`GET /api/v1/douyin/index/fetch_report_detail`

- 用途：获取指定趋势报告的完整详情；包含报告标题、封面、发布时间、所属产品、正文内容、图片资源、PDF 下载链接等
- 返回：报告完整数据：title, cover, publish_time, business, content, images, pdf_url 等
- Query：
  - `report_id` (必填,string) 报告ID/Report ID. Example: 1081
- 示例：

```
report_id = "1081"
```

## 获取报告相关推荐

`GET /api/v1/douyin/index/fetch_insight_get_rec`

- 用途：根据当前报告 ID 获取相关推荐的其他报告；通常用于报告详情页底部的"相关推荐"模块
- 返回：相关推荐的报告列表（含 ID、标题、封面、发布时间等）
- Query：
  - `report_id` (必填,string) 报告ID/Report ID
- 示例：

```
report_id = "1081"
```
