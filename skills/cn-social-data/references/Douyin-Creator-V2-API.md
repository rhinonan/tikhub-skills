# Douyin Creator V2 API

文件夹 `Douyin-Creator-V2-API` · 14 个接口
说明：抖音创作者V2数据接口（需要用户Cookie，可获取作品流量总览等数据）


## 获取作品总览数据

`POST /api/v1/douyin/creator_v2/fetch_item_overview_data`

- 用途：获取抖音作品总览数据，包括流量指标、审核状态、播放信息等；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- 返回：作品总览数据，根据 fields 参数返回对应的字段内容
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `ids` (必填,string) 作品ID列表,多个ID用逗号分隔/Item IDs, separated by comma
  - `fields` (选填) 需要返回的字段,多个字段用逗号分隔/Fields to return, separated by comma. 可选值: metrics(指标),review(审核),play_info(播放信息),dou_plus(抖+),integrated_incentive(综合激励),incentive_life(激励生命周期),content_analysis(内容分析)
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "ids": "7559536212910853422",
    "fields": "metrics,review,play_info,dou_plus,integrated_incentive,incentive_life,content_analysis"
}
```

### 字段组合示例/Field Combination Examples:
- 只获取流量指标: "metrics"
- 获取流量和审核: "metrics,review"
- 获取所有字段: "metrics,review,play_info,dou_plus,integrated_incentive,incentive_life,content_analysis"
```

## 获取作品流量来源统计

`POST /api/v1/douyin/creator_v2/fetch_item_play_source`

- 用途：获取抖音作品的流量来源统计数据；流量来源统计了作品从不同途径播放的占比；**若暂时没有看到某个渠道，说明对应渠道暂时没有播放**；**作品刚发布推荐页流量占比可能偏低，请等待系统推流**；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "item_id": "7559536212910853422"
}
```

### 返回数据示例/Response Example:
```json
{
    "play_source": [
        {
            "app_id": 1128,
            "history_difference": 0.8543689320388349,
            "key": "homepage_hot",
            "value": 0.8543689320388349
        },
        {
            "app_id": 1128,
            "history_difference": 0.05825242718446602,
            "key": "familiar",
            "value": 0.05825242718446602
        },
        {
            "app_id": 1128,
            "history_difference": 0.04854368932038835,
            "key": "search",
            "value": 0.04854368932038835
        }
    ],
    "status_code": 0,
    "status_msg": ""
}
```

### 数据解读/Data Interpretation:
- value 值表示该渠道的流量占比，例如 0.85 表示 85% 的流量来自该渠道
- homepage_hot 占比高说明作品获得了较好的系统推荐
- familiar 占比高说明作品在关注用户中传播较好
- search 占比高说明作品搜索热度高
```

## 获取作品搜索关键词统计

`POST /api/v1/douyin/creator_v2/fetch_item_search_keyword`

- 用途：获取抖音作品的搜索关键词统计数据；了解用户通过哪些搜索关键词找到并观看了该作品；帮助创作者优化内容标题、标签和描述，提升搜索曝光；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "item_id": "7559536212910853422"
}
```

### 返回数据示例/Response Example:
```json
{
    "keywords": [
        {
            "keyword": "搞笑视频",
            "count": 1250,
            "percentage": 35.5
        },
        {
            "keyword": "热门音乐",
            "count": 850,
            "percentage": 24.2
        },
        {
            "keyword": "舞蹈教学",
            "count": 620,
            "percentage": 17.6
        }
    ],
    "total_count": 3520,
    "status_code": 0,
    "status_msg": ""
}
```

### 数据解读/Data Interpretation:
- 关键词列表按搜索次数降序排列
- percentage 值越高，说明该关键词越受用户关注
- 可以根据高频关键词优化作品的标题、描述和标签
- 发现意外的热门关键词可能揭示新的内容方向
- **空列表**: 说明作品暂无搜索数据，作品主要通过其他渠道传播

### 应用建议/Application Suggestions:
1. **标题优化**: 在标题中自然融入高频关键词
2. **标签策略**: 使用搜索量高的关键词作为标签
3. **内容调整**: 创作更多用户搜索的相关内容
4. **竞品分析**: 对比不同作品的关键词差异
```

## 获取作品观看趋势分析

`POST /api/v1/douyin/creator_v2/fetch_item_watch_trend`

