# 上游数据服务（TikHub）

> 面向 AI 时代的一站式社交媒体数据基础设施：把 16 个主流社交平台的公开数据统一封装成一套 RESTful API，一个 API Key 全部打通。

> 本文是**仓库内部文档**，用于记录上游服务商的能力、计费与风险，不随 skill 包分发。产品本身叫「中文社媒数据引擎」，只在免费版凭证与数据来源披露处出现上游名称。

- 官网：https://tikhub.io
- 文档：https://docs.tikhub.io （中文版：https://docs.tikhub.io/doc-4579297）
- API 基址：`https://api.tikhub.io`（官方提示不要用 `api.tikhub.dev`，延迟更高）
- 控制台：https://user.tikhub.io
- 开源组织：https://github.com/TikHub

本文是**平台层面的介绍**，不涉及具体接口调用与参数说明。接口清单由 `tools/collect_inventory.py` 从官方 OpenAPI 生成，见 `src/platforms/`。

---

## 一、它解决什么问题

做社媒数据的人基本都撞过这几堵墙：

1. **平台各写各的**。TikTok、抖音、小红书、X、Instagram 的接口规则、签名算法、返回结构完全不同，接 5 个平台就是 5 套爬虫，每套都随时可能因为反爬升级而挂掉。
2. **官方 API 贵且窄**。官方开放平台通常只给你自家账号的数据、有严格配额，想做大范围内容研究基本不够用。
3. **自己维护采集层成本高**。IP 池、账号池、验证码、指纹、解析规则更新——这些是纯工程负担，跟业务价值无关。

TikHub 的定位就是把这层"脏活"承包掉：你注册拿 Key，直接请求标准化的 JSON，不用管签名、解析、代理和反爬。官方给自己的定位是 "Social data marketplace for the AI era"，即**数据基础设施**，而不是一个看板工具（"TikHub is infrastructure, not a dashboard"）。

## 二、平台覆盖

官方口径是 16 个平台。从 MCP 服务清单能看到实际的分组与工具规模（约 990+ 个 MCP 工具，对应 REST 端点 1000+）：

| 平台 | 标识 | 工具数 | 覆盖内容 |
|---|---|---|---|
| 抖音 Douyin | `douyin` | 247 | 作品、用户、搜索、热榜、创作者中心、星图 |
| TikTok | `tiktok` | 204 | 视频、用户、搜索、广告、小店、分析、创作者工具 |
| Instagram | `instagram` | 82 | 帖子、Reels、Stories、用户、评论、话题标签 |
| 小红书 Xiaohongshu | `xiaohongshu` | 71 | 笔记、用户、搜索、评论 |
| 微博 Weibo | `weibo` | 64 | 博文、用户、评论、搜索、热搜 |
| 其他 Others | `others` | 64 | Lemon8、皮皮虾、西瓜视频、今日头条、Sora2 |
| B 站 Bilibili | `bilibili` | 41 | 视频、用户、评论、弹幕、搜索 |
| YouTube | `youtube` | 37 | 视频、频道、评论、搜索、播放列表 |
| 快手 Kuaishou | `kuaishou` | 33 | 视频、用户、评论、搜索 |
| 知乎 Zhihu | `zhihu` | 32 | 问题、回答、用户、话题、搜索 |
| LinkedIn | `linkedin` | 25 | 个人资料、帖子、公司、搜索 |
| Reddit | `reddit` | 24 | 帖子、评论、子版块、用户、搜索 |
| 工具类 TikHub Utilities | `tikhub` | 23 | 账户信息、下载器、健康检查、混合解析、临时邮箱 |
| 微信公众号 WeChat | `wechat` | 19 | 文章、公众号、视频号、搜索 |
| X / Twitter | `twitter` | 13 | 推文、用户、搜索、时间线 |
| Threads | `threads` | 11 | 帖子、用户、回复、搜索 |

注意两点：
- 各平台体量极不均衡。抖音 + TikTok 占了近一半端点，是平台的重心；X/Twitter 只有 13 个，属于薄覆盖。
- `others` 和 `tikhub`（工具类）也算在"16 个平台"里，所以对外宣传的"16 平台"口径略宽松，实际独立社交平台约 13–14 个。

## 三、产品形态

TikHub 不只是裸 API，周边配套比较完整：

**1. RESTful API（主体）**
标准 REST，返回结构化 JSON，官方称亚秒级响应。认证方式统一为请求头 `Authorization: Bearer <token>`，也可以走 Cookie。按平台 + 版本分组，例如 `/{platform}/{web|app|app/v3}/...`。所有端点有 Swagger UI 可在线调试（https://api.tikhub.io）。

**2. MCP Server（对 AI 场景最关键的一块）**
为 16 个平台各提供一个独立的 MCP 服务，端点规则是 `https://mcp.tikhub.io/{platform}/mcp`，共 990+ 个工具。支持三种传输：Stdio（用 `npx mcp-remote` 桥接）、SSE（`/sse`）、Streamable HTTP（`/mcp`，最直接）。

意义在于：Claude Desktop、Cursor、Cline、Cherry Studio、VS Code 等 MCP 客户端，配置三行 JSON 就能让模型用自然语言直接拉社媒数据，不需要写胶水代码。也能通过 `langchain-mcp-adapters` 接进 LangGraph 智能体。另提供 `tikhub-mcp-dist` 仓库，可下载 exe 在本地跑。

