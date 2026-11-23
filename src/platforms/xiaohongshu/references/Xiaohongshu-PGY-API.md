# Xiaohongshu PGY API

文件夹 `Xiaohongshu-PGY-API` · 20 个接口
说明：小红书蒲公英数据接口


## 获取蒲公英笔记详情

`POST /api/v1/xiaohongshu/pgy/get_note_detail`

- 用途：获取单篇蒲公英笔记的详情数据
- 返回：笔记详情数据，主要字段:
- Body(JSON)：
  - `note_id` (必填,string) 笔记ID/Note ID
- 示例：

```
```json
{"note_id": "6a20edfa0000000021020951"}
```

`note_id` 从 `/get_blogger_notes` 的 `list[].noteId`、`/get_blogger_notes_v2` 的
`noteList[].noteInfo.noteId`，或 `/get_content_square` 的榜单结果里取。

Get `note_id` from `/get_blogger_notes`, `/get_blogger_notes_v2` or `/get_content_square` results.
```

## 获取蒲公英笔记精选评论

`POST /api/v1/xiaohongshu/pgy/get_note_comments`

- 用途：获取单篇笔记的精选评论，含博主本人的回复；对应蒲公英笔记详情弹窗里的「精选评论」区块
- 返回：`data.data` 是**数组**（不是对象），每项为一条评论线程:
- Body(JSON)：
  - `note_id` (必填,string) 笔记ID/Note ID
- 示例：

```
```json
{"note_id": "6a85646a0000000006005aea"}
```

**没有翻页参数**：上游固定返回精选 5 条，传 pageIndex / pageSize 也没用。
昵称和头像要用 `userIdStr` 去 `userMap` 里 join —— 评论对象本身只有 ID、没有昵称。

**No paging**: upstream always returns the same top-5 picked comments.
Join nicknames via `userMap[userIdStr]` — comment objects carry IDs only.
```

## 获取蒲公英笔记组件

`POST /api/v1/xiaohongshu/pgy/get_note_components`

- 用途：获取单篇笔记挂载的组件配置（正文搜索组件 / 评论区组件 / 底部组件）；对应笔记详情弹窗里标题下方的那几个组件标签
- 返回：`data.data` 下三个组件位，**没挂该组件时为 null**:
- Body(JSON)：
  - `note_id` (必填,string) 笔记ID/Note ID
- 示例：

```
```json
{"note_id": "6a85646a0000000006005aea"}
```

典型用法：先用 `/get_content_square` 找一批商业笔记，再逐条调本接口，
看它们分别挂了什么转化组件、导向哪个品牌或搜索词。
没挂该组件的位置返回 `null`，不是报错。

Typical flow: find sponsored notes via `/get_content_square`, then call this per note
to see which conversion component is attached. Absent slots return `null`, not an error.
```

## 获取蒲公英博主详情

`POST /api/v1/xiaohongshu/pgy/get_blogger_detail`

- 用途：获取单个博主的详细资料，对应蒲公英博主主页顶部资料区；结果已内嵌大量指标，通常不必再逐个调其它博主数据接口
- 返回：博主资料: userId / name / redId(小红书号) / headPhoto / location(地区) / personalTags(标签)；商业信息: 图文与视频报价、合作状态、所属机构(MCN)；标签: contentTags(内容类目) / featureTags(内容特征)；数据: 粉丝数、各项中位数、近 30 天曝光等
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
- 示例：

```
```json
{"user_id": "5c668b3e0000000012021605"}
```

`user_id` 从 `/get_blogger_list` 结果的 `kols[].userId` 取，或从蒲公英博主主页 URL 里截。
想要更细的数据分别用：`/get_blogger_data_summary`（成本与报价预估）、
`/get_blogger_notes_rate`（笔记表现）、`/get_blogger_fans_profile`（粉丝画像）。

Get `user_id` from `/get_blogger_list` → `kols[].userId`, or from the blogger's PGY page URL.
```

## 获取蒲公英博主笔记案例

`POST /api/v1/xiaohongshu/pgy/get_blogger_notes`

