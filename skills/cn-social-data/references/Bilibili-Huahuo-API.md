# Bilibili Huahuo API

文件夹 `Bilibili-Huahuo-API` · 45 个接口


## UP主广场搜索（搜UP主 / 搜内容）

`POST /api/v1/bilibili/huahuo/search_upper`

- 用途：在花火内容合作广场按 UP 主、UID 或内容关键词检索创作者；可组合基础属性、粉丝画像、报价与效果、内容表现、DMP 人群包、行业标签、
- 返回：`page`: 当前页码；`total_count`: 匹配结果总数，最大显示为 10000；`data`: UP 主列表。常见字段包括 `upper_mid`、`nickname`、`fans_num`、
- Body(JSON)：
  - `nickname_or_mids` (选填) 按 UP 主昵称或 UID 搜索，多个关键词用英文逗号分隔 / Creator nickname or UID query; separate multiple terms with commas
  - `main_search` (选填) 按内容关键词搜索，命中稿件会随结果返回 / Content-keyword query; matched videos are included in the result
  - `mids` (选填) 批量精确匹配的 UP 主 UID 列表 / List of creator UIDs to match exactly
  - `upper_mid` (选填) 单个 UP 主 UID 精确筛选 / Single creator UID for an exact match
  - `folder_id` (选填) 已保存 UP 主文件夹 ID，用于限定文件夹内搜索 / Saved-creator folder ID used to limit the search
  - `marketing_target` (选填) 营销目标：1=品牌曝光，2=心智种草，3=效果转化 / Marketing objective: 1=brand awareness, 2=consideration, 3=conversion
  - `panel_type` (选填) 行业策略面板：0=通用，1=游戏，2=美妆，3=数码，4=汽车，5=效果，6=食饮，8=网服 / Strategy panel: 0=general, 1=gaming, 2=beauty, 3=digital, 4=automotive, 5=performance, 6=food, 8=internet
  - `order_by` (选填) 排序字段，例如 fans_num、play_median、interactive_rate / Sort field, such as fans_num, play_median, or interactive_rate
  - `sort` (选填) 排序方向：desc=降序，asc=升序 / Sort direction: desc=descending, asc=ascending
  - `page` (选填) 页码，从 1 开始，每页返回 20 条 / One-based page number; each page returns 20 records
  - `request_id` (选填) 搜索会话标识；同组条件翻页时复用，留空则生成新值 / Search-session ID; reuse it across pages of the same filter set
  - `gender` (选填) UP 主性别，取值见 /api/v1/bilibili/huahuo/square_static_info 返回的 gender_info / Creator gender from gender_info returned by /api/v1/bilibili/huahuo/square_static_info
  - `min_fans_num` (选填) 粉丝数下限（含）/ Minimum follower count, inclusive
  - `max_fans_num` (选填) 粉丝数上限（含）/ Maximum follower count, inclusive
  - `region_id` (选填) 先调用 /api/v1/bilibili/huahuo/region_drop；把选中一级地域的 value 放入此数组 / Call /api/v1/bilibili/huahuo/region_drop first, then put selected primary-region values in this array
  - `second_region_id` (选填) 先调用 /api/v1/bilibili/huahuo/region_drop；把选中一级地域 children 中的二级 value 放入此数组 / Call /api/v1/bilibili/huahuo/region_drop first, then put selected child-region values in this array
  - `partition_id` (选填) 内容一级分区 ID，取值见 /api/v1/bilibili/huahuo/partition_drop / Primary content-category ID from /api/v1/bilibili/huahuo/partition_drop
  - `second_partition_id` (选填) 内容二级分区 ID 列表，取值见 /api/v1/bilibili/huahuo/partition_drop / Secondary content-category IDs from /api/v1/bilibili/huahuo/partition_drop
  - `mcn_ids` (选填) MCN 机构 ID 列表，取值见 /api/v1/bilibili/huahuo/mcn_drop / MCN organization IDs from /api/v1/bilibili/huahuo/mcn_drop
  - `provider_id` (选填) 服务商 ID 列表，使用花火筛选项的可选值 / Service-provider IDs using values offered by the Huahuo filter
  - `upper_types` (选填) 账号类型：1或4=机构签约，3=个人 / Creator type: 1 or 4=MCN-affiliated, 3=independent
  - `only_contract` (选填) 仅看可签约账号：1=是，0=不限 / Contract-eligible filter: 1=only eligible creators, 0=all
  - `is_painter_order` (选填) 是否筛选画师约稿能力 / Whether to require illustration-commission capability
  - `fans_age_tag` (选填) 粉丝年龄倾向标签，取值见 /api/v1/bilibili/huahuo/square_static_info / Audience age-affinity tags from /api/v1/bilibili/huahuo/square_static_info
  - `fans_gender_tag` (选填) 粉丝性别倾向标签，取值见 /api/v1/bilibili/huahuo/square_static_info / Audience gender-affinity tags from /api/v1/bilibili/huahuo/square_static_info
  - `fans_region_tag` (选填) 粉丝地域倾向标签，取值见 /api/v1/bilibili/huahuo/square_static_info / Audience region-affinity tags from /api/v1/bilibili/huahuo/square_static_info
  - `fans_stick` (选填) 粉丝黏性筛选值，0=不限，其他值取自静态筛选项 / Follower-loyalty filter; 0=all, otherwise use a static-option value
  - `av_active` (选填) 近期投稿活跃开关：1=启用，0=不限 / Recent-publishing activity switch: 1=enabled, 0=all
  - `av_active_tag` (选填) 近期投稿活跃档位，取值见 /api/v1/bilibili/huahuo/square_static_info 返回的 av_active_tag / Recent-publishing activity tier from av_active_tag returned by /api/v1/bilibili/huahuo/square_static_info
  - `dmp_group_id` (选填) DMP 自定义人群包 ID，取值见 /api/v1/bilibili/huahuo/dmp_pkg_list / DMP custom audience-package ID from /api/v1/bilibili/huahuo/dmp_pkg_list
  - `category_dmp_group_id` (选填) 内容类目 DMP 人群包 ID / Content-category DMP audience-package ID
  - `category_dmp_label` (选填) 内容类目 DMP 人群包展示名称 / Display label for the content-category DMP audience package
  - `dmp_pkg_name` (选填) DMP 特殊人群包名称关键词 / DMP special-audience package name query
  - `dmp_pkg_vertical_rate_gte` (选填) DMP 人群垂直度下限：相关视频数占总视频数比例 / Minimum DMP verticality: matching videos divided by all videos
  - `dmp_pkg_vertical_rate_lte` (选填) DMP 人群垂直度上限：相关视频数占总视频数比例 / Maximum DMP verticality: matching videos divided by all videos
  - `dmp_pkg_effect_rate_gte` (选填) DMP 人群影响力下限：近30天相关观众占该人群总量比例 / Minimum DMP influence: recent matching viewers divided by the audience population
  - `dmp_pkg_effect_rate_lte` (选填) DMP 人群影响力上限：近30天相关观众占该人群总量比例 / Maximum DMP influence: recent matching viewers divided by the audience population
  - `dmp_pkg_fan_rate_gte` (选填) DMP 人群关注度下限：粉丝中该人群占比 / Minimum DMP attention: matching audience members divided by all followers
  - `dmp_pkg_fan_rate_lte` (选填) DMP 人群关注度上限：粉丝中该人群占比 / Maximum DMP attention: matching audience members divided by all followers
  - `min_task_price` (选填) 标准合作报价下限，单位为人民币元 / Minimum standard cooperation quote in RMB
  - `max_task_price` (选填) 标准合作报价上限，单位为人民币元 / Maximum standard cooperation quote in RMB
  - `price_info` (选填) 合作报价筛选数组；先调用 /api/v1/bilibili/huahuo/square_static_info 并读取 price_info_options，每次搜索传一个合作类型，每项固定包含六个字段，不适用或未选择的数组传 [] / Cooperation-pricing filters from price_info_options returned by /api/v1/bilibili/huahuo/square_static_info; send one type per search, include all six fields, and use [] for unavailable arrays
  - `last_7_days_set_price` (选填) 近7天是否设置过报价：1=是，0=不限 / Quote-updated-in-7-days filter: 1=yes, 0=all
  - `last_14_days_set_price` (选填) 近14天是否设置过报价：1=是，0=不限 / Quote-updated-in-14-days filter: 1=yes, 0=all
  - `last_30_days_set_price` (选填) 近30天是否设置过报价：1=是，0=不限 / Quote-updated-in-30-days filter: 1=yes, 0=all
  - `min_interact_rate` (选填) 互动率下限；近180天合格原创稿件互动量除以播放量 / Minimum engagement rate for eligible original videos in the last 180 days
  - `max_interact_rate` (选填) 互动率上限；近180天合格原创稿件互动量除以播放量 / Maximum engagement rate for eligible original videos in the last 180 days
  - `blue_url_ctr_gte` (选填) 蓝链点击率下限，即蓝链点击量除以视频播放量 / Minimum blue-link CTR, blue-link clicks divided by video views
  - `blue_url_ctr_lt` (选填) 蓝链点击率上限，即蓝链点击量除以视频播放量 / Maximum blue-link CTR, blue-link clicks divided by video views
  - `blue_url_click_cost_gte` (选填) 蓝链点击成本下限，即合作及投流花费除以蓝链点击量 / Minimum blue-link click cost, cooperation and promotion spend divided by clicks
  - `blue_url_click_cost_lt` (选填) 蓝链点击成本上限，即合作及投流花费除以蓝链点击量 / Maximum blue-link click cost, cooperation and promotion spend divided by clicks
  - `min_play_median` (选填) 播放量中位数下限；统计近180天且发布满7天的合格原创稿件 / Minimum median views for eligible original videos published at least seven days ago
  - `max_play_median` (选填) 播放量中位数上限；统计近180天且发布满7天的合格原创稿件 / Maximum median views for eligible original videos published at least seven days ago
  - `play_median_traffic_type` (选填) 播放中位数流量口径：1=全部流量，2=自然流量 / Median-view traffic scope: 1=all traffic, 2=organic traffic
  - `play_median_cycle` (选填) 播放中位数统计周期：1=7天，2=15天，3=30天 / Median-view window: 1=7 days, 2=15 days, 3=30 days
  - `min_cpm` (选填) CPM 下限，即花费除以播放量再乘1000 / Minimum CPM, calculated as spend divided by views times 1,000
  - `max_cpm` (选填) CPM 上限，即花费除以播放量再乘1000 / Maximum CPM, calculated as spend divided by views times 1,000
  - `cpm_type` (选填) CPM 流量口径：1=全部流量，2=自然流量 / CPM traffic scope: 1=all traffic, 2=organic traffic
  - `cpm_cycle` (选填) CPM 统计周期：1=7天，2=15天，3=30天 / CPM window: 1=7 days, 2=15 days, 3=30 days
  - `min_cpc` (选填) CPC 下限，即花费除以组件点击次数 / Minimum CPC, calculated as spend divided by component clicks
  - `max_cpc` (选填) CPC 上限，即花费除以组件点击次数 / Maximum CPC, calculated as spend divided by component clicks
  - `cpc_traffic_type` (选填) CPC 流量口径：1=全部流量，2=自然流量 / CPC traffic scope: 1=all traffic, 2=organic traffic
  - `cpc_cycle` (选填) CPC 统计周期：1=7天，2=15天，3=30天 / CPC window: 1=7 days, 2=15 days, 3=30 days
  - `cpe_gte` (选填) CPE 下限，即花费除以有效互动次数 / Minimum CPE, calculated as spend divided by valid engagements
  - `cpe_lt` (选填) CPE 上限，即花费除以有效互动次数 / Maximum CPE, calculated as spend divided by valid engagements
  - `cpe_traffic_type` (选填) CPE 流量口径：1=全部流量，2=自然流量 / CPE traffic scope: 1=all traffic, 2=organic traffic
  - `cpe_cycle` (选填) CPE 统计周期：1=7天，3=30天 / CPE window: 1=7 days, 3=30 days
  - `draft_duration` (选填) 主流视频时长：1=0-30秒，2=30-60秒，3=1-3分，4=3-5分，5=5-10分，6=10分以上 / Dominant video duration bucket from under 30 seconds to over 10 minutes
  - `min_avid_cnt` (选填) 近90天有效原创稿件数下限 / Minimum eligible original-video count in the last 90 days
  - `max_avid_cnt` (选填) 近90天有效原创稿件数上限 / Maximum eligible original-video count in the last 90 days
  - `min_hot_avid_rate` (选填) 近90天爆款稿件占比下限 / Minimum viral-video ratio in the last 90 days
  - `max_hot_avid_rate` (选填) 近90天爆款稿件占比上限 / Maximum viral-video ratio in the last 90 days
  - `half_min_hot_avid_cnt` (选填) 近半年爆款稿件数下限 / Minimum viral-video count in the last six months
  - `half_max_hot_avid_cnt` (选填) 近半年爆款稿件数上限 / Maximum viral-video count in the last six months
  - `entry_cost_min` (选填) 近一年相关合作的进店成本下限 / Minimum store-entry cost for relevant cooperation in the last year
  - `entry_cost_max` (选填) 近一年相关合作的进店成本上限 / Maximum store-entry cost for relevant cooperation in the last year
  - `av_honor` (选填) 稿件荣誉没有独立选项接口，取值见 search_upper 文档；honor_type 始终为可多选数组 / Video honors have no separate options endpoint; use the search_upper documentation and always send honor_type as an array
  - `cooperate_experience_industry_ids` (选填) 非通用行业面板先调用 /api/v1/bilibili/huahuo/cooperate_experience_industry，再把选中行业 ID 放入此数组；通用面板不使用此字段 / For non-general panels, call /api/v1/bilibili/huahuo/cooperate_experience_industry first and put selected IDs here; unused by the general panel
  - `cooperate_experience_type` (选填) 非通用行业策略面板的合作经验类型：1=有当前行业经验，2=当前行业经验丰富，3=无当前行业经验，4=有其他行业经验；选择行业时仅使用1或2，通用面板改用 spark_tag / Experience type for non-general strategy panels: 1=experienced, 2=extensive, 3=none in current industry, 4=experience in other industries; use 1 or 2 with selected industries, while the general panel uses spark_tag
  - `special_tags` (选填) 特色标签列表，取值见 /api/v1/bilibili/huahuo/square_static_info / Feature-tag values from /api/v1/bilibili/huahuo/square_static_info
  - `spark_tag` (选填) 花火能力标签；通用面板合作次数使用 cooperate=有合作经验或 coo_frequent=合作经验丰富，并与 /api/v1/bilibili/huahuo/square_static_info 返回的行业树字段配合使用 / Huahuo capability tags; general-panel cooperation count uses cooperate or coo_frequent together with industry-tree values from /api/v1/bilibili/huahuo/square_static_info
  - `square_tag_in` (选填) 广场场景标签，例如 ad_partner_experienced / Marketplace scenario tags such as ad_partner_experienced
  - `label_array` (选填) 先调用 /api/v1/bilibili/huahuo/upper_label_tree；把内容类型分组中所有已选节点的 value 放入同一个内层数组 / Call /api/v1/bilibili/huahuo/upper_label_tree first, then put all selected content-type values in one inner array
  - `bdata_tag_lv5` (选填) B站五级内容标签筛选值列表 / Bilibili level-five content-tag filter values
  - `huahuo_first_industry_ids` (选填) 通用面板先调用 /api/v1/bilibili/huahuo/square_static_info；把 industry_tree 选中路径的一级 ID 放入此数组 / For the general panel, call /api/v1/bilibili/huahuo/square_static_info and put selected primary industry_tree IDs here
  - `huahuo_second_industry_ids` (选填) 通用面板先调用 /api/v1/bilibili/huahuo/square_static_info；把 industry_tree 选中路径的二级 ID 放入此数组 / For the general panel, call /api/v1/bilibili/huahuo/square_static_info and put selected secondary industry_tree IDs here
  - `huahuo_third_industry_ids` (选填) 通用面板先调用 /api/v1/bilibili/huahuo/square_static_info；把 industry_tree 选中路径的三级 ID 放入此数组 / For the general panel, call /api/v1/bilibili/huahuo/square_static_info and put selected tertiary industry_tree IDs here
  - `goods_permission` (选填) 带货权限筛选：1=有权限，0=不限 / Commerce permission filter: 1=required, 0=all
  - `goods_up_levels` (选填) 带货 UP 主等级列表 / Commerce-creator level values
  - `goods_category_first_ids` (选填) 带货一级类目 ID 列表，取值见 /api/v1/bilibili/huahuo/effect_goods_drop / Primary commerce-category IDs from /api/v1/bilibili/huahuo/effect_goods_drop
  - `goods_category_second_ids` (选填) 带货二级类目 ID 列表，取值见 /api/v1/bilibili/huahuo/effect_goods_drop / Secondary commerce-category IDs from /api/v1/bilibili/huahuo/effect_goods_drop
  - `goods_gpm_min` (选填) 近30天 GPM 下限，即每千次带货视频播放产生的支付 GMV / Minimum 30-day GPM, paid GMV per 1,000 commerce-video views
  - `goods_gpm_max` (选填) 近30天 GPM 上限，即每千次带货视频播放产生的支付 GMV / Maximum 30-day GPM, paid GMV per 1,000 commerce-video views
  - `goods_ctr_min` (选填) 带货组件点击率下限，即组件点击数除以曝光数 / Minimum commerce-component CTR, clicks divided by impressions
  - `goods_ctr_max` (选填) 带货组件点击率上限，即组件点击数除以曝光数 / Maximum commerce-component CTR, clicks divided by impressions
  - `goods_ctr_type` (选填) 带货点击率组件口径：1=全部组件，2=评论区组件 / Commerce CTR component scope: 1=all components, 2=comment component
  - `goods_avg_price_min` (选填) 近30天商品平均价格下限，单位为人民币元 / Minimum average product price in the last 30 days, in RMB
  - `goods_avg_price_max` (选填) 近30天商品平均价格上限，单位为人民币元 / Maximum average product price in the last 30 days, in RMB
  - `goods_is_high_video_play_permeate` (选填) 高视频播放渗透筛选，近30天播放用户占粉丝数比例居前20% / High video-view penetration filter, top 20% by recent viewers per follower
  - `goods_is_high_fans_play_permeate` (选填) 高粉丝播放渗透筛选 / High follower-view penetration filter
  - `is_boosting` (选填) 是否筛选内容加热中的 UP 主：1=是，0=不限 / Boosting-status filter: 1=currently boosting, 0=all
  - `is_treasure_up` (选填) 是否筛选宝藏 UP 主 / Whether to filter for treasure creators
  - `is_timely_response` (选填) 是否筛选及时响应的 UP 主 / Whether to require timely-response creators
  - `is_new_enter` (选填) 是否筛选新入驻 UP 主 / Whether to filter for newly onboarded creators
  - `custom_video_pricing_set` (选填) 是否已设置定制视频报价 / Whether custom-video pricing has been configured
  - `is_x_plan_better_up` (选填) 是否筛选 X 计划优选 UP 主 / Whether to filter for X Plan preferred creators
  - `high_potential_type` (选填) 高潜类型：0=全部，1=已入驻，2=未入驻 / High-potential type: 0=all, 1=onboarded, 2=not onboarded