- 用途：获取抖音作品的观看趋势分析数据；了解用户在观看作品时的行为模式；帮助创作者优化视频内容结构和节奏；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID
  - `analysis_type` (选填,integer) 分析类型/Analysis type: 1=留存分析(Retention), 2=点赞分析(Like), 7=跳出分析(Bounce)
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "item_id": "7559536212910853422",
    "analysis_type": 1
}
```

### 返回数据示例/Response Example:
```json
{
    "analysis_trend": {
        "current_item": [
            {
                "key": "00:00",
                "value": 0.2653
            },
            {
                "key": "00:01",
                "value": 0.2653
            },
            {
                "key": "00:05",
                "value": 0.0272
            },
            {
                "key": "00:10",
                "value": 0.1429
            }
        ],
        "similar_author": [
            {
                "key": "00:00",
                "value": 0.1594
            },
            {
                "key": "00:01",
                "value": 0.2229
            }
        ]
    },
    "status_code": 0,
    "status_msg": ""
}
```

### 数据解读/Data Interpretation:
**留存分析 (Retention)**:
- value 值表示该时间点的留存比例
- 数值越高表示越多观众看到这个时间点
- 对比 current_item 和 similar_author 可以看出作品表现
- 留存曲线下降陡峭说明内容吸引力不足

**点赞分析 (Like)**:
- value 值表示该时间点的点赞比例
- 数值越高表示该时间段内容越能引发点赞
- 点赞高峰通常出现在高潮、反转、笑点等位置
- 可以帮助识别最有价值的内容片段

**跳出分析 (Bounce)**:
- value 值表示该时间点的跳出比例
- 数值越高表示越多观众在此时离开
- 跳出率高的时间点需要重点优化
- 开头几秒的跳出率尤其重要

### 优化建议/Optimization Suggestions:
1. **前3秒黄金法则**: 确保开头吸引眼球，降低初期跳出
2. **节奏把控**: 在留存率下降前插入高潮或转折
3. **时长优化**: 根据留存曲线调整视频时长
4. **点赞热点**: 在点赞率高的时间段前后放置核心内容
5. **对标学习**: 参考 similar_author 数据优化内容
6. **持续测试**: 不同类型内容的最佳节奏不同

### 注意事项/Notes:
- 播放量超过 200 后，留存分析数据更准确
- 数据可能有延迟，建议作品发布一段时间后查看
- 结合其他指标（完播率、互动率）综合分析
```

## 获取作品弹幕分析

`POST /api/v1/douyin/creator_v2/fetch_item_danmaku_analysis`

- 用途：获取抖音作品的弹幕分析数据；了解观众在视频各个时间点的弹幕互动情况；帮助创作者识别视频中的热点片段和观众反应；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "item_id": "7559536212910853422"
}
```

### 返回数据示例/Response Example:
```json
{
    "bullet_distribution": [
        {
            "time_point": 5,
            "count": 328,
            "percentage": 15.2
        },
        {
            "time_point": 12,
            "count": 562,
            "percentage": 26.1
        },
        {
            "time_point": 18,
            "count": 445,
            "percentage": 20.6
        }
    ],
    "hot_words": [
        {
            "word": "哈哈哈",
            "count": 156,
            "sentiment": "positive"
        },
        {
            "word": "精彩",
            "count": 98,
            "sentiment": "positive"
        },
        {
            "word": "学到了",
            "count": 76,
            "sentiment": "positive"
        }
    ],
    "total_count": 2156,
    "peak_time": 12,
    "status_code": 0,
    "status_msg": ""
}
```

### 数据解读/Data Interpretation:
- **弹幕分布 (Bullet Distribution)**:
  - time_point 显示哪个时间点弹幕最密集
  - count 越高表示该片段越引起观众共鸣
  - percentage 帮助识别弹幕集中度
  - 多个弹幕高峰说明视频有多个精彩片段

- **热门词汇 (Hot Words)**:
  - 高频正面词汇（如"精彩"、"学到了"）说明内容质量好
  - 负面词汇可能揭示内容问题点
  - 疑问词汇（如"为什么"）可能是用户困惑点

- **总弹幕数 (Total Count)**:
  - 弹幕数量反映视频互动热度
  - 相对播放量的弹幕率可以衡量内容吸引力
  - 持续增长说明内容有长尾效应

### 优化建议/Optimization Suggestions:
1. **强化高峰**: 在弹幕高峰时间点前后强化内容质量
2. **延长精彩**: 延长弹幕密集片段的时长，满足观众期待
3. **回应反馈**: 根据热门词汇调整内容方向
4. **引导互动**: 在弹幕较少的时间点添加引导性内容
5. **情感共鸣**: 多设计能引发正面情感的片段
6. **问题解答**: 针对疑问类弹幕在后续视频中解答

### 注意事项/Notes:
- 弹幕数据可能有延迟，建议作品发布一段时间后查看
- 弹幕分析需要一定的样本量才准确，新作品可能数据不足
- 结合其他指标（互动率、完播率）综合分析效果更好
- 不同类型内容的弹幕特点不同，需要针对性分析
```

## 获取作品观众数据分析

`POST /api/v1/douyin/creator_v2/fetch_item_audience_portrait`

