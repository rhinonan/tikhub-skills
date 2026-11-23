# Douyin Xingtu V2 API

文件夹 `Douyin-Xingtu-V2-API` · 50 个接口
说明：抖音星图V2数据接口


## 获取星图热榜分类

`GET /api/v1/douyin/xingtu_v2/get_ranking_list_catalog`

- 用途：获取星图热榜分类列表，返回qualifier_id等分类信息；价格：0.002$ / 次
- 返回：热榜分类数据
- Query：
  - `codes` (选填,string) 分类代码，默认为空字符串/Classification codes, default is empty string
  - `biz_scene` (选填,string) 业务场景/Business scene
- 示例：

```
codes = ""
biz_scene = "douyin_flow_split_video_author_ranks"
```

## 获取星图达人商业榜数据

`GET /api/v1/douyin/xingtu_v2/get_ranking_list_data`

- 用途：获取星图达人商业榜数据；qualifier可以从`get_ranking_list_catalog`接口获取；价格：0.002$ / 次
- 返回：达人商业榜数据
- Query：
  - `code` (选填,integer) 榜单类型代码/Ranking type code
  - `qualifier` (选填,string) 榜单分类ID，从get_ranking_list_catalog获取/Category qualifier_id
  - `version` (选填,string) 版本/Version
  - `period` (选填,integer) 统计周期，7=周榜，30=月榜/Period, 7=weekly, 30=monthly
  - `date` (选填,string) 统计日期，格式YYYYMMDD/Date, format YYYYMMDD
- 示例：

```
code = 1
qualifier = "1901"
version = "flow_split"
period = 30
date = "20260131"
```

## 获取短剧演员热榜分类

`POST /api/v1/douyin/xingtu_v2/get_playlet_actor_rank_catalog`

- 用途：获取短剧演员热榜分类列表；价格：0.002$ / 次
- 返回：短剧演员热榜分类数据

## 获取短剧演员热榜

`GET /api/v1/douyin/xingtu_v2/get_playlet_actor_rank_list`

- 用途：获取短剧演员热榜数据；价格：0.002$ / 次
- 返回：短剧演员热榜数据
- Query：
  - `category` (选填,string) 分类/Category
  - `name` (选填,string) 榜单名称/Ranking name
  - `qualifier` (选填,string) 达人类型，空字符串=不限/Actor type, empty=all
  - `period` (选填,integer) 统计周期，7=周榜，30=月榜/Period, 7=weekly, 30=monthly
  - `date` (选填,string) 统计日期，格式YYYYMMDD/Date, format YYYYMMDD
- 示例：

```
category = "playlet_actor_list"
name = "playlet_actor_composite_list"
period = 30
date = "20251130"
```

## 获取达人广场筛选字段

`GET /api/v1/douyin/xingtu_v2/get_author_market_fields`

- 用途：获取达人广场所有筛选字段选项；价格：0.002$ / 次
- 返回：达人广场筛选字段数据
- Query：
  - `market_scene` (选填,integer) 市场场景，1=默认场景/Market scene, 1=default
- 示例：

```
market_scene = 1
```

## 获取达人广场筛选项取值

`GET /api/v1/douyin/xingtu_v2/get_search_field_options`

- 用途：获取达人广场中随合作对象变化的筛选项取值清单，如粉丝/观众八大人群等；与 get_author_market_fields（年龄/性别/地域/设备等）互补，两者合起来才是完整可选项；价格：0.002$ / 次
- 返回：service_options：字段名到取值选项的映射；各字段的值为 JSON 字符串，需自行解析
- Query：
  - `platform_source` (选填,integer) 平台来源，1=抖音 2=头条/Platform source, 1=Douyin, 2=Toutiao
  - `task_category` (选填,integer) 合作对象，1=抖音视频 6=抖音直播 11=头条图文/Task category, 1=Douyin video, 6=Douyin live, 11=Toutiao article
- 示例：

```
platform_source = 1
task_category = 1
```

## 达人搜索

`GET /api/v1/douyin/xingtu_v2/search_creator`