- 示例：

```
```json
{
  "main_search": "智能手机",
  "marketing_target": 1,
  "panel_type": 3,
  "min_fans_num": 100000,
  "max_fans_num": 1000000,
  "min_play_median": 50000,
  "play_median_traffic_type": 1,
  "play_median_cycle": 3,
  "goods_ctr_type": 1,
  "order_by": "play_median",
  "sort": "desc",
  "page": 1
}
```
```

## UP主搜索联想

`GET /api/v1/bilibili/huahuo/search_upper_suggest`

- 用途：根据昵称片段或 UID 返回候选 UP 主，适合搜索框联想和用户选择
- 返回：候选 UP 主列表及分页信息，通常包含 UID、昵称、头像和基础账号信息
- Query：
  - `nickname_or_mids` (必填,string) 昵称片段或 UP 主 UID / Creator nickname fragment or UID
  - `page` (选填,integer) 页码，从 1 开始 / One-based page number
  - `panel_type` (选填,integer) 行业策略面板，取值同 search_upper / Industry strategy panel; values match search_upper
  - `marketing_target` (选填,integer) 营销目标，取值同 search_upper / Marketing objective; values match search_upper
  - `cpm_type` (选填,integer) CPM 流量口径：1=全部流量，2=自然流量 / CPM traffic scope: 1=all, 2=organic
  - `cpm_cycle` (选填,integer) CPM 统计周期：1=7天，2=15天，3=30天 / CPM window: 1=7, 2=15, 3=30 days
  - `play_median_traffic_type` (选填,integer) 播放中位数流量口径：1=全部流量，2=自然流量 / Median-view traffic scope: 1=all, 2=organic
  - `play_median_cycle` (选填,integer) 播放中位数周期：1=7天，2=15天，3=30天 / Median-view window: 1=7, 2=15, 3=30 days
