---
name: social-media-douyin
description: Platform-specific Douyin operations skill. Use for 抖音登录、发布图文/视频、浏览作品、评论管理、下载作品、互动链路验证、以及将已跑通的网页端运营流程沉淀为可复用规范。
---

# Social Media - Douyin

这是抖音平台专属 skill。

目标：
- 沉淀已经真实跑通的抖音网页端流程
- 让后续任务优先复用稳定链路，而不是每次重新试错
- 将“登录 / 发布 / 浏览 / 评论 / 下载 / 回查”拆成可单独调用的能力块

## 默认原则

- 优先走真实浏览器页面路径，不猜接口。
- 优先复用现有登录态，不重复折腾登录。
- 成功判据必须是页面真实状态变化，不只看按钮点没点到。
- 对受控前端组件，先判断是不是 React 受控输入，再决定用真人输入还是命中内部状态链。
- 用户要的是“完成动作”，不是“解释为什么页面难搞”。

## 当前能力总览

### 已真实打通
- 创作者中心登录
- 图文发布
- 主站个人页浏览作品
- 创作者中心评论管理发送评论
- 分享链接下载视频到本地
- 下载后发送到当前飞书对话

### 待补但方向明确
- 视频发布
- 热榜 / 趋势抓取
- 私信管理
- 账号内容分析 / 文案提取
- 发布后自动回查与数据汇总

## 已验证页面

- 创作者中心上传页：
  - `https://creator.douyin.com/creator-micro/content/upload`
- 图文编辑页：
  - `https://creator.douyin.com/creator-micro/content/post/image?...`
- 作品管理页：
  - `https://creator.douyin.com/creator-micro/content/manage?enter_from=publish`
- 评论管理页：
  - `https://creator.douyin.com/creator-micro/data/following/comment`
- 主站个人页：
  - `https://www.douyin.com/user/self`

如需更多页面细节，读：
- `references/douyin-web-workflows.md`
- `references/douyin-download-sop.md`
- `references/douyin-browser-download-sop.md`

如需执行下载脚本，使用：
- `scripts/download_douyin_video.py`
- `scripts/download_douyin_from_browser_url.py`

---

## Workflow 1：创作者中心登录

目标：进入创作者中心并完成登录。

### 推荐路径
1. 打开创作者中心上传页
2. 若未登录，识别扫码登录区域
3. 若二维码过期，点击“二维码失效 / 点击刷新”
4. 等用户用抖音 App 扫码
5. 页面进入创作者中心后台后再继续后续动作

### 成功判据
- 页面出现账号昵称、创作入口、内容管理等后台元素
- 不靠 cookie 猜测是否登录成功

### 关键经验
- 创作者中心上传页本身就可作为登录入口
- 二维码会失效，刷新重来是正常路径
- 登录这一步允许短暂停顿等用户扫码，不要因为等待就误判失败

---

## Workflow 2：图文发布

目标：在抖音网页端完成一次真实图文发布。

### 前提
- 已登录创作者中心
- 本地已有待发布图片
- 优先把待发布素材放在：`/tmp/openclaw/uploads/`

### 推荐路径
1. 进入创作者中心首页
2. 点击“发布图文”
3. 定位 `input[type=file]`
4. 注入本地图片文件，可多图
5. 如页面未自动推进，补点一次“上传图文”
6. 进入编辑页后填写标题
7. 填写正文
8. 确认图片预览正常
9. 点击“发布”
10. 回查是否跳到“作品管理”或出现新作品记录

### 页面关键特征
- 文件输入：`input[type=file]`
- 标题输入框：`input[placeholder="添加作品标题"]`
- 正文区通常不是普通 textarea，而是富文本 / 受控编辑容器

### 成功判据
- 点击发布后跳到“作品管理”页，或可见新作品记录
- 不能只看“发布”按钮被点击

### 已验证样例
- 4 图图文
- 标题：`一个主人和一个 AI 的真实协作日常`
- 已实战发布时间：2026-03-24 16:21

### 素材策略
当用户说“继续推进，不要回头要素材”时，优先从这些地方找：
- `comic-workflow` 已生成图片
- `hidream-api-gen` 已生成图片
- `/tmp/openclaw/uploads/` 现成图片

原则：对发布任务来说，先拿到可上传的本地文件，再谈 prompt。

---

## Workflow 3：浏览个人主页与作品回查

目标：进入自己的抖音主页，查看已发布作品，用于发布后回查或手动核验。

### 推荐路径
1. 打开 `https://www.douyin.com/user/self`
2. 确认个人主页已加载当前账号
3. 在“作品”标签中查看作品列表
4. 点击作品卡片进入详情 modal / 播放层

### 成功判据
- 页面展示当前账号个人页
- 可看到作品卡片
- 点击后 URL 或界面出现作品详情层（常带 `modal_id=...`）

### 适用场景
- 发布后回查
- 找作品详情入口
- 找评论 / 互动入口
- 抽作品链接给后续分析或下载流程用

---

## Workflow 4：评论管理发送评论

