---
domain: xiaohongshu.com
aliases: [小红书, Xiaohongshu, 图文发布]
updated: 2026-03-24
---

# 小红书图文发布工作流索引

## 适用范围

当目标是把一组本地图片 + 标题 + 正文，稳定发布到小红书图文笔记时，优先走这条索引。

## 推荐总链路

1. 漫画/图片 prompts 准备
2. `comic-gen/scripts/generate_and_stage_xhs_images.py`
   - 生图或复用已有图
   - 下载到 `comic-gen/generated/`
   - 复制到 `/tmp/openclaw/uploads/comic-gen/`
   - 产出 manifest
3. `comic-gen/scripts/prepare_xiaohongshu_publish_payload.py`
   - 合并 manifest + 标题 + 正文
   - 产出统一 publish payload
4. 复用当前 OpenClaw 已登录浏览器/CDP
   - 打开发布页
   - 切到“上传图文”
   - 上传 payload.images
   - 填标题 payload.title
   - 填正文 payload.body
   - 点击发布
   - 以“发布成功”作为完成判据

## 输入/输出约定

### A. 生图与 staging
输入：prompts JSON
输出：
- 工作区图片：`comic-gen/generated/*.jpg`
- 上传目录图片：`/tmp/openclaw/uploads/comic-gen/*.jpg`
- manifest：`*-manifest.json`

### B. 发布 payload
输入：manifest + post metadata JSON
输出：`*-publish-payload.json`

payload 关键字段：
- `title`
- `body`
- `images[]`
- `steps[]`

## 已验证脚本

### 1) 生成并搬运图片
```bash
python3 comic-gen/scripts/generate_and_stage_xhs_images.py \
  --prompts comic-gen/post3-prompts.json \
  --direct
```

关键经验：
- HiDream 图链不能只读 `artifacts[].url`
- 必须兼容 `artifacts[].raw.image`
- 本地代理不稳时，优先加 `--direct`

### 2) 生成发布 payload
```bash
python3 comic-gen/scripts/prepare_xiaohongshu_publish_payload.py \
  --manifest comic-gen/post3-prompts-manifest.json \
  --post comic-gen/post-template.json \
  --out comic-gen/post3-publish-payload.json
```

## 浏览器操作判据

### 进入发布态的判据
- 页面出现标题输入框 `input[placeholder*=填写标题]`
- 页面出现正文 `contenteditable` 区域
- 页面底部出现“发布”按钮

### 成功判据
- 页面出现“发布成功”提示
- 不要只看按钮状态变化

## 已知陷阱

### 1. 默认回到视频上传
进入发布页后，默认有时落在“上传视频”，必须主动切到“上传图文”。

### 2. 文件上传后未进入编辑态
上传后有时仍停留在入口态，可再点击一次“上传图片”按钮推进。

### 3. 不要远程 URL 直传
必须先把图片下载到本地，再从 `/tmp/openclaw/uploads/` 上传。

### 4. 不要新开 Playwright 抢同一 profile
若当前浏览器已由 OpenClaw 管理并占用 profile，再起新的持久化浏览器实例会撞 `ProcessSingleton`。正确做法是继续复用当前 OpenClaw 浏览器/CDP 会话。

## 推荐操作策略

- 默认半自动：脚本准备素材与 payload，浏览器层执行上传与发布
- 发布前可人工快速看一眼标题、正文、封面顺序
- 若目标是“发出去”，只停在脚本产物阶段不算完成