- 示例：

```
```text
GET /search_upper_suggest?nickname_or_mids=小电视&page=1&panel_type=0
    &marketing_target=1&cpm_type=1&cpm_cycle=3
    &play_median_traffic_type=1&play_median_cycle=3
```
```

## 直播广场搜索

`POST /api/v1/bilibili/huahuo/search_live_upper`

- 用途：在直播合作广场检索适合内容直播或带货直播合作的主播；按主播属性、粉丝画像、直播分区、直播表现、公会、主营类目和 GMV 筛选
- 返回：`total_count`: 匹配主播总数；`data`: 主播列表，包含基础资料、粉丝画像、直播表现及相应合作能力指标
- Body(JSON)：
  - `nickname_or_mids` (选填) 按UP主昵称或UID搜索
  - `mids` (选填) 按UID批量精确匹配
  - `is_brand_live` (选填) 直播类型：1=内容直播 0=带货直播。两种类型可用的筛选项不同
  - `gender` (选填) 主播性别
  - `region_id` (选填) 主播常驻地域（一级）
  - `second_region_id` (选填) 主播常驻地域（二级）
  - `min_fans_num` (选填) 粉丝数下限
  - `max_fans_num` (选填) 粉丝数上限
  - `fans_gender_tag` (选填) 粉丝性别标签
  - `fans_age_tag` (选填) 粉丝年龄标签
  - `fans_region_tag` (选填) 粉丝地域标签
  - `live_subarea_id` (选填) 直播分区（二级），取值见 live_area_list
  - `partition_id` (选填) 投稿分区（一级）
  - `second_partition_id` (选填) 投稿分区（二级）
  - `min_popularity` (选填) 近30天场均人气峰值下限
  - `max_popularity` (选填) 近30天场均人气峰值上限
  - `live_audience_h_avg_30d_min` (选填) 近30天时均观众数下限
  - `live_audience_h_avg_30d_max` (选填) 近30天时均观众数上限
  - `live_danmu_h_avg_30d_min` (选填) 近30天时均弹幕数下限
  - `live_danmu_h_avg_30d_max` (选填) 近30天时均弹幕数上限
  - `live_guild_id` (选填) 直播公会，取值见 live_guild_drop
  - `high_potential_type` (选填) 入驻状态
  - `live_good_category` (选填) 主营类目，0=全部，取值见 live_good_category
  - `live_good_gmv` (选填) 近90天GMV档位，0=全部
  - `order_by` (选填) 排序字段
  - `sort` (选填) 排序方向：desc 或 asc
  - `page` (选填) 页码，从 1 开始，每页固定 20 条

