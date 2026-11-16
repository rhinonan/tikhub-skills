# Douyin Creator API（创作者中心 V1）

文件夹 `Douyin-Creator-API` · 17 个接口 · BASE `https://api.tikhub.io`

## 获取创作者活动详情

`GET /api/v1/douyin/creator/fetch_creator_activity_detail`

- 用途：获取抖音创作者活动详情数据
- 返回：创作者活动详情数据
- Query：
  - `activity_id` (必填,string) 活动ID/Activity ID

## 获取创作者活动列表

`GET /api/v1/douyin/creator/fetch_creator_activity_list`

- 用途：获取抖音创作者活动列表数据
- 返回：创作者活动列表数据
- Query：
  - `start_time` (必填,integer) 开始时间戳/Start timestamp
  - `end_time` (必填,integer) 结束时间戳/End timestamp

## 获取创作者内容创作合集分类

`GET /api/v1/douyin/creator/fetch_creator_content_category`

- 用途：获取抖音创作者平台内容创作的合集分类列表
- 返回：内容创作合集分类数据

## 获取创作者内容创作课程

`GET /api/v1/douyin/creator/fetch_creator_content_course`

- 用途：获取抖音创作者平台指定分类的内容创作课程
- 返回：指定分类的内容创作课程数据
- Query：
  - `category_id` (必填,integer) 分类ID/Category ID
  - `order` (integer,默认 1) 排序方式/Order type (1=推荐排序, 2=最受欢迎, 3=最新上传)
  - `limit` (integer,默认 24) 每页数量/Items per page
  - `offset` (integer,默认 0) 偏移量/Offset (starting position)

## 获取创作者热门挑战榜单

`GET /api/v1/douyin/creator/fetch_creator_hot_challenge_billboard`

- 用途：获取抖音创作者平台热门挑战榜单数据
- 返回：热门挑战榜单数据

## 获取创作者热门课程

`GET /api/v1/douyin/creator/fetch_creator_hot_course`

- 用途：获取抖音创作者平台热门课程数据或精选专题课程
- 返回：热门课程数据或精选专题课程数据
- Query：
  - `order` (integer,默认 1) 排序方式/Order type (1=推荐排序, 2=最受欢迎, 3=最新上传)
  - `limit` (integer,默认 24) 每页数量/Items per page (建议24)
  - `offset` (integer,默认 0) 偏移量/Offset
  - `category_id` 精选专题分类ID/Selected topic category ID - 不传则为热门课程，传入则为精选专题         可选值/Available values:         6976547830546582816=知识品类, 6976547923849006336=生活品类, 6976547940311633165=娱乐品类,         6976547972108635404=美食品类, 6980288134957272352=正能量, 6980288181744766219=游戏品类,         6980288219548011776=通用

## 获取创作者热门音乐榜单

`GET /api/v1/douyin/creator/fetch_creator_hot_music_billboard`

- 用途：获取抖音创作者平台热门音乐榜单数据
- 返回：热门音乐榜单数据
- Query：
  - `billboard_tag` (integer,默认 0) 榜单标签/Billboard tag (0=全部，具体分类值可通过配置接口获取)
  - `order_key` (integer,默认 1) 排序键/Order key (1=播放最高, 2=点赞最多, 4=热度最高, 5=投稿最多)
  - `time_filter` (integer,默认 1) 时间筛选/Time filter (1=24小时, 2=7天, 3=30天)

## 获取创作者热门道具榜单

`GET /api/v1/douyin/creator/fetch_creator_hot_props_billboard`

- 用途：获取抖音创作者热门道具榜单数据
- 返回：创作者热门道具榜单数据
- Query：
  - `billboard_tag` (integer,默认 0) 榜单标签，0=全部，其他值请通过config接口获取/Billboard tag, 0=all, other values can be obtained through config interface
  - `order_key` (integer,默认 1) 排序键: 1=播放最高, 5=投稿最多, 6=展现最高, 7=收藏最高/Order key: 1=highest views, 5=most submissions, 6=highest exposure, 7=most favorites
  - `time_filter` (integer,默认 1) 时间筛选: 1=24小时, 2=7天, 3=30天/Time filter: 1=24 hours, 2=7 days, 3=30 days

## 获取创作者中心创作热点

`GET /api/v1/douyin/creator/fetch_creator_hot_spot_billboard`

- 用途：获取抖音创作者热点榜单数据
- 返回：创作者热点榜单数据
- Query：
  - `billboard_tag` (string,默认 0) 热点标签，多个标签用逗号分隔，如'1004,1000,1002'/Hot spot tag - multiple tags separated by comma, like '1004,1000,1002'
  - `hot_search_type` (integer,默认 1) 热搜类型: 1=热点总榜, 2=同城热点榜, 3=热点上升榜/Hot search type: 1=Overall ranking, 2=Local ranking, 3=Rising ranking
  - `city_code` 城市代码，当hot_search_type=2时必需/City code - required when hot_search_type=2

## 获取创作者热门话题榜单

