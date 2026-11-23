# Douyin Xingtu API

文件夹 `Douyin-Xingtu-API` · 32 个接口
说明：抖音星图数据接口


## 获取加密图片解析

`GET /api/v1/douyin/xingtu/get_sign_image`

- 用途：解析星图加密图片，获取可访问的图片URL；价格：0.001$ / 次
- 返回：解析后的图片数据，包含可访问的图片URL
- Query：
  - `uri` (必填,string) 图片的uri/Image URI
  - `durationTS` (选填,integer) 有效期时长（秒）/Duration in seconds
  - `format` (选填,string) 图片格式/Image format
- 示例：

```
uri = "tos-cn-i-0813c000-ce/oMKzDA3A9QGAuebfsDIAwlDoAfCFEEzSEw8FQZ"
durationTS = 86400
format = "webp"
```

## 根据抖音用户ID获取游客星图kolid

`GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_uid`

- 用途：通过抖音用户ID获取游客星图kolid；价格：0.001$ / 次
- 返回：游客星图kolid
- Query：
  - `uid` (必填,string) 抖音用户ID/Douyin User ID
- 示例：

```
uid = "70452002324"
```

## 根据抖音sec_user_id获取游客星图kolid

`GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_sec_user_id`

- 用途：通过抖音sec_user_id获取游客星图kolid；价格：0.001$ / 次
- 返回：游客星图kolid
- Query：
  - `sec_user_id` (必填,string) 抖音用户sec_user_id/Douyin User sec_user_id
- 示例：

```
sec_user_id = "MS4wLjABAAAAoxwUZouIdKL6sZ8EB96KDjkrhfBMS1KbCgsMJR1kIUs"
```

## 根据抖音号获取游客星图kolid

`GET /api/v1/douyin/xingtu/get_xingtu_kolid_by_unique_id`

- 用途：通过抖音号获取游客星图kolid；价格：0.001$ / 次
- 返回：游客星图kolid
- Query：
  - `unique_id` (必填,string) 抖音号/Douyin User unique_id
- 示例：

```
unique_id = "m6640150"
```

## 获取kol基本信息V1

`GET /api/v1/douyin/xingtu/kol_base_info_v1`

- 用途：获取kol基本信息V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol基本信息
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `platformChannel` (必填,string) 平台渠道/Platform Channel
- 示例：

```
kolId = "7048929565493690398"
platformChannel = "_1"
```

## 获取kol观众画像V1

`GET /api/v1/douyin/xingtu/kol_audience_portrait_v1`

- 用途：获取kol观众画像V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol观众画像
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取kol粉丝画像V1

`GET /api/v1/douyin/xingtu/kol_fans_portrait_v1`

- 用途：获取kol粉丝画像V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol粉丝画像
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `fansType` (选填,string) 粉丝类型/Fans Type
- 示例：

```
kolId = "7048929565493690398"
fansType = "_1"
```

## 获取kol服务报价V1

`GET /api/v1/douyin/xingtu/kol_service_price_v1`

- 用途：获取kol服务报价V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol Service Price
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `platformChannel` (必填,string) 平台渠道/Platform Channel
- 示例：

```
kolId = "7048929565493690398"
platformChannel = "_1"
```

## 获取kol数据概览V1

`GET /api/v1/douyin/xingtu/kol_data_overview_v1`

- 用途：获取kol数据概览V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol数据概览
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `_type` (必填,string) 类型/Type
  - `_range` (必填,string) 范围/Range
  - `flowType` (必填,integer) 流量类型/Flow Type
  - `onlyAssign` (选填,boolean) 是否指派/Whether assigned (optional)
- 示例：

```
kolId = "7048929565493690398"
_type = "_1"
_range = "_2"
flowType = 1
onlyAssign = None  # or True/False if needed
```

## [已废弃]关键词搜索kol V1

`GET /api/v1/douyin/xingtu/search_kol_v1`

- **已标记 deprecated，可能失效**
- 用途：关键词搜索kol V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol列表
- Query：
  - `keyword` (必填,string) 关键词/Keyword
  - `platformSource` (必填,string) 平台来源/Platform Source
  - `page` (必填,integer) 页码/Page
- 示例：

```
keyword = "人工智能"
platformSource = "_1"
page = 1
```

