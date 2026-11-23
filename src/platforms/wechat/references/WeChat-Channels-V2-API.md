# WeChat Channels V2 API

文件夹 `WeChat-Channels-V2-API` · 12 个接口
说明：微信视频号 V2 数据接口


## 获取视频号账号信息

`POST /api/v1/wechat_channels/v2/fetch_channel_info`

- 用途：获取指定视频号账号的「更多信息」：基础信息分区（IP 归属地 / 资料所在地 / **视频号 ID**=sph 公开号）+ 认证信息分区（服务单位 / 主体类型 / 互联网新闻信息服务许可证编号 / 服务类别 / 认证时间）；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：视频号账号的基础信息与认证信息
- Body(JSON)：
  - `username` (必填,string) 视频号 finder username（v2_…@finder 格式）/WeChat Channels finder username (v2_…@finder format)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure
- 返回结构（实测）：
  - `data` 是对象（6 个字段）：`baseResponse`, `pbRequestMsgInfo`, `pair`, `sections`, `debug_id`, `debug_info`
  - `data.baseResponse` 是对象（3 个字段）：`ret`, `errMsg`, `pbRequestMsgInfo`
  - `data.pair` 是数组（长度 0）
  - `data.sections` 是数组（长度 2）；首元素字段：`title`, `items`, `pbRequestMsgInfo`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 视频号ID转finder username

`POST /api/v1/wechat_channels/v2/fetch_channel_id_to_username`

- 用途：把对外可见的视频号 ID（`sph…` 短号）解析成 finder username（`v2_…@finder`）；拿到 username 后即可调用 `fetch_user_videos`、`fetch_channel_info`、`fetch_user_profile` 等接口；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：解析出的 finder username 及账号昵称、简介
- Body(JSON)：
  - `channel_id` (必填,string) 视频号 ID（sph 开头的短号）/WeChat Channels ID (short ID starting with sph)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取视频号用户作品列表

`POST /api/v1/wechat_channels/v2/fetch_user_videos`

- 用途：获取指定视频号账号主页的作品列表；每个视频带媒体地址 `media`（含 `url` / `url_token` / `full_url` / `decode_key`），可直接下载并解密；支持翻页获取更多作品；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `id` / `object_nonce_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：用户作品列表及翻页游标
- Body(JSON)：
  - `username` (必填,string) 视频号 finder username（v2_…@finder 格式）/WeChat Channels finder username (v2_…@finder format)
  - `last_buffer` (选填) 翻页游标（base64），首页留空/Pagination cursor (base64), leave empty for first page
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构（推荐做媒体下载）/True=raw response; False=simplified parsed structure (recommended for media download)

## 获取视频号作品详情

`POST /api/v1/wechat_channels/v2/fetch_video_detail`

- 用途：获取视频号作品详情，返回作品完整详情（媒体地址 `media` + `decode_key`）；支持三种入参，**三选一、优先级 object_id > export_id > share_url**；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：作品完整详情（含媒体下载地址与解密密钥）
- Body(JSON)：
  - `object_id` (选填) 作品 objectId（纯数字，最优先）/Video objectId (numeric, highest priority)
  - `export_id` (选填) 搜索结果中的 exportId（export/ 开头，会过期，需尽快使用）/exportId from search results (starts with export/, expires soon)
  - `object_nonce_id` (选填) 配套 objectNonceId（纯数字，可选，提升命中率）/Optional objectNonceId (numeric, improves hit rate)
  - `share_url` (选填) 视频号分享短链（https://weixin.qq.com/sph/…），仅在 object_id 与 export_id 都为空时使用/Share URL (https://weixin.qq.com/sph/…), used only when object_id and export_id are empty
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构（推荐做媒体下载）/True=raw response; False=simplified parsed structure (recommended for media download)

## 获取视频号作品评论

`POST /api/v1/wechat_channels/v2/fetch_video_comments`

- 用途：获取作品的一级评论（含 IP 属地 / 点赞数）；传 `comment_id` 则返回该评论下的二级回复；支持翻页获取更多评论；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `comment_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：评论列表及翻页游标
- Body(JSON)：
  - `object_id` (必填,string) 作品 objectId（纯数字）/Video objectId (numeric)
  - `last_buffer` (选填) 翻页游标（base64），首页留空/Pagination cursor (base64), leave empty for first page
  - `comment_id` (选填) 展开某条评论的二级回复时传其 commentId（纯数字），首页留空/Pass a commentId (numeric) to expand its replies, leave empty for first-level comments
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 生成视频号作品分享链接

`POST /api/v1/wechat_channels/v2/fetch_video_share_url`

- 用途：给定作品 `object_id`，返回一条可对外分享的 `weixin.qq.com/sph/…` 短链（与 `fetch_video_detail` 的 `share_url` 入参互为反向）；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：作品分享短链
- Body(JSON)：
  - `object_id` (必填,string) 作品 objectId（纯数字）/Video objectId (numeric)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取视频号账号主页资料+统计

