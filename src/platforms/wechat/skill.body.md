### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 视频号账号信息 | `POST wechat_channels/v2/fetch_channel_info` | body `username` |
| 视频号作品详情 | `POST wechat_channels/v2/fetch_video_detail` | body `object_id` 或 `share_url` |
| 导出公众号文章正文 | `POST wechat_mp/v2/fetch_article_detail_h5` | body `url` |
| 搜一搜 | `POST wechat_search/v2/fetch_search` | body `keyword`, `business_type` |

- 微信接口几乎全部是 **POST + JSON body**，参数用 `-b` 传，不要用 `-q`。
- 视频号账号是 `v2_...@finder` 长串，公众号是 `gh_` 开头；文章优先用 H5 版本接口。