## UP主详情

`GET /api/v1/bilibili/huahuo/upper_detail`

- 用途：获取指定 UP 主的完整商业合作画像，用于达人评估、投放选人和合作报价分析
- 返回：基础资料、合作报价 `upper_prices`、数据概览 `overview_v3`、内容与人设标签；稿件分区及时长分布、粉丝画像 `*_distributions`，以及播放受众画像
- Query：
  - `upper_mid` (必填,integer) UP主UID

## UP主稿件数据趋势

`GET /api/v1/bilibili/huahuo/upper_draft_trend`

- 用途：分析指定 UP 主近期稿件在播放、互动或播放时长方面的变化趋势
- 返回：指标趋势序列、中位数、最大值和最小值，以及逐条稿件的指标明细
- Query：
  - `upper_mid` (必填,integer) UP主UID
  - `trend_type` (选填,integer) 指标：3=播放量 4=点赞量 5=评论量 6=弹幕量 7=播放时长

## UP主粉丝增长趋势

`GET /api/v1/bilibili/huahuo/upper_fans_trend`

- 用途：查看指定 UP 主的粉丝规模和增长速度，用于判断账号成长性与稳定性
- 返回：逐日粉丝趋势，以及近 7、30、90、180、365 天的增长量和增长率
- Query：
  - `upper_mid` (必填,integer) UP主UID
  - `query_type` (选填,integer) 口径：1=总量 2=增量

