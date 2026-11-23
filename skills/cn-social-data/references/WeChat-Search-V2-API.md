# WeChat Search V2 API

文件夹 `WeChat-Search-V2-API` · 2 个接口
说明：微信搜索 V2 数据接口


## 微信综合搜索（搜一搜）

`POST /api/v1/wechat_search/v2/fetch_search`

- 用途：微信「搜一搜」综合搜索，垂类由 `business_type` **字符串键**切换，传关键词即可；**实测可搜**：综合 / 公众号（含服务号、视频号）/ 文章 / 视频号视频 / 表情；⚠️ 其余垂类（直播 / 朋友圈 / 新闻 / 读书 / 听书 / 图片 / 百科 / 微信指数 / 划线 / 评论 / 贴图 / 小游戏 / AI 搜索）由微信服务端按账号与地区下发，当前实测恒返回空结果（`no_more` 文案非空即为正常空结果，`raw=true` / `raw=false` 都在顶层；`raw=false` 时另有 `count=0` + `items=[]`。仍按一次正常调用计费）；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `docID` / `feedNonceId` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：搜索结果列表（结构随垂类略有差异）
- Body(JSON)：
  - `keyword` (必填,string) 搜索关键词（1-100 字）/Search keyword (1-100 chars)
  - `business_type` (选填,string) 垂类字符串键（共 18 个）。**实测有结果**：综合 all / 公众号·服务号·视频号 account / 文章 article / 视频 video / 表情 sticker。其余键（underline / encyclopedia / live_stream / comment / listen / news / photos / book / moments / image / mini_game / weixin_index / ai_search）由微信服务端按账号与地区下发，当前实测恒返回空结果（count=0 + no_more 文案，仍按一次正常调用计费）。当前账号真正可用的 tab 以综合搜索响应里的 categories 为准；传列表外的值直接报错（422）/Vertical key (18 total). **Verified to return data**: all / account / article / video / sticker. The rest (underline / encyclopedia / live_stream / comment / listen / news / photos / book / moments / image / mini_game / weixin_index / ai_search) are gated server-side per account & region and currently always come back empty (count=0 plus a no_more message — still billed as a normal call). Use the `categories` field of an `all` search for the authoritative per-account tab list. Values outside this list are rejected (422)
  - `sort` (选填) 排序（结果页「排序」下拉，综合与各垂类通用）：不限(相关性) default/0 / 最新(发布时间降序) latest/1 / 最热(点赞降序) hot/2，字符串键或整数均可/Sort (result page 'sort' dropdown, common to all verticals): default/0 (relevance) / latest/1 (newest) / hot/2 (most liked); string key or integer
  - `publish_time` (选填) 发布时间（结果页「时间」下拉，通用）：不限 all/0 / 最近一天 day/1 / 最近七天 week/2 / 最近半年 half_year/3，字符串键或整数均可/Publish time (result page 'time' dropdown, common): all/0 / day/1 / week/2 / half_year/3; string key or integer
  - `offset` (选填,integer) 首页传 0；翻页请用 cursor（只传 offset 无效，每页都回到第一页）/Pass 0 for the first page; use cursor to paginate (offset alone does not work — it returns the first page every time)
  - `cursor` (选填) 翻页游标：首页留空；翻页时把上一页响应返回的 cursor 原样传回/Pagination cursor: leave empty for the first page; for the next page pass back the cursor returned in the previous response
  - `raw` (选填,boolean) True=原始搜索响应；False=精简解析结构/True=raw search response; False=simplified parsed structure
- 返回结构（实测）：
  - `data` 是对象（12 个字段）：`keyword`, `business_type`, `continue_flag`, `offset`, `cursor`, `categories`, `no_more`, `total`, `count`, `items`, `debug_id`, `debug_info`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 搜视频号视频（时长/排序/时间筛选）

`POST /api/v1/wechat_search/v2/fetch_search_videos`

- 用途：专搜视频号视频（`video` 垂类），并支持搜索结果页里的「时长」「不限/最新/最热」排序与「时间」下拉；等价于综合搜索 `/fetch_search`（`business_type=video`）再叠加筛选，筛选项均实测有效；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `docID` / `feedNonceId` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：视频号视频搜索结果列表（结构同综合搜索的 `video` 垂类）
- Body(JSON)：
  - `keyword` (必填,string) 搜索关键词（1-100 字）/Search keyword (1-100 chars)
  - `duration` (选填) 时长档（video 垂类专属）：不限 all/0 / 短(<5min) short/1 / 中(5-10min) medium/2 / 长(20min+) long/3，字符串键或整数均可/Duration tier (Channels video only): all/0 / short/1 (<5min) / medium/2 (5-10min) / long/3 (20min+); string key or integer
  - `sort` (选填) 排序：不限(相关性) default/0 / 最新(发布时间降序) latest/1 / 最热(点赞降序) hot/2，字符串键或整数均可/Sort: default/0 (relevance) / latest/1 (newest) / hot/2 (most liked); string key or integer
  - `publish_time` (选填) 发布时间：不限 all/0 / 最近一天 day/1 / 最近七天 week/2 / 最近半年 half_year/3，字符串键或整数均可/Publish time: all/0 / day/1 / week/2 / half_year/3; string key or integer
  - `offset` (选填,integer) 首页传 0；翻页请用 cursor（只传 offset 无效）/Pass 0 for the first page; use cursor to paginate (offset alone does not work)
  - `cursor` (选填) 翻页游标，用法同综合搜索：首页留空；翻页时把上一页响应返回的 cursor 原样传回/Pagination cursor, same as universal search: leave empty for the first page; pass back the cursor from the previous response
  - `raw` (选填,boolean) True=原始搜索响应；False=精简解析结构/True=raw search response; False=simplified parsed structure
