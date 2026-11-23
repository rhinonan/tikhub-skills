# Hybrid Parsing

文件夹 `Hybrid-Parsing` · 1 个接口
说明：混合解析单个视频接口


## 混合解析单一视频接口

`GET /api/v1/hybrid/video_data`

- 用途：该接口用于解析抖音/TikTok单一视频的数据
- 返回：`data`: 视频数据
- Query：
  - `url` (必填,string)
  - `minimal` (选填,boolean) 是否返回最小数据/Whether to return minimal data
  - `base64_url` (选填,boolean) 是否Base64编码提交URL/Base64 encoding URL
- 返回结构（实测）：
  - `data` 是对象（191 个字段）：`xigua_task`, `packed_clips`, `component_control`, `can_be_oc_cover`, `anchors`, `chapter_list`, `boost_status`, `image_album_music_info`, `author_mask_tag`, `is_ads`, `is_karaoke`, `relation_labels`
  - `data.xigua_task` 是对象（1 个字段）：`is_xigua_task`
  - `data.component_control` 是对象（0 个字段）：
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23