## 粉丝重合UP主

`GET /api/v1/bilibili/huahuo/upper_overlap_uppers`

- 用途：查找与目标 UP 主受众重合度较高的其他创作者，用于竞品分析和达人扩展
- 返回：重合 UP 主列表、受众重合指标、创作者基础信息及分页信息
- Query：
  - `upper_mid` (必填,integer) UP主UID
  - `fans_range` (选填,string) 粉丝量级档位：9=200万以上 8=100~200万 7=50~100万 6=30~50万 5=20~30万 4=10~20万 3=5~10万 2=1~5万
  - `page` (选填,integer)

## 内容相似UP主

`GET /api/v1/bilibili/huahuo/upper_similar`

- 用途：发现与指定 UP 主内容方向相近的创作者，用于拓展同类达人候选池
- 返回：内容相似 UP 主数组，包含 UID、昵称、头像及相似度相关信息
- Query：
  - `upper_mid` (必填,integer) UP主UID

## UP主代表作

`GET /api/v1/bilibili/huahuo/upper_representative`

- 用途：获取指定 UP 主的个人或商业代表作，用于快速评估内容质量与商业案例
- 返回：代表作列表，包含稿件标识、标题、封面、时长、播放量和稿件亮点标记
- Query：
  - `upper_mid` (必填,integer) UP主UID
  - `type` (选填,integer) 作品类型：1=个人作品 2=商业作品

