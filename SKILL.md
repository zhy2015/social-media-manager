---
name: social-media-manager
description: Unified social media operations manager. Use when a task spans content planning, posting, commenting, engagement, platform routing, or operating workflows across one or more social platforms such as 小红书、抖音、B站、微博、Twitter/X and similar channels. Prefer this as the top-level orchestration skill for social operations, then route into platform-specific sub-skills contained in this repository.
---

# Social Media Manager

本仓库已升级为“社交媒体运营聚合仓”，而不只是单一 `social-media-manager` 文件。

## 使用方式

优先把本仓库视为一个两层结构：

1. 总入口：`skills/social-media-manager/`
2. 平台子 skill：
   - `skills/social-media-xiaohongshu/`
   - `skills/social-media-douyin/`
   - `skills/social-media-bilibili/`

## 何时命中本 skill

当任务涉及以下任一情况时，优先命中本总入口：
- 多个平台联动
- 平台未明确，需要先判断路由
- 任务属于内容发布、评论、互动、调研、账号运营、数据汇总中的任一类
- 需要统一运营目标后再拆分到平台执行

## 默认路由

| 场景 | 默认路由 |
|---|---|
| 小红书运营、浏览、评论、发帖、互动 | `skills/social-media-xiaohongshu/` |
| 抖音运营、登录、发帖、浏览、评论管理、互动 | `skills/social-media-douyin/` |
| B站运营、投稿、私信、字幕/弹幕、热点/关键词分析 | `skills/social-media-bilibili/` |
| 涉及多个平台的统一运营任务 | `skills/social-media-manager/` 先做总编排 |

## 仓库说明

- `skill.md`：仓库级入口说明，便于整体引入
- `skills/social-media-manager/`：总入口 skill
- `skills/social-media-xiaohongshu/`：小红书子 skill
- `skills/social-media-douyin/`：抖音子 skill
- `skills/social-media-bilibili/`：B站子 skill

设计原则：
- 总入口保持薄，只负责路由与边界
- 平台流程下沉到各自子 skill
- 优先沉淀真实跑通的运营链路