- 用途：搜索或筛选抖音短视频达人，支持关键词搜索、合作诉求、达人属性、效果指标、
- 返回：`authors`: 达人搜索结果列表，包含达人信息、粉丝数、报价和效果指标等；`pagination`: 分页信息，包含当前页、每页数量、是否还有下一页和结果总数；其它统计信息以响应中的 `extra_data` 等字段为准
- Query：
  - `keyword` (选填,string) 可选搜索词；留空时仅按筛选条件浏览。seach_type=2匹配昵称，=3匹配内容/Optional keyword; empty means filter-only browsing
  - `seach_type` (选填,integer) 搜索方式，2=按昵称找人，3=按内容找人/Search mode: 2=nickname, 3=content
  - `time_range_days` (选填,integer) 内容搜索时间范围，30/90/180天，仅seach_type=3时生效/Content time range; only for seach_type=3
  - `page` (选填,integer) 页码/Page number
  - `sort_field` (选填,string) 排序字段，默认score综合排序/Sort field, default score (comprehensive)
  - `sort_type` (选填,integer) 排序方式，1=升序，2=降序/Sort type, 1=asc, 2=desc
  - `task_category` (选填,integer) 合作对象/Cooperation target
  - `marketing_target` (选填,integer) 营销目标/Marketing target
  - `first_industry_id` (选填,integer) 适配行业ID，0=不限/Industry ID, 0=unlimited
  - `author_list_id` (选填) 主题推荐达人清单ID/Featured creator list ID
  - `price_type` (选填) 短视频报价时长档位：1=1-20秒、2=21-60秒、3=60秒以上；仅与price_min/price_max配合使用/Creator video price tier
  - `price_min` (选填) 达人报价下限，提供时必须同时提供price_type/Minimum creator price
  - `price_max` (选填) 达人报价上限，提供时必须同时提供price_type/Maximum creator price
  - `tag` (选填) 达人类型ID，多个用逗号分隔，如`1,6`/Creator category IDs, comma-separated
  - `persona_tags` (选填) 达人人设/学历/认证/调性ID。逗号分隔=满足任一；分号分组=每组都要满足，如`1129,110401;110213`/Persona IDs. Comma=match any, semicolon=group AND
  - `gender` (选填) 达人性别，1=男，2=女/Creator gender, 1=male, 2=female
  - `fans_min` (选填) 粉丝数下限/Minimum followers
  - `fans_max` (选填) 粉丝数上限/Maximum followers
  - `expected_play_min` (选填) 预期播放量下限/Minimum expected plays
  - `expected_play_max` (选填) 预期播放量上限/Maximum expected plays
  - `cpm_min` (选填) 预期CPM下限/Minimum expected CPM
  - `cpm_max` (选填) 预期CPM上限/Maximum expected CPM
  - `cpe_min` (选填) 预期CPE下限/Minimum expected CPE
  - `cpe_max` (选填) 预期CPE上限/Maximum expected CPE
  - `interact_rate_min` (选填) 互动率下限，0-1小数，0.02=2%/Minimum interaction rate, 0-1 decimal
  - `interact_rate_max` (选填) 互动率上限，0-1小数/Maximum interaction rate, 0-1 decimal
  - `play_over_rate_min` (选填) 完播率下限，0-1小数/Minimum play-completion rate, 0-1 decimal
  - `play_over_rate_max` (选填) 完播率上限，0-1小数/Maximum play-completion rate, 0-1 decimal
  - `burst_text_rate_min` (选填) 爆文率下限，0-1小数/Minimum viral-post rate, 0-1 decimal
  - `burst_text_rate_max` (选填) 爆文率上限，0-1小数/Maximum viral-post rate, 0-1 decimal
  - `extra_filter` (选填) 额外画像筛选的JSON数组字符串，每项必须包含非空字符串field_name和field_value；支持内容主题、观众/粉丝画像、八大人群和地域等维度/Extra profile filters as a JSON-array string; field_name and field_value must be non-empty strings
- 示例：

```
keyword = "飞机"
seach_type = 2

# [示例 2：按内容搜索 / Example 2: content search]
keyword = "飞机"
seach_type = 3
time_range_days = 180

# [示例 3：纯条件筛选 / Example 3: filter-only search]
keyword = ""
seach_type = 3
time_range_days = 180
page = 1
sort_field = "score"
sort_type = 2
task_category = 1
marketing_target = 1
first_industry_id = 0
tag = "36"
gender = 2
fans_min = 100000
fans_max = 200000
extra_filter = '[{"field_name":"content_theme_labels_180d","field_value":"[\"生活好物评测\"]"},{"field_name":"watcher_gender_female_rate_v2__ge","field_value":"0.6"},{"field_name":"link_crowd_profile","field_value":"[60,55,53,57]"}]'
```

## 主播搜索

`GET /api/v1/douyin/xingtu_v2/search_anchor`

