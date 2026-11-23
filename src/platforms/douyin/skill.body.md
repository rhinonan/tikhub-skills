### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 作品详情 | `GET douyin/web/fetch_one_video` | `aweme_id` |
| 下载无水印视频 | `GET douyin/web/fetch_video_high_quality_play_url` | `aweme_id` 或 `share_url` |
| 分享链接解析 | `GET douyin/web/fetch_one_video_by_share_url` | `share_url` |
| 用户主页作品 | `GET douyin/web/fetch_user_post_videos` | `sec_user_id`, `max_cursor` |
| 热榜 | `GET douyin/web/fetch_hot_search_result` | — |

- 用户 ID 有 `uid` / `short_id` / `sec_uid` / `sec_user_id` 四种，接口要求各不相同；列表翻页常见 `cursor` 或毫秒时间戳 `max_cursor`。
- 网页端 `play_count` 常为 0，用 `douyin/app/v3` 兜底；同类通道按 `web` → `app/v3` → `v2` 降级。
