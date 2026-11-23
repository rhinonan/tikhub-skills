### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 笔记详情 | `GET xiaohongshu/web_v3/fetch_note_detail` | `note_id`, `xsec_token` |
| 用户笔记列表 | `GET xiaohongshu/app_v2/get_user_posted_notes` | `user_id` 或 `share_text` |
| 笔记评论 | `GET xiaohongshu/app_v2/get_note_comments` | `note_id`, `cursor` |
| 搜索笔记 | `GET xiaohongshu/app_v2/search_notes` | `keyword`, `page` |

- Web V3 详情必须同时给 `note_id` 和 `xsec_token`，token 失效时改走 App V2 详情接口。
- 蒲公英（PGY）接口全部是 POST + JSON body，和常规 query 风格不同。