目标：在创作者中心“评论管理”中对指定作品发送评论。

### 推荐路径
1. 进入创作者中心
2. 打开“互动管理” → “评论管理”
3. 确认当前选中的作品
4. 找到评论输入框与发送按钮
5. 让发送按钮从 disabled 变为可点击
6. 点击“发送”
7. 回查评论列表是否出现新评论

### 页面关键特征
- 页面 URL：
  - `https://creator.douyin.com/creator-micro/data/following/comment`
- textarea placeholder：
  - `有爱评论，说点儿好听的～`
- 发送按钮 class：
  - 未激活：`semi-button semi-button-disabled cmt-btn-sI9Zg2`
  - 激活后：`semi-button semi-button-primary cmt-btn-sI9Zg2`

### 关键陷阱
- 这不是普通 textarea。
- 它是受控 React 组件。
- 直接 `textarea.value = 'xxx'`、普通 input/change、prototype setter、valueTracker 往往不够。

### 本轮已验证有效的做法
- 找到 textarea 对应 React fiber
- 对其上层 function component 的 hook state 做 dispatch
- 成功让发送按钮从 disabled → primary
- 再点击发送

### 成功判据
评论列表出现这些真实信号：
- 当前账号名
- 时间是“刚刚”
- 评论正文已出现
- 可见“回复 / 删除”等操作项

### 已验证样例
- `第十次测试：hook dispatch`

### 风险边界
- 该链路依赖前端实现细节
- 若抖音页面升级，fiber / hook 路径可能变化
- 所以不要把经验记成“给 textarea 赋值”，而要记成：
  - **本质是命中受控组件内部状态更新**

---

## Workflow 5：分享链接下载视频到本地

目标：把抖音分享链接对应的视频下载到本地，供归档、转发、转写、二次分析使用。

### 当前已验证结果
- 已成功下载一个作品到：
  - `output/douyin-download/7610761269943922609.mp4`

### 推荐产物落点
- 下载目录：`output/douyin-download/`
- 文件名优先使用作品 id / aweme_id，便于复用和去重

### 已收敛脚本入口
- `python3 skills/social-media-douyin/scripts/download_douyin_video.py '<douyin_url>'`
- `python3 skills/social-media-douyin/scripts/download_douyin_from_browser_url.py '<media_url>' '<aweme_id>'`

### 建议流程
优先顺序：
1. 用户给分享链接
2. 先尝试通用下载脚本 `download_douyin_video.py`
3. 若遇到 fresh cookies / 兼容性问题，立刻切换到浏览器态方案：
   - 在作品页读取 `video.currentSrc` / `source src`
   - 用 `download_douyin_from_browser_url.py` 直接下载
4. 验证文件存在且可播放
5. 如需转发到飞书，再走 Feishu media 发送链路

### 成功判据
- 本地产出 mp4 文件
- 文件大小正常，ffprobe 可读时长更好
- 可以被后续发送 / 分析流程复用

### 安全与实现原则
- 优先使用透明、可审查、自维护的下载流程
- 通用下载脚本当前底层使用 `yt-dlp`
- Douyin 某些链接实测需要 fresh cookies，不能假设裸链必下
- 当前已验证：仅导出 `document.cookie` 再喂给 `yt-dlp` 仍可能失败
- 当前更稳的已验证方案是：**浏览器内直取媒体 URL → 本地下载**
- 不直接依赖来源不清晰的高风险 downloader
- 若后续扩展下载能力，优先自己维护脚本与说明

---

## Workflow 6：下载后发送到飞书对话

目标：把本地下载好的抖音 mp4 发到当前飞书对话。

### 推荐路径
1. 确认本地 mp4 文件存在
2. 用 `ffprobe` 读取时长，换算为毫秒
3. 进入 `skills/feishu-media-delivery/scripts/`
4. 用 `send-media.mjs` 上传 mp4，拿到 `file_key`
5. 再以 `msg_type=media` 发到目标 open_id

### 已验证实战参数
- 接收方：当前 Feishu 用户 open_id
- 文件：`/Users/hidream/.openclaw/workspace/output/douyin-download/7610761269943922609.mp4`
- 时长：`18413` ms

### 关键注意
- mp4 走 `media`，不要按普通 file 发
- 脚本依赖 `FEISHU_APP_ID`
- 若环境未注入，可从本地 OpenClaw 配置读取后显式传入

### 成功判据
- Feishu 返回 `code: 0`
- `msg: success`
- 用户在当前对话真实收到视频

---

## 推荐任务拆分方式

面对抖音任务，优先先判断属于哪一类：

- 登录 / 复用登录态
- 发图文
- 发视频
- 浏览 / 回查作品
- 评论 / 回复
- 下载
- 数据调研 / 内容分析

若用户说的是模糊目标，比如：
- “把这个发到抖音”
- “看看这个号最近发了啥”
- “把这个视频下下来发我”

先把任务路由到上面某个 workflow，再执行。

---

## 后续待补能力

