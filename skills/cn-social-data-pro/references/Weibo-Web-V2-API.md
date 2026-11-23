# Weibo Web V2 API

文件夹 `Weibo-Web-V2-API` · 33 个接口
说明：新浪微博 Web V2 数据接口


## 检查微博是否允许带图评论

`GET /api/v1/weibo/web_v2/check_allow_comment_with_pic`

- 用途：检查指定微博是否允许用户在评论时上传图片
- 返回：result: true表示允许带图评论，false表示不允许
- 注意：不同微博的图片评论权限可能不同
- Query：
  - `id` (必填,string) 微博ID/Weibo ID
- 示例：

```
id = "5092682368025584"
```

## 获取单个作品数据

`GET /api/v1/weibo/web_v2/fetch_post_detail`

- 用途：获取指定微博的详细信息，包括内容、作者、互动数据等
- 返回：微博详细数据，包含完整文本、图片、视频、点赞数、评论数、转发数等
- Query：
  - `id` (必填,string) 作品id/Post id
  - `is_get_long_text` (选填,string) 是否获取长微博全文/Whether to get the full text of long Weibo posts (true/false)
- 示例：

```
id = "5092682368025584"
is_get_long_text = "true"
```

## 获取用户信息

`GET /api/v1/weibo/web_v2/fetch_user_info`

- 用途：获取微博用户的详细信息，包括昵称、头像、简介、关注数、粉丝数等
- 返回：用户详细信息数据
- 注意：uid和custom参数至少需要提供一个；如果同时提供，优先使用uid；建议优先使用uid参数
- Query：
  - `uid` (选填) 用户id/User id
  - `custom` (选填) 自定义微博用户名/Custom Weibo username
- 示例：

```
uid = "1722594714"
# or
custom = "shuqi"
```

## 获取用户基本信息

`GET /api/v1/weibo/web_v2/fetch_user_basic_info`

- 用途：获取微博用户的基本信息（轻量级接口）
- 返回：用户基本信息，包括用户ID、用户名、头像、简介、认证信息
- 注意：与fetch_user_info相比，本接口返回数据更少，响应更快；适合批量用户信息获取和用户卡片展示
- Query：
  - `uid` (必填,string) 用户id/User id
- 示例：

```
uid = "7277477906"
```

## 获取微博用户文章数据

`GET /api/v1/weibo/web_v2/fetch_user_posts`

- 用途：获取指定用户发布的微博列表，支持分页和多种数据详细程度
- 返回：微博列表数据，包含微博内容、图片、视频等信息；包含 since_id 字段用于翻页
- 注意：feature=0性能最佳，feature=3数据最全
- Query：
  - `uid` (必填,string) 用户id/User id
  - `page` (选填,integer) 页数/Page number
  - `feature` (选填,integer) 特征值，控制返回数据的数量和字段：0=返回10条基础数据，1=返回20条扩展数据，2=返回20条图片相关数据，3=返回20条视频相关数据，字段逐级增加/Feature type: 0=10 basic posts, 1=20 extended posts, 2=20 image-related posts, 3=20 video-related posts, fields increase progressively
  - `since_id` (选填,string) 翻页标识，用于获取下一页数据/Pagination identifier for getting next page data
- 示例：

```
uid = "7277477906"
page = 1
feature = 0
```
- 返回结构（实测）：
  - `data` 是对象（2 个字段）：`data`, `ok`
  - `data.data` 是对象（7 个字段）：`since_id`, `list`, `status_visible`, `bottom_tips_visible`, `bottom_tips_text`, `topicList`, `total`
  - `data.data.list` 是数组（长度 20）；首元素字段：`visible`, `created_at`, `id`, `idstr`, `mid`, `mblogid`, `user`, `can_edit`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取微博用户原创微博数据

`GET /api/v1/weibo/web_v2/fetch_user_original_posts`

- 用途：获取指定用户发布的原创微博列表（排除转发内容）
- 返回：原创微博列表，包含微博内容、图片、视频、互动数据等
- 注意：与fetch_user_posts的区别：本接口只返回原创微博，排除转发；since_id必须先调用fetch_user_posts获取，第一页必传，后续页面不传
- Query：
  - `uid` (必填,string) 用户id/User id
  - `page` (选填,integer) 页数/Page number
  - `since_id` (选填,string) 翻页标识，用于获取下一页数据/Pagination identifier for getting next page data
