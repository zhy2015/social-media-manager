# Douyin Download SOP

## 目标

把抖音分享链接稳定落地成可复用的本地 mp4 文件，并在需要时继续发送到飞书。

## 推荐入口

脚本：
- `scripts/download_douyin_video.py`

默认输出目录：
- `output/douyin-download/`

## 输入

支持以下常见输入：
- 分享链接
- `https://www.douyin.com/video/<id>`
- 带 `modal_id` 的作品页 URL
- 其他可解析出 `aweme_id / group_id / modal_id` 的抖音链接

## 标准流程

1. 从输入里提取作品 id
2. 以作品 id 作为文件名输出到 `output/douyin-download/`
3. 调用 `yt-dlp` 下载视频
4. 如平台要求，附带新鲜 cookies
5. 用 `ffprobe` 读取时长
6. 输出结构化 JSON，供后续发送 / 分析复用

## 命令

```bash
python3 skills/social-media-douyin/scripts/download_douyin_video.py '<douyin_url>'
```

指定输出路径：

```bash
python3 skills/social-media-douyin/scripts/download_douyin_video.py '<douyin_url>' '/tmp/test.mp4'
```

## 成功输出示例

```json
{
  "ok": true,
  "source": "https://www.douyin.com/video/7610761269943922609",
  "aweme_id": "7610761269943922609",
  "output_path": "/Users/hidream/.openclaw/workspace/output/douyin-download/7610761269943922609.mp4",
  "size_bytes": 12345678,
  "duration_ms": 18413
}
```

## 失败处理

### 场景 1：未安装 `yt-dlp`

当前脚本会直接返回：
- `ok: false`
- `error: yt-dlp not found; install it first`

处理方式：
- 先安装 `yt-dlp`
- 再重跑脚本

### 场景 2：链接可解析但下载失败

脚本会返回：
- 作品 id
- 目标输出路径
- 失败命令
- stderr / stdout 中的错误信息

先看是不是：
- 链接失效
- 风控 / 区域限制
- 页面结构变化
- `yt-dlp` 版本过旧
- 缺少新鲜 cookies

当前实测结论：
- Douyin 公开页面下载经常要求 fresh cookies
- 即使能解析出作品 id，没有可用 cookies 也可能被拒绝

### 场景 3：下载完成但文件未落地

脚本会报：
- `download finished but output file not found`

优先检查：
- `yt-dlp` 模板输出是否被改写
- 目标目录权限
- 文件是否被写成别的扩展名

## 当前已验证样例

本轮已有真实样例文件：
- `output/douyin-download/7610761269943922609.mp4`

后续若再打通更多样例，优先把“输入链接 → 实际输出文件”补到这里。

## Cookies 复用

当前实测说明：
- 仅把 `document.cookie` 导出成 Netscape cookies 文件，仍可能不够
- Douyin 的 fresh cookies 校验不一定只依赖普通 cookie 文本
- 即使页面里已登录，`yt-dlp --cookies cookies.txt` 也可能仍被拒绝

因此当前推荐分两层：

### 层 1：轻量复用
- 从活动浏览器会话导出 cookie 文本
- 写成 Netscape cookies 文件
- 用 `yt-dlp --cookies <file>` 尝试下载

适用：
- 低成本试探
- 站点风控要求不高时

### 层 2：真实浏览器态导出 / 直接浏览器内取数
若层 1 失败，优先考虑：
- 从真实浏览器 profile / cookie store 导出更完整 cookies
- 或改成直接在浏览器上下文中抓真实媒体 URL，再下载

当前对 Douyin 的结论：
- 已验证层 1 不稳定，不能当成最终闭环方案
- 后续更稳的方向是“浏览器态直取媒体地址”或“更完整 cookie 导出”

## 发回飞书的后续链路

下载成功后，如需发回当前飞书对话：

1. 用 `ffprobe` 读时长
2. 走 `skills/feishu-media-delivery/scripts/send-media.mjs`
3. 以 `msg_type=media` 发送 mp4

注意：
- mp4 不走普通 file
- 成功判据是 Feishu 返回 `code: 0` 且用户真实收到视频

## 维护原则

- 保持下载链路透明、可审查
- 优先自维护轻脚本，不引黑盒 downloader
- 每次真实跑通新的链接类型，再补充到本 SOP