`GET /api/v1/douyin/creator/fetch_creator_hot_topic_billboard`

- 用途：获取抖音创作者热门话题榜单数据
- 返回：创作者热门话题榜单数据
- Query：
  - `billboard_tag` (integer,默认 0) 榜单标签，0=全部，其他值请通过config接口获取/Billboard tag, 0=all, other values can be obtained through config interface
  - `order_key` (integer,默认 1) 排序键: 1=播放最高, 2=点赞最多, 3=评论最多, 4=投稿最多/Order key: 1=highest views, 2=most likes, 3=most comments, 4=most submissions
  - `time_filter` (integer,默认 1) 时间筛选: 1=24小时, 2=7天, 3=30天/Time filter: 1=24 hours, 2=7 days, 3=30 days

## 获取创作者中心热门视频榜单

`GET /api/v1/douyin/creator/fetch_creator_material_center_billboard`

- 用途：获取抖音创作者中心热门视频榜单数据
- 返回：创作者中心热门视频榜单数据
- Query：
  - `billboard_tag` (integer,默认 0) 榜单标签，0=全部，其他值请通过config接口获取/Billboard tag, 0=all, other values can be obtained through config interface
  - `order_key` (integer,默认 1) 排序键: 1=播放最高, 2=点赞最多, 3=评论最多, 4=热度最高/Order key: 1=highest views, 2=most likes, 3=most comments, 4=highest popularity
  - `time_filter` (integer,默认 1) 时间筛选: 1=24小时, 2=7天, 3=30天/Time filter: 1=24 hours, 2=7 days, 3=30 days

## 获取创作者中心配置

`GET /api/v1/douyin/creator/fetch_creator_material_center_config`

- 用途：获取抖音创作者中心配置信息
- 返回：创作者中心配置数据

## 获取话题

`GET /api/v1/douyin/creator/fetch_creator_material_center_related`

- 用途：获取抖音创作者中心某个话题/热点/道具/音乐的相关视频列表
- 返回：该 query_id 对应的相关视频列表数据
- Query：
  - `query_id` (必填,string) 查询ID/Query ID (话题ID/热点ID，从其他榜单接口获取)
  - `billboard_type` (integer,默认 2) 榜单类型/Billboard type (2=热点, 3=话题, 4=道具, 5=音乐)
  - `limit` (integer,默认 20) 每页数量/Items per page
  - `offset` (integer,默认 0) 偏移量/Offset

## 获取行业分类配置

`GET /api/v1/douyin/creator/fetch_industry_category_config`

- 用途：获取抖音创作者平台的行业分类配置
- 返回：返回完整的行业分类树结构

## 获取商单任务列表

`GET /api/v1/douyin/creator/fetch_mission_task_list`

- 用途：获取抖音创作者平台的商单任务列表
- 返回：返回符合条件的商单任务列表
- Query：
  - `cursor` (integer,默认 0) 游标/Cursor (分页)
  - `limit` (integer,默认 24) 每页数量/Items per page
  - `mission_type` (integer,默认 1) 任务类型/Mission type
  - `tab_scene` (integer,默认 1) 场景类型/Scene type (1=可投稿, 2=可报名, 3=好物测评)
  - `industry_lv1` (integer,默认 -1) 一级行业/Primary industry (-1=全部)
  - `industry_lv2` (integer,默认 -1) 二级行业/Secondary industry (-1=全部)
  - `platform_channel` 平台渠道/Platform channel (1=抖音视频, 2=抖音直播, 3=抖音图文)
  - `pay_type` 付费类型/Pay type (1=视频等级, 2=自定义, 3=按转化付费, 4=按有效播放量, 5=按销售量, 9=按核销量, 14=按付费分佣)
  - `greater_than_cost_progress` 成本进度/Cost progress (20=高于20%, 50=高于50%, 80=高于80%)
  - `publish_time_start` 发布开始时间/Publish start time (时间戳)
  - `quick_selector_scene` 快速选择场景/Quick selector (1=高收益, 4=保底收入, 5=合作过)
  - `keyword` 关键词/Keyword (任务名称或ID)

## 搜索用户

`GET /api/v1/douyin/creator/fetch_user_search`

- 用途：搜索抖音用户，支持抖音号和抖音昵称搜索
- 返回：最多返回20个匹配的用户信息
- Query：
  - `user_name` (必填,string) 用户名/Username (支持抖音号和抖音昵称)

## 获取作品弹幕列表

`GET /api/v1/douyin/creator/fetch_video_danmaku_list`

- 用途：获取指定作品的弹幕列表，支持管理和筛选弹幕
- 返回：作品弹幕列表数据
- Query：
  - `item_id` (必填,string) 作品ID/Video item ID
  - `count` (integer,默认 20) 每页数量/Items per page
  - `offset` (integer,默认 0) 偏移量/Offset (starting position)
  - `order_type` (integer,默认 1) 排序类型/Order type (1=时间排序, 2=其他排序)
  - `is_blocked` (boolean,默认 False) 是否被屏蔽/Is blocked