- 用途：主播搜索(抖音直播广场)，按关键词搜索抖音直播主播，支持完整筛选条件；价格：0.002$ / 次
- 返回：主播搜索结果数据（含主播信息、直播报价、ACU/PCU、场均观看等）
- Query：
  - `keyword` (必填,string) 搜索关键词，可为主播昵称、抖音号、星图ID或直播内容词/Search keyword: nickname, Douyin ID, Xingtu ID or live content word
  - `page` (选填,integer) 页码/Page number
  - `sort_field` (选填,string) 排序字段，默认score综合排序/Sort field, default score (comprehensive)
  - `sort_type` (选填,integer) 排序方式，1=升序，2=降序/Sort type, 1=asc, 2=desc
  - `task_category` (选填,integer) 合作对象/Cooperation target
  - `marketing_target` (选填,integer) 营销目标/Marketing target
  - `first_industry_id` (选填) 适配行业ID/Industry ID
  - `author_list_id` (选填) 主题推荐达人清单ID/Featured creator list ID
  - `price_type` (选填) 直播报价类型，固定为9；仅与price_min/price_max配合使用/Live-stream price type, fixed to 9
  - `price_min` (选填) 主播报价下限，提供时必须同时提供price_type/Minimum anchor price
  - `price_max` (选填) 主播报价上限，提供时必须同时提供price_type/Maximum anchor price
  - `tag` (选填) 达人类型ID，多个用逗号分隔，如`1,6`/Creator category IDs, comma-separated
  - `persona_tags` (选填) 达人人设/学历/认证/调性ID。逗号分隔=满足任一；分号分组=每组都要满足，如`1129,110401;110213`/Persona IDs. Comma=match any, semicolon=group AND
  - `gender` (选填) 达人性别，1=男，2=女/Creator gender, 1=male, 2=female
  - `fans_min` (选填) 粉丝数下限/Minimum followers
  - `fans_max` (选填) 粉丝数上限/Maximum followers
  - `expected_play_min` (选填) 预期播放量下限/Minimum expected plays
  - `expected_play_max` (选填) 预期播放量上限/Maximum expected plays
  - `cpm_min` (选填) 预期CPM下限/Minimum expected CPM
  - `cpm_max` (选填) 预期CPM上限/Maximum expected CPM
  - `cpe_min` (选填) 预期CPE下限/Minimum expected CPE
  - `cpe_max` (选填) 预期CPE上限/Maximum expected CPE
  - `interact_rate_min` (选填) 互动率下限，0-1小数，0.02=2%/Minimum interaction rate, 0-1 decimal
  - `interact_rate_max` (选填) 互动率上限，0-1小数/Maximum interaction rate, 0-1 decimal
  - `play_over_rate_min` (选填) 完播率下限，0-1小数/Minimum play-completion rate, 0-1 decimal
  - `play_over_rate_max` (选填) 完播率上限，0-1小数/Maximum play-completion rate, 0-1 decimal
  - `burst_text_rate_min` (选填) 爆文率下限，0-1小数/Minimum viral-post rate, 0-1 decimal
  - `burst_text_rate_max` (选填) 爆文率上限，0-1小数/Maximum viral-post rate, 0-1 decimal
  - `extra_filter` (选填) 额外画像筛选的JSON数组字符串，每项必须包含非空字符串field_name和field_value；支持内容主题、观众/粉丝画像、八大人群和地域等维度/Extra profile filters as a JSON-array string; field_name and field_value must be non-empty strings
- 示例：

```
keyword = "游戏"
page = 1
gender = 2
fans_min = 10000
```

## 头条创作者搜索

`GET /api/v1/douyin/xingtu_v2/search_toutiao_creator`

