### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 作品详情/下载地址（App） | `GET kuaishou/app/fetch_one_video` | `photo_id` |
| 分享链接解析 | `GET kuaishou/app/fetch_one_video_by_url` | `share_text` |
| 作品评论 | `GET kuaishou/app/fetch_video_comment` | `photo_id`, `pcursor` |
| 视频搜索 | `GET kuaishou/app/search_video_v2` | `keyword`, `pcursor` |

- 作品主键是 `photo_id`（短字符串），用户标识是 `user_id`；列表统一用 `pcursor`，返回空串即到底。
- Web 端 `fetch_one_video` 只接受分享链接，传 `photo_id` 要走 App 端。
