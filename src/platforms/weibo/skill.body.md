### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 用户信息 | `GET weibo/web_v2/fetch_user_info` | `uid` |
| 导出微博正文 | `GET weibo/web_v2/fetch_post_detail` | `id` |
| 用户微博时间线 | `GET weibo/web_v2/fetch_user_posts` | `uid`, `page`, `since_id` |
| 微博评论 | `GET weibo/web_v2/fetch_post_comments` | `id`, `count`, `max_id` |
| 完整热搜榜 | `GET weibo/web_v2/fetch_hot_search_summary` | — |

- 用户 ID 是数字 `uid`，微博正文主键叫 `id`；时间线翻页用 `page` + `since_id`，评论用 `max_id` 游标。
- Web V2 与 App 两套通道返回结构不同，Web 失败时用 App 接口兜底。