## 高级搜索kol V2

`GET /api/v1/douyin/xingtu/search_kol_v2`

- 用途：高级搜索kol V2，支持粉丝范围和内容标签筛选；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol列表（支持高级筛选）
- Query：
  - `keyword` (必填,string) 关键词/Keyword
  - `followerRange` (选填,string) 粉丝范围(可选)/Follower Range (optional), 例如 10-100 表示10万-100万粉丝
  - `contentTag` (选填,string) 内容标签(可选)/Content Tag (optional), 例如 tag-1 或 tag_level_two-7
  - `page` (选填,string) 页码(可选)/Page (optional)
  - `sort` (选填,string) 排序方式(可选)/Sort order (optional)
  - `searchType` (选填,string) 搜索类型(可选)/Search type (optional)
  - `marketingTarget` (选填,string) 营销目标(可选)/Marketing target (optional)
  - `industry` (选填,string) 所属行业(可选)/Industry (optional)
  - `isSuperstar` (选填,string) 是否明星(可选)/Whether superstar (optional)
  - `kolPriceType` (选填,string) 报价类型(可选)/KOL price type (optional)
  - `kolPriceRange` (选填,string) 报价区间(可选)/KOL price range (optional)
  - `contentTheme` (选填,string) 内容主题(可选)/Content theme (optional)
  - `personaTag` (选填,string) 人设标签(可选)/Persona tag (optional)
  - `gender` (选填,string) 达人性别(可选)/Author gender (optional)
  - `location` (选填,string) 达人地域(可选)/Author location (optional)
  - `tonalityTag` (选填,string) 内容调性标签(可选)/Tonality tag (optional)
  - `connectedUserRange` (选填,string) 连接人数区间(可选)/Connected user range (optional)
  - `audienceImage` (选填,string) 观众画像筛选(可选)/Audience image (optional)
  - `fansImage` (选填,string) 粉丝画像筛选(可选)/Fans image (optional)
  - `expectedPlayRange` (选填,string) 预期播放区间(可选)/Expected play range (optional)
  - `expectedCpmRange` (选填,string) 预期CPM区间(可选)/Expected CPM range (optional)
  - `expectedCpeRange` (选填,string) 预期CPE区间(可选)/Expected CPE range (optional)
  - `interactionRateRange` (选填,string) 互动率区间(可选)/Interaction rate range (optional)
  - `completionRateRange` (选填,string) 完播率区间(可选)/Completion rate range (optional)
  - `viralRateRange` (选填,string) 爆款率区间(可选)/Viral rate range (optional)
  - `progressTaskRange` (选填,string) 在途任务数区间(可选)/In-progress task range (optional)
  - `isCuratedAuthor` (选填,string) 是否精选达人(可选)/Whether curated author (optional)
  - `authorList` (选填,string) 指定达人列表(可选)/Specific author list (optional)
- 示例：

