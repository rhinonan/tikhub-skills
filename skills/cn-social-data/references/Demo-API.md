# Demo API

文件夹 `Demo-API` · 6 个接口
说明：TikHub API示例项目


## 查看Demo缓存状态

`GET /api/v1/demo/demo/cache_status`

- 用途：查看当前缓存的Demo数据；了解缓存过期时间

## 【Demo】抖音Web获取固定作品数据（1小时缓存）

`GET /api/v1/demo/douyin/web/fetch_one_video`

- 用途：用于测试API连接和数据格式；了解返回数据结构；开发阶段的功能验证
- 返回：固定作品的缓存数据
- 示例：

```
```
# 无需参数，始终返回固定作品数据
# No parameters needed, always returns fixed video data
GET /api/v1/douyin/web/fetch_one_video
```
```
- 返回结构（实测）：
  - `data` 是对象（3 个字段）：`aweme_detail`, `log_pb`, `status_code`
  - `data.aweme_detail` 是对象（155 个字段）：`activity_video_type`, `anchors`, `authentication_token`, `author`, `author_mask_tag`, `author_user_id`, `aweme_control`, `aweme_id`
  - `data.log_pb` 是对象（1 个字段）：`impr_id`
  - 响应消息：请求成功，本次请求将被计费。
  - 实测时间：2026-11-23

## 【Demo】抖音APP获取固定作品数据（1小时缓存）

`GET /api/v1/demo/douyin/app/fetch_one_video`

- 用途：用于测试API连接和数据格式；了解返回数据结构；开发阶段的功能验证
- 返回：固定作品的缓存数据
- 示例：

```
```
# 无需参数，始终返回固定作品数据
# No parameters needed, always returns fixed video data
GET /api/v1/douyin/app/fetch_one_video
```
```

## 【Demo】抖音搜索综合搜索（1小时缓存）

`GET /api/v1/demo/douyin_search/app/general_search`

- 示例：

```
```
# 无需参数，始终返回固定关键词搜索结果
# No parameters needed, always returns fixed keyword search results
GET /api/v1/douyin_search/app/general_search
```
```

## 【Demo】快手获取固定视频信息（1小时缓存）

`GET /api/v1/demo/kuaishou/web/fetch_one_video`

- 示例：

```
```
# 无需参数，始终返回固定视频数据
# No parameters needed, always returns fixed video data
GET /api/v1/kuaishou/web/fetch_one_video
```
```

## 【Demo】微信公众号文章提取（1小时缓存）

`GET /api/v1/demo/wechat/article_extract`

- 用途：用于测试API连接和数据格式；了解返回数据结构；开发阶段的功能验证
- 返回：固定文章的缓存数据
- 示例：

```
```
# 无需参数，始终返回固定文章数据
# No parameters needed, always returns fixed article data
GET /api/v1/wechat/article_extract
```
```