## UP主稿件表现

`GET /api/v1/bilibili/huahuo/upper_draft_performance`

- 用途：汇总指定周期内 UP 主稿件的内容结构和流量表现
- 返回：稿件分区分布、视频时长分布、流量来源分布及相关汇总指标
- Query：
  - `upper_mid` (必填,integer) UP主UID
  - `day_range` (选填,integer) 统计周期：1=近30天 2=近90天 3=近180天

## UP主稿件高光

`GET /api/v1/bilibili/huahuo/upper_archive_highlights`

- 用途：查看指定 UP 主在选定周期内的稿件高光表现，识别高潜力内容
- 返回：全站 TOP、热门稿件、超值稿件等高光标记及其聚合统计
- Query：
  - `upper_mid` (必填,integer) UP主UID
  - `day_range` (选填,integer) 统计周期：1=近30天 2=近90天 3=近180天

## UP主基础信息

`GET /api/v1/bilibili/huahuo/upper_base_info`

- 用途：获取 UP 主的基础身份信息和可支持的合作形式
- 返回：UID、昵称、头像、所属 MCN，以及支持的合作类型 `state_types`
- Query：
  - `mid` (必填,integer) UP主UID

## UP主询单配置

`GET /api/v1/bilibili/huahuo/upper_seek_info`

- 用途：查询指定 UP 主可接受的合作询单类型及相关能力配置
- 返回：询单状态、支持的合作类型和相关配置字段
- Query：
  - `mid` (必填,integer) UP主UID

## UP主档期占用

`GET /api/v1/bilibili/huahuo/upper_busy_time`

- 用途：查询指定 UP 主的档期占用情况，辅助安排合作发布时间
- 返回：已占用或不可用的档期日期列表及相关日程信息
- Query：
  - `mid` (必填,integer) UP主UID

## 按昵称查UP主

`GET /api/v1/bilibili/huahuo/upper_by_nickname`

- 用途：按完整或部分昵称查找 UP 主，适合从名称定位 UID 和基础资料
- 返回：匹配 UP 主列表，包含 UID、昵称、头像及基础账号信息
- Query：
  - `nickname` (必填,string) UP主昵称

## 直播UP主详情

`GET /api/v1/bilibili/huahuo/live_upper_portrait`

- 用途：获取主播在直播维度的详细画像，用于评估内容直播合作能力
- 返回：主播基础资料、直播表现、观众规模、互动指标、直播标签和合作能力信息
- Query：
  - `mcn_id` (必填,integer) MCN机构ID，可从广场搜索结果或 upper_base_info 取得
  - `upper_mid` (选填) UP主UID，可选

## 直播带货能力

`GET /api/v1/bilibili/huahuo/live_commerce_info`

- 用途：查询指定 UP 主的直播带货能力和近期商业表现
- 返回：直播带货场次、商品类目、成交表现、观众与互动等商业指标
- Query：
  - `upper_mid` (必填,integer) UP主UID

## UP主榜单

`GET /api/v1/bilibili/huahuo/popular_up_list`