```
keyword = "美妆"
followerRange = "10-100"  # 10万-100万粉丝
contentTag = "tag-1"  # 美妆一级标签
contentTag = "tag_level_two-2"  # 美妆教程二级标签

# [内容标签映射表/Content Tag Mapping]

## 一级标签 (First-level tags) - 格式: tag-{id}

| 参数 | 分类 | 参数 | 分类 | 参数 | 分类 |
|------|------|------|------|------|------|
| tag-1 | 美妆 | tag-6 | 时尚 | tag-11 | 萌宠 |
| tag-15 | 测评 | tag-23 | 游戏 | tag-25 | 二次元 |
| tag-27 | 旅行 | tag-31 | 汽车 | tag-36 | 生活 |
| tag-41 | 音乐 | tag-46 | 舞蹈* | tag-48 | 美食 |
| tag-55 | 母婴亲子 | tag-60 | 运动健身 | tag-64 | 科技数码 |
| tag-68 | 教育培训 | tag-72 | 颜值达人 | tag-79 | 才艺技能 |
| tag-85 | 影视娱乐 | tag-87 | 艺术文化 | tag-91 | 财经投资 |
| tag-95 | 三农* | tag-97 | 剧情搞笑 | tag-100 | 情感* |
| tag-102 | 园艺* | tag-130 | 随拍* | tag-139 | 房产 |
| tag-1001 | 生活家居 | tag-1002 | 媒体号* | | |

*注: 标记*的分类无二级标签

## 二级标签 (Second-level tags) - 格式: tag_level_two-{id}

### 美妆 (tag-1)
- tag_level_two-2: 美妆教程
- tag_level_two-3: 妆容展示
- tag_level_two-4: 护肤保养
- tag_level_two-5: 美妆测评种草

### 时尚 (tag-6)
- tag_level_two-7: 穿搭
- tag_level_two-8: 街拍
- tag_level_two-10: 造型
- tag_level_two-135: 时尚媒体

### 萌宠 (tag-11)
- tag_level_two-12: 日常宠物
- tag_level_two-13: 特别宠物
- tag_level_two-14: 宠物周边

### 测评 (tag-15)
- tag_level_two-16: 美妆测评
- tag_level_two-17: 3C数码测评
- tag_level_two-18: 汽车测评
- tag_level_two-19: 美食产品测评
- tag_level_two-20: 母婴产品测评
- tag_level_two-21: 综合测评
- tag_level_two-132: 酒店测评

### 游戏 (tag-23)
- tag_level_two-121: 游戏剧情
- tag_level_two-122: 游戏解说
- tag_level_two-123: 游戏资讯
- tag_level_two-124: 游戏其他
- tag_level_two-440: 游戏录屏
- tag_level_two-441: 游戏集锦

### 二次元 (tag-25)
- tag_level_two-125: 二次元真人
- tag_level_two-126: 动画漫画
- tag_level_two-127: 配音声优
- tag_level_two-128: 宅物手办

### 旅行 (tag-27)
- tag_level_two-28: 旅行记录
- tag_level_two-29: 旅行攻略
- tag_level_two-30: 旅行推荐
- tag_level_two-442: 户外生活

### 汽车 (tag-31)
- tag_level_two-32: 汽车测评
- tag_level_two-33: 汽车知识
- tag_level_two-34: 汽车周边

### 生活 (tag-36)
- tag_level_two-37: 生活记录
- tag_level_two-39: 生活小窍门
- tag_level_two-40: 好物推荐
- tag_level_two-118: 健康养生
- tag_level_two-422: 婚恋

### 音乐 (tag-41)
- tag_level_two-42: 歌曲演唱
- tag_level_two-43: 乐器演奏
- tag_level_two-44: 音乐教学
- tag_level_two-45: 音乐其他
- tag_level_two-136: 音乐剪辑

### 美食 (tag-48)
- tag_level_two-49: 美食教程
- tag_level_two-50: 美食探店
- tag_level_two-52: 美食产品测评
- tag_level_two-53: 乡村野食
- tag_level_two-54: 美食其他
- tag_level_two-423: 酒类

### 母婴亲子 (tag-55)
- tag_level_two-56: 育儿科普
- tag_level_two-57: 萌娃日常
- tag_level_two-58: 亲子互动
- tag_level_two-59: 测评种草

### 运动健身 (tag-60)
- tag_level_two-61: 健身
- tag_level_two-63: 极限运动
- tag_level_two-424: 体育资讯
- tag_level_two-443: 冰雪
- tag_level_two-444: 垂钓
- tag_level_two-445: 格斗
- tag_level_two-446: 球类项目
- tag_level_two-447: 综合体育

### 科技数码 (tag-64)
- tag_level_two-65: 3C数码
- tag_level_two-66: 家居电器
- tag_level_two-133: 科技

### 教育培训 (tag-68)
- tag_level_two-69: 考学培训
- tag_level_two-70: 语言教学
- tag_level_two-71: 个人管理
- tag_level_two-425: 职业教育

### 颜值达人 (tag-72)
- tag_level_two-73: 美女
- tag_level_two-74: 帅哥

### 才艺技能 (tag-79)
- tag_level_two-80: 创意才能
- tag_level_two-81: 手工
- tag_level_two-82: 摄影
- tag_level_two-83: 绘画
- tag_level_two-84: 其他才艺

### 影视娱乐 (tag-85)
- tag_level_two-413: 影视解说
- tag_level_two-414: 影视混剪
- tag_level_two-415: 明星资讯
- tag_level_two-416: 综艺解说
- tag_level_two-417: 综艺混剪

### 艺术文化 (tag-87)
- tag_level_two-88: 传统文化
- tag_level_two-89: 人文科普
- tag_level_two-90: 自然科学

### 财经投资 (tag-91)
- tag_level_two-92: 传统金融
- tag_level_two-93: 互联网金融
- tag_level_two-94: 财经知识

### 剧情搞笑 (tag-97)
- tag_level_two-98: 剧情
- tag_level_two-99: 搞笑

### 生活家居 (tag-1001)
- tag_level_two-100101: 硬装
- tag_level_two-100102: 软装
- tag_level_two-100103: 生活技巧
- tag_level_two-100104: 家居氛围

### 房产 (tag-139)
- tag_level_two-140: 其他房产
- tag_level_two-437: 房产知识
- tag_level_two-439: 房产及投资
- tag_level_two-448: 楼盘评测
- tag_level_two-449: 楼市资讯
- tag_level_two-450: 租房
```