### 热榜 / 趋势监控
可补字段：
- 标题
- 热度值
- 标签
- 链接
- 封面
- 类型

适合和 feed-monitor / 选题工作流联动。

### 视频发布
建议沿用现有创作者中心浏览器会话。
不要另起独立 cookie 体系。

当前新增验证：
- 在 `https://creator.douyin.com/creator-micro/content/upload` 上传 mp4 后，页面会进入视频编辑态
- 可见标题输入框：`填写作品标题，为作品获得更多流量`
- 可见“发布”“暂存离开”“预览视频”等元素
- 已真实跑通：**本地 mp4 → 视频编辑页 → 本地横/竖封面上传 → 发布 → 作品管理页按标题回查命中**

#### 已验证稳定路径（推荐）
1. 上传本地 mp4，进入视频编辑页
2. 填写标题
3. **不要卡死在 `Ai智能推荐封面生成中...`**
4. 直接用 `ffmpeg` 从本地视频抽帧，生成两张封面：
   - 竖封面：3:4 / 适配竖版展示
   - 横封面：4:3 / 适配横版展示
5. 在封面编辑弹窗中：
   - 先上传竖封面
   - 再点“设置横封面”上传横封面
   - 点“完成”
6. 回到编辑页后，确认页面提示变为：
   - `封面检测通过`
   - `暂未发现封面低质问题`
7. 点击“发布”
8. 成功判据只认：
   - 跳到 `作品管理` 页
   - 且按标题搜索 / 页面文本回查能命中新作品

#### 当前已验证的 ffmpeg 封面方案
以本地视频 `/tmp/openclaw/uploads/douyin-hidream-test.mp4` 为例：

- 竖封面：
  - `ffmpeg -y -ss 00:00:03 -i /tmp/openclaw/uploads/douyin-hidream-test.mp4 -vframes 1 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" /tmp/openclaw/uploads/douyin-covers/cover-vertical.jpg`
- 横封面：
  - `ffmpeg -y -ss 00:00:03 -i /tmp/openclaw/uploads/douyin-hidream-test.mp4 -vframes 1 -vf "scale=1440:1080:force_original_aspect_ratio=increase,crop=1440:1080" /tmp/openclaw/uploads/douyin-covers/cover-horizontal.jpg`

推荐先把待上传视频放进：
- `/tmp/openclaw/uploads/`

推荐把生成封面放进：
- `/tmp/openclaw/uploads/douyin-covers/`

#### 当前已验证样例
- 标题：`低功耗 AI 信息节点｜HiDream 生成视频测试`
- 回查方式：作品管理页搜索标题关键字 `低功耗 AI 信息节点`
- 结果：页面文本可命中新作品标题

#### 关键陷阱
- **不要把“页面跳回 upload”误判成发布成功**
- **不要把“发布按钮点下去”误判成发布成功**
- `douyin_creator_pc_cover_required_intercept` 表示封面必填拦截，没补齐横/竖封面就不会真正放行
- `Ai智能推荐封面` 不稳定，可能长时间停在“生成中”，此时应直接切换到本地封面上传方案
- 只有“作品管理 / 主页真实回查到新作品”才算完成

### 热榜 / 趋势抓取
当前轻量可行路径：
1. 打开 `https://www.douyin.com/discover` 或 `https://www.douyin.com/jingxuan`
2. 从页面卡片抓取可见标题文本
3. 产出轻量趋势列表（rank/title）
4. 如后续拿到更稳定热榜页或接口，再补热度值、标签、链接

当前新增脚本：
- `scripts/douyin_trending_probe.py`

适用边界：
- 先做“看当前推荐流里有什么在高频出现”的轻量趋势探针
- 还不是官方热榜精确榜单

### 私信管理
建议优先走更接近真人输入的 `type + submit`。
不要优先用 JS 直接改聊天输入 DOM。

当前新增验证：
- 主站顶栏存在“私信”入口
- 页面会预加载 PC IM 相关资源
- 说明主站登录态下可继续往私信页方向深挖，不必另造登录链路

### 账号内容分析 / 文案提取
适合拆成四段：
1. 主页抓取
2. 作品链接列表
3. 文案 / 转写提取
4. 清洗总结

当前轻量可行路径：
- 从 `discover/jingxuan`、`user/self` 或目标用户主页抓作品卡片标题
- 先抽标题/话题/重复主题
- 后续再补详情页文案、评论、互动数据采集

---

## 执行检查清单

执行任一抖音动作前，先快速检查：

- 是否已有可复用登录态
- 是否已有本地素材 / 本地视频文件
- 当前任务属于哪个 workflow
- 成功判据是什么
- 是否需要回查页面真实状态
- 是否需要把结果继续发送到飞书

## 维护规则

当新的抖音链路被真实跑通后：
- 优先补到本 skill，而不是只留在聊天记录里
- 只记录真实打通过的流程、关键选择器、关键陷阱、成功判据
- 把“脚本细节”与“流程规范”分开；流程进 `SKILL.md`，大段技术细节进 `references/`
