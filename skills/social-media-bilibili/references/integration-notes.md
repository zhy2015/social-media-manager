# Bilibili Integration Notes

## 本次收口来源

已下载样本：
- bilibili-all-in-one
- bilibili-skill
- bilibili-video-publish
- bilibili-messager
- bilibili-analytics
- bilibili-transcript

## 取舍结论

### 保留为主要参考骨架
- `bilibili-all-in-one`
  - 原因：能力面最全，结构相对完整，适合当 B站能力地图参考

### 局部吸收
- `bilibili-messager`
  - 吸收：消息页最小快照、会话定位、发送后回查思路
- `bilibili-analytics`
  - 吸收：关键词搜索抓取与统计报告框架
- `bilibili-transcript`
  - 吸收：字幕优先、转录兜底、输出结构化文本的流程设计

### 不直接继承
- `bilibili-video-publish`
  - 原因：偏人工 SOP，文案质量低，不适合作为长期主规范
- `bilibili-skill`
  - 原因：实现契约混杂，引用了不适合直接复用的外部路径假设

## 风险记录

### 凭据风险
多个外部 skill 依赖：
- SESSDATA
- bili_jct
- buvid3

处理原则：
- 凭据默认视为高风险
- 不把 cookie 明文写入 skill 文档
- 若后续要固化凭据方案，应单独沉淀到受控位置，不放进公开工作流说明

### 浏览器自动化风险
- 私信 / 投稿链路都依赖前端页面结构
- 页面 DOM 或交互改版后，旧选择器/注入方式可能失效
- 真实成功判据必须是页面结果回查，不认“按钮点击成功”

### 下载/批量风险
- 高质量下载可能受登录态与限频影响
- 批量下载、批量抓取需加节流

## 后续建议

1. 补一版 `social-media-manager` 对 B站的路由说明
2. 后续如真实跑通 B站投稿/私信，再把页面级细节下沉到：
   - `references/bilibili-publish-workflow.md`
   - `references/bilibili-messaging-workflow.md`
3. 若确定长期需要下载/分析，可补本地脚本到 `scripts/`
4. 若要进一步收口外部样本，可将低价值样本转移到归档区而非长期暴露
