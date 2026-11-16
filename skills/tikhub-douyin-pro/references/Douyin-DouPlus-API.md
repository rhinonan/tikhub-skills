# Douyin DouPlus API（抖+ 投放）

文件夹 `Douyin-DouPlus-API` · 17 个接口 · BASE `https://api.tikhub.io`

## DOU+成本计算

`POST /api/v1/douyin/douplus/calculate_cost`

- 用途：DOU+ 成本计算：给定投放账号 + 作品 + 推广目标，返回各预算档位的预估（套餐 / 价格 / 预计效果）
- 返回：各预算档位的套餐 / 价格 / 预计效果
- Body(JSON)：
  - `cookie` (必填,string) 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `sec_uid` (必填,string) 投放账号的 sec_uid/Delivery account sec_uid
  - `item_ids` (必填,string) 作品ID,多个用逗号分隔/Item id(s), comma separated
  - `target_id` (默认 31) 推广目标ID/Promotion target id. 31=点赞评论量, 32=粉丝量, 33=主页浏览量, 37=视频播放量, 45=评论链接点击, 78=高质量互动

## 投放数据明细

`POST /api/v1/douyin/douplus/fetch_analyse_detail`

- 用途：DOU+ 投放数据明细（逐订单 / 逐作品的指标列表，支持分页与排序），账号 / 视频 / 直播由 query.analysisType 区分
- 返回：明细列表数据（含分页信息）
- Body(JSON)：
  - `cookie` (必填,string) 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `query` (必填,object) 分析查询对象/Analysis query object. 关键字段/key fields: startTime,endTime(秒级时间戳字符串/second timestamp string); analysisType(1=账号/account, 2=视频/video, 3=直播/live); authorSecIdList(账号 sec_uid 列表); statusList(投放状态过滤); metrics(指标列表,如 stat_cost,total_play,total_like,dy_comment,dy_share,dy_follow); SecondaryTargetIds; CollectWayIds. graph 额外/extra: dimension; detail 额外/extra: page,limit,orderByMetric,orderByType; 视频/直播分析额外/extra: liveRoomIdList

## 投放数据趋势图

`POST /api/v1/douyin/douplus/fetch_analyse_graph`

- 用途：DOU+ 投放数据趋势图（按时间维度返回指标曲线），账号 / 视频 / 直播由 query.analysisType 区分
- 返回：趋势图数据（各时间点的指标值）
- Body(JSON)：
  - `cookie` (必填,string) 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `query` (必填,object) 分析查询对象/Analysis query object. 关键字段/key fields: startTime,endTime(秒级时间戳字符串/second timestamp string); analysisType(1=账号/account, 2=视频/video, 3=直播/live); authorSecIdList(账号 sec_uid 列表); statusList(投放状态过滤); metrics(指标列表,如 stat_cost,total_play,total_like,dy_comment,dy_share,dy_follow); SecondaryTargetIds; CollectWayIds. graph 额外/extra: dimension; detail 额外/extra: page,limit,orderByMetric,orderByType; 视频/直播分析额外/extra: liveRoomIdList

## 投放数据概览(账号

`POST /api/v1/douyin/douplus/fetch_analyse_overview`

- 用途：DOU+ 投放数据概览，支持账号 / 视频 / 直播三种维度（由 query.analysisType 区分：1=账号, 2=视频, 3=直播）
- 返回：概览统计数据
- Body(JSON)：
  - `cookie` (必填,string) 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `query` (必填,object) 分析查询对象/Analysis query object. 关键字段/key fields: startTime,endTime(秒级时间戳字符串/second timestamp string); analysisType(1=账号/account, 2=视频/video, 3=直播/live); authorSecIdList(账号 sec_uid 列表); statusList(投放状态过滤); metrics(指标列表,如 stat_cost,total_play,total_like,dy_comment,dy_share,dy_follow); SecondaryTargetIds; CollectWayIds. graph 额外/extra: dimension; detail 额外/extra: page,limit,orderByMetric,orderByType; 视频/直播分析额外/extra: liveRoomIdList

## 获取DOU+预计投放效果

`POST /api/v1/douyin/douplus/fetch_delivery_effect_estimate`

