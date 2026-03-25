# Douyin Web Workflows

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

## 已验证 DOM / 状态特征

### 登录页
- 出现“扫码登录”与二维码区域
- 失效时可点“二维码失效 / 点击刷新”

### 发布图文页
- 存在 `input[type=file]`
- 存在“发布图文”“上传图文”按钮
- 标题输入框 placeholder：`添加作品标题`

### 评论管理页
- 评论 textarea placeholder：`有爱评论，说点儿好听的～`
- 发送按钮 class：`cmt-btn-sI9Zg2`
- 未激活：`semi-button semi-button-disabled cmt-btn-sI9Zg2`
- 激活后：`semi-button semi-button-primary cmt-btn-sI9Zg2`

## 可补充的能力方向

### 热榜 / 趋势
- 可接抖音热榜抓取
- 字段可包含：标题、热度、链接、封面、标签、类型

### 视频发布
- 可在现有图文发布链路基础上扩成视频上传与发布
- 建议继续复用 OpenClaw 浏览器/CDP，不另起独立 cookie 体系

### 私信管理
- 建议走更接近真人输入的 type + submit 思路
- 避免靠 JS 直接篡改聊天输入 DOM

### 账号分析
- 可从主页作品列表抓链接，再做文案提取、总结、竞品分析

### 下载
- 有需求，但当前优先自己做透明实现，不直接引高风险外部 downloader

## 关键陷阱

1. 评论输入框不是普通 DOM 输入框
   - 直接 `textarea.value = '...'` 不足以激活按钮
   - 受控组件会把无效赋值抹掉

2. 普通 input/change 事件可能不够
   - 即使事件触发，若没命中组件内部 state，也不会使按钮可用

3. 判断成功不能只看点击完成
   - 必须看页面是否真实出现评论记录 / 作品记录

## 已验证成功样例

### 评论管理成功评论
- `第十次测试：hook dispatch`

### 图文发布成功样例
- 标题：`一个主人和一个 AI 的真实协作日常`
- 发布时间：2026-03-24 16:21