- 用途：头条创作者搜索(头条图文广场)，按关键词搜索今日头条图文创作者，支持完整筛选条件；价格：0.002$ / 次
- 返回：头条创作者搜索结果数据（含创作者信息、报价、粉丝数、预期阅读量等）
- Query：
  - `keyword` (必填,string) 搜索关键词，可为创作者昵称、头条号或内容词/Search keyword: nickname, Toutiao ID or content word
  - `page` (选填,integer) 页码/Page number
  - `sort_field` (选填,string) 排序字段，默认score综合排序/Sort field, default score (comprehensive)
  - `sort_type` (选填,integer) 排序方式，1=升序，2=降序/Sort type, 1=asc, 2=desc
  - `task_category` (选填,integer) 合作对象/Cooperation target
  - `marketing_target` (选填,integer) 营销目标/Marketing target
  - `first_industry_id` (选填) 适配行业ID/Industry ID
  - `author_list_id` (选填) 主题推荐达人清单ID/Featured creator list ID
  - `price_type` (选填) 头条图文报价类型，固定为11；仅与price_min/price_max配合使用/Toutiao image-text price type, fixed to 11
  - `price_min` (选填) 图文报价下限，提供时必须同时提供price_type/Minimum image-text price
  - `price_max` (选填) 图文报价上限，提供时必须同时提供price_type/Maximum image-text price
  - `tag` (选填) 达人类型ID，多个用逗号分隔，如`1,6`/Creator category IDs, comma-separated
  - `persona_tags` (选填) 达人人设/学历/认证/调性ID。逗号分隔=满足任一；分号分组=每组都要满足，如`1129,110401;110213`/Persona IDs. Comma=match any, semicolon=group AND
  - `gender` (选填) 达人性别，1=男，2=女/Creator gender, 1=male, 2=female
  - `fans_min` (选填) 粉丝数下限/Minimum followers
  - `fans_max` (选填) 粉丝数上限/Maximum followers
  - `expected_play_min` (选填) 预期播放量下限/Minimum expected plays
  - `expected_play_max` (选填) 预期播放量上限/Maximum expected plays
  - `cpm_min` (选填) 预期CPM下限/Minimum expected CPM
  - `cpm_max` (选填) 预期CPM上限/Maximum expected CPM
  - `cpe_min` (选填) 预期CPE下限/Minimum expected CPE
  - `cpe_max` (选填) 预期CPE上限/Maximum expected CPE
  - `interact_rate_min` (选填) 互动率下限，0-1小数，0.02=2%/Minimum interaction rate, 0-1 decimal
  - `interact_rate_max` (选填) 互动率上限，0-1小数/Maximum interaction rate, 0-1 decimal
  - `play_over_rate_min` (选填) 完播率下限，0-1小数/Minimum play-completion rate, 0-1 decimal
  - `play_over_rate_max` (选填) 完播率上限，0-1小数/Maximum play-completion rate, 0-1 decimal
  - `burst_text_rate_min` (选填) 爆文率下限，0-1小数/Minimum viral-post rate, 0-1 decimal
  - `burst_text_rate_max` (选填) 爆文率上限，0-1小数/Maximum viral-post rate, 0-1 decimal
  - `extra_filter` (选填) 额外画像筛选的JSON数组字符串，每项必须包含非空字符串field_name和field_value；支持内容主题、观众/粉丝画像、八大人群和地域等维度/Extra profile filters as a JSON-array string; field_name and field_value must be non-empty strings
- 示例：

```
keyword = "数码"
page = 1
gender = 2
fans_min = 10000
```

## 获取创作者基本信息

`GET /api/v1/douyin/xingtu_v2/get_author_base_info`

- 用途：获取创作者基本信息；价格：0.002$ / 次
- 返回：创作者基本信息数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator author ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `recommend` (选填,boolean) 是否返回推荐信息/Whether to return recommendation info
  - `need_sec_uid` (选填,boolean) 是否返回sec_uid/Whether to return sec_uid
  - `need_linkage_info` (选填,boolean) 是否返回联动信息/Whether to return linkage info
- 示例：

```
o_author_id = "7589271892177518598"
```

## 获取创作者商业卡片信息

`GET /api/v1/douyin/xingtu_v2/get_author_business_card_info`

- 用途：获取创作者商业卡片信息；价格：0.002$ / 次
- 返回：创作者商业卡片信息数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator author ID
- 示例：

```
o_author_id = "7589271892177518598"
```

## 获取创作者位置信息

`GET /api/v1/douyin/xingtu_v2/get_author_local_info`

- 用途：获取创作者位置信息；价格：0.002$ / 次
- 返回：创作者位置信息数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator author ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `time_range` (选填,integer) 时间范围(天)/Time range in days
- 示例：

```
o_author_id = "7146074596666507300"
```

## 获取创作者视频列表

`GET /api/v1/douyin/xingtu_v2/get_author_show_items`

- 用途：获取创作者视频列表；价格：0.002$ / 次
- 返回：创作者视频列表数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator author ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `only_assign` (选填,boolean) 仅看指派视频/Only show assigned videos
  - `flow_type` (选填,integer) 流量类型/Flow type
- 示例：

```
o_author_id = "7589271892177518598"
```

## 获取创作者主页作品列表

`GET /api/v1/douyin/xingtu_v2/get_author_homepage_videos`

- 用途：获取创作者主页作品列表，支持翻页，返回作品互动率、完播率、内容主题标签等；可按「是否星图作品」与发布时间范围过滤；与`get_author_show_items`的区别：本接口可翻页、可过滤，返回中含总数与是否还有下一页；价格：0.002$ / 次
- 返回：作品列表数据（含 items 与 pagination，pagination 内有 total_count / has_more）
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `page` (选填,integer) 页码/Page number
  - `is_star_item` (选填) 1=仅星图作品，0=仅非星图作品，不传=全部/1=star items only, 0=non-star only, omit=all
  - `start_time` (选填) 作品发布起始时间，unix秒/Publish start time, unix seconds
  - `end_time` (选填) 作品发布结束时间，unix秒/Publish end time, unix seconds
- 示例：

```
o_author_id = "7029342444797820939"
page = 1
is_star_item = 1
```

## 获取创作者粉丝画像分布

`GET /api/v1/douyin/xingtu_v2/get_author_fans_distribution`

