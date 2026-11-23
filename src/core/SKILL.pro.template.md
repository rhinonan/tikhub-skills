---
name: {{name}}
description: {{description}}
version: {{version}}
category: data-acquisition
author: rhinonan
license: MIT
agent_created: true
---

# 中文社媒数据引擎（付费版）

下载抖音无水印视频、解析分享链接、批量导出评论、查账号与作品数据、追热搜热榜、找达人——用一套 CLI 查接口、调接口，覆盖抖音、微博、小红书、B站、知乎、微信、快手，收录 {{count}} 个接口。只读数据，不含登录、发布、点赞等写操作。

> **付费版 = 按次付费。** 不需要注册或充值上游，每次调用经作者网关走支付宝 AI 按量付费（A2M）。
> 已有上游账号、用量稳定？用免费版 `cn-social-data` 自带 Key 直连。

## 能帮你做什么

| 用户这样说 | 对应能力 | 第一步 |
|---|---|---|
| 下载抖音/快手/B站无水印视频、解析分享链接 | 无水印播放地址、链接解析 | `search 无水印` / `search 分享链接` |
| 导出某账号最近作品和评论 | 主页作品、一级/二级评论 | `search 评论 --platform douyin` |
| 看看这个博主/UP主/公众号的数据 | 用户资料、粉丝数、作品/文章列表 | `search 用户信息 --platform <平台>` |
| 今天微博热搜、抖音热榜是什么 | 热榜、热搜榜单 | `search 热榜` |
| 找某领域的达人，看粉丝画像 | 星图/蒲公英/花火、粉丝画像 | `search 达人` / `search 粉丝画像` |
| 导出公众号或微博文章正文 | 文章详情、互动数据 | `search 文章详情 --platform 微信` |
| 搜某个关键词在各平台的内容 | 综合/视频/用户搜索 | `search 搜索 --platform <平台>` |

绝大多数需求都走这三步：`search 关键词` → `show <候选路径>` → `call <路径> -q ...`。

## 0. 先自检

```bash
python3 scripts/social.py doctor
python3 scripts/social.py doctor --net
```

约定：

- 命令都在 **skill 根目录**下执行；在别的目录时用绝对路径 `python3 <skill目录>/scripts/social.py ...`。
- 解释器 `python3` 优先，老环境用 `python`。
- 所有命令都不写入业务系统，只读数据。

## 覆盖平台

{{platform_table}}

## 一次性准备：支付依赖

按次付款由支付宝买家侧 CLI 完成，需要 Node ≥ 18：

```bash
npx -y @alipay/agent-payment@latest install
```

装好后 `alipay-bot` 才可用；`doctor` 会提示缺失。

## 查询额度

```bash
python3 scripts/social.py balance     # 剩余 / 已购 / 已消耗
python3 scripts/social.py usage       # 最近调用与扣费
python3 scripts/social.py recharge --yes    # 购买额度包（¥9.90 / 200 点；不加 --yes 会先确认）
```

## 付费前必须确认

任何会花钱的调用，先展示预估清单给用户，确认后再执行：

```bash
# 单接口预估
python3 scripts/social.py estimate douyin/web/fetch_one_video

# 多接口任务预估（计划文件）
python3 scripts/social.py estimate --file plan.json
```

清单包含：**预计请求多少个接口、每个接口的档位、扣多少点、当前额度、需要补多少、推荐套餐**。

- `call` 默认也会先打印这份清单。
- 终端交互会提示输入 `y` 确认；非交互环境（agent 调用）必须加 `--yes` 才会真正发出请求，否则只打印清单并退出。
- 计划文件格式：

```json
{"title": "抖音账号分析", "endpoints": [
  {"path": "douyin/web/handler_user_profile", "repeat": 1},
  {"path": "douyin/web/fetch_user_post_videos", "repeat": 3},
  {"path": "douyin/web/fetch_video_comments", "repeat": 3}
]}
```

多接口任务的推荐流程：`estimate` → 把清单给用户确认 → 逐条 `call <path> --yes`；额度不足时 CLI 会自动购买额度包（`--no-auto-recharge` 可关闭）。单独 `recharge` 也会先打印商品与价格，输入 `y` 或加 `--yes` 才发起支付。

## 三步工作流

```bash
# 1) 搜
python3 scripts/social.py search 评论 --platform weibo

# 2) 看
python3 scripts/social.py show weibo/web_v2/fetch_post_comments

# 3) 调（先打印付费清单；用户确认后加 --yes 执行）
python3 scripts/social.py call weibo/web_v2/fetch_post_comments \
  -q id=5283919831764022 --out out/comments.json --yes
```

标准接口每次 ¥0.10（有额度时扣 1 点）；高价值/批量扣 6/30 点，不做单次收款。上游失败不计费。

## 计费规则

| 档位 | 计费 | 适用 |
|---|---|---|
| 标准 | ¥0.10 / 次，可单次付款 | 常规详情、评论、用户、搜索 |
| 高价值 | 6 点 / 次（约 ¥0.30） | 指数、星图/花火/蒲公英、榜单类 |
| 批量 | 30 点 / 次（约 ¥1.49） | 批量作品、批量查询 |
| 额度包 | ¥9.90 / 200 点 | 高价值与批量只能走额度；标准也可用 |
| 任务包 | ¥1.99 起 | 组合任务（如账号分析） |

**高价值与批量接口不支持单次付款**：额度不足时 CLI 会提示并自动购买额度包，然后重试本次调用；不想自动付款可加 `--no-auto-recharge`，先手动 `recharge`。标准接口在没有额度时才会单次收款。

## 平台速查

{{platform_bodies}}

## 分类导航

完整的分类清单在 `references/index.md`（约 {{count}} 个接口分成若干类，每个平台一组）。**不要一次把所有分类文档读进上下文**：

- 用 `search` / `list` / `show` 按需定位；
- 机器可读清单是 `references/inventory.json`；
- 每个分类的详细参数在 `references/<分类>.md`，只在确认要用某一类时打开。

## 常见问题

| 问题 | 处理 |
|---|---|
| 401 | 账户 token 无效，运行 `recharge` 重新获取 |
| 402 | 标准接口：CLI 自动唤起支付宝按次付款；高价值/批量：自动购买额度包后重试 |
| 422 | 必填参数漏了，`show <path>` 看参数表 |
| 429 | 限流，降低并发或等 30s |
| 404 | 路径写错，用 `search`/`show` 重新确认 |
| 502 | 上游失败，本次未计费，可直接重试 |
| data 为 null | 有些接口内容在 `business_data` 等顶层字段，用 `--raw` 看完整响应 |

## 输出与合规

- `--out` 把 `data` 落盘；`--raw` 输出完整响应；`--preview N` 控制终端预览长度。
- 数据来源：TikHub。只采集公开数据；不要高频轰炸上游，不要用于侵犯隐私或绕过平台风控。
- 数据版权归原平台与内容作者，遵守目标平台的用户协议与当地法规（含个人信息保护要求）。