- 示例：

```
uid = "7277477906"
page = 1
since_id = "4924526881242703"  # from fetch_user_posts response
```

## 获取微博评论

`GET /api/v1/weibo/web_v2/fetch_post_comments`

- 用途：获取指定微博的一级评论列表
- 返回：评论列表数据，包含评论内容、评论者信息、点赞数等；包含 max_id 字段用于翻页
- 注意：当没有更多评论时，max_id 为空
- Query：
  - `id` (必填,string) 微博ID/Weibo ID
  - `count` (选填,integer) 评论数量/Number of comments
  - `max_id` (选填,string) 页码/Page number
- 示例：

```
id = "5283919831764022"
count = 10
max_id = ""
```

## 获取微博子评论

`GET /api/v1/weibo/web_v2/fetch_post_sub_comments`

- 用途：获取指定评论的回复（子评论）列表
- 返回：子评论列表数据，包含回复内容、回复者信息、点赞数等；包含 max_id 字段用于翻页
- 注意：与fetch_post_comments的区别：本接口获取的是评论的回复，而非微博的主评论
- Query：
  - `id` (必填,string) 主评论ID/Comment ID
  - `count` (选填,integer) 子评论数量/Number of sub-comments
  - `max_id` (选填,string) 分页标识/Page identifier
- 示例：

```
id = "5283574244704555"
count = 10
max_id = ""
```

## 搜索用户微博

`GET /api/v1/weibo/web_v2/search_user_posts`