- 用途：获取创作者粉丝画像分布（性别、年龄、地域、兴趣等多个维度）；价格：0.002$ / 次
- 返回：粉丝画像分布数据（distributions 为多维度分布数组）
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
- 示例：

```
o_author_id = "7029342444797820939"
```

## 获取创作者视频触达分布

`GET /api/v1/douyin/xingtu_v2/get_author_touch_distribution`

- 用途：获取创作者视频触达分布数据；价格：0.002$ / 次
- 返回：视频触达分布数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
- 示例：

```
o_author_id = "7029342444797820939"
```

## 批量获取创作者信息

`POST /api/v1/douyin/xingtu_v2/multi_get_author_info`

- 用途：批量获取创作者信息，一次调用查询多个创作者，节省调用次数；价格：0.002$ / 次
- 返回：创作者信息数据（authors 为命中的创作者，not_exist_author_ids 为不存在的ID）
- Body(JSON)：
  - `author_ids` (必填,array) 创作者ID列表，一次最多50个/Creator ID list, up to 50 per call
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
- 示例：

```
author_ids = ["7029342444797820939", "6675458265154846728"]
```

## 获取创作者评论热词

`GET /api/v1/douyin/xingtu_v2/get_author_hot_comment_tokens`

- 用途：获取创作者评论热词；价格：0.002$ / 次
- 返回：创作者评论热词数据
- Query：
  - `author_id` (必填,string) 创作者ID/Creator author ID
  - `num` (选填,integer) 返回热词数量/Number of hot tokens
  - `without_emoji` (选填,boolean) 是否排除emoji/Whether to exclude emoji
- 示例：

```
author_id = "7589271892177518598"
```

## 获取创作者内容热词

`GET /api/v1/douyin/xingtu_v2/get_author_content_hot_keywords`

- 用途：获取创作者内容热词；价格：0.002$ / 次
- 返回：创作者内容热词数据
- Query：
  - `author_id` (必填,string) 创作者ID/Creator author ID
  - `keyword_type` (选填,integer) 热词类型/Keyword type
- 示例：

```
author_id = "7589271892177518598"
```

## 获取相似创作者推荐

`POST /api/v1/douyin/xingtu_v2/get_recommend_for_star_authors`

- 用途：获取相似创作者推荐；价格：0.002$ / 次
- 返回：相似创作者推荐数据
- Body(JSON)：
  - `author_ids` (必填,array) 创作者ID列表/List of creator author IDs
  - `similar_type` (选填,string) 相似类型/Similarity type
  - `page` (选填,integer) 页码/Page number
- 示例：

```
author_ids = ["7589271892177518598"]
similar_type = "content"
```

## 获取优秀行业分类列表

`GET /api/v1/douyin/xingtu_v2/get_excellent_case_category_list`

- 用途：获取连接用户漏斗中的优秀行业分类列表；价格：0.002$ / 次
- 返回：优秀行业分类列表数据
- Query：
  - `platform_source` (选填,integer) 平台来源/Platform source
- 示例：

```
platform_source = 1
```

## 获取创作者传播价值

`GET /api/v1/douyin/xingtu_v2/get_author_spread_info`

- 用途：获取创作者商业能力的传播价值信息；价格：0.002$ / 次
- 返回：创作者传播价值数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator author ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `type` (选填,integer) 视频类型，1=个人视频/Video type, 1=personal video
  - `flow_type` (选填,integer) 流量类型/Flow type
  - `only_assign` (选填,boolean) 仅看指派视频/Only assigned videos
  - `range` (选填,integer) 时间范围，2=近30天，3=近90天/Time range, 2=last 30 days, 3=last 90 days
- 示例：

```
o_author_id = "7589271892177518598"
range = 2
```

## 获取创作者视频内容分布

`GET /api/v1/douyin/xingtu_v2/get_author_video_distribution`

- 用途：获取创作者的视频内容分布，用于分析主要内容方向与视频构成；价格：0.002$ / 次
- 返回：创作者视频内容分布数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源，抖音为1/Platform source, 1 for Douyin
  - `platform_channel` (选填,integer) 平台渠道，短视频为1/Platform channel, 1 for short video

## 获取创作者传播表现视频

`GET /api/v1/douyin/xingtu_v2/get_author_spread_videos`

- 用途：获取创作者具有代表性的传播表现视频，辅助评估内容传播能力；价格：0.002$ / 次
- 返回：创作者传播表现视频数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源，抖音为1/Platform source, 1 for Douyin
  - `platform_channel` (选填,integer) 平台渠道，短视频为1/Platform channel, 1 for short video

## 获取创作者连接指标日趋势

`GET /api/v1/douyin/xingtu_v2/get_author_daily_link`

