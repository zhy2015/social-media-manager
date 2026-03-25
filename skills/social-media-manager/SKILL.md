---
name: social-media-manager
description: Unified social media operations manager. Use when a task spans content planning, posting, commenting, engagement, platform routing, or operating workflows across one or more social platforms such as 小红书、微博、B站、Twitter/X and similar channels. Prefer this as the top-level orchestration skill for social operations, then route into platform-specific sub-skills.
---

# Social Media Manager

这是社交媒体运营总管理 skill。

## 作用

统一处理以下类型任务：
- 平台选择与路由
- 账号运营动作编排
- 内容发布 / 评论 / 互动 / 调研
- 多平台运营策略拆分
- 将通用运营目标下沉到具体平台 skill

## 路由原则

| 场景 | 默认路由 |
|---|---|
| 小红书运营、浏览、评论、发帖、互动 | `skills/social-media-xiaohongshu/` |
| 抖音运营、登录、发帖、浏览、评论管理、互动 | `skills/social-media-douyin/` |
| B站运营、投稿、私信、字幕/弹幕、热点/关键词分析 | `skills/social-media-bilibili/` |
| 其他平台运营 | 后续补对应子 skill |
| 涉及多个平台的统一运营任务 | 由本 skill 做总编排 |

## 总体设计

推荐按两层管理：
1. **总管理层**：`social-media-manager`
2. **平台子 skill 层**：例如 `social-media-xiaohongshu`

本 skill 负责：
- 判断目标平台
- 判断是“调研 / 发布 / 评论 / 回复 / 账号管理 / 数据汇总”哪类动作
- 将任务下发给具体平台 skill

## 当前已接入子 skill

- `social-media-xiaohongshu`
- `social-media-douyin`
- `social-media-bilibili`

## 治理规则

- 社交平台操作优先保留“流程说明 + 风险边界 + 最佳路径”，避免把所有脚本细节堆在总 skill 里。
- 平台专属登录、选择器、评论链路、发帖链路，写入平台子 skill。
- 若某平台已经实战打通，应把“真实可用流程”沉淀在对应子 skill 中，便于刷新后续用。