- 用途：获取抖音作品的观众数据分析；了解观看作品的用户画像特征；包含活跃分布、性别分布、地域分布、年龄分布等多维度数据；帮助创作者精准定位目标受众，优化内容策略；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "item_id": "7559536212910853422"
}
```

### 返回数据示例/Response Example:
```json
{
    "active": [
        {
            "key": "2",
            "value": 0.0949367088607595
        },
        {
            "key": "3",
            "value": 0.15822784810126583
        },
        {
            "key": "4",
            "value": 0.6962025316455697
        },
        {
            "key": "-1",
            "value": 0.05063291139240506
        }
    ],
    "gender": {
        "ratio_list": [
            {
                "key": "male",
                "value": 0.7612903225806451
            },
            {
                "key": "female",
                "value": 0.23870967741935484
            }
        ],
        "tgi_list": [
            {
                "key": "male",
                "value": 135.47066238136884
            },
            {
                "key": "female",
                "value": 54.49489346627035
            }
        ]
    },
    "province": {
        "ratio_list": [
            {
                "key": "浙江",
                "value": 0.24050632911392406
            },
            {
                "key": "江苏",
                "value": 0.12025316455696203
            },
            {
                "key": "广东",
                "value": 0.0759493670886076
            },
            {
                "key": "湖北",
                "value": 0.06329113924050633
            }
        ],
        "tgi_list": [
            {
                "key": "浙江",
                "value": 379.3041755346526
            },
            {
                "key": "江苏",
                "value": 169.70798949761055
            },
            {
                "key": "广东",
                "value": 70.0324843724158
            },
            {
                "key": "湖北",
                "value": 164.36825973059874
            }
        ]
    },
    "age": {
        "ratio_list": [
            {
                "key": "18-23",
                "value": 0.3548387096774194
            },
            {
                "key": "-18",
                "value": 0.1935483870967742
            },
            {
                "key": "31-40",
                "value": 0.14838709677419354
            },
            {
                "key": "50-",
                "value": 0.11612903225806452
            },
            {
                "key": "41-50",
                "value": 0.10967741935483871
            },
            {
                "key": "24-30",
                "value": 0.07741935483870968
            }
        ],
        "tgi_list": [
            {
                "key": "-18",
                "value": 563.217280988937
            },
            {
                "key": "18-23",
                "value": 191.33476395324902
            },
            {
                "key": "50-",
                "value": 80.07137972518639
            },
            {
                "key": "41-50",
                "value": 73.75840394976595
            },
            {
                "key": "31-40",
                "value": 49.79826524888418
            },
            {
                "key": "24-30",
                "value": 41.07687409864829
            }
        ]
    },
    "career": [],
    "city_level": {
        "ratio_list": [],
        "tgi_list": []
    },
    "new_user": [],
    "status_code": 0,
    "status_msg": ""
}
```

### 数据解读/Data Interpretation:
**活跃分布 (active)**:
- key="2": 上午时段（通常指6:00-12:00）
- key="3": 下午时段（通常指12:00-18:00）
- key="4": 晚上时段（通常指18:00-24:00）
- key="-1": 其他时段或未分类
- value值越高，说明该时段观众越多
- 示例中晚上时段（key="4"）占比69.6%，是主要观看时段

**性别分布 (gender)**:
- ratio_list显示实际性别占比
- tgi_list显示性别偏好度（TGI>100表示该性别用户偏好此内容）
- 示例中男性占比76.1%，TGI为135.5，说明男性用户是核心受众
- 女性TGI仅54.5，低于平均水平，可考虑优化以吸引女性用户

**地域分布 (province)**:
- ratio_list显示各省份用户占比
- tgi_list显示地域偏好度
- 示例中浙江占比24%，TGI高达379，说明浙江用户特别喜欢此类内容
- 江苏、湖北的TGI也较高（>160），是重点地域
- 可针对高TGI地域制作本地化内容

**年龄分布 (age)**:
- "-18": 18岁以下，TGI高达563，说明未成年用户特别喜欢
- "18-23": 18-23岁，占比35.5%，TGI为191，是主力受众
- "24-30": 24-30岁，TGI仅41，低于平均水平
- "31-40", "41-50", "50-": 中老年用户占比和TGI都较低
- 此作品明显偏向年轻化受众

**TGI指数应用**:
- TGI>150: 高度偏好，是核心目标群体
- TGI 100-150: 中度偏好，有潜力拓展
- TGI 50-100: 低度偏好，需要优化内容吸引
- TGI<50: 不匹配，可能不是目标受众

### 优化建议/Optimization Suggestions:
1. **时间优化**: 根据active数据，在高活跃时段发布（示例中晚上最佳）
2. **内容适配**: 根据高TGI年龄段调整内容风格（示例应偏向18-23岁年轻化）
3. **性别策略**: 针对高TGI性别深化内容，或优化以平衡性别受众
4. **地域营销**: 为高TGI地域（如浙江、江苏）创作本地化内容或方言版本
5. **受众拓展**: 关注TGI低的群体（如24-30岁），寻找增长机会
6. **精准定位**: 聚焦TGI>150的群体，他们是最有价值的核心受众
7. **内容调整**: 如果想拓展受众，需要调整内容以提升低TGI群体的兴趣
8. **A/B测试**: 针对不同TGI群体制作差异化内容，测试效果

### 注意事项/Notes:
- 观众数据需要一定播放量才准确，建议作品有1000+播放后查看
- 数据可能有延迟，通常在作品发布24-48小时后更新
- Index值用于与平台均值对比，帮助识别特色受众
- 结合作品内容特点和目标受众综合分析
- 不同内容类型的受众特征差异较大，需要针对性优化
```