- 用途：获取成长黑马、超值优选或头部必选 UP 主榜单，辅助快速发现优质达人
- 返回：UP 主排名、基础资料和榜单指标。成长黑马榜侧重粉丝增量，超值优选榜侧重
- Query：
  - `rank_cate` (选填,integer) 榜单类型：1=成长黑马榜 2=超值优选榜 3=头部必选榜
  - `tid_name` (选填,string) 榜单分区名，取值见 popular_up_tid_drop，空=全部
  - `page` (选填,integer)

## X火榜行业下拉

`GET /api/v1/bilibili/huahuo/x_huo_industry_drop`

- 用途：获取 X 火榜可用的两级行业树，为种草榜和商品榜提供行业 ID
- 返回：两级行业列表；节点 `id` 可作为相应榜单接口的 `x_huo_industry_id`
- Query：
  - `scene` (选填,integer) 场景：1=UP主榜 2=商品榜

## X火榜可选期数

`GET /api/v1/bilibili/huahuo/x_huo_date_options`

- 用途：获取 X 火榜可查询的月度或季度期数，便于构造 `popular_up_x_huo` 请求
- 返回：按时间升序排列的 `YYYY-MM` 期数列表；最后一项为最新已结束周期，
- Query：
  - `rank_date_type` (选填,integer) 榜单周期：1=月度榜 2=季度榜

## X火种草榜

`GET /api/v1/bilibili/huahuo/popular_up_x_huo`

- 用途：获取指定行业和周期的 X 火种草 UP 主榜单，用于行业达人选取和趋势分析
- 返回：UP 主排名、账号资料、行业相关度和种草表现指标，以及分页信息
- Query：
  - `x_huo_industry_id` (必填,integer) 行业ID，取值见 x_huo_industry_drop
  - `rank_date_type` (选填,integer) 榜单周期：1=月度榜 2=季度榜
  - `rank_date` (选填) 榜单期数 `YYYY-MM`，取值见 x_huo_date_options；留空取最新一期
  - `page` (选填,integer)

## X火商品榜

`GET /api/v1/bilibili/huahuo/popular_goods_list`

- 用途：获取指定行业的 X 火商品榜，分析热门商品及其内容带货表现
- 返回：商品排名、商品信息、价格、行业和带货表现指标，以及分页信息
- Query：
  - `x_huo_industry_id` (必填,integer) 行业ID，取值见 x_huo_industry_drop?scene=2
  - `page` (选填,integer)
  - `rank_type` (选填) 榜单口径
  - `data_cycle` (选填) 数据周期
  - `min_goods_price` (选填) 商品价格下限
  - `max_goods_price` (选填) 商品价格上限

## 商品带货UP主榜

`GET /api/v1/bilibili/huahuo/popular_goods_up_list`

- 用途：查询指定商品下带货表现较好的 UP 主，辅助寻找同品合作达人
- 返回：UP 主排名、账号资料及该商品相关的带货表现指标和分页信息
- Query：
  - `goods_id` (必填,integer) 商品ID，取值见 popular_goods_list
  - `page` (选填,integer)

## 行业带货UP主榜

`GET /api/v1/bilibili/huahuo/popular_goods_industry_up_list`

- 用途：查询指定商品行业下带货表现较好的 UP 主，辅助行业达人筛选
- 返回：行业带货 UP 主排名、账号资料、带货表现指标及分页信息
- Query：
  - `x_huo_industry_id` (必填,integer) 行业ID，取值见 x_huo_industry_drop?scene=2
  - `page` (选填,integer)

## UP主榜单分区下拉

`GET /api/v1/bilibili/huahuo/popular_up_tid_drop`

- 用途：获取 UP 主榜单支持的内容分区名称，用于构造 `popular_up_list` 的 `tid_name`
- 返回：可用分区名称列表及相应展示信息

## 视频榜单

`GET /api/v1/bilibili/huahuo/popular_avid_list`

- 用途：获取花火视频榜单，查看指定行业或全部行业的高表现商业内容
- 返回：视频排名、稿件标识、标题、封面、UP 主资料、播放与互动表现及分页信息
- Query：
  - `category` (选填,string) 行业名，取值见 popular_avid_category_drop，空=全部
  - `page` (选填,integer)

## 视频榜单行业下拉

`GET /api/v1/bilibili/huahuo/popular_avid_category_drop`

- 用途：获取花火视频榜支持的行业名称，用于筛选 `popular_avid_list`
- 返回：视频榜可用行业名称列表及展示信息

## 广场筛选字典

`GET /api/v1/bilibili/huahuo/square_static_info`

- 用途：获取内容合作广场常用筛选项的完整取值字典，用于构建搜索表单
- 返回：`fans_age_tag`、`fans_gender_tag`、`fans_region_tag`: 粉丝画像筛选项；`gender_info`: UP 主性别筛选项；`av_active_tag`: 近期投稿活跃筛选项；特色标签及子项，以及 `data.industry_tree` 三级合作行业树；`data.price_info_options`: `search_upper.price_info` 的合作报价字典：

## 搜UP主筛选面板配置

`GET /api/v1/bilibili/huahuo/upper_label_tree`