`POST /api/v1/wechat_channels/v2/fetch_user_profile`

- 用途：获取创作者的主页资料与互动统计。与 `fetch_channel_info`（认证主体 / 许可证）**互补**：本接口给昵称 / 签名 / 头像、粉丝 / 作品 / 获赞 / 收藏 / 转发数、直播时长、IP 属地、合集数、关联公众号等；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：账号主页资料与互动统计
- Body(JSON)：
  - `username` (必填,string) 视频号 finder username（v2_…@finder 格式）/WeChat Channels finder username (v2_…@finder format)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取视频号合集列表

`POST /api/v1/wechat_channels/v2/fetch_user_collections`

- 用途：获取创作者主页的「合集」列表。每个合集的 `topic_id` 可传 `fetch_collection_videos` 取该合集内的视频；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `topic_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：合集列表
- Body(JSON)：
  - `username` (必填,string) 视频号 finder username（v2_…@finder 格式）/WeChat Channels finder username (v2_…@finder format)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取视频号合集内视频

`POST /api/v1/wechat_channels/v2/fetch_collection_videos`

- 用途：给定合集 `topic_id`（来自 `fetch_user_collections`），返回该合集内的视频列表；每个视频带媒体地址 `media`（含 `url` / `url_token` / `decode_key`），可直接下载解密；支持翻页获取更多视频；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `id` / `topic_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：合集内视频列表及翻页游标
- Body(JSON)：
  - `topic_id` (必填,string) 合集 ID（纯数字，来自 fetch_user_collections 的 topic_id）/Collection ID (numeric, from topic_id of fetch_user_collections)
  - `topic` (选填) 合集名（可选，提高命中）/Collection name (optional, improves hit rate)
  - `username` (选填) 创作者 finder username（可选，提高命中）/Creator finder username (optional, improves hit rate)
  - `last_buffer` (选填) 翻页游标（base64），首页留空/Pagination cursor (base64), leave empty for first page
  - `topic_type` (选填,integer) 合集类型，默认 16（与 fetch_user_collections 返回的 topic_type 对齐）/Collection type, default 16 (align with topic_type from fetch_user_collections)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构（推荐做媒体下载）/True=raw response; False=simplified parsed structure (recommended for media download)

## 获取视频号直播回放列表

`POST /api/v1/wechat_channels/v2/fetch_live_history`

- 用途：获取创作者的直播回放列表。回放本身就是视频对象，每条带媒体地址 `media`（含 `url` / `url_token` / `decode_key`），可直接下载解密；支持翻页获取更多回放；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：直播回放列表及翻页游标
- Body(JSON)：
  - `username` (必填,string) 视频号 finder username（v2_…@finder 格式）/WeChat Channels finder username (v2_…@finder format)
  - `last_buffer` (选填) 翻页游标（base64），首页留空/Pagination cursor (base64), leave empty for first page
  - `flag` (选填,integer) 拉取标志，默认 12/Fetch flag, default 12
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构（推荐做媒体下载）/True=raw response; False=simplified parsed structure (recommended for media download)

## 获取视频号直播间详情

`POST /api/v1/wechat_channels/v2/fetch_live_detail`

- 用途：传直播 `live_id` 返回直播间详情：主播信息、直播状态、在线人数、回放信息等；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `live_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：直播间详情
- Body(JSON)：
  - `live_id` (必填,string) 直播 ID（纯数字）/Live ID (numeric)
  - `scene` (选填,integer) 进入场景，默认 5/Entry scene, default 5
  - `finder_username` (选填) 主播 finder username（可选，提高命中）/Anchor finder username (optional, improves hit rate)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 视频号号内搜索

`POST /api/v1/wechat_channels/v2/fetch_search_channel_videos`

- 用途：号内搜：在指定创作者的视频号内，按关键词搜索其发布的视频（只在**该号内部**检索）；**单页返回**：一次调用取一页。`continue_flag=1` 且 `next_cursor` 非空时，把 `next_cursor` **原样回传** `cursor` 参数取下一页；⚠️ `next_cursor` 是**不透明字符串**，请勿解析或拼接 —— 上游已将其密封（旧版明文里带有检索会话等内部状态）；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `doc_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：号内搜索命中列表
- Body(JSON)：
  - `username` (必填,string) 创作者 finder username（v2_…@finder 格式）/Creator finder username (v2_…@finder format)
  - `keyword` (必填,string) 在该号内搜索的关键词（1-100 字）/Keyword to search within this channel (1-100 chars)
  - `cursor` (选填) 翻页游标：首页留空；翻页时原样回传上一页响应的 next_cursor（不透明字符串，勿解析或拼接）/Pagination cursor: leave empty for the first page; pass back the previous response's next_cursor verbatim (opaque string, do not parse or concatenate)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure
