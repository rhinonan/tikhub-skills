### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 视频详情 | `GET bilibili/web/fetch_one_video` | `bv_id` |
| 下载视频/播放流地址 | `GET bilibili/web/fetch_video_playurl` | `bv_id`, `cid` |
| 视频评论 | `GET bilibili/web/fetch_video_comments` | `bv_id`, `pn` |
| UP 主投稿 | `GET bilibili/web/fetch_user_post_videos` | `uid`, `pn`, `ps` |

- 视频主键是 `bv_id`，只有 `aid` 时先用 `bv_to_aid` 互转；播放流还要 `cid`（视频详情里取）。
- 列表分页用 `pn` + `ps`；大会员清晰度单独调 `fetch_vip_video_playurl`。