- 用途：获取指定作品在给定推广目标、预算和投放时长下的预计投放效果
- 返回：当前预算、时长和推广目标对应的预计投放效果数据
- Body(JSON)：
  - `item_ids` (必填,string) 作品ID,多个用逗号分隔;单作品通常配合 schema=0,多作品配合 schema=3/Item id(s), comma separated; normally use schema=0 for one item and schema=3 for multiple items
  - `external_action` (integer,默认 44) 优化动作编码,需与 target_id 对应,默认44(NativeAction);常用:45=点赞,46=关注,47=评论,51=链接点击,102=多互动,181=主页访问/Optimization action code; must match target_id, default 44 (NativeAction). Common values: 45=like, 46=follow, 47=comment, 51=link click, 102=multiple native actions, 181=homepage visit
  - `target_id` (integer,默认 31) 推广目标ID,默认31(点赞评论量);常用:32=粉丝量,33=主页访问,37=视频播放,40=直播间人气,45=评论链接点击,63=粉丝展示,78=自然流量提升,81=高互动频次/Promotion target id, default 31 (likes and comments). Common values: 32=followers, 33=homepage visits, 37=video plays, 40=live popularity, 45=comment-link clicks, 63=show to followers, 78=natural promotion, 81=high interaction frequency
  - `schema` (integer,默认 0) 投放场景编码:0=单作品默认(Default),3=多作品批量投放(BatchDelivery);官方前端按 item_ids 数量选择/Delivery schema: 0=single-item Default, 3=multi-item BatchDelivery; the official client selects it from the item count
  - `is_max_cv` (boolean,默认 True) 是否使用MaxCV最大转化量模式预估;官方前端会根据优化目标能力、素材数量、预算及是否手动出价计算,默认true/Whether to estimate in MaxCV (maximum-conversion-volume) mode; the official client derives it from target capability, item count, budget and manual-bid state, default true
  - `pay_type` (integer,默认 1) 支付通道类型:0=CashDesk,1=IAP,2=Caijing,3=CgTradeCash;官方预计效果调用固定传1/Payment channel: 0=CashDesk, 1=IAP, 2=Caijing, 3=CgTradeCash; the official estimate request uses 1
  - `cost_int` (integer,默认 30000) 投放预算,单位为厘(人民币1/1000元),默认30000(30元)/Delivery budget in li (CNY 1/1000), default 30000 (CNY 30)
  - `duration_seconds` (integer,默认 21600) 投放时长,单位为秒,默认21600(6小时)/Delivery duration in seconds, default 21600 (6 hours)

## 获取可推广作品列表(含点赞评论量)

`POST /api/v1/douyin/douplus/fetch_promotable_item_list`

- 用途：获取指定抖音账号在 DOU+ 投放页可推广的作品列表，包含每个作品的点赞、评论、播放等数据
- 返回：可推广作品列表数据（含作品ID、标题、封面、点赞量、评论量、播放量等）
- Body(JSON)：
  - `sec_uid` (必填,string) 投放账号的 sec_uid/Delivery account sec_uid
  - `count` (默认 30) 返回作品数量/Number of items
  - `target_id` (默认 31) 推广目标(DOU+ 页面上的目标卡片)ID/Promotion target id (the goal card on the page). 31=点赞评论量, 32=粉丝量, 33=主页浏览量, 37=视频播放量, 40=直播间人气, 45=评论链接点击, 63=展示给粉丝, 78=高质量互动. 仅用于按推广目标筛选可投作品;只拉作品列表用默认 31 即可/Only filters promotable items by goal; keep 31 for a plain video list
  - `aim_ids` 可选高级参数:投放优化目标编码,多个逗号分隔;留空即可(按 target_id 自动匹配),一般无需填写/Optional advanced param: optimization objective code(s), comma separated; leave empty (auto-matched by target_id), usually no need to set

## 获取投放过的账号

`POST /api/v1/douyin/douplus/fetch_promoted_accounts`

- 用途：获取当前 DOU+ 账户下投放过（有过订单）的抖音账号列表，支持游标翻页
- 返回：投放过的账号列表（含昵称、sec_uid 等）
- Body(JSON)：
  - `cookie` (必填,string) 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `limit` (默认 20) 每页账号数量/Number of accounts per page
  - `cursor` 翻页游标,首页留空,后续传上一页响应里的 sortID 值/Pagination cursor, empty for first page, then pass the `sortID` value from the previous response

## 获取DOU+ POST请求所需的sec_token

`POST /api/v1/douyin/douplus/fetch_sec_token`

- 用途：获取 DOU+ 需要鉴权的 POST 接口（如「成本计算」）所需的 sec_token
- 返回：含 sec_token 字段的数据，用于后续 DOU+ 鉴权 POST 接口
- Body(JSON)：
  - `cookie` (必填,string) 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie

## 获取达人分类

`POST /api/v1/douyin/douplus/fetch_talent_categories`

- 用途：获取 DOU+ 达人分类列表；其分类名可用作"按分类搜索达人"接口的 name 字段
- 返回：达人分类列表
- Body(JSON)：
  - `cookie` 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie

## 按分类搜索达人

`POST /api/v1/douyin/douplus/fetch_talents_by_category`

- 用途：按分类搜索/筛选 DOU+ 达人
- 返回：达人列表
- Body(JSON)：
  - `cookie` 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `name` 达人分类名/搜索词(取自达人分类接口);留空为全部/Category name or keyword (from the talent category endpoint); empty for all
  - `page` (默认 0) 页码,从0开始/Page index from 0
  - `limit` (默认 20) 每页数量/Page size