**3. Chrome 扩展**
自带 Key（bring-your-own-key）的浏览器侧边栏客户端，在 TikTok、抖音、Instagram、X、B 站页面里直接采集评论、分析账号、生成报告，不上传用户数据。

**4. 数据集**
1B+ 条已采集的结构化记录，覆盖 10+ 平台，交付格式 CSV / JSON / JSONL / Parquet，持续刷新、去重，可商用授权。适合模型训练、离线研究，按记录量阶梯计价（量级大时约 $0.40 / 1K 条）。

**5. Marketplace（未上线）**
计划让第三方发布 API、数据集、AI Agent 并变现，平台抽 10%（对标行业常见的 ~20%）。目前状态是 "Coming soon"。

**6. SDK 与开源**
官方维护 Python（异步、基于 HTTPX）、JavaScript、Java、C++、TypeScript、Go 等多语言 SDK，以及演示代码仓库、跨平台无水印下载器 GUI。Python SDK 是主推，星标最多。另有 n8n 集成插件，可接低代码工作流。

## 四、计费模式

**按量付费（credit 制），没有订阅制，没有月最低消费。**

| 档位 | 价格 | 说明 |
|---|---|---|
| 免费 | $0 | 注册送约 50 次请求，默认 10 RPS，可用全部 16 个平台，但部分端点需付费额度 |
| 按量 | $0.001 – $0.01 / 请求 | 每个端点单独定价，日用量阶梯折扣最高 50% |
| 企业 | 定制 | 一次性 $3,000 起或累计 $4,500，永久免 5% 手续费、3–10% 赠送额度、定制端点、私有化部署 |

几个容易踩的细节：
- **阶梯是边际计价**，像累进税一样分段算，不是整单打折。日用量 1,000 以内 $0.001，3 万以上降到 $0.0005。
- **RPS（并发速率）是单独购买的**，不包含在请求单价里。免费档 10 RPS 对批量任务明显不够。
- 付费余额和免费额度是分开的两套，部分端点只收付费余额。
- 充值最低 $5，支持支付宝、PayPal、USDT、对公转账。
- 某些端点固定价（例如抖音批量作品接口固定 $0.05/次），不参与阶梯。

## 五、宣称的数据与合规

官网首页的可核对数字：

- 30,000+ 开发者与数据团队
- 日均处理 300M+ 请求
- 16 个社交平台
- 已交付 1B+ 数据集记录
- GDPR / CCPA 合规声明，"Public data only"

**但这部分要打个折看**：30000 用户、3 亿次日请求是平台自述，无第三方审计。合规声明也是自我声明——"只处理公开数据"能降低风险，但不能消除风险。

## 六、实际使用时的风险判断

如果你要把它接进生产，有几件事值得先想清楚：

1. **合规不等于合法**。数据是"公开可访问"的，不代表平台方授权你批量抓取。各平台服务条款普遍禁止自动化采集，TikTok、Meta 都有过实际诉讼。TikHub 卖的是技术通道，法律责任在使用方。
2. **上游稳定性不在你手里**。它的数据来自对目标平台的解析，平台一改签名或风控策略，端点就可能失效。官方有状态监控（monitor.tikhub.io），但接口语义变更、字段增删是常态，别把字段当契约写死。
3. **个人信息风险**。用户主页、粉丝列表、评论者信息属于个人信息范畴，在国内还受《个人信息保护法》约束。做舆情监测、竞品分析相对安全，做人脸/身份画像、大规模用户画像就要谨慎。
4. **端点质量不均**。1000+ 端点里，官方主推的（抖音、TikTok）维护得勤，长尾平台（如 Threads、LinkedIn）更新慢、成功率低。选型前先用免费额度实测目标端点。
5. **价格陷阱**。$0.001/请求听起来极便宜，但批量采集很容易上量：抓 10 万条评论就是 $100 起，加上 RPS 费用，成本并不低。做预算时按"端点单价 × 预估量 + RPS 套餐"算。

## 七、与本仓库的关系

本仓库对外只交付两个 skill：`cn-social-data`（自备上游 Key）与 `cn-social-data-pro`（按次付费）。两者共用同一份接口清单与 CLI（`scripts/social.py`），覆盖抖音、微博、小红书、B站、知乎、微信、快手 7 个平台，约 630 个接口。

分工是：

- `docs/upstream.md`（本文）= 上游是什么、值不值得用、钱怎么花、风险在哪。
- `src/platforms/<平台>/` = 各平台接口的清单、分类文档与场景速查。
- `tools/collect_inventory.py` = 从官方 OpenAPI 生成清单；`tools/verify_endpoints.py` = 抽检真实返回。
- 网关（`gateway/`）= 付费版的 402 收款与上游转发，白名单只放行上述 7 个平台。

## 八、参考来源

- 官网首页：https://tikhub.io
- 定价页：https://tikhub.io/pricing
- MCP 文档：https://tikhub.io/mcp
- API 文档（README / 认证 / 状态码）：https://docs.tikhub.io
- 数据集：https://tikhub.io/datasets
- GitHub 组织：https://github.com/TikHub
- 服务状态：https://monitor.tikhub.io

> 数字与功能描述取自 2026-11 官方站点，平台迭代较快，接入前请以官网为准。