- 用途：按日期获取创作者指定连接指标的趋势数据；价格：0.002$ / 次
- 返回：指定日期范围内的连接指标趋势
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `link_type` (必填,integer) 星图连接指标类型ID/Xingtu link metric type ID
  - `start_date` (必填,string) 开始日期，建议YYYYMMDD/Start date, YYYYMMDD recommended
  - `end_date` (必填,string) 结束日期，建议YYYYMMDD/End date, YYYYMMDD recommended
  - `platform_source` (选填,integer) 平台来源，抖音为1/Platform source, 1 for Douyin
  - `platform_channel` (选填,integer) 平台渠道，短视频为1/Platform channel, 1 for short video
  - `industry_id` (选填,integer) 行业ID，0为不限/Industry ID, 0 for all

## 获取创作者连接指数日趋势

`GET /api/v1/douyin/xingtu_v2/get_author_daily_link_score`

- 用途：按日期获取创作者指定连接指数的趋势数据；价格：0.002$ / 次
- 返回：指定日期范围内的连接指数趋势
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `link_score_type` (必填,integer) 星图连接指数类型ID/Xingtu link-score type ID
  - `start_date` (必填,string) 开始日期，建议YYYYMMDD/Start date, YYYYMMDD recommended
  - `end_date` (必填,string) 结束日期，建议YYYYMMDD/End date, YYYYMMDD recommended
  - `platform_source` (选填,integer) 平台来源，抖音为1/Platform source, 1 for Douyin
  - `platform_channel` (选填,integer) 平台渠道，短视频为1/Platform channel, 1 for short video
  - `industry_id` (选填,integer) 行业ID，0为不限/Industry ID, 0 for all

## 获取创作者性价比与效果预估

`GET /api/v1/douyin/xingtu_v2/get_author_commerce_spread_info`

- 用途：获取创作者短视频合作的性价比与效果预估，可查看CPM、CPE等指标；可用于评估排除营销流量后的内容传播效果；价格：0.002$ / 次
- 返回：植入视频：`cpm_20_60`、`cpe_20_60`；定制视频：`cpm_60`、`cpe_60`；其它创作者商业传播效果预估数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
- 示例：

```
o_author_id = "7112600044674482187"
```

## 获取用户主页二维码

`GET /api/v1/douyin/xingtu_v2/get_user_profile_qrcode`

- 用途：生成用户主页二维码；core_user_id和sec_uid二选一传入即可；价格：0.002$ / 次
- 返回：用户主页二维码数据
- Query：
  - `core_user_id` (选填) 用户核心ID(与sec_uid二选一)/User core ID (pick one with sec_uid)
  - `sec_uid` (选填) 用户sec_uid(与core_user_id二选一)/User sec_uid (pick one with core_user_id)
- 示例：

```
core_user_id = "1113181577281568"
```

## 获取内容趋势指南

`GET /api/v1/douyin/xingtu_v2/get_content_trend_guide`

- 用途：获取内容趋势指南数据（CDN静态JSON，无需Cookie）；价格：0.002$ / 次
- 返回：内容趋势指南数据

## 获取星图IP日历行业列表

`GET /api/v1/douyin/xingtu_v2/get_ip_activity_industry_list`

- 用途：获取星图IP日历的行业列表；价格：0.002$ / 次
- 返回：行业列表数据

## 获取星图IP日历活动列表

`POST /api/v1/douyin/xingtu_v2/get_ip_activity_list`

- 用途：获取星图IP日历活动列表；价格：0.002$ / 次
- 返回：IP日历活动列表数据
- Body(JSON)：
  - `query_start_time` (必填,string) 查询开始时间戳/Query start timestamp
  - `query_end_time` (必填,string) 查询结束时间戳/Query end timestamp
  - `industry_id_list` (选填) 行业ID列表/Industry ID list
  - `category_list` (选填) IP类型列表/IP category list
  - `status_list` (选填) IP状态列表/IP status list
- 示例：

```
query_start_time = "1767196800"
query_end_time = "1774972799"
```

## 获取星图IP活动详情

`GET /api/v1/douyin/xingtu_v2/get_ip_activity_detail`

- 用途：获取星图IP日历活动详情；价格：0.002$ / 次
- 返回：IP活动详情数据
- Query：
  - `id` (必填,integer) 活动ID，从get_ip_activity_list获取/Activity ID from get_ip_activity_list
- 示例：

```
id = 347
```

## 获取营销活动案例

`GET /api/v1/douyin/xingtu_v2/get_resource_list`

- 用途：获取营销活动案例列表；价格：0.002$ / 次
- 返回：营销活动案例数据
- Query：
  - `resource_id` (必填,integer) 资源ID/Resource ID
- 示例：

```
resource_id = 1052
```

## 搜索MCN机构列表

`GET /api/v1/douyin/xingtu_v2/get_demander_mcn_list`