## 获取用户主页作品

`POST /api/v1/douyin/douplus/fetch_user_posts`

- 用途：获取指定用户主页的作品列表（简洁版接口，支持游标翻页）
- 返回：用户作品列表，以及翻页信息
- Body(JSON)：
  - `cookie` 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `sec_uid` (必填,string) 用户 sec_uid/User sec_uid
  - `cursor` (默认 0) 翻页游标(字符串),首页传 "0",后续传上一页响应里的 cursor/Pagination cursor (string), "0" for first page, then pass the cursor from the previous response
  - `count` (默认 10) 每页数量/Page size

## 获取视频详情(按ID或链接)

`POST /api/v1/douyin/douplus/fetch_video_detail`

- 用途：通过视频ID 或 视频链接/分享文本 获取视频详情
- 返回：匹配到的视频数据
- Body(JSON)：
  - `cookie` 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `video` (必填,string) 视频ID 或 视频链接/分享文本/Video ID, or share link/text. 例/e.g. "7651708301280906538" 或/or 含 v.douyin.com 链接的分享文案

## 获取 DOU+ 视频排行榜

`POST /api/v1/douyin/douplus/fetch_video_ranking`

- 用途：获取 DOU+ 视频排行榜（热门榜），可按时间范围、垂类、榜单维度筛选
- 返回：视频排行榜数据（含作品、作者、各项指标等）
- Body(JSON)：
  - `time_range` (默认 2) 时间范围/Time range: 1 / 2 / 3
  - `tag_id` (默认 634) 垂类ID/Category id. 601剧情,602明星,606音乐,607二次元,608游戏,609时事,612舞蹈,614三农,615科技,616财经,617亲子,619生活,621健康,623情感,624文化,625职场,626教育,627摄影,628美食,629旅行,631时尚,633体育,634娱乐,635汽车
  - `dim_type` (默认 5) 榜单维度/Ranking dimension: 1=低粉爆款, 2=高完播率, 3=高点赞率, 4=高涨粉率, 5=热度指数
  - `adv_id` 广告主ID,可留空/Advertiser id (optional)

## 搜索直播间(抖音号

`POST /api/v1/douyin/douplus/search_live_room`

- 用途：搜索 DOU+ 直播间，支持按抖音号或抖音昵称搜索，支持游标翻页
- 返回：匹配的直播间列表，以及翻页信息
- Body(JSON)：
  - `cookie` 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `keyword` (必填,string) 抖音号 或 抖音昵称/Douyin ID or nickname
  - `cursor` (默认 0) 翻页游标,首页传 0,后续传上一页响应里的 cursor/Pagination cursor, 0 for first page
  - `count` (默认 10) 每页数量/Page size

## 搜索 DOU+ 用户

`POST /api/v1/douyin/douplus/search_user`

- 用途：在 DOU+ 投放场景下搜索抖音用户，支持抖音号 / ID / 昵称
- 返回：匹配的用户列表（含昵称、抖音号、sec_uid、粉丝数等），以及 cursor / has_more 翻页信息
- Body(JSON)：
  - `keyword` (必填,string) 搜索关键词,支持抖音号/ID/昵称/Search keyword (Douyin ID / nickname)
  - `count` (默认 20) 每页数量/Number of results per page
  - `cursor` (默认 0) 翻页游标,首页传 0,后续传上一页响应里的 cursor/Pagination cursor, 0 for first page, then pass the cursor from the previous response

## 搜索用户 V2

`POST /api/v1/douyin/douplus/search_user_v2`

- 用途：DOU+ 用户搜索 V2，支持游标翻页与 scope 搜索范围
- 返回：匹配结果列表，以及翻页信息
- Body(JSON)：
  - `cookie` 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `keyword` (必填,string) 搜索关键词/Search keyword
  - `cursor` (默认 0) 翻页游标,首页传 0,后续传上一页响应里的 cursor/Pagination cursor, 0 for first page
  - `count` (默认 10) 每页数量/Page size
  - `scope` (默认 1) 搜索范围/Search scope

## 搜索视频(按标题)

`POST /api/v1/douyin/douplus/search_video`

- 用途：按标题/关键词搜索 DOU+ 视频，支持游标翻页
- 返回：匹配的视频列表，以及翻页信息
- Body(JSON)：
  - `cookie` 用户 www.douyin.com 网页版 Cookie/User www.douyin.com web Cookie
  - `keyword` (必填,string) 视频标题/关键词/Video title or keyword
  - `cursor` (默认 0) 翻页游标,首页传 0,后续传上一页响应里的 cursor/Pagination cursor, 0 for first page
  - `count` (默认 12) 每页数量/Page size
