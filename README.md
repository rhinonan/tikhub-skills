# 中文社媒数据引擎

把国内主流社媒平台的公开数据接口封装成一个 Skill：**一个包、一套 CLI、一份接口清单**，只区分免费版与付费版。

用户侧最常做的事：**下载抖音/B站无水印视频、解析分享链接、批量导出评论、查博主/UP主数据、追微博热搜与抖音热榜、找小红书/知乎达人、导出公众号文章**。

- 免费版 `cn-social-data`：自备上游 API Key（数据由 [TikHub](https://tikhub.io) 提供）
- 付费版 `cn-social-data-pro`：走作者网关，支付宝按次付费，用户无需注册或充值上游

两个版本能力完全一致——同一份清单、同一套场景文档、同一个 CLI；差别只在“谁付上游的钱”和“请求打到哪”。

---

## 1. 覆盖平台

| 平台 | 接口数 | 典型能力 |
|---|---:|---|
| 抖音 | 330 | 作品、评论、用户主页、搜索、热榜、星图、巨量算数、创作者中心、DOU+、直播 |
| B站 | 88 | 视频详情/播放流/弹幕、评论、UP 主、搜索、热门、直播、花火商业数据 |
| 微博 | 56 | 用户、微博正文、评论/转发/点赞、时间线、热搜与各类榜单、搜索 |
| 小红书 | 45 | 笔记详情/评论、用户笔记、笔记/用户/商品搜索、蒲公英博主画像与关键词指数 |
| 知乎 | 41 | 问题/回答、专栏、想法、用户、评论、各类搜索、热榜 |
| 快手 | 38 | 作品详情、评论、用户作品、搜索、热榜/直播/购物/品牌榜单 |
| 微信 | 25 | 视频号账号/作品/评论/合集/直播回放、公众号文章/互动/文章列表、搜一搜 |
| 通用 | 7 | 免费 Demo 演示接口、多平台短视频混合解析 |
| **合计** | **630** | 只读数据接口，不含登录、发布、点赞等写操作 |

TikTok 与海外平台不在本产品范围内。

## 2. 设计原则

1. **一个产品，两个版本。** 不再按平台拆 skill；平台只是清单里的一个维度。
2. **付费版不是阉割版。** 两端共用 `src/core/social.py` 与合并清单，避免功能漂移。
3. **开场不铺全量接口。** `SKILL.md` 只放 7 行平台总表、三步工作流和每平台 3 条速查；完整清单在 `references/inventory.json` 与分类文档里，按需加载。
4. **数据可复跑。** 清单从官方 OpenAPI 确定性生成，实测返回结构单独存放、可重复注入。
5. **品牌克制。** 对外名称是“中文社媒数据引擎”；上游名称只出现在免费版凭证配置、数据来源披露与内部文档中。

## 3. Skill 包结构

```
skills/cn-social-data/                 # 免费版（-pro 结构相同）
├── SKILL.md                           # 开场文件：平台表 + 工作流 + 每平台速查（≤ 250 行）
├── skill_meta.json                    # edition / base_url / gateway_url / platforms[]
├── _skillhub_meta.json                # 上架元数据（名称、版本、pay_mode、示例问法）
├── _icon.png                          # 512×512；付费版带 PRO 角标
├── scripts/social.py                  # 唯一 CLI
└── references/
    ├── index.md                       # 平台 → 分类 → 接口数 → 文件（唯一导航）
    ├── inventory.json                 # 630 条机器可读清单（参数、示例、实测返回结构）
    ├── _meta.json                     # 数据快照信息（规范版本、各平台计数）
    └── <分类>.md                      # 26 个分类文档，按需打开
```

## 4. 仓库结构

```
skill-hub/
├── build.py                       # src/ → skills/ 合并组装（--check / --zip / --clean）
├── src/
│   ├── product.json               # 产品与平台清单（唯一事实源）
│   ├── core/
│   │   ├── social.py              # 唯一 CLI 实现（多平台）
│   │   ├── SKILL.free.template.md
│   │   └── SKILL.pro.template.md
│   ├── editions/{free,pro}.json   # 版本配置（base_url / gateway_url / pay_mode）
│   ├── assets/_icon.png(_pro)     # 产品图标（tools/make_icons.py --product 生成）
│   └── platforms/<slug>/          # meta.json + skill.body.md + references/
├── tools/
│   ├── collect_inventory.py       # 官方 OpenAPI → inventory.json + 分类文档
│   ├── verify_endpoints.py        # 每平台 2–3 个核心接口真实抽检
│   ├── patch_returns.py           # 实测结构注入 inventory 与分类 md
│   ├── make_engine_icon.py        # 生成产品图标母版
│   └── make_icons.py              # 母版 → 512 图标（含 PRO 角标）
├── gateway/                       # 付费版后端（402 收款 → 白名单 → 上游转发），独立部署
├── pricing/                       # 官方价格清单（逐接口上游单价，定价的权威来源）
├── docs/upstream.md               # 上游服务商背景（内部文档，不随包分发）
└── skills/                        # 构建产物（入库，方便直接上传）
```

## 5. 数据流水线

```bash
# 1) 采集/更新接口清单（读取 https://api.tikhub.io/openapi.json，可 --spec 指定快照）
python tools/collect_inventory.py --platforms all

# 2) 真实抽检（会产生少量上游费用；不加 --yes 只预览）
python tools/verify_endpoints.py --platforms all --yes

# 3) 把实测返回结构注入清单与分类文档
python tools/patch_returns.py --all --write

# 4) 合并组装
python build.py --clean
python build.py --check
python build.py --zip
```

- `collect_inventory.py` 只依赖标准库；下载的规范缓存在 `.local/openapi-<version>.json`。
- 价格优先读 `pricing/tikhub_pricing_2026-11-23.csv`（`--pricing-csv` 可换文件，`none` 关闭），接口描述里的价格只作兜底；两者冲突以 CSV 为准。
- `verify_endpoints.py` 每个平台挑 2–3 个高频接口，把真实返回的字段结构写进 `returns-detail.json`；失败会如实记录，不编造。
- `patch_returns.py` 幂等，可重复执行。
- `build.py` 把 8 个平台目录合并成一份清单与导航；`--check` 校验条目数、分类文档、path 唯一性、SKILL.md 行数与“无全量接口表”。

## 6. CLI

```bash
python3 scripts/social.py doctor                # 自检：环境/清单/凭证/网络
python3 scripts/social.py list                  # 按平台分组浏览分类
python3 scripts/social.py search 评论            # 跨 7 平台搜索
python3 scripts/social.py show weibo/web_v2/fetch_post_comments
python3 scripts/social.py estimate douyin/web/fetch_one_video --no-balance
python3 scripts/social.py call weibo/web_v2/fetch_post_comments \
  -q id=5283919831764022 --dry-run
python3 scripts/social.py call weibo/web_v2/fetch_post_comments \
  -q id=5283919831764022 --out out/comments.json --yes
```

- `--platform` 接受 slug 或中文名；短路径跨平台命中多个时用它消歧。
- 付费版每次调用前会打印预估清单（接口数、档位、扣点、当前额度、覆盖套餐）；非交互环境必须加 `--yes` 才真正执行。
- 多接口任务用 `estimate --file plan.json` 预估，确认后再逐条 `call --yes`。
- 免费版凭证优先级：`TIKHUB_API_KEY` > `skill/.token` > `~/.workbuddy/tikhub_token`。
- 付费版使用网关账户 token（`recharge --yes` 后写入 `~/.workbuddy/tikhub_gateway_token`）。
- `demo/*` 接口免 token、不扣额度，用于先跑通链路。

## 7. 付费网关

```
付费版 CLI ──POST /v1/call──▶ 作者网关 ──注入作者 Key──▶ 上游 API
                 ▲ 402 + Payment-Needed
                 └─ alipay-bot 付款 → Payment-Proof → 验付 → 履约
```

- 网关只放行本产品的 7 个平台与 demo/hybrid 路径，其他平台一律 `UNSUPPORTED_PLATFORM`。
- 付费版 CLI 在发请求前会打印预估清单（接口数、档位、扣点、当前额度、覆盖套餐）；非交互环境必须加 `--yes` 才真正执行，`recharge` 购买额度包也需要确认。
- 计费：标准档 ¥0.10/次（可单次付款，或有额度时扣 1 点）；高价值 6 点/次、批量 30 点/次，只走额度包、不按次卖；额度包 ¥9.90 / 200 点。
- 逐接口定价：以官方价格清单 `pricing/tikhub_pricing_2026-11-23.csv` 为权威来源（623/630 个接口有明确单价），`tools/collect_inventory.py` 把它写进 `gateway/endpoint_costs.json`。网关按真实成本归档（≤$0.01 标准、$0.01–$0.05 高价值、≥$0.05 批量），没标价的接口才退回路径正则。当前分布：573 标准 / 52 高价值 / 5 批量。
- 订单按 `resource_id`（path + 参数指纹）绑定，同一凭证重试幂等；上游失败自动退还额度。

本地自测：

```bash
cd gateway
MOCK_UPSTREAM=1 python tests/mock_server.py     # 另开终端
python smoke_test.py                            # 预期 55 通过 / 0 失败
```

## 8. 常见问题

| 问题 | 处理 |
|---|---|
| 清单里搜不到某接口 | 接口可能已下线；重跑 `collect_inventory.py` 更新规范 |
| 实测参数和文档不符 | 以 `verify_endpoints.py` 的结果为准，把差异写进 `returns-detail.json` |
| 新平台要加进来 | 在 `src/product.json` 与 `collect_inventory.py` 的 `PLATFORMS` 加 slug，再补 meta/body |
| 上架名变了 | SkillHub 旧条目需下架重传；网关无商品 ID 依赖 |
| 免费版 401 | 换新 token；`doctor` 会显示当前凭证来源 |

## 9. 合规与风险

- 只采集公开数据，不提供登录、发布、点赞等写操作。
- 上游数据服务条款与各目标平台的服务条款仍需遵守；转售公开数据存在条款风险，接入前请自行评估。
- 用户主页、粉丝列表、评论者信息属于个人信息，受《个人信息保护法》等约束；不要做大规模个人画像。
- 上游端点可能随时变更或失效，字段不应被视为稳定契约；生产使用建议加缓存与降级。

## 10. 路线图

| 阶段 | 内容 | 状态 |
|---|---|---|
| P0 | 多平台合并 CLI、合并清单、两版构建 | 完成 |
| P1 | OpenAPI 采集器 + 实测抽检 + 返回结构注入 | 完成 |
| P2 | 网关白名单、微博等新平台计费校验 | 完成 |
| P3 | 支付宝生产环境配置与公网部署 | 待账号/部署 |
| P4 | 额度看板、退款流程、未标价接口的成本核验 | 待开始 |
| P5 | SkillHub 双版本上架与用户文档 | 待开始 |
