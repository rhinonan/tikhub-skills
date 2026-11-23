---
name: {{name}}
description: {{description}}
version: {{version}}
category: data-acquisition
author: rhinonan
license: MIT
agent_created: true
---

# 中文社媒数据引擎（免费版）

下载抖音无水印视频、解析分享链接、批量导出评论、查账号与作品数据、追热搜热榜、找达人——用一套 CLI 查接口、调接口，覆盖抖音、微博、小红书、B站、知乎、微信、快手，收录 {{count}} 个接口。只读数据，不含登录、发布、点赞等写操作。

> **免费版 = 自备上游 Key。** 数据由 TikHub 提供，需要你自己的 TikHub token，本 skill 不向你收费。
> 不想注册或充值上游？安装付费版 `cn-social-data-pro`，按次付费、无需上游账号。

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
python3 scripts/social.py doctor --net    # 顺带测网络与凭证
```

约定：

- 命令都在 **skill 根目录**下执行；在别的目录时用绝对路径 `python3 <skill目录>/scripts/social.py ...`。
- 解释器 `python3` 优先，老环境用 `python`。
- 所有命令都不写入业务系统，只读数据。

## 覆盖平台

{{platform_table}}

## 三步工作流

```bash
# 1) 搜：中文名、英文名、路径、用途都能搜
python3 scripts/social.py search 评论 --platform weibo

# 2) 看：参数、必填项、返回结构、注意事项
python3 scripts/social.py show weibo/web_v2/fetch_post_comments

# 3) 调：先 dry-run 确认，再真调并落盘
python3 scripts/social.py call weibo/web_v2/fetch_post_comments \
  -q id=5283919831764022 -q count=20 --dry-run
python3 scripts/social.py call weibo/web_v2/fetch_post_comments \
  -q id=5283919831764022 --out out/comments.json
```

免费版也可用 `python3 scripts/social.py estimate <path ...>` 预估上游成本；免费版不拦截调用，付费版会强制先确认。

常用参数：

| 想做什么 | 命令 |
|---|---|
| 按平台/分类浏览 | `list` / `list --platform douyin` / `list --folder Douyin-Web-API` |
| 看某平台有哪些分类 | `list --platform wechat` |
| 短路径命中多个平台 | 加 `--platform` 消歧 |
| POST + JSON body | `call <path> -b '{"url":"..."}'` |
| body 是数组 | `call <path> -b '["id1","id2"]'` |
| 首次接入新平台 | 先 `search <平台名>`，再 `show <候选>` |

## 一次性准备：Token

数据由 **[TikHub](https://tikhub.io)** 提供，免费版用你自己的 token：

1. 注册并生成 API Key（控制台：`https://user.tikhub.io`，最低充值 $5，按次扣费）。
2. 保存在下面任一位置，CLI 按优先级读取：
   - 环境变量 `TIKHUB_API_KEY`
   - `python3 scripts/social.py token <你的token>`（写入 `~/.workbuddy/tikhub_token`）
   - skill 目录下的 `.token`

没有 token 也能先跑通链路：`common` 平台下的 `demo/*` 接口返回固定数据、不扣额度：

```bash
python3 scripts/social.py call demo/douyin/web/fetch_one_video --out out/demo.json
```

## 平台速查

{{platform_bodies}}

## 分类导航

完整的分类清单在 `references/index.md`（约 {{count}} 个接口分成若干类，每个平台一组）。**不要一次把所有分类文档读进上下文**：

- 用 `search` / `list` / `show` 按需定位；
- 机器可读清单是 `references/inventory.json`，需要批量处理时直接读它；
- 每个分类的详细参数在 `references/<分类>.md`，只在确认要用某一类时打开。

## 常见问题

| 问题 | 处理 |
|---|---|
| 401 / Invalid token | token 没配或过期，按上面重新保存 |
| 402 / 余额不足 | 上游账户余额不够，去控制台充值；或先用 `demo/*` 接口 |
| 422 | 必填参数漏了，`show <path>` 看参数表 |
| 429 | 限流，降低并发或等 30s |
| 404 | 路径写错，用 `search`/`show` 重新确认 |
| data 为 null | 有些接口内容在 `business_data` 等顶层字段，用 `--raw` 看完整响应 |
| 某接口失效 | 换同平台同类通道（Web → App 版本），或用 `hybrid/video_data` 兜底 |

## 输出与合规

- `--out` 把 `data` 落盘；`--raw` 输出完整响应；`--preview N` 控制终端预览长度。
- 只采集公开数据；不要高频轰炸上游，不要用于侵犯隐私或绕过平台风控。
- 数据版权归原平台与内容作者，遵守目标平台的用户协议与当地法规（含个人信息保护要求）。
