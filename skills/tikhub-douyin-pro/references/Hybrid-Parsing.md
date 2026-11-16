# Hybrid Parsing（多平台混合解析）

文件夹 `Hybrid-Parsing` · 1 个接口 · BASE `https://api.tikhub.io`

## 混合解析单一视频接口

`GET /api/v1/hybrid/video_data`

- 用途：该接口用于解析抖音/TikTok单一视频的数据。
- 返回：`data`: 视频数据。
- Query：
  - `url` (必填,string)
  - `minimal` (boolean,默认 False) 是否返回最小数据/Whether to return minimal data
  - `base64_url` (boolean,默认 False) 是否Base64编码提交URL/Base64 encoding URL