## 获取作品观众其他数据分析

`POST /api/v1/douyin/creator_v2/fetch_item_audience_others`

- 用途：获取抖音作品的观众其他数据分析，包括受众分布和受众关注词；了解观众是否为粉丝，以及观众关注的兴趣话题；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `item_id` (必填,string) 作品ID/Item ID
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "item_id": "7559536212910853422"
}
```

### 返回数据示例/Response Example:
```json
{
    "audience_distribution": {
        "fan_list": [
            {
                "key": "1",
                "value": 0.156
            },
            {
                "key": "0",
                "value": 0.844
            }
        ]
    },
    "audience_keyword": {
        "keyword_list": [
            {
                "keyword": "美食",
                "value": 0.35
            },
            {
                "keyword": "旅游",
                "value": 0.28
            },
            {
                "keyword": "生活",
                "value": 0.22
            },
            {
                "keyword": "娱乐",
                "value": 0.15
            }
        ]
    },
    "status_code": 0,
    "status_msg": ""
}
```

### 数据解读/Data Interpretation:

**受众分布 (audience_distribution)**:
- key="1": 表示粉丝，value=0.156 表示15.6%的观众是已关注的粉丝
- key="0": 表示非粉丝，value=0.844 表示84.4%的观众是未关注的路人
- 粉丝占比高说明内容对现有粉丝吸引力强
- 非粉丝占比高说明作品破圈能力强，吸引了很多新观众

**受众关注词 (audience_keyword)**:
- keyword_list展示观众群体关注的其他话题
- 可以了解观众的兴趣偏好，用于内容规划
- 示例中观众主要关注"美食"(35%)、"旅游"(28%)等话题
- 可以结合这些关键词创作相关内容，提高吸引力

### 优化建议/Optimization Suggestions:
1. **粉丝维护**: 如果粉丝占比高(>30%)，说明内容符合粉丝预期，继续保持风格
2. **破圈拓展**: 如果非粉丝占比高(>80%)，说明内容有爆款潜力，可加大推广
3. **内容规划**: 根据audience_keyword规划相关主题内容，覆盖观众兴趣点
4. **跨界合作**: 结合高占比关键词，进行跨领域内容创作
5. **粉丝转化**: 对于非粉丝占比高的爆款作品，在评论区引导关注
6. **兴趣匹配**: 关注观众兴趣词与作品内容的匹配度，调整内容方向
7. **话题借势**: 利用观众关注的热门话题，制作相关内容蹭热度
8. **受众画像**: 结合关注词描绘完整的受众兴趣画像

### 注意事项/Notes:
- 观众数据需要一定播放量才准确，建议作品有1000+播放后查看
- 数据可能有延迟，通常在作品发布24-48小时后更新
- 粉丝占比与作品是否爆款无关，重点看内容质量和推广效果
- 受众关注词反映的是观众整体兴趣，不一定与当前作品主题相关
- 如果返回空列表，说明该作品目前暂无足够数据
- 结合其他数据（如观众画像）综合分析效果更好
```

## 获取作品垂类标签

`POST /api/v1/douyin/creator_v2/fetch_item_analysis_involved_vertical`

- 用途：获取指定时间段内投稿作品涉及的垂类标签；用于后续调用投稿分析接口时的参数；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYYMMDD)/Start date (format YYYYMMDD)
  - `end_date` (必填,string) 结束日期(格式YYYYMMDD)/End date (format YYYYMMDD)
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "start_date": "20250713",
    "end_date": "20251011"
}
```

### 返回数据示例/Response Example:
```json
{
    "primary_verticals": ["动物", "美食", "旅游"],
    "status_code": 0,
    "status_msg": ""
}
```

### 数据解读/Data Interpretation:
- primary_verticals列表包含该账号投稿作品涉及的所有垂类
- 如果返回空列表，说明该时间段内没有投稿或垂类未分类
- 获取到垂类后，可用于投稿分析接口的primary_verticals参数

### 注意事项/Notes:
- 日期格式必须为YYYYMMDD（8位数字）
- 时间跨度不能超过90天
- 建议先调用此接口获取垂类，再调用投稿分析接口
- 如果时间范围内无投稿，可能返回空列表
```

## 获取投稿分析概览

`POST /api/v1/douyin/creator_v2/fetch_item_analysis_overview`

- 用途：获取账号投稿作品的综合分析数据；包括不同体裁、垂类的投稿表现统计；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**；**建议先调用 fetch_item_analysis_involved_vertical 接口获取垂类标签**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYYMMDD)/Start date (format YYYYMMDD)
  - `end_date` (必填,string) 结束日期(格式YYYYMMDD)/End date (format YYYYMMDD)
  - `genres` (选填,array) 体裁类型列表/Genres list: 1=1min以内视频, 2=1-3min视频, 3=3-5min视频, 4=5min+视频, 5=图文, 8=长图文
  - `primary_verticals` (必填,array) 垂类标签列表/Primary verticals list (从involved_vertical接口获取)
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "start_date": "20250713",
    "end_date": "20251011",
    "genres": [1, 2, 3, 4, 5, 8],
    "primary_verticals": ["动物"]
}
```

### 体裁类型说明/Genre Type Description:
- **1**: 1分钟以内视频（短视频）
- **2**: 1-3分钟视频（中短视频）
- **3**: 3-5分钟视频（中视频）
- **4**: 5分钟以上视频（长视频）
- **5**: 图文（图片+文字）
- **8**: 长图文（多图片+长文字）

### 使用流程/Usage Flow:
1. 先调用 `fetch_item_analysis_involved_vertical` 获取垂类标签
2. 使用返回的 primary_verticals 作为参数
3. 调用本接口获取投稿分析数据
4. 分析不同体裁和垂类的表现

### 数据解读/Data Interpretation:
- 可以看到不同体裁内容的表现差异
- 了解哪种体裁更受欢迎
- 分析垂类内容的表现趋势
- 优化内容创作方向

### 优化建议/Optimization Suggestions:
1. **体裁优化**: 根据数据选择表现更好的体裁类型
2. **内容时长**: 分析观众偏好的视频时长
3. **垂类聚焦**: 专注于表现好的垂类领域
4. **内容多样化**: 尝试不同体裁和垂类的组合
5. **发布策略**: 根据不同体裁的表现调整发布频率

### 注意事项/Notes:
- 日期格式必须为YYYYMMDD（8位数字）
- 时间跨度不能超过90天
- primary_verticals参数必须从 fetch_item_analysis_involved_vertical 接口获取
- 如果时间范围内无投稿，可能返回空数据
- genres参数可以自由组合，按需筛选体裁
- 数据分析建议至少有7天以上的投稿数据
```

## 获取投稿表现数据

`POST /api/v1/douyin/creator_v2/fetch_item_analysis_item_performance`

- 用途：获取投稿作品的表现数据，包括播放量、点赞量、评论量、分享量等指标；分析不同体裁和垂类的内容表现；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**；**建议先调用 fetch_item_analysis_involved_vertical 接口获取垂类标签**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYYMMDD)/Start date (format YYYYMMDD)
  - `end_date` (必填,string) 结束日期(格式YYYYMMDD)/End date (format YYYYMMDD)
  - `genres` (选填,array) 体裁类型列表/Genres list: 1=1min以内视频, 2=1-3min视频, 3=3-5min视频, 4=5min+视频, 5=图文, 8=长图文
  - `primary_verticals` (必填,array) 垂类标签列表/Primary verticals list (从involved_vertical接口获取)
  - `metric_type` (选填,integer) 指标类型/Metric type: 1=播放量(Views), 2=点赞量(Likes), 3=评论量(Comments), 4=分享量(Shares)
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "start_date": "20250713",
    "end_date": "20251011",
    "genres": [2, 3, 4, 5, 8],
    "primary_verticals": ["动物"],
    "metric_type": 1
}
```

### 指标类型说明/Metric Type Description:
- **metric_type=1 (播放量/Views)**: 查看作品的播放量表现
- **metric_type=2 (点赞量/Likes)**: 查看作品的点赞量表现
- **metric_type=3 (评论量/Comments)**: 查看作品的评论量表现
- **metric_type=4 (分享量/Shares)**: 查看作品的分享量表现

### 体裁类型说明/Genre Type Description:
- **1**: 1分钟以内视频（短视频）- 快速吸引注意力
- **2**: 1-3分钟视频（中短视频）- 平衡内容与时长
- **3**: 3-5分钟视频（中视频）- 深度内容展示
- **4**: 5分钟以上视频（长视频）- 完整故事叙述
- **5**: 图文（图片+文字）- 静态内容展示
- **8**: 长图文（多图片+长文字）- 深度图文内容

### 使用流程/Usage Flow:
1. 先调用 `fetch_item_analysis_involved_vertical` 获取垂类标签
2. 使用返回的 primary_verticals 作为参数
3. 选择需要分析的指标类型 (metric_type)
4. 调用本接口获取投稿表现数据
5. 分析不同体裁和垂类的表现差异

### 数据解读/Data Interpretation:
- **播放量 (metric_type=1)**: 反映内容的曝光度和吸引力
- **点赞量 (metric_type=2)**: 反映内容的质量和受欢迎程度
- **评论量 (metric_type=3)**: 反映内容的互动性和话题性
- **分享量 (metric_type=4)**: 反映内容的传播力和价值

### 优化建议/Optimization Suggestions:
1. **播放量优化**:
   - 优化标题和封面，提高点击率
   - 选择合适的发布时间
   - 利用热门话题和标签

2. **点赞量优化**:
   - 提升内容质量，引发共鸣
   - 在视频中引导点赞
   - 创作有价值、有趣的内容

3. **评论量优化**:
   - 设置互动话题，引导评论
   - 在评论区积极回复
   - 创作有争议或讨论性的内容

4. **分享量优化**:
   - 创作有价值、实用的内容
   - 制作有趣、有共鸣的内容
   - 适当加入情感元素

5. **体裁选择**:
   - 根据不同指标表现选择合适的体裁
   - 短视频适合快速传播
   - 中长视频适合深度内容
   - 图文适合知识分享

6. **垂类聚焦**:
   - 专注于表现好的垂类
   - 分析垂类特点和受众偏好
   - 持续优化内容方向

### 注意事项/Notes:
- 日期格式必须为YYYYMMDD（8位数字）
- 时间跨度不能超过90天
- primary_verticals参数必须从 fetch_item_analysis_involved_vertical 接口获取
- 如果时间范围内无投稿，可能返回空数据
- genres参数可以自由组合，按需筛选体裁
- 不同metric_type展示不同维度的表现数据
- 建议结合多个指标综合分析内容表现
- 数据分析建议至少有7天以上的投稿数据
```