## 获取kol转化能力分析V1

`GET /api/v1/douyin/xingtu/kol_conversion_ability_analysis_v1`

- 用途：获取kol转化能力分析V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol转化能力分析
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `_range` (必填,string) 时间范围/Time Range
- 示例：

```
kolId = "7048929565493690398"
_range = "_1"
```

## 获取kol视频表现V1

`GET /api/v1/douyin/xingtu/kol_video_performance_v1`

- 用途：获取kol视频表现V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol视频表现
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `onlyAssign` (必填,boolean) 是否只显示分配作品/Whether to display only assigned works
- 示例：

```
kolId = "7048929565493690398"
onlyAssign = False
```

## 获取kol星图指数V1

`GET /api/v1/douyin/xingtu/kol_xingtu_index_v1`

- 用途：获取kol星图指数V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol星图指数
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取kol转化视频展示V1

`GET /api/v1/douyin/xingtu/kol_convert_video_display_v1`

- 用途：获取kol转化视频展示V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol转化视频展示
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `detailType` (必填,string) 详情类型/Detail Type
  - `page` (必填,integer) 页码/Page
- 示例：

```
kolId = "7048929565493690398"
detailType = "_1"
page = 1
```

## 获取kol连接用户V1

`GET /api/v1/douyin/xingtu/kol_link_struct_v1`

- 用途：获取kol连接用户V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol连接用户
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取kol连接用户来源V1

`GET /api/v1/douyin/xingtu/kol_touch_distribution_v1`

- 用途：获取kol连接用户来源V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol连接用户来源
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取kol性价比能力分析V1

`GET /api/v1/douyin/xingtu/kol_cp_info_v1`

- 用途：获取kol性价比能力分析V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol性价比能力分析
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取kol内容表现V1

`GET /api/v1/douyin/xingtu/kol_rec_videos_v1`

- 用途：获取kol内容表现V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol内容表现
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取kol粉丝趋势V1

`GET /api/v1/douyin/xingtu/kol_daily_fans_v1`

- 用途：获取kol粉丝趋势V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol粉丝趋势
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
  - `startDate` (必填,string) 开始日期/Start Date
  - `endDate` (必填,string) 结束日期/End Date
- 示例：

```
kolId = "7048929565493690398"
startDate = "2024-12-01"
endDate = "2025-01-01"
```

## 获取kol热词分析评论V1

`GET /api/v1/douyin/xingtu/author_hot_comment_tokens_v1`

- 用途：获取kol热词分析评论V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol热词分析评论
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取kol热词分析内容V1

`GET /api/v1/douyin/xingtu/author_content_hot_comment_keywords_v1`

- 用途：获取kol热词分析内容V1；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：kol热词分析内容
- Query：
  - `kolId` (必填,string) 用户的kolId/User kolId
- 示例：

```
kolId = "7048929565493690398"
```

## 获取达人主页视频列表V1

`GET /api/v1/douyin/xingtu/author_homepage_videos_v1`

- 用途：获取星图达人主页的视频列表；价格：0.02$ / 次
- 返回：视频列表数据，包含:
- 注意：`platform_source` and `platform_channel` default to 1 upstream and do not need to be
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu author ID
  - `page` (选填,integer) 页码，从1开始，每页20条/Page number, starts from 1, 20 items per page
  - `videoType` (选填,string) 流量类型：ALL/PERSONAL/XINGTU / Traffic type: ALL/PERSONAL/XINGTU
  - `onlyAssign` (选填,boolean) 是否仅返回指派视频/Only return assigned videos
  - `keyword` (选填,string) 视频标题关键词筛选(可选)/Filter by video title keyword (optional)
  - `startDate` (选填,string) 起始日期(可选), 格式 yyyyMMdd/Start date (optional), format yyyyMMdd
  - `endDate` (选填,string) 结束日期(可选), 格式 yyyyMMdd/End date (optional), format yyyyMMdd