- 用途：获取指定行业策略面板支持的 UP 主筛选配置，用于动态展示可用条件
- 返回：筛选分组、字段、标签、可选值及展示顺序组成的配置树；`search_upper.label_array` 仅使用“内容类型”分组节点的 `value`；所有选中的
- Query：
  - `panel_type` (选填,integer) 行业策略面板：0=通用，1=游戏，2=美妆，3=数码，4=汽车，5=效果，6=食饮，8=网服 / Strategy panel: 0=general, 1=gaming, 2=beauty, 3=digital, 4=automotive, 5=performance, 6=food, 8=internet

## MCN机构下拉

`GET /api/v1/bilibili/huahuo/mcn_drop`

- 用途：获取可用于 UP 主搜索筛选的 MCN 机构列表
- 返回：MCN 机构 ID、名称及相关展示信息；将选中机构的 ID 放入
- Query：
  - `name` (选填,string) 按名称模糊过滤，空=全部

## 地域下拉

`GET /api/v1/bilibili/huahuo/region_drop`

- 用途：获取 UP 主常驻地域筛选所需的省市层级字典
- 返回：把选中一级地域节点的 `value` 放入 `search_upper.region_id`；把选中一级节点

## 稿件分区下拉

`GET /api/v1/bilibili/huahuo/partition_drop`

- 用途：获取稿件内容分区字典，用于按创作领域筛选 UP 主或内容
- 返回：一级和二级稿件分区 ID、名称及父子关系；将选中的一级 ID 填入

## 人群包列表

`GET /api/v1/bilibili/huahuo/dmp_pkg_list`

- 用途：获取当前广告主可选择的自定义人群包，用于受众匹配相关筛选
- 返回：人群包 ID、名称、标签及可用的受众匹配指标；将选中的自定义人群包 ID

## 带货类目下拉

`GET /api/v1/bilibili/huahuo/effect_goods_drop`

- 用途：获取内容带货筛选支持的商品类目字典
- 返回：商品类目 ID、名称和层级关系；将选中的一级、二级 ID 分别放入

## 直播公会下拉

`GET /api/v1/bilibili/huahuo/live_guild_drop`

- 用途：获取直播合作广场可筛选的直播公会列表
- 返回：直播公会 ID、名称及相关展示信息
- Query：
  - `name` (选填,string) 按名称模糊过滤，空=全部

## 合作经验行业列表

`GET /api/v1/bilibili/huahuo/cooperate_experience_industry`

- 用途：获取非通用行业策略面板可用于合作经验筛选的细分行业列表。通用面板
- 返回：将选中行业的 ID 放入 `search_upper.cooperate_experience_industry_ids`；同时设置 `search_upper.cooperate_experience_type`：未选行业时可用
- Query：
  - `industry_type` (必填,integer) 行业序号：1=游戏 2=日化/小家电 3=数码家电 4=汽车 5=食饮 6=网服

## 直播分区下拉

`GET /api/v1/bilibili/huahuo/live_area_list`

- 用途：获取直播内容分区字典，用于直播合作广场的主播筛选
- 返回：一级和二级直播分区 ID、名称及父子关系

## 直播人设标签

`GET /api/v1/bilibili/huahuo/live_parent_tag`

- 用途：获取直播主播的人设标签，用于描述主播风格和内容定位
- 返回：直播人设标签 ID、名称及展示信息

## 直播带货类目

`GET /api/v1/bilibili/huahuo/live_good_category`

- 用途：获取直播带货主营商品类目，用于筛选具有相应品类经验的主播
- 返回：直播带货商品类目 ID、名称及展示顺序

## 人设标签字典

`GET /api/v1/bilibili/huahuo/tag_character`

- 用途：获取描述 UP 主个人形象和账号定位的人设标签字典
- 返回：人设标签 ID、名称及相关展示信息

## 职业标签字典

`GET /api/v1/bilibili/huahuo/tag_occupation`

- 用途：获取描述 UP 主职业身份的标签字典，用于达人画像和筛选
- 返回：职业标签 ID、名称及相关展示信息

## 商业标签字典

`GET /api/v1/bilibili/huahuo/tag_commercial`

- 用途：获取描述 UP 主商业合作特征和能力的标签字典
- 返回：商业标签 ID、名称及相关展示信息

## 行业标签字典

`GET /api/v1/bilibili/huahuo/industry_tags`

- 用途：获取广告主业务和内容合作场景可使用的行业标签字典
- 返回：行业标签 ID、名称及分类信息

## 内容风格字典

`GET /api/v1/bilibili/huahuo/label_char_style`

- 用途：获取描述 UP 主内容表达方式和视觉风格的标签字典
- 返回：内容风格标签 ID、名称及相关展示信息

## 当前广告主账号信息

`GET /api/v1/bilibili/huahuo/account_session_info`

- 用途：获取当前广告主账号的基础身份和角色信息，便于确认数据所属业务主体
- 返回：广告主 ID、用户 ID、用户名、操作者类型、UID 名称、MID 等账号字段