## 获取投稿作品列表

`POST /api/v1/douyin/creator_v2/fetch_item_list`

- 用途：获取指定时间范围内发布的所有投稿作品列表；支持分页查询，每次最多返回100条数据；数据更新说明：
- 返回：投稿作品列表数据，包含作品的详细指标信息；has_more: 是否还有更多数据；cursor: 下一页的游标，用于分页查询；items: 作品列表数组
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `count` (选填,integer) 每页数量/Count per page (最多100条)
  - `order_by` (选填,integer) 排序方式/Order by (1-26): 1=发布时间↓(新到旧), 2=发布时间↑(旧到新), 3=播放量↓, 4=播放量↑, 5=点赞量↓, 6=点赞量↑, 7=评论量↓, 8=评论量↑, 9=分享量↓, 10=分享量↑, 11=收藏量↓, 12=收藏量↑, 13=2s跳出率↓, 14=2s跳出率↑, 15=5s完播率↓, 16=5s完播率↑, 17=完播率↓, 18=完播率↑, 19=封面点击率↓, 20=封面点击率↑, 21=平均播放时长↓, 22=平均播放时长↑, 23=主页访问量↓, 24=主页访问量↑, 25=粉丝增量↓, 26=粉丝增量↑
  - `fields` (选填,string) 需要返回的字段/Fields to return
  - `need_cooperation` (选填,boolean) 是否需要合作信息/Need cooperation info
  - `start_time` (必填,integer) 开始时间戳(毫秒)/Start time timestamp (milliseconds)
  - `end_time` (必填,integer) 结束时间戳(毫秒)/End time timestamp (milliseconds)
  - `need_long_article` (选填,boolean) 是否包含长图文/Include long articles
  - `cursor` (选填) 分页游标/Pagination cursor (可选)
- 示例：

```
### 基础请求/Basic Request (默认按发布时间排序):
```json
{
    "cookie": "Your_Cookie_Here",
    "start_time": 1758988800000,
    "end_time": 1760198399000,
    "count": 10
}
```

### 按播放量排序/Sort by Views (找爆款视频):
```json
{
    "cookie": "Your_Cookie_Here",
    "start_time": 1758988800000,
    "end_time": 1760198399000,
    "count": 20,
    "order_by": 3
}
```

### 按完播率排序/Sort by Completion Rate (优质内容分析):
```json
{
    "cookie": "Your_Cookie_Here",
    "start_time": 1758988800000,
    "end_time": 1760198399000,
    "count": 20,
    "order_by": 17
}
```

### 按粉丝增量排序/Sort by Follower Growth (涨粉效果分析):
```json
{
    "cookie": "Your_Cookie_Here",
    "start_time": 1758988800000,
    "end_time": 1760198399000,
    "count": 20,
    "order_by": 25
}
```

### 分页请求/Pagination Request:
```json
{
    "cookie": "Your_Cookie_Here",
    "start_time": 1758988800000,
    "end_time": 1760198399000,
    "count": 10,
    "cursor": 1234567890
}
```

### 返回数据示例/Response Example:
```json
{
    "has_more": true,
    "cursor": 1234567890,
    "items": [
        {
            "item_id": "7559536212910853422",
            "metrics": {
                "play_count": 12345,
                "digg_count": 678,
                "comment_count": 90,
                "share_count": 45,
                "collect_count": 123
            },
            "review": {
                "status": 2
            },
            "visibility": {
                "is_public": true
            }
        }
    ]
}
```

### 注意事项/Notes:
1. **时间范围**: 建议不要设置过长的时间范围，可能导致请求超时
2. **分页查询**: 如果has_more=true，务必使用返回的cursor继续请求
3. **数据更新频率**:
   - 实时更新：播放量、点赞量、评论量、分享量、收藏量
   - 每小时更新：跳出率、完播率、封面点击率、平均播放时长、粉丝增量
   - 每天更新：主页访问量
4. **数据量限制**: 单次请求最多返回100条，如需更多请使用分页或导出接口
5. **体裁筛选**: 仅支持前100条作品的体裁筛选
6. **排序选择**: 根据分析目标选择合适的排序方式（共26种）
7. **Cookie有效性**: 如果返回错误，请检查Cookie是否过期
8. **排序说明**: ↓表示从高到低，↑表示从低到高
```