- 用途：在指定用户的微博中搜索包含特定关键词的内容
- 返回：搜索结果列表，包含微博内容、作者信息、互动数据等
- 注意：搜索结果受用户隐私设置影响；时间戳参数使用Unix时间戳格式
- Query：
  - `uid` (必填,string) 用户ID/User ID
  - `q` (选填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页数/Page number
  - `starttime` (选填) 开始时间戳/Start timestamp
  - `endtime` (选填) 结束时间戳/End timestamp
  - `hasori` (选填,integer) 是否包含原创微博，1=包含，0=不包含/Include original posts, 1=include, 0=exclude
  - `hasret` (选填,integer) 是否包含转发微博，1=包含，0=不包含/Include retweets, 1=include, 0=exclude
  - `hastext` (选填,integer) 是否包含文字微博，1=包含，0=不包含/Include text posts, 1=include, 0=exclude
  - `haspic` (选填,integer) 是否包含图片微博，1=包含，0=不包含/Include image posts, 1=include, 0=exclude
  - `hasvideo` (选填,integer) 是否包含视频微博，1=包含，0=不包含/Include video posts, 1=include, 0=exclude
  - `hasmusic` (选填,integer) 是否包含音乐微博，1=包含，0=不包含/Include music posts, 1=include, 0=exclude
- 示例：

```
uid = "7277477906"
q = "python" # 为空表示搜索全部内容
page = 1
```

## 获取用户微博视频收藏夹列表

`GET /api/v1/weibo/web_v2/fetch_user_video_collection_list`

- 用途：获取指定用户的视频收藏夹列表
- 返回：收藏夹列表，包含收藏夹ID、名称、描述、视频数量等
- 注意：收藏夹列表受用户隐私设置影响；部分用户可能没有创建视频收藏夹
- Query：
  - `uid` (必填,string) 用户ID/User ID
- 示例：

```
uid = "7277477906"
```

## 获取用户微博视频收藏夹详情

`GET /api/v1/weibo/web_v2/fetch_user_video_collection_detail`

- 用途：获取指定收藏夹的详细内容，包括视频列表
- 返回：收藏夹信息和视频列表，包含视频标题、封面、时长、播放数等；包含 next_cursor 和 has_more 字段用于翻页
- 注意：不同排序方式的cursor不通用，切换排序需重新开始分页
- Query：
  - `cid` (必填,string) 收藏夹ID/Collection ID
  - `cursor` (选填,string) 分页游标/Pagination cursor
  - `tab_code` (选填,integer) 排序方式：0=默认，1=最热，2=最新/Sort type: 0=default, 1=hottest, 2=latest
- 示例：

```
cid = "4883992307236954"
cursor = ""
tab_code = 0
```

## 获取微博用户全部视频

`GET /api/v1/weibo/web_v2/fetch_user_video_list`

- 用途：获取指定用户发布的所有视频内容（瀑布流展示）
- 返回：视频列表数据，包含视频标题、封面、播放量等信息；包含 next_cursor 和 has_more 字段用于翻页
- 注意：与收藏夹接口的区别：本接口获取用户发布的视频，收藏夹接口获取用户收藏的视频
- Query：
  - `uid` (必填,string) 用户ID/User ID
  - `cursor` (选填,string) 分页游标/Pagination cursor
- 示例：

```
uid = "7277477906"
cursor = "0"
```

## 获取用户关注列表

`GET /api/v1/weibo/web_v2/fetch_user_following`

- 用途：获取指定用户的关注列表（该用户关注了谁）
- 返回：关注用户列表，包含用户名、头像、简介、粉丝数等
- 注意：关注列表受用户隐私设置影响；page参数从0开始，而不是1；与fetch_user_fans的区别：本接口获取用户关注了谁，fetch_user_fans获取谁关注了该用户
- Query：
  - `uid` (必填,string) 用户ID/User ID
  - `page` (选填,integer) 页码/Page number
- 示例：

```
uid = "1722594714"
page = 0
```

## 获取用户粉丝列表

`GET /api/v1/weibo/web_v2/fetch_user_fans`

- 用途：获取指定用户的粉丝列表（谁关注了该用户）
- 返回：粉丝用户列表，包含用户名、头像、简介、粉丝数等
- 注意：粉丝列表受用户隐私设置影响；page参数从0开始，而不是1；与fetch_user_following的区别：本接口获取谁关注了该用户，fetch_user_following获取用户关注了谁
- Query：
  - `uid` (必填,string) 用户ID/User ID
  - `page` (选填,integer) 页码/Page number
- 示例：

```
uid = "1722594714"
page = 0
```

## 获取所有分组信息

`GET /api/v1/weibo/web_v2/fetch_all_groups`

- 用途：获取微博平台的所有分组信息，包括默认分组和用户自定义分组
- 返回：分组列表，包含分组ID、名称、容器ID等
- 注意：返回的gid和containerid可用于时间轴接口的参数；分组信息变化不频繁，建议缓存
- 示例：

```
# No parameters needed
```

## 获取微博主页推荐时间轴

`GET /api/v1/weibo/web_v2/fetch_user_recommend_timeline`

- 用途：获取微博主页的推荐时间轴内容，基于用户兴趣展示个性化推荐
- 返回：推荐微博列表，包含微博内容、作者信息、互动数据等；包含 max_id 字段用于翻页
- 注意：建议先调用fetch_all_groups获取可用分组
- Query：
  - `refresh` (选填,integer) 刷新类型，0=正常刷新，1=强制刷新/Refresh type, 0=normal refresh, 1=force refresh
  - `group_id` (选填,string) 分组ID/Group ID
  - `containerid` (选填,string) 容器ID/Container ID
  - `extparam` (选填,string) 扩展参数/Extended parameters
  - `max_id` (选填,string) 最大ID/Max ID
  - `count` (选填,integer) 获取数量/Count
- 示例：

```
refresh = 0
group_id = "102803"
containerid = "102803"
max_id = "0"
count = 10
```

## 获取微博热门榜单时间轴

`GET /api/v1/weibo/web_v2/fetch_hot_ranking_timeline`

- 用途：获取微博平台各种类型的热门榜单内容
- 返回：热门微博列表，包含微博内容、作者信息、互动数据等
- 注意：不同榜单更新频率不同：小时榜实时性最强，周榜影响力较大
- Query：
  - `ranking_type` (必填,string) 榜单类型：hour=小时榜，yesterday=昨日榜，day_before=前日榜，week=周榜，male=男榜，female=女榜/Ranking type: hour=hourly, yesterday=yesterday, day_before=day before, week=weekly, male=male ranking, female=female ranking
  - `since_id` (选填,string) 分页标识，默认为0/Pagination identifier, default is 0
  - `max_id` (选填,string) 最大ID，默认为0/Max ID, default is 0
  - `count` (选填,integer) 获取数量，默认10/Count, default is 10
- 示例：

```
ranking_type = "hour"
max_id = "0"
count = 10
```

## 获取微博热搜词条(10条)

`GET /api/v1/weibo/web_v2/fetch_hot_search_index`

- 用途：快速获取微博热搜前10条
- 返回：热搜词条列表，包含关键词、热度值、排名等
- 注意：只返回前10条热搜；热搜更新频繁，建议缓存2-5分钟；如需完整热搜，使用fetch_hot_search_summary
- 示例：

```
# No parameters needed
```

## 获取微博完整热搜榜单(50条)

`GET /api/v1/weibo/web_v2/fetch_hot_search_summary`

- 用途：获取微博完整热搜榜单（50条）
- 返回：完整热搜列表，包含排名、关键词、标签（热点/沸点/官宣/新）、热度值
- 注意：与fetch_hot_search_index的区别：本接口返回50条，fetch_hot_search_index返回10条；rank为0表示置顶内容；建议缓存5-10分钟
- 示例：

```
# No parameters needed
```
- 返回结构（实测）：
  - `data` 是对象（2 个字段）：`total`, `data`
  - `data.data` 是数组（长度 51）；首元素字段：`rank`, `is_top`, `keyword`, `keyword_url`, `tag`, `heat`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 获取微博热搜榜单

`GET /api/v1/weibo/web_v2/fetch_hot_search`

- 用途：获取微博实时热搜榜单数据
- 返回：热搜数据，包含realtime（实时热搜）、hotgov等多个板块
- 注意：热搜更新频繁，建议缓存2-5分钟
- 示例：

```
# No parameters needed
```

## 获取微博文娱榜单

`GET /api/v1/weibo/web_v2/fetch_entertainment_ranking`

- 用途：获取微博文娱榜单数据（娱乐圈、影视、综艺等）
- 返回：文娱话题列表，包含话题、热度值、排名、分类等
- 注意：建议缓存5-10分钟
- 示例：

```
# No parameters needed
```

## 获取微博生活榜单

`GET /api/v1/weibo/web_v2/fetch_life_ranking`

- 用途：获取微博生活榜单数据（美食、旅游、健康、时尚等）
- 返回：生活话题列表，包含话题、热度值、排名、分类等
- 注意：建议缓存5-10分钟
- 示例：

```
# No parameters needed
```

## 获取微博社会榜单

`GET /api/v1/weibo/web_v2/fetch_social_ranking`

- 用途：获取微博社会榜单数据（时事新闻、社会热点、民生话题等）
- 返回：社会话题列表，包含话题、热度值、排名、分类等
- 注意：社会热点变化较快，建议缓存2-5分钟
- 示例：

```
# No parameters needed
```

## 获取微博相似搜索词推荐

`GET /api/v1/weibo/web_v2/fetch_similar_search`

- 用途：根据关键词获取微博推荐的相似搜索词
- 返回：相似搜索词列表，包含推荐词、搜索次数等
- 注意：相似词推荐相对稳定，可缓存15-30分钟
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
- 示例：

```
keyword = "#微博奇遇记#"
```

## 微博智能搜索

`GET /api/v1/weibo/web_v2/fetch_ai_search`

- 用途：通过微博AI智能搜索获取搜索结果
- 返回：AI搜索结果，包含推荐内容、相关话题等
- 注意：AI搜索结果会根据用户行为进行个性化调整
- Query：
  - `query` (必填,string) 搜索关键词/Search keyword
- 示例：

```
query = "#法国#"
```

## 微博AI搜索内容扩展

`GET /api/v1/weibo/web_v2/fetch_ai_related_search`

- 用途：获取与关键词相关的内容扩展（相关问题、博主推荐、参考博文等）
- 返回：HTML格式的扩展内容，包含相关问题、博主推荐、参考博文等
- 注意：返回内容为HTML格式，需要进行HTML解析处理；HTML结构可能会发生变化，需要做好容错处理
- Query：
  - `keyword` (必填,string) 搜索关键词/Search keyword
- 示例：

```
keyword = "#微博奇遇记#"
```

## 微博高级搜索

`GET /api/v1/weibo/web_v2/fetch_advanced_search`

- 用途：微博高级搜索，支持多维度筛选
- 返回：搜索结果列表，包含微博内容、作者信息、图片、视频、互动数据等
- 注意：视频播放需设置请求头 Referer=https://weibo.com/
- Query：
  - `q` (必填,string) 搜索关键词/Search keyword
  - `search_type` (选填) 搜索类型/Search type: all(全部), hot(热门), original(原创), verified(认证用户), media(媒体), viewpoint(观点)
  - `include_type` (选填) 包含类型/Include type: all(全部), pic(含图片), video(含视频), music(含音乐), link(含短链)
  - `timescope` (选填) 时间范围/Time scope (custom:start:end)
  - `page` (选填,integer) 页码/Page number
- 示例：

```
q = "python"
search_type = "hot"
include_type = "pic"
page = 1
```

## 地区省市映射

`GET /api/v1/weibo/web_v2/fetch_city_list`

- 用途：获取地区省市映射数据，用于用户搜索等接口的地区筛选参数
- 返回：省市映射数据，用于fetch_user_search等接口的region参数
- 注意：返回的编码格式为 custom:省代码:市代码，如 custom:11:1
- Query：
  - `normalized` (选填,boolean) 是否返回标准化结构（省份列表+城市数组）/Whether to return normalized structure
- 示例：

```
normalized = True
```

## 实时搜索

`GET /api/v1/weibo/web_v2/fetch_realtime_search`

- 用途：获取微博实时搜索结果（按时间排序的最新微博）
- 返回：实时搜索结果列表，包含微博内容、作者信息、图片、视频、互动数据等
- 注意：视频播放需设置请求头 Referer=https://weibo.com/；返回结构与高级搜索一致
- Query：
  - `query` (必填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页码/Page number
- 示例：

```
query = "苹果发布会"
page = 1
```

## 用户搜索

`GET /api/v1/weibo/web_v2/fetch_user_search`

- 用途：搜索微博用户，支持多种筛选条件
- 返回：用户列表，包含uid、昵称、头像、粉丝数、主页链接
- 注意：筛选参数过多可能导致无结果
- Query：
  - `query` (选填) 搜索关键词/Query（提供则视为“全部”搜索；留空则仅应用高级筛选参数）
  - `page` (选填,integer) 页码/Page
  - `region` (选填) 地区编码，从 /city_list 获取/Region code from /city_list
  - `auth` (选填) 认证类型 org_vip(机构)/per_vip(个人)/ord(普通)/Auth type
  - `gender` (选填) 性别 man / women / Gender
  - `age` (选填) 年龄段 18y/22y/29y/39y/40y / Age bucket
  - `nickname` (选填) 昵称筛选/Nickname filter
  - `tag` (选填) 标签筛选/Tag filter
  - `school` (选填) 学校筛选/School filter
  - `work` (选填) 公司筛选/Company filter
- 示例：

```
query = "yu7"
page = 1
```

## 视频搜索（热门/全部）

`GET /api/v1/weibo/web_v2/fetch_video_search`

- 用途：搜索微博视频内容，支持热门和全部模式
- 返回：视频列表，包含微博ID、作者、内容、视频链接、互动数据
- 注意：播放视频需设置Referer=https://weibo.com/
- Query：
  - `query` (必填,string) 搜索关键词/Search keyword
  - `mode` (选填,string) 搜索模式：hot=热门 / all=全部
  - `page` (选填,integer) 页码/Page number
- 示例：

```
query = "yu7"
mode = "hot"
page = 1
```

## 图片搜索

`GET /api/v1/weibo/web_v2/fetch_pic_search`

- 用途：搜索微博图片内容，按微博ID聚合多图
- 返回：图片列表，包含微博ID、缩略图、原图链接、作者信息、图片数量
- 注意：缩略图会自动转换为原图链接
- Query：
  - `query` (必填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页码/Page number
- 示例：

```
query = "yu7"
page = 1
```

## 话题搜索

`GET /api/v1/weibo/web_v2/fetch_topic_search`

- 用途：搜索微博话题，获取话题名称、封面、讨论量、阅读量
- 返回：话题列表，包含话题名、封面图、讨论数、阅读数
- 注意：数量单位（万/亿）已转换为整数
- Query：
  - `query` (必填,string) 搜索关键词/Search keyword
  - `page` (选填,integer) 页码/Page number
- 示例：

```
query = "yu7"
page = 1
```
