### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 问题下的回答 | `GET zhihu/web/fetch_question_answers` | `question_id`, `cursor` |
| 回答详情/导出正文 | `GET zhihu/web/fetch_answer_detail` | `answer_id` |
| 用户回答列表 | `GET zhihu/web/fetch_user_answers` | `user_url_token`, `offset` |
| 首页热榜 | `GET zhihu/web/fetch_hot_list` | `limit` |

- 用户标识是 `user_url_token`（URL 里的英文串），不是数字 ID 或昵称。
- 知乎基本只有 Web 通道，没有 App 兜底；ID 类型（问题/回答/专栏/想法）不能混用。