## 导出投稿作品列表

`POST /api/v1/douyin/creator_v2/fetch_item_list_download`

- 用途：导出指定时间范围内前1000条投稿作品的详细数据；支持按体裁类型筛选导出内容；**此接口用于批量导出数据，不适合实时查询**；**导出任务为异步处理，需要等待服务器生成文件**；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- 返回：**直接返回Excel文件流**，浏览器会自动下载；文件名：作品列表导出.xlsx；文件格式：Excel (.xlsx)；Content-Type: application/vnd.ms-excel
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `min_cursor` (必填,integer) 最小游标(开始时间戳,毫秒)/Min cursor (start timestamp in milliseconds)
  - `max_cursor` (必填,integer) 最大游标(结束时间戳,毫秒)/Max cursor (end timestamp in milliseconds)
  - `type_filters` (选填,array) 体裁类型过滤/Type filters: 1=1min以内视频, 2=1-3min视频, 3=3-5min视频, 4=5min+视频, 5=图文, 8=长图文
  - `need_long_article` (选填,boolean) 是否包含长图文/Include long articles
- 示例：

```
### 导出所有体裁/Export All Genres:
```json
{
    "cookie": "Your_Cookie_Here",
    "min_cursor": 1752336000000,
    "max_cursor": 1760198399000,
    "type_filters": [1, 2, 3, 4, 5, 8],
    "need_long_article": true
}
```

### 仅导出视频作品/Export Only Videos:
```json
{
    "cookie": "Your_Cookie_Here",
    "min_cursor": 1752336000000,
    "max_cursor": 1760198399000,
    "type_filters": [1, 2, 3, 4],
    "need_long_article": false
}
```

### 仅导出图文作品/Export Only Image Posts:
```json
{
    "cookie": "Your_Cookie_Here",
    "min_cursor": 1752336000000,
    "max_cursor": 1760198399000,
    "type_filters": [5, 8],
    "need_long_article": true
}
```

### 返回数据说明/Response Description:
- 此接口直接返回Excel文件流，不返回JSON数据
- 响应头包含 `Content-Disposition: attachment; filename="作品列表导出.xlsx"`
- 浏览器会自动识别并触发文件下载
- 文件内容为二进制流（application/vnd.ms-excel）

### 使用方式示例/Usage Examples:

**使用 cURL 下载:**
```bash
curl -X POST "https://your-api.com/api/v1/douyin_creator_v2/fetch_item_list_download"       -H "Authorization: Bearer YOUR_TOKEN"       -H "Content-Type: application/json"       -d '{
    "cookie": "Your_Cookie_Here",
    "min_cursor": 1752336000000,
    "max_cursor": 1760198399000,
    "type_filters": [1,2,3,4,5,8]
  }'       -o "作品列表导出.xlsx"
```

**使用 Python requests:**
```python
import requests

response = requests.post(
    "https://your-api.com/api/v1/douyin_creator_v2/fetch_item_list_download",
    headers={"Authorization": "Bearer YOUR_TOKEN"},
    json={
        "cookie": "Your_Cookie_Here",
        "min_cursor": 1752336000000,
        "max_cursor": 1760198399000,
        "type_filters": [1,2,3,4,5,8]
    }
)

# 保存文件
with open("作品列表导出.xlsx", "wb") as f:
    f.write(response.content)
```

**使用 JavaScript (Axios):**
```javascript
const axios = require('axios');
const fs = require('fs');