- 示例：

```
oAuthorId = "7386881810501730341"
page = 1
videoType = "ALL"
onlyAssign = False
```

## 获取达人可见性状态V1

`GET /api/v1/douyin/xingtu/author_display_status_v1`

- 用途：查询达人在星图平台上的可见性状态（是否可被检索、可被下单等）；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人可见性状态
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `platformChannel` (选填,string) 平台渠道/Platform Channel
- 示例：

```
oAuthorId = "7048929565493690398"
platformChannel = "_1"
```

## 获取达人渠道指标V1

`GET /api/v1/douyin/xingtu/author_platform_channel_info_v1`

- 用途：获取达人在指定平台渠道下的指标概况；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人渠道指标
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `platformChannel` (选填,string) 平台渠道/Platform Channel
- 示例：

```
oAuthorId = "7048929565493690398"
platformChannel = "_1"
```

## 获取达人接单经验V1

`GET /api/v1/douyin/xingtu/author_order_experience_v1`

- 用途：获取达人在星图平台的接单经验数据（合作品牌、接单量等）；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人接单经验
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `period` (选填,string) 时间范围/Time Period
- 示例：

```
oAuthorId = "7048929565493690398"
period = "DAY_30"
```

## 获取达人侧基础信息V1

`GET /api/v1/douyin/xingtu/author_side_base_info_v1`

- 用途：获取达人侧的基础信息；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人侧基础信息
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
- 示例：

```
oAuthorId = "7048929565493690398"
```

## 获取达人标签V1

`GET /api/v1/douyin/xingtu/author_tags_v1`

- 用途：获取达人的标签信息（内容标签、人设标签等）；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人标签
- Query：
  - `starAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
- 示例：

```
starAuthorId = "7048929565493690398"
```

## 获取达人直播统计V1

`GET /api/v1/douyin/xingtu/author_live_statistics_v1`

- 用途：获取达人的直播统计数据；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人直播统计数据
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `liveType` (选填,string) 直播类型(可选)/Live Type (optional)
  - `period` (选填,string) 时间范围(可选)/Time Period (optional)
  - `onlyStarOrder` (选填,string) 是否仅星图订单(可选)/Only Xingtu orders (optional)
  - `flowType` (选填,string) 流量类型(可选)/Flow Type (optional)
- 示例：

```
oAuthorId = "7048929565493690398"
liveType = "ALL"
period = "DAY_30"
```

## 获取达人直播观看分布V1

`GET /api/v1/douyin/xingtu/author_live_watch_distribution_v1`

- 用途：获取达人直播的观看人群分布；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人直播观看人群分布
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `liveCrowdType` (选填,string) 人群类型(可选)/Live Crowd Type (optional)
  - `liveType` (选填,string) 直播类型(可选)/Live Type (optional)
- 示例：

```
oAuthorId = "7048929565493690398"
liveCrowdType = "AUDIENCE"
```

## 获取达人商业种草基础信息V1

`GET /api/v1/douyin/xingtu/author_commerce_seed_base_info_v1`

- 用途：获取达人商业种草的基础信息；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人商业种草基础信息
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `_range` (选填,string) 时间范围(可选)/Time Range (optional)
- 示例：

```
oAuthorId = "7048929565493690398"
_range = "DAY_90"
```

## 获取达人合同基础信息V1

`GET /api/v1/douyin/xingtu/author_contract_base_info_v1`

- 用途：获取达人合同的基础信息；该接口数据使用企业账号进行请求，收费较贵；价格：0.02$ / 次
- 返回：达人合同基础信息
- Query：
  - `oAuthorId` (必填,string) 星图达人ID/Xingtu Author ID
  - `_range` (选填,string) 时间范围(可选)/Time Range (optional)
- 示例：

```
oAuthorId = "7048929565493690398"
_range = "DAY_90"
```
