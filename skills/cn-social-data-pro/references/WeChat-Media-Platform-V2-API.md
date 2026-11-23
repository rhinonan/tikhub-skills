# WeChat Media Platform V2 API

文件夹 `WeChat-Media-Platform-V2-API` · 11 个接口
说明：微信公众号 V2 数据接口


## 获取公众号文章详情

`POST /api/v1/wechat_mp/v2/fetch_article_detail`

- 用途：传文章 URL，返回文章正文 / 标题 / 作者 / 封面 / 发布时间 / 合集信息等；无论 `raw` 取值，嵌套的 `content` JSON 串都会被解析成对象（结构归一化），`raw` 只控制外层字段的投影范围；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `comment_id` / `msgId` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据
- 返回：文章详情（正文 / 标题 / 作者 / 封面 / 发布时间 / 合集信息）
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/… 或带 __biz 的长链）/WeChat MP article URL (https://mp.weixin.qq.com/s/… or long URL with __biz)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号文章详情（H5 版本，推荐）

`POST /api/v1/wechat_mp/v2/fetch_article_detail_h5`

- 用途：传文章 URL，返回文章正文 / 标题 / 作者 / 封面 / 发布时间 / 合集信息等，**推荐默认使用本接口**；与 `/fetch_article_detail` 是**两个独立接口**，各自返回结果，不会自动切换：
- 返回：文章详情（正文 / 标题 / 作者 / 封面 / 发布时间 / 合集 / 标签 / IP 属地 / 图片清单等）
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/… 或带 __biz 的长链）/WeChat MP article URL (https://mp.weixin.qq.com/s/… or long URL with __biz)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure
- 返回结构（实测）：
  - `data` 是对象（6 个字段）：`url`, `bizUin`, `itemIdx`, `content`, `debug_id`, `debug_info`
  - `data.content` 是对象（206 个字段）：`title`, `nick_name`, `author`, `user_name`, `desc`, `content_noencode`, `content_text`, `create_time`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取公众号文章互动数据（H5 版本）

`POST /api/v1/wechat_mp/v2/fetch_article_stats_h5`

- 用途：传文章 URL，返回**评论数 / 精选评论数**。与 `/fetch_article_stats` 是**两个独立接口**，
- 返回：评论数 / 精选评论数；其余互动指标为 `null` 并列在 `unavailable[]`
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/… 或带 __biz 的长链）/WeChat MP article URL (https://mp.weixin.qq.com/s/… or long URL with __biz)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure
  - `comment_id` (选填) 文章的评论 id（可选，**性能捷径**）：不传时上游要先抓并解析整篇文章 HTML 才能拿到它，约占本接口耗时的一半；已有该值时传进来可显著加快。取自 /fetch_article_detail 或 /fetch_article_detail_h5 响应的 `$.data.content.comment_id`/Article comment id (optional, performance shortcut): when omitted, upstream must fetch and parse the whole article HTML to obtain it, which accounts for about half of this endpoint's latency

## 获取公众号文章互动数据

`POST /api/v1/wechat_mp/v2/fetch_article_stats`

- 用途：传文章 URL，返回文章的互动指标（阅读量 / 点赞 / 在看 / 分享 / 收藏 / 评论数）；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：文章互动数据
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/… 或带 __biz 的长链）/WeChat MP article URL (https://mp.weixin.qq.com/s/… or long URL with __biz)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号文章评论

`POST /api/v1/wechat_mp/v2/fetch_article_comments`

- 用途：获取公众号文章评论（单页，`buffer` 游标翻页），返回文章的一页精选评论；**翻页**：首页 `buffer` 留空 → 取响应的 `buffer` → 下次请求传回 `buffer` 取下一页；`has_more` 为 false 即到末页；逐条评论的二级回复请用 `fetch_comment_replies`（传评论的 `content_id`）；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `content_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据；💡 **提速**：传 `comment_id` 可让上游跳过整篇文章的抓取解析，实测本接口从 15.10s 降到 6.91s / 评论接口从 8.28s 降到 6.13s。该值取自 `/fetch_article_detail` 或 `/fetch_article_detail_h5` 响应的 `$.data.content.comment_id`，拿它是零成本的
- 返回：单页评论列表及翻页游标
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/…）/WeChat MP article URL (https://mp.weixin.qq.com/s/…)
  - `buffer` (选填) 翻页游标，首页留空；翻页传上一页响应的 buffer/Pagination cursor, leave empty for first page; pass buffer from the previous response
  - `comment_id` (选填) 文章的评论 id（可选，**性能捷径**）：不传时上游要先抓并解析整篇文章 HTML 才能拿到它，约占本接口耗时的一半；已有该值时传进来可显著加快。取自 /fetch_article_detail 或 /fetch_article_detail_h5 响应的 `$.data.content.comment_id`/Article comment id (optional, performance shortcut): when omitted, upstream must fetch and parse the whole article HTML to obtain it, which accounts for about half of this endpoint's latency
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号评论的二级回复

`POST /api/v1/wechat_mp/v2/fetch_comment_replies`

- 用途：返回某条一级评论下的二级回复；链路：先调 `fetch_article_comments` 取到每条评论的 `content_id`，再把它喂给本接口；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况；⚠️ 大整数 ID 精度：响应中的 `content_id` / `reply_id` 等为 64 位大整数，超出 JavaScript 安全整数范围（2^53-1）。请始终以**字符串**方式接收 / 传递这类 ID（解析 JSON 用 json-bigint 或按文本取值），勿让其经过 JS `Number`。Swagger UI 文档页对超大整数会末位舍入显示，属正常现象，不影响接口实际返回的数据；💡 **提速**：传 `comment_id` 可让上游跳过整篇文章的抓取解析，实测本接口从 15.10s 降到 6.91s / 评论接口从 8.28s 降到 6.13s。该值取自 `/fetch_article_detail` 或 `/fetch_article_detail_h5` 响应的 `$.data.content.comment_id`，拿它是零成本的
- 返回：二级回复列表及翻页信息
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/…）/WeChat MP article URL (https://mp.weixin.qq.com/s/…)
  - `content_id` (选填) 目标一级评论的 content_id（纯数字），不传则自动取第一条有回复的评论/content_id (numeric) of the target first-level comment; defaults to the first comment that has replies
  - `offset` (选填,integer) 回复翻页偏移，首页 0；has_more=true 时传上次返回的 next_offset/Reply pagination offset, 0 for first page; pass next_offset from the previous response when has_more=true
  - `comment_id` (选填) 文章的评论 id（可选，**性能捷径**）：不传时上游要先抓并解析整篇文章 HTML 才能拿到它，约占本接口耗时的一半；已有该值时传进来可显著加快。取自 /fetch_article_detail 或 /fetch_article_detail_h5 响应的 `$.data.content.comment_id`/Article comment id (optional, performance shortcut): when omitted, upstream must fetch and parse the whole article HTML to obtain it, which accounts for about half of this endpoint's latency
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号关联文章

`POST /api/v1/wechat_mp/v2/fetch_related_articles`

- 用途：传文章 URL，返回文章底部「关联 / 相关文章」。未开启该功能的文章返回空列表；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：关联文章列表
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/… 或带 __biz 的长链）/WeChat MP article URL (https://mp.weixin.qq.com/s/… or long URL with __biz)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号文章广告

`POST /api/v1/wechat_mp/v2/fetch_article_ad`

- 用途：传文章 URL，返回文章内嵌的广告位信息。该接口响应相对较慢，请耐心等待；未投放广告的文章返回空；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：文章广告位信息
- Body(JSON)：
  - `url` (必填,string) 公众号文章链接（https://mp.weixin.qq.com/s/… 或带 __biz 的长链）/WeChat MP article URL (https://mp.weixin.qq.com/s/… or long URL with __biz)
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号资料页

`POST /api/v1/wechat_mp/v2/fetch_account_profile`

- 用途：传公众号 username，返回公众号资料页：昵称 / IP 属地 / 原创文章数 / 认证主体类型 / 关联视频号等；⚠️ **签名（简介）与头像这条路取不到** —— 微信的资料页响应里既没有可读简介也没有头像
- 返回：公众号资料页信息
- Body(JSON)：
  - `username` (必填,string) 公众号 username。三种形态都支持：`gh_…`、`gh_…@app`（关联小程序的账号）、以及自定义微信号（如 `nikejdi`）。取自文章详情接口响应的 `$.data.content.user_name`/Official account username. Three forms are supported: `gh_…`, `gh_…@app` (mini-program-linked accounts) and custom WeChat IDs (e.g. `nikejdi`). Taken from `$.data.content.user_name` of the article detail endpoints
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号文章列表

`POST /api/v1/wechat_mp/v2/fetch_account_articles`

- 用途：传 `gh_username`，返回公众号历史发文（**文章** tab）的**单页**列表；**手动翻页**：首页 `offset` 留空 → 从响应取 `next_offset`（base64 游标）→ 下次请求放进 **`offset`** 取下一页；`is_end` 为真即末页；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：公众号文章列表（单页）及翻页游标
- Body(JSON)：
  - `username` (必填,string) 公众号 username。三种形态都支持：`gh_…`、`gh_…@app`（关联小程序的账号）、以及自定义微信号（如 `nikejdi`）。取自文章详情接口响应的 `$.data.content.user_name`/Official account username. Three forms are supported: `gh_…`, `gh_…@app` (mini-program-linked accounts) and custom WeChat IDs (e.g. `nikejdi`). Taken from `$.data.content.user_name` of the article detail endpoints
  - `page_size` (选填,integer) 每页数量（默认 20）。⚠️ 微信当前**忽略**该参数：返回条数由公众号自身决定，实测取 1 与取 40 结果完全相同；翻页请用 offset / next_offset/Articles per page (default 20). NOTE: WeChat currently ignores this parameter — the count is decided by the account itself; paginate with offset / next_offset
  - `offset` (选填) 翻页游标（base64），首页留空；翻页传上一页响应的 next_offset/Pagination cursor (base64), leave empty for first page; for the next page pass next_offset from the previous response
  - `item_show_type` (选填) 内容栏目：留空/0=文章（默认）、5=视频、7=音频、8=贴图/Content tab: empty/0=articles (default), 5=videos, 7=audios, 8=image-text posts
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure

## 获取公众号服务/自定义菜单

`POST /api/v1/wechat_mp/v2/fetch_account_services`

- 用途：传 `gh_username`，返回公众号底部的自定义菜单 / 服务入口。未配置自定义菜单的账号返回空菜单；价格：0.01$/次；⏱️ 由于微信服务器原因，本接口响应较慢，请将客户端请求超时（timeout）设置为 30 秒；timeout 设置过小会造成已扣费但收不到响应的情况
- 返回：公众号自定义菜单 / 服务入口
- Body(JSON)：
  - `username` (必填,string) 公众号 username。三种形态都支持：`gh_…`、`gh_…@app`（关联小程序的账号）、以及自定义微信号（如 `nikejdi`）。取自文章详情接口响应的 `$.data.content.user_name`/Official account username. Three forms are supported: `gh_…`, `gh_…@app` (mini-program-linked accounts) and custom WeChat IDs (e.g. `nikejdi`). Taken from `$.data.content.user_name` of the article detail endpoints
  - `raw` (选填,boolean) True=原始响应；False=精简解析结构/True=raw response; False=simplified parsed structure