axios.post('https://your-api.com/api/v1/douyin_creator_v2/fetch_item_list_download', {
    cookie: 'Your_Cookie_Here',
    min_cursor: 1752336000000,
    max_cursor: 1760198399000,
    type_filters: [1,2,3,4,5,8]
}, {
    headers: { 'Authorization': 'Bearer YOUR_TOKEN' },
    responseType: 'arraybuffer'
}).then(response => {
    fs.writeFileSync('作品列表导出.xlsx', response.data);
});
```

### 注意事项/Notes:
1. **数据量限制**: 最多导出前1000条作品数据
2. **即时生成**: 接口会立即生成Excel文件并返回，无需等待
3. **时间范围**: 建议不要设置过长的时间范围，以免数据量过大导致超时
4. **体裁筛选**: 可以根据分析需求选择特定体裁类型
5. **文件格式**: Excel (.xlsx) 格式，兼容 Microsoft Excel、WPS、Google Sheets等
6. **响应类型**: 返回二进制流，不是JSON，请使用正确的响应处理方式
7. **Cookie有效性**: 如果返回错误，请检查Cookie是否过期
8. **超时设置**: 建议设置较长的超时时间（60秒以上），因为需要生成文件
9. **文件编码**: 文件名使用UTF-8编码，支持中文显示
```

## 获取直播场次历史记录

`POST /api/v1/douyin/creator_v2/fetch_live_room_history_list`

- 用途：获取抖音创作者的直播场次历史记录；查看指定时间范围内的所有直播场次数据；支持查询正在进行的直播和历史直播记录；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
  - `start_date` (必填,string) 开始日期(格式YYYY-MM-DD)/Start date (format YYYY-MM-DD)
  - `end_date` (必填,string) 结束日期(格式YYYY-MM-DD)/End date (format YYYY-MM-DD)
  - `limit` (选填,integer) 每页数量限制/Limit per page (最多400条)
  - `need_living` (选填,integer) 是否包含正在直播的场次/Include living rooms: 0=不包含, 1=包含
  - `download` (选填,integer) 是否下载/Download: 0=不下载, 1=下载
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here",
    "start_date": "2025-09-11",
    "end_date": "2025-10-11",
    "limit": 400,
    "need_living": 1,
    "download": 0
}
```

### 返回数据示例/Response Example:
```json
{
    "data": {
        "code": 0,
        "componentID": "",
        "data": {
            "series": [
                {
                    "clientCommentUcntTd": "0",
                    "coverUri": "https://p3-webcast-sign.douyinpic.com/...",
                    "endTime": "2025-11-20 13:52:20",
                    "liveConsumeUcnt": "1",
                    "liveDurationWithoutPause": "1分钟5秒",
                    "liveFansConsumeUcntTd": "1",
                    "liveNewFollowUcnt": "0",
                    "liveServerWatchDurationTdPavg": "0.5666666666666667",
                    "pcu": "1",
                    "playStatus": "4",
                    "roomID": "75746809889xxxxxx",
                    "roomLiveEarnScore": "1",
                    "roomTitle": "xxxxxxxx",
                    "serverLikeCntTd": "0",
                    "serverWatchUcntTdDirect": "1",
                    "startTime": "2025-11-20 13:51:15",
                    "watchCnt": "1"
                }
            ]
        },
        "meta": ""
    }
}
```

### 数据解读/Data Interpretation:
- **watchCnt**: 总观看人次，反映直播的曝光度和吸引力
- **pcu**: 峰值同时在线人数（Peak Concurrent Users），反映直播的热度峰值
- **liveServerWatchDurationTdPavg**: 平均观看时长，反映内容的吸引力
- **liveNewFollowUcnt**: 新增关注数，反映直播的转粉效果
- **roomLiveEarnScore**: 直播收益积分，反映直播的收益能力
- **liveConsumeUcnt/liveFansConsumeUcntTd**: 消费用户数/粉丝消费用户数，反映直播的转化能力
- **互动率**: (serverLikeCntTd+clientCommentUcntTd)/watchCnt，反映用户活跃度

### 优化建议/Optimization Suggestions:
1. **高峰分析**: 分析pcu最高出现的时间点，强化该时段的内容
2. **留存优化**: 提升liveServerWatchDurationTdPavg平均观看时长，增加内容的连贯性和吸引力
3. **互动引导**: 在直播中增加互动环节，提升serverLikeCntTd点赞数、clientCommentUcntTd评论数
4. **转粉策略**: 在直播中适时引导关注，提升liveNewFollowUcnt新增关注数
5. **消费转化**: 分析高roomLiveEarnScore场次的特点，优化直播策略
6. **时间选择**: 根据历史数据选择watchCnt观看人次最多的时段开播
```

## 获取创作者账号诊断

`POST /api/v1/douyin/creator_v2/fetch_author_diagnosis`

- 用途：获取抖音创作者账号的诊断数据和优化建议；自动分析最近一周（从当天起往前7天）的账号表现；提供完播率、互动指数等关键指标的评估和改进建议；帮助创作者了解账号健康度，优化内容策略；**此接口需要用户提供有效的抖音创作者平台Cookie**；**使用 POST 方法，Cookie 在请求体中传输，更安全**；**无需指定时间范围，系统自动获取最近7天数据**
- Body(JSON)：
  - `cookie` (必填,string) 用户Cookie/User Cookie
- 示例：

```
```json
{
    "cookie": "Your_Cookie_Here"
}
```
```
