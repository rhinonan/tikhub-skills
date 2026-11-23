### 场景速查

| 需求 | 接口 | 关键参数 |
|---|---|---|
| 验证链路（免费） | `GET demo/douyin/web/fetch_one_video` | — |
| 抖音演示搜索 | `GET demo/douyin_search/app/general_search` | — |
| 混合解析视频链接 | `GET hybrid/video_data` | `url` |

- Demo 接口返回固定数据并缓存 1 小时，不扣额度，适合在配置 token 前验证 CLI。
- `hybrid/video_data` 支持多个平台的分享链接；传 `minimal=true` 只返回核心字段。
