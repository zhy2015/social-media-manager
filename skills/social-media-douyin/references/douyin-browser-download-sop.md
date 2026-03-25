# Douyin Browser Download SOP

## 目标

不依赖 `yt-dlp` 对 Douyin 的兼容性，直接复用已登录浏览器上下文，从作品页拿真实视频资源地址，再下载成本地 mp4。

## 适用场景

当以下任一情况出现时，优先走本 SOP：
- `yt-dlp` 提示需要 fresh cookies
- 普通 cookies.txt 复用失败
- 已经能在浏览器里正常打开目标作品页
- 需要更贴近真实网页播放链路的下载方式

## 核心思路

1. 用浏览器打开作品详情页
2. 等页面视频元素完成挂载
3. 读取：
   - `video.currentSrc`
   - `video src/source src`
   - 页面里已暴露的 play URL
4. 选一个真实可访问的 mp4 地址
5. 本地直接下载
6. `ffprobe` 校验时长

## 当前已验证样例

作品：
- `https://www.douyin.com/video/7610761269943922609`

已成功在浏览器中取到真实媒体地址，并用本地脚本下载：
- 输出：`output/douyin-download/7610761269943922609.mp4`
- 时长：`18413` ms

## 浏览器提取要点

优先读取：
- `document.querySelector('video')?.currentSrc`
- `document.querySelector('video')?.src`
- `Array.from(document.querySelectorAll('video source')).map(s => s.src)`

如果页面已正常播放，`currentSrc` 往往就是最直接可用的地址。

## 下载脚本

- `scripts/download_douyin_from_browser_url.py`

用法：

```bash
python3 skills/social-media-douyin/scripts/download_douyin_from_browser_url.py '<media_url>' '<aweme_id>'
```

指定输出路径：

```bash
python3 skills/social-media-douyin/scripts/download_douyin_from_browser_url.py '<media_url>' '<aweme_id>' '/tmp/test.mp4'
```

## 为什么这条更稳

- 不再依赖下载器对 Douyin 反爬策略的适配
- 直接复用浏览器已拿到的真实播放地址
- 和现有 OpenClaw 浏览器工作流天然一致

## 边界

- 媒体 URL 可能带时效参数，适合即时下载，不适合长期缓存成固定链接
- 页面未完成加载时，`currentSrc` 可能为空，需要等视频元素就绪
- 若视频页切换实现，仍需重新确认提取字段，但整体思路不变：
  - **在浏览器态里拿真实播放地址，而不是让外部下载器自己猜**
