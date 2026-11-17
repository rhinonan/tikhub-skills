# TikHub 抖音接口分类索引

共 332 个接口，分 12 类。三种查法，按场景选：

| 我要做什么 | 怎么做 |
|---|---|
| 只记得关键词（"评论""热榜""星图"） | `python3 scripts/tikhub.py search <关键词>` |
| 已经知道接口名或路径 | `python3 scripts/tikhub.py show <path 或路径后缀>` |
| 想按分类逐个浏览 | 打开下面对应的 `references/<分类>.md`；或 `python3 scripts/tikhub.py list --folder <分类>` |

## 分类清单

| 分类 | 接口数 | 参考文件 | 典型用途 |
|---|---|---|---|
| Douyin Web API（网页端） | 55 | `references/Douyin-Web-API.md` | 作品详情、分享链接解析、评论、用户主页、热榜 |
| Douyin App V3 API（APP 端） | 38 | `references/Douyin-App-V3-API.md` | APP 协议兜底、评论/用户/搜索 |
| Douyin Search API（搜索） | 23 | `references/Douyin-Search-API.md` | 综合/视频/用户/直播搜索 |
| Douyin Billboard API（榜单/热点） | 31 | `references/Douyin-Billboard-API.md` | 热点总榜、上升榜、同城、垂类标签、低粉爆款 |
| Douyin Index API（数据指数/巨量算数） | 51 | `references/Douyin-Index-API.md` | 关键词热度、视频/账号指数趋势 |
| Douyin Xingtu API（星图 V1） | 32 | `references/Douyin-Xingtu-API.md` | 星图老版接口 |
| Douyin Xingtu V2 API（星图 V2） | 50 | `references/Douyin-Xingtu-V2-API.md` | 达人画像、受众分布、商业榜 |
| Douyin Creator API（创作者中心 V1） | 17 | `references/Douyin-Creator-API.md` | 投稿分析、粉丝画像 |
| Douyin Creator V2 API（创作者中心 V2） | 14 | `references/Douyin-Creator-V2-API.md` | 投稿表现、作品分析 |
| Douyin DouPlus API（抖+ 投放） | 17 | `references/Douyin-DouPlus-API.md` | 可推广作品、投放预估 |
| Demo API（免费演示接口，固定数据 + 1h 缓存） | 3 | `references/Demo-API.md` | 无 token 跑通链路、验证字段结构 |
| Hybrid Parsing（多平台混合解析） | 1 | `references/Hybrid-Parsing.md` | 混合解析单视频 |

合计 332 个。另外两份速查：`references/api-index.md`（单行表格，332 行全量）、
`references/inventory.json`（机器可读，含 query/body 参数与请求示例）。

## 找不到接口时

1. 换更短的关键词（中文名、英文名、路径片段、用途都能匹配）。
2. 多关键词按 AND 搜不到时，CLI 会自动放宽成 OR 并列出相近接口。
3. 仍没有，多半是 TikHub 未提供该类数据 —— 用 `search` 结果里的同类通道降级
   （`web` → `app/v3` → `v2/v1` → `douplus`）。

> 若 `search`/`show` 报"清单无法读取"，说明 `inventory.json` 缺失或损坏（此时 CLI 已自动降级扫
> `references/*.md`）；重装 skill 包即可恢复，`call` 不受影响。