- 用途：搜索MCN机构列表；价格：0.002$ / 次
- 返回：MCN机构列表数据
- Query：
  - `mcn_name` (选填,string) MCN机构名称，支持模糊搜索/MCN name, supports fuzzy search
  - `page` (选填,integer) 页码/Page number
  - `order_by` (选填,string) 排序方式/Sort by
- 示例：

```
mcn_name = ""
page = 1
```

## 抖音UID转星图达人ID

`GET /api/v1/douyin/xingtu_v2/get_xingtu_kolid_by_uid`

- 用途：通过抖音用户ID(uid)获取星图达人ID；星图其余达人接口所需的 o_author_id 即此处返回的星图达人ID；价格：0.002$ / 次
- 返回：星图达人ID数据；用户不存在或未入驻星图时返回 exist=false
- Query：
  - `uid` (必填,string) 抖音用户ID/Douyin User ID (uid)
- 示例：

```
uid = "70452002324"
```

## 抖音sec_user_id转星图达人ID

`GET /api/v1/douyin/xingtu_v2/get_xingtu_kolid_by_sec_user_id`

- 用途：通过抖音 sec_user_id 获取星图达人ID；价格：0.002$ / 次
- 返回：星图达人ID数据；用户不存在或未入驻星图时返回 exist=false；sec_user_id 未提供、为空或抖音明确返回“UserId不合法”时返回 exist=false、reason=invalid_parameter；HTTP 200 会计费
- Query：
  - `sec_user_id` (选填,string) 抖音用户sec_user_id/Douyin User sec_user_id
- 示例：

```
sec_user_id = "MS4wLjABAAAAoxwUZouIdKL6sZ8EB96KDjkrhfBMS1KbCgsMJR1kIUs"
```

## 抖音号转星图达人ID

`GET /api/v1/douyin/xingtu_v2/get_xingtu_kolid_by_unique_id`

- 用途：通过抖音号(unique_id)获取星图达人ID；价格：0.002$ / 次
- 返回：星图达人ID数据；用户不存在或未入驻星图时返回 exist=false；unique_id 未提供、为空、仅包含空白或抖音明确返回“参数不合法”时，返回 exist=false、reason=invalid_parameter；HTTP 200 会计费
- Query：
  - `unique_id` (选填,string) 抖音号/Douyin User unique_id
- 示例：

```
unique_id = "m6640150"
```

## 获取创作者受众画像分布

`GET /api/v1/douyin/xingtu_v2/get_author_audience_distribution`

- 用途：获取创作者受众画像分布；价格：0.002$ / 次
- 返回：受众画像分布数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `link_type` (必填,integer) 受众画像类型，必填；示例值5/Audience profile link type, required; example: 5
- 示例：

```
o_author_id = "7112600044674482187"
link_type = 5
```

## 获取创作者推荐视频

`GET /api/v1/douyin/xingtu_v2/get_author_rec_videos_v2`

- 用途：获取创作者的推荐视频，用于查看其代表性内容与近期内容表现；价格：0.002$ / 次
- 返回：创作者推荐视频列表及相关表现数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源，1=抖音/Platform source, 1=Douyin
  - `platform_channel` (选填,integer) 平台渠道，1=抖音短视频/Platform channel, 1=Douyin video
- 示例：

```
o_author_id = "7112600044674482187"
platform_source = 1
platform_channel = 1
```

## 获取创作者每日粉丝趋势

`GET /api/v1/douyin/xingtu_v2/get_author_daily_fans`