- 用途：分页获取博主的笔记明细，对应博主主页「笔记数据 → 笔记案例」；想看「这个博主接过哪些商单」，把 note_type 设为 3(合作笔记)；**本接口只覆盖原生笔记，少数博主（笔记以跨平台/跨域内容为主）会返回空列表
- 返回：list[]: 笔记数组，每条含 noteId / title / imgUrl(封面) / date(发布日期) / isVideo(是否视频)；数据: readNum(阅读) / likeNum(点赞) / collectNum(收藏) / thirdReadUserNum(站外阅读人数)；合作: isAdvertise(是否商业合作) / brandName(合作品牌)；total: 命中总数（随筛选变化，可据此算总页数）；拿到 noteId 后可调 /get_note_detail 查正文、图片/视频与完整互动数据；**注意**: 本接口的封面字段是 `imgUrl`，`/get_blogger_notes_v2` 是 `imageUrl`，一字之差
- 注意：This endpoint only covers native notes; a few bloggers (whose notes are mostly
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
  - `page_number` (选填,integer) 页码，从 1 开始/Page number, from 1
  - `page_size` (选填,integer) 每页数量，1-8（蒲公英网页固定 8）/Page size, 1-8 (fixed at 8 on PGY web)
  - `note_type` (选填,integer) 笔记类型 4=全部类型(默认) 3=合作笔记 1=图文 2=视频/Note type
  - `order_type` (选填,integer) 排序 1=最新发布(默认) 2=阅读最多 3=互动最多/Sort
  - `advertise_switch` (选填,integer) 流量类型 1=全部(含商业合作) 0=仅自然流量/Traffic type
  - `feature_tag` (选填,string) 按内容特征筛选，如 韩系；取值见博主详情的 featureTags/Filter by feature tag
  - `content_tag` (选填,string) 按内容类目筛选，如 美妆；取值见博主详情的 contentTags/Filter by content tag
  - `is_third_platform` (选填,integer) 1=只看跨域合作笔记 0=不限(默认)/Cross-platform notes only
- 示例：

```
```json
// ① 最近发布的全部笔记
{"user_id": "5c668b3e0000000012021605", "page_number": 1, "page_size": 8}

// ② 只看合作笔记（商单）
{"user_id": "5c668b3e0000000012021605", "page_number": 1, "page_size": 8, "note_type": 3}

// ③ 只看视频、按互动排序
{"user_id": "5c668b3e0000000012021605", "page_number": 1, "page_size": 8, "note_type": 2, "order_type": 2}

// ④ 只看广告投放过的笔记
{"user_id": "5c668b3e0000000012021605", "page_number": 1, "page_size": 8, "advertise_switch": 1}

// ⑤ 按类目过滤
{"user_id": "5c668b3e0000000012021605", "page_number": 1, "page_size": 8, "content_tag": "美妆"}
```

**返空时改用 `/get_blogger_notes_v2`**：本接口走原生 KOL 链路，对跨域博主可能返回空列表。
两个接口的返回结构不同（v2 在 `noteList[].noteInfo` 下），解析代码不能混用。

If this returns an empty list for a cross-domain blogger, switch to `/get_blogger_notes_v2`.
Their response shapes differ — do not reuse the same parser.
```

## 获取蒲公英博主笔记案例 v2（覆盖跨域）

`POST /api/v1/xiaohongshu/pgy/get_blogger_notes_v2`

- 用途：分页获取博主的笔记案例（v2）。与 `/get_blogger_notes` 是**两套独立接口**：
- 返回：noteList[]: 笔记数组，每条含 noteInfo（noteId / title / imageUrl / notePublishTime /
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
  - `page_number` (选填,integer) 页码，从 1 开始/Page number, from 1
  - `page_size` (选填,integer) 每页数量，1-8（蒲公英网页固定 8）/Page size, 1-8 (fixed at 8 on PGY web)
  - `note_type` (选填,integer) 笔记类型 0=全部类型(默认) 1=图文 2=视频/Note type
  - `order_type` (选填,integer) 排序 1=最新发布(默认) 2=阅读最多 3=互动最多/Sort
- 示例：

```
```json
// ① 第一页
{"user_id": "592b6f7c5e87e74d3669f3ba", "page_number": 1, "page_size": 8}

// ② 只看视频笔记
{"user_id": "592b6f7c5e87e74d3669f3ba", "page_number": 1, "page_size": 8, "note_type": 2}

// ③ 换排序
{"user_id": "592b6f7c5e87e74d3669f3ba", "page_number": 1, "page_size": 8, "order_type": 2}
```

**什么时候用这个**：`/get_blogger_notes` 对跨域博主返空时。
返回结构与那个接口不同（本接口在 `noteList[].noteInfo` 下），解析代码不要混用。

Use this when `/get_blogger_notes` returns empty for a cross-domain blogger.
```

## 获取蒲公英博主数据表现

`POST /api/v1/xiaohongshu/pgy/get_blogger_notes_rate`

- 用途：获取博主笔记的整体数据表现，用于评估内容质量与稳定性；对应博主主页「数据概览 → 笔记数据」与「笔记数据 → 数据表现」
- 返回：各项中位数: impMedian(曝光) / readMedian(阅读) / interactionMedian(互动)；比率: 互动率、完播率、百赞/千赞笔记比例；超越同行的百分位(如 impMedianBeyondRate)
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
  - `business` (选填,integer) 笔记口径 0=日常笔记(默认) 1=合作笔记/Note scope: 0=organic, 1=sponsored
  - `note_type` (选填,integer) 笔记类型 3=图文+视频(默认) 1=图文 2=视频/Note type
  - `date_type` (选填,integer) 时间范围 1=近30日(默认) 2=近90日/Date range: 1=last 30d, 2=last 90d
  - `advertise_switch` (选填,integer) 流量类型 1=全部(含合作) 0=仅自然流量/Traffic type
- 示例：

```
```json
// 日常笔记表现
{"user_id": "5c668b3e0000000012021605"}

// 合作笔记（商单）表现，近 90 日
{"user_id": "5c668b3e0000000012021605", "business": 1, "date_type": 2}
```
```

## 获取蒲公英博主核心数据

`POST /api/v1/xiaohongshu/pgy/get_blogger_core_data`

- 用途：获取博主的逐日趋势与区间汇总，用于绘制表现趋势图；对应博主主页「笔记数据 → 数据表现 → 核心指标趋势」
- 返回：dailyData[]: 逐日趋势数据点；sumData: 区间汇总（曝光/阅读/互动/CPM/CPE 等）
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
  - `business` (选填,integer) 笔记口径 0=日常笔记(默认) 1=合作笔记/Note scope
  - `note_type` (选填,integer) 笔记类型 3=图文+视频(默认) 1=图文 2=视频/Note type
  - `date_type` (选填,integer) 时间范围 1=近30日(默认) 2=近90日/Date range
  - `advertise_switch` (选填,integer) 流量类型 1=全部(含合作) 0=仅自然流量/Traffic type
- 示例：

```
```json
// ① 默认：日常笔记 · 近 30 日趋势
{"user_id": "5c668b3e0000000012021605"}

// ② 近 90 日
{"user_id": "5c668b3e0000000012021605", "date_type": 2}

// ③ 合作笔记口径 · 仅自然流量
{"user_id": "5c668b3e0000000012021605", "business": 1, "advertise_switch": 0}

// ④ 只看视频 · 近 90 日 · 合作笔记
{"user_id": "5c668b3e0000000012021605", "business": 1, "note_type": 2, "date_type": 2}
```

`dailyData[]` 可直接画趋势图，`sumData` 是同区间的汇总值。
逐日点数随 `date_type` 变化（近 30 日约 30 个点）。
```

## 获取蒲公英博主数据概览

`POST /api/v1/xiaohongshu/pgy/get_blogger_data_summary`

- 用途：获取博主账号维度的数据概览汇总
- 返回：成本/报价预估: estimatePictureCpm / estimateVideoCpm / pictureReadCost 等；服务表现: 近 7 天活跃天数、邀约 48 小时回复率；成长表现: 粉丝量变化幅度及其同行百分位
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
  - `business` (选填,integer) 笔记口径 0=日常笔记(默认) 1=合作笔记/Note scope
- 示例：

```
```json
// ① 日常笔记口径
{"user_id": "5c668b3e0000000012021605"}

// ② 合作笔记口径（按商单价格评估性价比时用这个）
{"user_id": "5c668b3e0000000012021605", "business": 1}
```

**两种口径的成本类指标不同** —— 实测同一博主日常图文 CPM ≈11、合作口径 ≈19。
想评估「按商单价格算的性价比」请传 `business=1`。

The two modes yield different cost metrics; pass `business=1` to evaluate sponsored-price ROI.
```

## 获取蒲公英博主粉丝概览

`POST /api/v1/xiaohongshu/pgy/get_blogger_fans_summary`

- 用途：获取博主粉丝的核心指标概览，对应博主主页「粉丝分析 → 核心指标」
- 返回：fansNum(粉丝数) / fansIncreaseNum(增量) / fansGrowthRate(增长率)；activeFansRate(活跃粉丝占比) / 阅读粉丝占比 / 互动粉丝占比；各项的同行百分位（如 activeFansBeyondRate）
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
- 示例：

```
```json
{"user_id": "5c668b3e0000000012021605"}
```

配合 `/get_blogger_fans_profile`（画像）与 `/get_blogger_fans_history`（趋势）一起看，
三个接口分别回答「粉丝有多少」「粉丝是谁」「粉丝怎么变的」。

Use together with `/get_blogger_fans_profile` and `/get_blogger_fans_history`.
```

## 获取蒲公英博主粉丝画像

`POST /api/v1/xiaohongshu/pgy/get_blogger_fans_profile`

- 用途：获取博主粉丝的分布画像，用于判断受众与品牌目标人群是否吻合
- 返回：ages[]: 年龄分布；gender: 性别分布（male / female）；provinces[] / cities[]: 地域分布（省 / 市）；devices[]: 设备分布；interests[]: 兴趣分布
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
- 示例：

```
```json
{"user_id": "5c668b3e0000000012021605"}
```

选号时最常用的两个字段是 `gender`（性别构成）与 `cities[]`（城市分布）——
投地域性强的产品时先看这两个再决定要不要谈。

The two most-used fields when shortlisting: `gender` and `cities[]`.
```

## 获取蒲公英博主粉丝增长历史

`POST /api/v1/xiaohongshu/pgy/get_blogger_fans_history`

- 用途：获取博主粉丝随时间的变化曲线，对应博主主页「粉丝分析 → 粉丝趋势」
- 返回：list[]: 逐日数据点（当日值与日期）；fansNumInc: 区间净增；fansNumIncRate: 区间增长率
- Body(JSON)：
  - `user_id` (必填,string) 博主用户ID/Blogger user ID
  - `increase_type` (选填,integer) 曲线口径 1=粉丝总量(默认，累计) 2=粉丝增量(每日新增)/Curve: 1=total, 2=daily increment
  - `date_type` (选填,integer) 时间范围 1=近30日(默认) 2=近60日/Date range: 1=last 30d, 2=last 60d
- 示例：

```
```json
// ① 累计粉丝数曲线（默认，近 30 日）
{"user_id": "5c668b3e0000000012021605"}

// ② 每日新增曲线，近 60 日
{"user_id": "5c668b3e0000000012021605", "increase_type": 2, "date_type": 2}

// ③ 累计曲线拉到近 60 日
{"user_id": "5c668b3e0000000012021605", "date_type": 2}
```

`increase_type=2` 的曲线出现孤立尖峰，通常意味着买量或蹭到热点，
选号时值得再看一眼那几天的笔记。

Isolated spikes in the daily-increase curve usually mean bought traffic or a viral hit.
```

## 获取蒲公英相似博主推荐

`POST /api/v1/xiaohongshu/pgy/get_blogger_similar`

- 用途：给定一个博主，返回平台判定与其相似的其它博主，对应博主主页下方「相似博主推荐」；典型用法：先选出一个满意的标杆博主，再用本接口按相似度扩量选号
- 返回：结构与「笔记博主广场」完全一致 —— 同样的 kols[] + total，可直接复用解析代码；相似博主总数通常只有个位数到几十，total 即为上限
- Body(JSON)：
  - `user_id` (必填,string) 目标博主用户ID/Target blogger user ID
  - `page_num` (选填,integer) 页码，从 1 开始/Page
  - `page_size` (选填,integer) 每页数量，1-4（网页固定 4）/Page size, 1-4
- 示例：

```
```json
// ① 第一页（每页最多 4 个，这是蒲公英网页的固定值）
{"user_id": "5c668b3e0000000012021605", "page_num": 1, "page_size": 4}

// ② 翻页：只改 page_num
{"user_id": "5c668b3e0000000012021605", "page_num": 2, "page_size": 4}
```

**想「找相似 + 再按粉丝量/报价筛一遍」**，用 `/get_blogger_list` 的 `similar_user_id`
参数 —— 那条链路支持叠加全部筛选；本接口只按相似度返回、不支持筛选。

To combine similarity with other filters, use `similar_user_id` on `/get_blogger_list` instead.
```

## 蒲公英笔记博主广场（找博主/选号）

`POST /api/v1/xiaohongshu/pgy/get_blogger_list`

- 用途：复刻蒲公英网页「找博主 → 笔记博主广场」的搜索与筛选，约 60 个筛选条件按 7 组传入；每条结果内嵌约 140 个字段（报价、阅读/互动中位数、直播场次等），通常不必再逐个调博主详情类接口
- Body(JSON)：
  - `page_num` (选填,integer) 页码，1-250（上游只放出前 5000 条）/Page, 1-250
  - `page_size` (选填,integer) 每页数量，1-20（网页固定 20，建议保持 20）/Page size, 1-20
  - `keyword` (选填,string) 搜索词；空=只筛选不搜索/Keyword
  - `search_type` (选填,integer) 1=按笔记关键词找博主(默认) 0=按昵称搜/Search mode
  - `column` (选填,string) 排序字段，共 34 个，见接口说明的排序字段表/Sort column, 34 options, see endpoint docs
  - `sort` (选填,string) 排序方向 desc/asc
  - `brand_user_id` (选填) 品牌方/广告主用户ID，可不填/Brand user ID, optional
  - `similar_user_id` (选填) 找相似博主：填一个博主的 userId，返回与他相似的博主，**并且可以叠加下面所有筛选**（这是它与 /get_blogger_similar 的关键区别）/Find similar bloggers; unlike /get_blogger_similar it can be combined with all filters below
  - `similar_word` (选填) 配合 similar_user_id 的博主昵称，仅用于回显、不影响结果/Nickname echo for similar_user_id; does not affect results
  - `goal` (选填) 合作目标筛选/Cooperation goal filters
  - `blogger` (选填) 博主属性筛选/Blogger attribute filters
  - `fans` (选填) 粉丝画像筛选/Fans profile filters
  - `note` (选填) 日常笔记数据筛选/Organic note metric filters
  - `coop` (选填) 合作笔记数据筛选/Sponsored note metric filters
  - `live` (选填) 直播数据筛选/Live metric filters
  - `flags` (选填) 开关类筛选/Boolean flag filters
- 示例：

```
```json
// ① 关键词找博主：搜「咖啡」相关笔记的博主，按粉丝数降序；带品牌方 ID 做个性化推荐并剔除已合作过的
{"page_num": 1, "page_size": 20, "keyword": "咖啡", "search_type": 1,
 "column": "fansCount", "sort": "desc",
 "brand_user_id": "5dcfa5370000000001006030",
 "flags": {"exclude_cooperated": true}}

// ② 按昵称找号：search_type=0 时 keyword 匹配的是博主昵称而不是笔记内容
{"page_num": 1, "page_size": 20, "keyword": "小鹿", "search_type": 0}

// ③ 最基础的类目 + 粉丝量筛选：粉丝 1 万-5 万的美妆博主，按互动中位数降序
{"page_num": 1, "page_size": 20, "column": "mEngagementNum",
 "fans": {"count": {"min": 10000, "max": 50000}},
 "blogger": {"content_tag": ["美妆"]}}

// ④ 按画像选号：1 万-5 万粉、粉丝以 25-34 岁女性为主的美妆「妈妈」博主
{"page_num": 1, "page_size": 20,
 "blogger": {"content_tag": ["美妆"], "personal_tags": ["妈妈"]},
 "fans": {"count": {"min": 10000, "max": 50000}, "gender": 2, "age": 3}}

// ⑤ 按预算与响应速度选号：图文报价 1 万-5 万、48h 邀约回复率 ≥80%
{"page_num": 1, "page_size": 20,
 "coop": {"pic_price": {"min": 10000, "max": 50000},
          "reply_48h_ratio": {"min": 80}}}

// ⑥ 按性价比选号：图文报价 ≤5000、阅读中位数 ≥3000 的视频博主，只看优质号并剔除低活
{"page_num": 1, "page_size": 20,
 "note": {"read_median": {"min": 3000}, "note_type": 2},
 "coop": {"pic_price": {"max": 5000}},
 "flags": {"high_quality": true, "exclude_low_active": true}}

// ⑦ 找会直播带货的博主：近 30 天开播 1-5 场、场均销售额 ≥1 万，且笔记+直播均可合作
{"page_num": 1, "page_size": 20,
 "live": {"live_count": {"min": 1, "max": 5}, "avg_gmv": {"min": 10000}},
 "flags": {"note_and_live": true}}

// ⑧ 多维组合：7 个筛选组同时生效（字段名写错会直接 422，不会被静默忽略）
{"page_num": 1, "page_size": 20, "column": "comprehensiverank", "sort": "desc",
 "goal":    {"market_target": "mAccumImpNum"},
 "blogger": {"content_tag": ["美妆"], "gender": "女", "signed": 0},
 "fans":    {"count": {"min": 10000}, "age": 3, "device_brand": ["苹果"]},
 "note":    {"inter_median": {"min": 500}, "thousand_like_percent": {"min": 20}},
 "coop":    {"industry": "美妆个护", "video_price": {"max": 8000}},
 "live":    {"avg_viewer": {"min": 5000}},
 "flags":   {"exclude_cooperated": true}}


// ⑨ 找相似博主：给一个满意的标杆博主，扩一批相似的，**并叠加自己的筛选**
//    （/get_blogger_similar 只按相似度返回、不支持筛选，需要叠加筛选就用这里）
{"page_num": 1, "page_size": 20,
 "similar_user_id": "5a8cf39111be10466d285d6b",
 "fans": {"count": {"min": 50000}},
 "coop": {"pic_price": {"max": 20000}}}

// ⑩ 预算优先：按「图文预估阅读单价」从低到高排，先看最便宜的
{"page_num": 1, "page_size": 20,
 "column": "pictureReadCost", "sort": "asc",
 "coop": {"pic_price": {"min": 1000, "max": 10000}}}

// ⑪ 涨粉快的新秀：按近 30 天粉丝增长率降序，并剔除掉粉的
{"page_num": 1, "page_size": 20,
 "column": "fans30GrowthRate", "sort": "desc",
 "fans": {"count": {"min": 5000, "max": 100000}},
 "flags": {"exclude_fans_down": true}}

// ⑫ 爆款率优先：按百赞笔记占比降序（看重内容稳定性而非粉丝量时用）
{"page_num": 1, "page_size": 20,
 "column": "hundredLikePercent30", "sort": "desc",
 "note": {"thousand_like_percent": {"min": 10}}}

// ⑬ 地域投放：找上海本地的探店博主
//    blogger.location 直接填地名即可，不要填「上海市-上海市-黄浦区」这种全路径
{"page_num": 1, "page_size": 20,
 "blogger": {"location": ["上海"], "content_tag": ["美食"]}}

// ⑭ 按粉丝所在地投放（和 ⑬ 是两个不同维度：⑬ 是博主在哪，⑭ 是粉丝在哪）
{"page_num": 1, "page_size": 20,
 "fans": {"location": ["广东"], "count": {"min": 20000}}}

// ⑮ 直播带货 + 90 天口径：场均观播 ≥5000、场均销售额 ≥1 万
//    注意 avg_viewer / avg_gmv 是近 90 天，而 live_count 是近 30 天
{"page_num": 1, "page_size": 20,
 "live": {"live_count": {"min": 1}, "avg_viewer": {"min": 5000}, "avg_gmv": {"min": 10000}}}
```

### 常见错误写法 / Common mistakes

分两类。**第二类才是真正的坑** —— 它们不会报错，只会安静返回 0 条。

#### A. 会直接 422 的写法（好在会立刻报错）

```json
// ✗ 区间写成了数字 —— 区间型字段必须是对象
{"fans": {"count": 10000}}
// ✓
{"fans": {"count": {"min": 10000}}}

// ✗ 字段名拼错（驼峰）—— 本接口 extra="forbid"，写错直接 422，不会被静默忽略
{"blogger": {"contentTag": ["美妆"]}}
// ✓
{"blogger": {"content_tag": ["美妆"]}}

// ✗ 排序列填了未放行的值
{"column": "forecastReadUv"}
// ✓ 见第 1 节的 34 个排序字段
{"column": "avgAgmv90d"}

// ✗ page_size 超上限（1-20）
{"page_size": 100}
// ✓
{"page_size": 20}

// ✗ 百分比量纲错了 —— 千赞比例填 200 或 9500（按万分比/原始条数填）
{"note": {"thousand_like_percent": {"min": 200}}}
// ✓ 想表达「20%」就填 20
{"note": {"thousand_like_percent": {"min": 20}}}
```

#### B. 不会报错、但查不到数据的写法（最难排查）

下面这些**全都能通过校验**，返回 200，结果却是 0 条 —— 因为值本身合法、只是没有匹配项。

```json
// ✗ 地域填了带分隔符的全路径
{"blogger": {"location": ["上海市-上海市-黄浦区"]}}
// ✓ 直接填地名
{"blogger": {"location": ["上海"]}}

// ✗ 百分比填了小数（0.2 是合法的 0.2%，不是 20%）
{"note": {"thousand_like_percent": {"min": 0.2}}}
// ✓ 想表达「20%」
{"note": {"thousand_like_percent": {"min": 20}}}

// ✗ 类目值是自己编的
{"blogger": {"content_tag": ["美妆护肤"]}}
// ✓ 用 /get_blogger_filter_options 的 contentTags 里真实存在的值
{"blogger": {"content_tag": ["美妆"]}}

// ✗ 开关型填 false —— 等于没筛，不是「反向筛」
{"flags": {"exclude_cooperated": false}}
// ✓ 想生效就填 true
{"flags": {"exclude_cooperated": true}}

// ✗ 把「行业」当成「博主类目」用（两个是不同的筛选）
{"flags": {"industry_first": "美妆"}}
// ✓ 博主类目用 blogger.content_tag
{"blogger": {"content_tag": ["美妆"]}}
```

**搜不到结果时的排查顺序**：先把筛选一个个去掉，定位是哪个条件卡住的；
需要查字典的筛选（类目 / 场景 / 消费行为 / 地域）优先怀疑值写错了。
```

## 获取蒲公英找博主筛选项字典

`POST /api/v1/xiaohongshu/pgy/get_blogger_filter_options`

- 用途：获取 `/get_blogger_list` 里那些**树形筛选**的可选值，是找博主的配套字典接口；这些选项由平台维护、会随运营变动，**不要写死在代码里**；结果基本不变，建议客户端缓存后复用
- 返回：`industryTags` → 网页「**行业**」（`taxonomy1Tag` 一级 + `taxonomy2Tags` 二级），
- 示例：

```
```json
// 取全部字典（首次接入时跑一次，把结果缓存起来）
{}
```

字典变化很慢，**建议本地缓存复用**，不必每次筛选前都调。

需要先查本接口才能填的筛选：博主类目（`contentTags`，含二级如 美妆 → 唇妆/眼妆）、
笔记场景（`contentScenes`）、预估消费行为（`consumerBehavior`）、
博主地域（`areas`，到区县）、粉丝地域（`fansAreas`，只到市）。
其余多数筛选是固定枚举，照 `/get_blogger_list` 的文档直接填即可。

Cache the result — it rarely changes. Dictionary-backed filters: blogger category,
note scene, consumption behavior, blogger/fans location.
```

## 蒲公英直播博主广场（直播带货选号）

`POST /api/v1/xiaohongshu/pgy/get_live_blogger_list`

- 用途：复刻蒲公英网页「找博主 → 直播博主广场」，按电商转化力/直播表现/粉丝购买力等筛选带货博主
- Body(JSON)：
  - `page_num` (选填,integer) 页码，1-250（上游只放出前 5000 条）/Page, 1-250
  - `page_size` (选填,integer) 每页数量，1-20（网页固定 20）/Page size, 1-20
  - `seed` (选填,integer) 翻页种子：首页传 0，之后回传上一页返回的 seed/Paging seed, echo back from previous page
  - `nick_name` (选填,string) 按博主昵称搜索/Search by nickname
  - `category` (选填) 合作品类/Category filters
  - `buyer` (选填) 买手天团 + 内容人设/Buyer group & persona filters
  - `ecom` (选填) 电商转化力/E-commerce conversion filters
  - `live` (选填) 直播投入度 + 表现力/Live activity & performance filters
  - `fans` (选填) 粉丝购买力/Fans purchasing power filters
  - `flags` (选填) 平台推荐开关/Platform recommendation flags
- 示例：

```
```json
// ① 快速开始：主营女装、场均销售额 ≥10 万的买手
{"page_num": 1, "page_size": 20,
 "category": {"first": ["女装/女士精品"]},
 "ecom": {"avg_gmv": {"min": 100000}}}

// ② 有直播计划、观播人数高、且能看到联系方式的买手
{"page_num": 1, "page_size": 20,
 "live": {"has_plan": true, "avg_viewer": {"min": 10000}},
 "flags": {"contact_visible": true, "actively_seeking": true}}

// ③ 按粉丝购买力选号（女性粉丝占比高 + 高消费人群占比高）
{"page_num": 1, "page_size": 20,
 "fans": {"count": {"min": 10000, "max": 100000}, "gender": 2, "consumption": ["high"]}}

// ④ 高客单价 + 买手天团/内容人设标签（atv 按档位匹配，与区间有重叠的档位都会命中）
{"page_num": 1, "page_size": 20,
 "ecom": {"atv": {"min": 200, "max": 500}, "brand_avg_gmv": {"min": 50000}},
 "buyer": {"group_tag": ["气质简约"], "persona_tag": ["模特"]}}

// ⑤ 按昵称搜索 + 合作品类下钻到二级，只看邀约回复率高的
{"page_num": 1, "page_size": 20, "nick_name": "李",
 "category": {"first": ["女装/女士精品"], "second": ["连衣裙"]},
 "flags": {"high_reply_rate": true}}

// ⑥ 指定日期有排播的日播买手（plan_days 为 YYYYMMDD，需配合 has_plan 使用）
{"page_num": 1, "page_size": 20,
 "live": {"has_plan": true, "plan_days": ["20260901", "20260902"], "max_online": {"min": 5000}},
 "fans": {"age": 3, "consumption": ["high", "middle"]},
 "flags": {"daily_buyer": true, "live_potential_high": true}}

// ⑦ 翻页第 1 页：seed 传 0（或省略），从响应里取回本次结果集的 seed
{"page_num": 1, "page_size": 20, "seed": 0}

// ⑧ 翻页第 2 页：把上一页返回的 seed 原样带上，其余筛选必须保持不变
{"page_num": 2, "page_size": 20, "seed": 1787045123}

// 取数：buyers = resp["data"]["data"]["distributor_info_list"]；下一页要回传的 seed = resp["data"]["data"]["seed"]
```
```

## 蒲公英内容广场（热门内容榜单）

`POST /api/v1/xiaohongshu/pgy/get_content_square`

- 用途：复刻蒲公英「学内容 → 创意灵感 → 内容广场」：**不需要任何 ID**，直接查「现在什么内容在火」；与其它接口方向相反 —— 其余接口都要先有博主/笔记 ID，本接口是入口式的，
- Body(JSON)：
  - `biz_type` (必填,integer) 榜单 1=小红书热门 2=产品种草 3=电商推广 4=蒲公英合作 5=客资收集 6=电商热门 7=种草直达 8=应用推广/Leaderboard
  - `page_num` (选填,integer) 页码；每个榜固定只有 100 条/Page; each board has only 100 items
  - `page_size` (选填,integer) 每页数量，1-34（网页固定 34）/Page size, 1-34
  - `search_word` (选填,string) 关键词，留空=看整榜；支持英文逗号分隔批量搜/Keyword, comma-separated for batch
  - `order_by` (选填,string) 排序字段，留空=用该榜默认排序/Sort field, empty=board default
  - `date_range` (选填,integer) 统计窗口：近 3/7/14/30 日/Date window in days
  - `sub_biz_type` (选填) 【仅榜 8】1=应用下载 2=小程序推广 3=应用唤起(默认)/Board 8 only
  - `category` (选填) 【仅榜 1】类目，格式「一级#二级」，如 "内容类目#美妆"/Board 1 only
  - `industry` (选填) 【榜 2/3/4/5/6/7/8】所属行业名，取值集因榜而异/Industry, values differ per board
  - `note_type` (选填) 内容类型 1=图文 2=视频/Content type
  - `content_type` (选填) 内容来源 1=博主合作 2=明星合作 3=员工 5=买手 6=专业号 11=主理人 -1=用户/Content source
  - `theme` (选填) 【榜 2/4/5/7/8】题材名/Theme
  - `author_type` (选填) 【仅榜 4】1=蒲公英博主 2=明星/Board 4 only
  - `placement` (选填) 【榜 2/3/5/7/8】流量场域 1=发现 2=搜索 3=视频内流/Traffic placement
  - `marketing_target` (选填) 【仅榜 3】3=商品推广 8=直播推广/Board 3 only
  - `price` (选填) 【仅榜 4】创作者报价/Creator price, board 4 only
  - `fans` (选填) 【仅榜 4】创作者粉丝量区间/Creator fans range, board 4 only
- 示例：

```
```json
// ① 近 7 日全平台最热的美妆视频（榜 1 用 category，不是 industry）
{"biz_type": 1, "category": "内容类目#美妆", "note_type": 2}

// ② 母婴行业近 30 日互动率最高的蒲公英合作笔记，博主图文报价 1~5 万
{"biz_type": 4, "industry": "母婴", "date_range": 30,
 "order_by": "premium_engage_rate",
 "price": {"kind": 1, "range": {"min": 10000, "max": 50000}}}

// ③ 电商推广榜按笔记支付金额排序，只看搜索场域
{"biz_type": 3, "order_by": "premium_ecm_dgmv", "placement": 2}

// ④ 带关键词看榜
{"biz_type": 1, "search_word": "面膜"}

// ⑤ 批量关键词（英文逗号分隔）+ 只看博主合作笔记
{"biz_type": 1, "search_word": "面膜,精华", "content_type": 1}

// ⑥ 翻页：只改 page_num，其余参数原样不动（改了口径两页会重复/遗漏）；每榜只有 100 条，34/页翻到第 3 页到底
{"biz_type": 1, "page_num": 1, "page_size": 34, "category": "内容类目#美妆"}
{"biz_type": 1, "page_num": 2, "page_size": 34, "category": "内容类目#美妆"}

// ⑦ 蒲公英合作榜（仅榜 4 支持站外指标）：按小红星站外转化率排，限蒲公英博主、10~50 万粉的视频
{"biz_type": 4, "order_by": "taobao_third_active_pgy_user_ratio", "author_type": 1,
 "note_type": 2, "fans": {"min": 100000, "max": 500000}}

// ⑧ 产品种草榜近 3 日：美妆个护行业、测评题材、发现页场域的图文（留空 order_by = 用该榜默认排序）
{"biz_type": 2, "industry": "美妆个护", "theme": "测评类", "placement": 1,
 "note_type": 1, "date_range": 3}

// ⑨ 电商推广榜只看直播推广（marketing_target 仅榜 3 可用），按支付订单数排
{"biz_type": 3, "marketing_target": 8, "order_by": "premium_ecm_order_pv", "note_type": 2}

// ⑩ 电商热门榜近 14 日：industry 这里是电商商品类目（与榜 2/4/5/7/8 的行业名不是一套），看买手笔记的支付转化率
{"biz_type": 6, "industry": "厨房电器", "order_by": "premium_ecm_order_rate",
 "content_type": 5, "date_range": 14}

// ⑪ 应用推广榜（sub_biz_type 仅榜 8 可用）：应用下载口径、互联网行业、发现页的知识科普题材
{"biz_type": 8, "sub_biz_type": 1, "industry": "互联网", "placement": 1, "theme": "知识科普"}

// 取数：notes = resp["data"]["data"]["noteList"]
```
```

## 蒲公英关键词概览（搜索指数+博主画像）

`POST /api/v1/xiaohongshu/pgy/get_keyword_stat`

- 用途：给定一个关键词，返回它在小红书全站的热度概览，以及发这个词的博主长什么样；对应蒲公英内容广场搜索后的「全站数据」+「合作博主画像」两张卡片
- Body(JSON)：
  - `search_word` (必填,string) 关键词，如 面膜/Keyword
- 示例：

```
```json
{"search_word": "面膜"}
```

**选题流程**：`/get_keyword_related` 扩出一批词 → 逐个调本接口比 `searchScore`
与 `noteNum` → 挑「搜索量不低但笔记数少」的词，即竞争小的机会词。

同一个关键词还可以调 `/get_keyword_daily` 看逐日走势。三个接口互相独立，按需调用。

Workflow: expand words via `/get_keyword_related`, compare `searchScore` vs `noteNum` here,
pick high-search / low-supply keywords.
```

## 蒲公英关键词逐日搜索指数

`POST /api/v1/xiaohongshu/pgy/get_keyword_daily`

- 用途：关键词的搜索热度逐日走势，用来判断一个词是在涨还是在退、有没有季节性；对应内容广场搜索后「全站数据 → 查看详情」里的趋势图
- 返回：`dailyData[]`: 每天一条，含 `dateKey` 日期、`searchScore` 搜索指数、
- Body(JSON)：
  - `search_word` (必填,string) 关键词，如 面膜/Keyword
- 示例：

```
```json
{"search_word": "面膜"}
```

用来判断一个词是在涨还是在退、有没有季节性。
时间范围由平台决定（实测约近三个月），**没有可调的时间参数**。
要汇总值与环比请用 `/get_keyword_stat`。

Time range is decided upstream (~3 months) and is not adjustable.
```

## 蒲公英关键词关联词（选题扩词）

`POST /api/v1/xiaohongshu/pgy/get_keyword_related`

- 用途：返回用户搜这个词**之前**和**之后**还会搜什么，对应内容广场的「相关灵感」卡片；典型用法是选题扩词：拿一个核心词跑出一批关联词，再用 `/get_keyword_stat` 逐个比热度，
- 返回：`upSearchWords[]`（上游词）与 `downSearchWords[]`（下游词）；每个词自带 `searchScore` 搜索指数、`readTotalCount` 阅读总量、`noteNum` 笔记数、
- Body(JSON)：
  - `search_word` (必填,string) 关键词，如 面膜/Keyword
- 示例：

```
```json
{"search_word": "面膜"}
```

返回的 `upSearchWords[]`（上游词）与 `downSearchWords[]`（下游词）就是扩词的种子，
拿去逐个跑 `/get_keyword_stat` 比热度，挑竞争小的。

`upSearchWords[]` / `downSearchWords[]` are your expansion seeds — score them with
`/get_keyword_stat`.
```