- 用途：获取创作者每日粉丝趋势，可选日期范围；价格：0.002$ / 次
- 返回：每日粉丝趋势数据（含 daily / delta 等）
- Query：
  - `author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `start_date` (选填) 起始日期，格式YYYYMMDD，可选/Start date, format YYYYMMDD, optional
  - `end_date` (选填) 结束日期，格式YYYYMMDD，可选/End date, format YYYYMMDD, optional
  - `author_type` (选填) 达人类型，可选/Author type, optional
- 示例：

```
author_id = "7029342444797820939"
```

## 获取创作者转化能力

`GET /api/v1/douyin/xingtu_v2/get_author_convert_ability`

- 用途：获取创作者转化能力数据（GMV、点击、转化率等区间）；价格：0.002$ / 次
- 返回：转化能力数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `industry_id` (选填,integer) 行业ID，0=不限/Industry ID, 0=unlimited
  - `time_range` (选填,integer) 时间档，默认2/Time range tier, default 2
- 示例：

```
o_author_id = "7029342444797820939"
```

## 获取创作者CP合作信息

`GET /api/v1/douyin/xingtu_v2/get_author_cp_info`

- 用途：获取创作者CP（合作）信息；价格：0.002$ / 次
- 返回：CP合作信息数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
- 示例：

```
o_author_id = "7029342444797820939"
```

## 获取创作者转化视频/商品明细

`GET /api/v1/douyin/xingtu_v2/get_author_convert_videos_or_products`

- 用途：获取创作者转化视频/商品明细，支持翻页；价格：0.002$ / 次
- 返回：转化视频/商品明细数据
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `detail_type` (选填,integer) 明细类型，1=相关视频，2=相关商品/Detail type, 1=videos, 2=products
  - `industry_id` (选填,integer) 行业ID，0=不限/Industry ID, 0=unlimited
  - `time_range` (选填,integer) 时间档，默认2/Time range tier, default 2
  - `page` (选填,integer) 页码/Page number
- 示例：

```
o_author_id = "7589271892177518598"
detail_type = 1
```

## 获取创作者星图连接指数

`GET /api/v1/douyin/xingtu_v2/get_author_link_info`

- 用途：获取创作者星图连接指数（合作指数、CP指数、转化指数、购物指数）；价格：0.002$ / 次
- 返回：星图连接指数数据（cooperate_index / cp_index / link_convert_index / link_shopping_index）
- Query：
  - `o_author_id` (必填,string) 创作者ID/Creator ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `platform_channel` (选填,integer) 平台渠道/Platform channel
  - `industy_tag` (选填,integer) 行业标签，0=不限/Industry tag, 0=unlimited
- 示例：

```
o_author_id = "7589271892177518598"
```

## 获取单个视频播放量(含详情)

`GET /api/v1/douyin/xingtu_v2/get_item_play_count`

- 用途：获取单个视频(item)的播放量(watch_cnt)及完整详情，播放量已提到顶层方便直接取用；注意：watch_cnt 为**含投流(广告加热)**的总播放量，并附带作品详情；如需**未投流(自然)**
- 返回：exist: 视频是否存在（已删除/ID非法为false）；watch_cnt: 播放量(int)，取不到为null；stats: 完整统计块（点赞/评论/转发/收藏/互动率/人均观看时长等）；item: 完整视频详情（标题/封面/时长/发布时间/作者ID等）
- Query：
  - `item_id` (必填,string) 视频(item) ID/Video (item) ID
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `need_cover_url` (选填,boolean) 是否返回封面URL/Whether to return cover URL
- 示例：

```
item_id = "7630036460159111515"
```

## 批量获取视频数据(播放量/点赞等)

`POST /api/v1/douyin/xingtu_v2/multi_get_item_stats`

- 用途：批量获取视频(item)的播放量等统计与详情，一次最多20个，节省调用次数；每条含 stats（watch_cnt 播放量 / like_cnt 点赞 / comment_cnt 评论 / share_cnt 转发 /
- 返回：items: 命中的视频列表，每条含 stats 与视频详情（无效/已删除ID会被上游丢弃）
- Body(JSON)：
  - `item_ids` (必填,array) 视频(item) ID列表，一次最多20个/Video (item) ID list, up to 20 per call
  - `platform_source` (选填,integer) 平台来源/Platform source
  - `need_cover_url` (选填,boolean) 是否返回封面URL/Whether to return cover URL
- 示例：

```
item_ids = ["7630036460159111515", "7634126662552474854"]
```

## 获取视频详情报告

`POST /api/v1/douyin/xingtu_v2/get_item_report_detail`

- 用途：获取单个视频的详情报告与核心表现指标；价格：0.002$ / 次
- 返回：视频基础信息及详情报告数据
- Body(JSON)：
  - `item_id` (必填,string) 视频(item) ID/Video (item) ID
- 示例：

```
{"item_id": "7451907165419359488"}
```

## 获取视频互动分析

`POST /api/v1/douyin/xingtu_v2/get_item_report_th_analysis`

- 用途：获取单个视频的互动分析数据；价格：0.002$ / 次
- 返回：视频互动表现分析数据
- Body(JSON)：
  - `item_id` (必填,string) 视频(item) ID/Video (item) ID
- 示例：

```
{"item_id": "7451907165419359488"}
```

## 获取视频整体表现趋势

`POST /api/v1/douyin/xingtu_v2/get_item_report_trend`

- 用途：获取单个视频的整体表现与趋势数据；价格：0.002$ / 次
- 返回：视频整体表现趋势数据
- Body(JSON)：
  - `item_id` (必填,string) 视频(item) ID/Video (item) ID
- 示例：

```
{"item_id": "7451907165419359488"}
```

## 获取视频评论分析

`POST /api/v1/douyin/xingtu_v2/get_item_report_comments`

- 用途：获取单个视频的评论分析数据；价格：0.002$ / 次
- 返回：视频评论分析数据
- Body(JSON)：
  - `item_id` (必填,string) 视频(item) ID/Video (item) ID
- 示例：

```
{"item_id": "7451907165419359488"}
```
