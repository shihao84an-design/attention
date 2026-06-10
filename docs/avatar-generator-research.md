# 自拍 → 个性化风格头像系统：技术选型研究报告

> 研究日期：2026-06-10　｜　面向场景：**自托管(self-hosted)、我和朋友多人上传自拍、生成保留个人特质的特定风格头像**
> 方法：5 个角度并行联网调研，关键结论均经 ≥2 个独立来源交叉验证，存疑项在文末"可信度说明"中标注。

---

## 0. 给你的一句话结论

- 你的场景是**个人 + 朋友小圈子使用，不对外卖**，这一点非常关键：它让最棘手的法律问题（见下面的 InsightFace 许可证）**对你基本不构成限制**，可选的方案一下子宽了很多。
- **最快上线、零硬件门槛**：用 **Replicate 或 fal.ai** 的云端 API（它们直接托管了 InstantID / PuLID / PhotoMaker 这些"保人脸"模型），约 **¥0.2–0.5 / 张**，几天就能搭出可用系统。**这是给你的起步推荐。**
- **想完全免费 + 数据不出门**：本地跑 **ComfyUI + SDXL + InstantID**，但需要一张 **≥12GB 显存的 NVIDIA 显卡**，且配置较复杂。
- 系统骨架（前端上传 → 后端异步队列 → 出图 → 图库）对三种方案都一样，**后端生成引擎做成可切换**，就能先用云端起步、以后换本地。

---

## 1. 必须先理解的两个底层认知

### 1.1 "身份 vs 风格"是这件事的根本矛盾
锁住人脸（身份）的技术，往往会**抵抗重度风格化**；而强风格化又容易**把脸冲淡**。所有方案的本质，都是把一个"身份方法"和一个"风格方法"叠在一起，再调两者的相对权重。常用调节旋钮（已交叉验证，作为起步值，需按具体脸/风格微调）：
- **IP-Adapter scale**：`1.0` = 几乎完全照着照片（身份最强）；`~0.5` = 身份与风格平衡。
- **FaceID 权重**：建议 `0.7–1.0`，越高越像但风格自由度越低。
- **风格 LoRA 强度**：`<lora:名字:0.5~1.0>` 是可用区间；>1.0 开始压过脸部，>1.5 易出伪影。
- **InstantID**：想更像就调高 `controlnet_conditioning_scale` 和 `ip_adapter_scale`；想给风格更多空间（或修色彩溢出）就**先调低 `ip_adapter_scale`**。

### 1.2 InsightFace 许可证陷阱（对你=好消息）
几乎所有顶级"保人脸"技术（**InstantID、PuLID、IP-Adapter FaceID、ReActor**）底层都依赖 **InsightFace** 的人脸识别模型权重（antelopev2 / buffalo_l / inswapper_128）。这些**权重是"仅限非商用研究"**，即使外层代码是 Apache/MIT 也不能覆盖这条限制——**商用产品**需要单独向 InsightFace 购买商业授权。
> 来源：<https://github.com/Gourieff/ComfyUI-ReActor> · <https://huggingface.co/InstantX/InstantID/discussions/2> · <https://www.insightface.ai/services/models-commercial-licensing>

**对你的意义**：你是个人和朋友自用、不售卖，属于非商用范畴，**这条限制基本不影响你**。但如果哪天想做成对外收费产品，就必须重新处理这块授权（买 InsightFace 商授，或换成不依赖 InsightFace 的方案，如 PhotoMaker v1 仅用 CLIP）。

---

## 2. 人脸保持(identity-preserving)技术对比

| 方法 | 是否需逐人训练 | 身份保真度 | 风格自由度 | 显存 | 基座模型 | 商用许可 |
|---|---|---|---|---|---|---|
| **InstantID** | 否(零样本，单张照片) | 高(第一梯队) | 中(关键点会锁脸型/姿势) | ~12GB+ | SDXL | 代码 Apache，但依赖 InsightFace→非商用 |
| **PuLID / PuLID-Flux** | 否 | 顶级(与 InstantID 并列第一) | 高(刻意保留背景/光照/可编辑性) | 16GB(12GB 可调) | SDXL / FLUX.1-dev | 同上(InsightFace→非商用) |
| **IP-Adapter FaceID** | 否 | 良(略低于上两者) | 高(轻量、不锁空间) | SD1.5 约 8GB | SD1.5 / SDXL | 非商用(InsightFace) |
| **PhotoMaker v1 / v2** | 否(免训练，秒级) | 中→良(照片越多越好) | 高(文本可控性强) | ~11GB | SDXL | **v1 仅用 CLIP→最适合商用**；v2 加了 InsightFace→非商用 |
| **ReActor / Roop 换脸** | 否(单张源图，瞬时) | 高(但 128px 固定，需配超分) | 不适用(只换脸不重绘风格) | 很低(可 CPU) | 模型无关(作用于成图) | 非商用(InsightFace) |
| **LoRA / DreamBooth 微调** | **是**(需 15–20 张、几分钟到几小时) | 最高上限(姿势/表情泛化最好) | 最高(训练后随便配风格) | LoRA <16GB(SDXL) | SD1.5/SDXL/FLUX | **无 InsightFace 依赖，授权最干净**(看基座模型) |

**当前最佳(2024–2025)**：
- 零样本单图、最强身份：**PuLID-Flux** 与 **InstantID** 并列第一梯队。
- 2025 最新 SOTA：**InfiniteYou(字节跳动, ICCV 2025 Highlight)**，基于 Flux/DiT，论文称在身份相似度、文本对齐、画质上**超过 PuLID-Flux**，并修掉了 PuLID 的"复制粘贴脸"问题。<https://github.com/bytedance/InfiniteYou>
- 风格最灵活的零样本：PhotoMaker、IP-Adapter FaceID。
- 能接受"逐人训练"换取最高保真：DreamBooth / LoRA。

> 注：有来源对 InstantID vs PuLID 谁是绝对第一存在分歧（取决于工作流和评测指标），但两者都明确属于顶级。

---

## 3. 云端图像生成 API 对比（起步首选路线）

> ⚠️ 价格易变，多个官方定价页对抓取工具返回 403，部分单价来自搜索摘要/聚合站，**接入前请到官方页面再核实**（已在文末标注）。

| 平台 | 人脸/参考图支持 | 风格控制 | 约单价/张 | 是否拿你的图训练 | 接后端难度 |
|---|---|---|---|---|---|
| **Replicate** | ✅ 直接托管 InstantID/PhotoMaker/PuLID/IP-Adapter | 看所选模型(LoRA/ControlNet) | ~$0.029(flux-pulid)、~$0.066(InstantID) | 否(不 opt-in 不训练)，**API 输入输出 1 小时后自动删除** | **最佳**：REST + webhook + Py/Node/Go SDK |
| **fal.ai** | ✅ 托管 PuLID-Flux/InstantID/IP-Adapter；FLUX.2 多参考图 | 各模型/FLUX 系 | FLUX.1[dev] $0.025/百万像素 | ⚠️ ToS 含"可基于客户输入派生 Usage Data 来训练模型"，措辞较宽松 | **极佳**：REST 队列 API + webhook + SDK |
| **Stability AI** | 弱(无原生 InstantID) | ✅ 风格/结构/控制端点 | $0.04–$0.08(1 credit=$0.01) | Community License；训练条款不清晰 | 良：REST，多偏同步无 webhook 队列 |
| **Leonardo.Ai** | ✅ Character Reference(身份嵌入，非换脸) | ✅ Style/Content Reference | ~$0.02(按 token) | 付费版私密不外用；**免费版图片可能被平台使用** | 良：REST + webhook(需付费版) |
| **OpenAI gpt-image** | ✅ 编辑端点 `input_fidelity:"high"` 保脸 | 仅靠提示词(无 LoRA) | ~$0.011–$0.25(按质量/分辨率) | **默认不训练**，30 天留存，**支持 ZDR 零留存** | 良：REST+SDK，**无原生异步 webhook** |
| **Google Imagen/Gemini** | ✅ Imagen 主体定制 / Gemini(Nano Banana)参考编辑 | ✅ Imagen 控制参考 | Imagen4 $0.02/$0.04/$0.06；Gemini Flash Image ~$0.039 | Vertex 付费版不训练；**消费级/免费层条款不同** | 良：Vertex/Gemini REST+SDK，但 GCP 配置略重 |

**结论**：
- **真·"自拍→风格头像 + 保身份 + 风格灵活"的最佳两家：Replicate / fal.ai**——只有它们把 InstantID/PuLID/PhotoMaker/IP-Adapter 这些开源身份模型直接做成了 REST+webhook API，单价便宜(~¥0.2–0.5)，最易接异步后端。
  - **Replicate 隐私更干净**（1 小时自动删、不 opt-in 不训练）→ **处理朋友的自拍，推荐它**。
  - fal 队列/webhook 开发体验更顺，但"Usage Data"条款较模糊，介意隐私就少用或看企业条款。
- **隐私姿态最强**：OpenAI gpt-image（ZDR、默认不训练）或 Vertex Imagen——但它们没有开源身份适配器，靠 `input_fidelity:"high"`/主体定制，效果好但**可控性不如 PuLID/InstantID**。
- **Stability** 身份能力最弱，更适合你自己本地跑 SD+InstantID 而非用它的云 API。

---

## 4. 本地 / 自托管开源方案（想完全免费、数据不出门）

### 4.1 基座模型显存与速度
| 模型 | 最低显存 | 推荐显存 | 速度(大致) | 备注 |
|---|---|---|---|---|
| **SD 1.5** | ~4GB | 6–8GB | <2s/张(512px) | 最小最快、生态最深、基础画质最低 |
| **SDXL** | 8GB(需 `--medvram`) | **12GB** | 12GB 约 20s / 8GB 约 60s(1024px) | **画质/生态甜点区** |
| **FLUX.1 dev** | ~7GB(GGUF Q4) | 12–16GB | 4090 约 9–18s | 画质/跟随最好，**许可非商用** |
| **FLUX.1 schnell** | ~7GB(GGUF Q4) | 12–16GB | 4090 约 2–4s(4 步) | 蒸馏版、快，**Apache 可商用** |

> FLUX 全精度 FP16 约需 24–33GB（超出消费级显卡）；FP8≈12–13GB；GGUF Q4≈7GB(8GB 卡可跑，画质略降)。SDXL "最低 8GB、推荐 12GB" 最稳。

### 4.2 运行时 / UI 对比
| 运行时 | SDXL 最低显存 | 配置难度 | API/无头 | FLUX 支持 | 保人脸工作流 |
|---|---|---|---|---|---|
| **ComfyUI** ⭐ | ~6GB(智能卸载) | 中(节点图) | **API 优先，原生** | 最好 | 最好：InstantID/IP-Adapter/PuLID/ReActor 全有节点 |
| **AUTOMATIC1111** | 8GB | 低-中 | 有(`--api`) | 弱(需 Forge 分支) | 靠扩展 |
| **Forge**(A1111 分支) | 更低 | 低-中 | A1111 兼容 | 好(加了 FLUX) | 同 A1111 扩展 |
| **Fooocus** | 8GB(4GB 可调) | **最低** | 几乎无 | 无(仅 SDXL) | 内置但有限，不适合做后端 |
| **InvokeAI** | 8GB | 低(模型管理最好) | 有(自带 FastAPI) | 有 | 内置 IP-Adapter/ControlNet |
| **SD.Next** | 8GB | 中 | A1111 兼容 | 有 | 内置 ControlNet/IP-Adapter，AMD 支持最好 |

**做后端首选 ComfyUI**：它本身就是 REST + WebSocket 服务器，可无头启动（`python main.py --listen 0.0.0.0 --port 8188`），UI 里"Save(API Format)"导出工作流 JSON，后端 `POST /prompt` 提交、WebSocket 跟进度、`/history`+`/view` 取图。生产常用配方：**FaceDetailer + InstantID + IP-Adapter (SDXL)**，或更高质量(更重)的 **PuLID-FLUX**。

### 4.3 硬件现实
- **CPU 跑**：能跑但慢到不可用，别考虑。
- **Apple Silicon (Mac)**：SDXL 在 16GB+ 统一内存可用；FLUX 能跑但慢（M4 Max 1024px 约 85s，vs 4090 的 2–18s），32GB+ 才舒服。适合开发原型，**不适合做出图后端**。
- **结论**：要做真正的出图服务，**NVIDIA 12GB+（理想 24GB 的 3090/4090）** 才实际。

---

## 5. 风格化（动漫/像素/油画/3D/职业风）怎么做

- **风格 LoRA**：几十~几百 MB 的小挂件，把基座模型推向某种风格。主要来源 **Civitai**、Hugging Face。多数 LoRA 有**触发词**(trigger word)，必须写进提示词且靠前放，语法 `<lora:文件名:强度>`。
- **基座模型是风格的主杠杆**：
  - 动漫/插画：用动漫原生 SDXL 检查点，如 **Illustrious XL**、**Pony Diffusion V6 XL**。
  - 写实/职业头像：用写实 SDXL 或 FLUX；Pony/Illustrious 即便"写实"分支也偏卡通，常做"Pony/Illustrious 出形 → 写实 SDXL 二次过"。
  - 油画/像素等特定媒介：用专门的**风格检查点**（如 Painter's Checkpoint、Pixel Art Diffusion XL），比 LoRA 更"上头"但更不灵活。
  - ⚠️ LoRA 必须和基座同族(SD1.5 / SDXL / Pony / Illustrious / Flux 互不通用)。
- **检查点 vs LoRA**：检查点=整模型，风格更强更一致；LoRA=可叠加可换。
- **云端 API 如何暴露风格**：
  - **fal.ai** 的 FLUX-LoRA / SD-LoRA 端点的 `path` 可直接吃 Civitai/HF 的 LoRA URL，`scale` 调强度，可叠多个；FLUX-general 图生图把 LoRA+ControlNet+IP-Adapter 合一，最接近本地"身份+风格"栈。
  - **Replicate** 有 InstantID(带风格预设)、多 LoRA Flux；**FLUX.1 Kontext** 用文字指令重绘成动漫/吉卜力/油画/漫画等同时保脸，并有专门的"职业头像"应用，Kontext Pro ≈ $0.04/张(~8–10s)。
- **进阶技巧**：**InstantStyle** 只把风格特征注入"风格块"、屏蔽其余，从而在不盖掉身份的前提下加风格，且与 InstantID 兼容。
- **Civitai 授权提醒**：多数是 RAIL-M（个人/朋友自用没问题），但创作者可叠加"署名/禁商用/禁生成服务"等附加限制且**可随时改**；部分检查点明确非商用。商用前务必看具体模型的 License 标签。

---

## 6. 多用户自托管系统架构（三种方案共用同一骨架）

### 6.1 为什么必须异步（不能在 HTTP 请求里直接出图）
出图要 10–60s，而浏览器/反代/Web 服务器普遍有 ~30–60s 超时；同步还会占住 worker 线程拖垮并发。**经验法则：>3 秒的活就该放后台。**

### 6.2 标准架构（Web-Queue-Worker / 异步请求-应答）
1. **前端上传 UI**：拖拽上传 → 显示进度 → 展示头像。轮询 `GET /jobs/{id}`(指数退避)或 WebSocket。
2. **API 服务**：鉴权 → 校验/净化上传 → 存原图 → 建 job 记录(queued) → 入队 → 立刻返回 **`202 Accepted` + job_id**。保持无状态、快。
3. **队列 + worker**：Redis 作 broker；worker 跑模型 → 写结果 → 更新状态。worker 可独立横向扩展。
   - Python 后端 → **Celery + Redis**（多进程，适合 CPU/GPU 重活）。
   - Node 后端 → **BullMQ + Redis**（高吞吐、内置重试退避）。
   - 务必：**job 幂等(按 job_id)** + 重试指数退避 + 超次进死信/失败态。
4. **对象/文件存储**：图片存**在 web 根目录之外**，用 S3 兼容存储（自托管 **MinIO**）或挂载卷；用**签名短时 URL** 提供，别给公开直链。
5. **数据库**：用户 + 任务(状态/时间戳/存储 key/归属)。朋友圈规模用 **Postgres 或 SQLite** 足够。

### 6.3 轻量多用户登录（小圈子，别上企业 SSO）
**推荐：邀请码 + Magic Link(魔法链接) + HttpOnly 会话 Cookie**。
- 魔法链接：朋友填邮箱→收到一次性登录链接→点开即登录。无需存密码/做找回，攻击面小，链接快速过期。
- 邀请机制天然契合：**邀请本身就是一条魔法链接**，点开即建号 + 授权。
- 登录后下发服务端会话，放在 **HttpOnly + Secure + SameSite** Cookie（JS 取不到）。
- 现成库如 **Better Auth** 可直接给你 magic-link + 会话 + 邀请流程。
- 注意：魔法链接需要可用的事务邮件通道(邮件送达率)。

### 6.4 部署 + 让朋友访问（无需端口转发）
- **Docker Compose** 一把梭：`web/api`、`worker`、`redis`、`db`、`minio`、`反向代理` 各一服务，同一 Docker 网络。
- **反代/HTTPS 选 Caddy**：两行 Caddyfile 即自动 HTTPS(Let's Encrypt 自动签发续期 + HTTP→HTTPS 跳转)，小自托管最省心。
- **让朋友访问**：
  - 仅局域网：直接发布反代端口，朋友访问 `http(s)://<你的IP>`。
  - **公网且对非技术朋友最友好 → Cloudflare Tunnel**：`cloudflared` 走**出站**连到 Cloudflare 边缘，**不用开端口/端口转发**、隐藏家庭 IP，朋友打开一个**普通 HTTPS 网址即可、无需装任何客户端**，免费额度够用还带 DDoS 防护。
  - Tailscale：适合**你自己**远程管理/SSH，但每个朋友都要装客户端入网，门槛高（除非用 Tailscale Funnel）。
  - ngrok：适合临时演示，不适合长期给朋友用。
- **推荐组合**：Docker Compose + **Caddy(自动 HTTPS)** + **Cloudflare Tunnel(对外)**，外加 Tailscale 给自己做管理。

---

## 7. 隐私与安全（处理朋友的人脸照，务必做）

### 7.1 上传文件净化（纵深防御，对齐 OWASP）
- **别信 `Content-Type` 头和扩展名**（都可伪造）。用**magic bytes/文件签名**按白名单(只放 JPEG/PNG/WebP)校验真实类型。
- **绝不使用用户原始文件名**：生成随机 **UUID** 文件名，顺带杀掉路径穿越和双扩展名把戏。
- **在反代层和应用层都设大小上限**，并限制图片尺寸防"解压炸弹"DoS。
- **每张图都重新编码**(Pillow/ImageMagick 输出纯像素)——这是**性价比最高的一步**：同时**抹掉 EXIF 元数据**(含 GPS 位置)并摧毁多语言(polyglot)恶意载荷。
- **存到 web 根目录之外**并**禁止上传目录执行脚本**；用应用处理器或签名 URL 提供，加 `Content-Disposition`。
- 用 **ClamAV** 扫描后再开放访问。

### 7.2 隐私与法律（人脸=敏感，GDPR 视角，信息性非法律意见）
- 普通照片是个人数据；**只有当你用它做"唯一识别"(生成人脸模板/embedding)时才升级为"特殊类别"生物识别数据**。纯风格化、不建识别模板的管线一般不算特殊类别，但仍应把人脸当敏感数据对待。
- **向朋友取得明确、知情、可撤销的同意**（一个清楚的勾选项 + 说明你会怎么用/存）。
- **数据最小化**：只留必要的；若生成了人脸 embedding 别多留，**用完即删原图**。
- **留存与删除/被遗忘权**：设留存策略(如出图后自动删原图，或 N 天后删)，给删除按钮，删除要清到**所有存储含备份**。
- 加密(传输/静态) + 访问控制(每人只看自己的图，存储 key 按归属隔离)。
- 规模化或做识别用途才需 DPIA；朋友圈规模通常用不上，但增长了要留意。

---

## 8. 三套推荐组合方案

### 方案 A —— 纯云端 API（最省事，⭐ 给你的起步推荐）
- **生成引擎**：Replicate(隐私更干净，处理自拍首选) 或 fal.ai，调用 InstantID / PuLID / PhotoMaker。
- **系统**：FastAPI + Celery + Redis + Postgres + MinIO + Caddy + Cloudflare Tunnel；魔法链接登录。
- **成本**：约 **¥0.2–0.5 / 张**(按量) + 一台小服务器/家用机即可(不需显卡)；起步几乎零固定成本。
- **硬件**：任意能跑 Docker 的机器(家用 NAS/旧电脑/便宜云主机都行)。
- **难度**：★★☆☆☆。几天可上线。
- **适合**：先验证想法、出图质量好、不想折腾显卡。

### 方案 B —— 混合（平衡，未来过渡用）
- 后端把"生成引擎"抽象成接口，**默认走云端 API**，等你买了显卡再切到本地 ComfyUI，**前端/队列/数据库都不用改**。
- **成本**：起步同方案 A；后期本地化后边际出图成本趋零。
- **难度**：★★★☆☆。多写一层 provider 抽象。
- **适合**：现在想快，但明确以后要自托管模型、控成本/隐私。

### 方案 C —— 完全本地免费（数据不出门）
- **生成引擎**：本地 **ComfyUI(无头) + SDXL + InstantID/IP-Adapter(+FaceDetailer)**，或质量更高的 PuLID-FLUX。后端 `POST /prompt` 驱动。
- **成本**：出图免费，但需 **一张 NVIDIA ≥12GB（理想 24GB 3090/4090）** 显卡 + 电费。
- **硬件**：12GB 可用，24GB 舒服；Mac 仅适合开发不适合做后端。
- **难度**：★★★★☆。ComfyUI 工作流 + 模型管理 + 显卡运维。
- **适合**：在意隐私/长期量大/愿意折腾；个人朋友自用，InsightFace 非商用限制不影响你。

> 三套方案的**网站骨架完全一样**，差别只在"生成引擎"那一块——所以无论选哪个，第一步都先把上传→异步队列→图库这套搭好。

---

## 9. 建议的起步路径

1. **先搭骨架 + 接 Replicate**(方案 A)：FastAPI + Celery + Redis + Postgres + MinIO，生成引擎做成可切换的 provider，先实现 `MockProvider`(无 key 也能跑通流程)和 `ReplicateProvider`。
2. **跑通端到端**：上传自拍 → 选风格 → 异步出图 → 图库展示 → 删除。
3. **加最小账户系统**：邀请码 + 魔法链接 + HttpOnly Cookie；每人只看自己的图。
4. **做好上传净化与隐私**：白名单 + UUID 名 + 重编码抹 EXIF + 大小限制 + 用完删原图 + 同意勾选。
5. **Docker Compose + Caddy + Cloudflare Tunnel** 让朋友用网址访问。
6. **风格**：先用 Replicate 的 InstantID 风格预设 / FLUX Kontext 起步；想要更细的动漫/像素/油画风，再上 fal.ai 的 FLUX-LoRA(挂 Civitai LoRA)。
7. **(可选)以后** 买显卡 → 把 provider 切到本地 ComfyUI，前端无感。

我可以按这个路径，下一步直接帮你把**方案 A 的可运行系统骨架**搭出来（含 Mock provider，没 key 也能演示全流程）。

---

## 10. 可信度说明 / 待核实项

- **高可信(多源交叉验证)**：身份-风格矛盾与调节旋钮区间；InsightFace 非商用限制波及 InstantID/PuLID/IP-Adapter FaceID/ReActor；ComfyUI 是 API 优先可无头；Replicate/fal 托管这些身份模型且 ~$0.03/张；异步 Web-Queue-Worker 模式；OWASP 上传净化(magic bytes/重编码/UUID/双层限流/ClamAV)；隧道对比(Cloudflare Tunnel 无端口转发、对非技术朋友最友好)；Caddy 自动 HTTPS 最省心；魔法链接登录。
- **中等/区间**：所有显存数字是区间（FLUX 全精度 24 vs 33GB 取决于是否算文本编码器；FP8≈12–13GB、Q4≈7GB 较一致；SDXL 取 8GB 最低/12GB 推荐最稳）；出图速度是特定显卡/步数的点测，会随版本/加速后端浮动 2–3 倍；身份方法的具体推荐权重值(如 0.8/0.6)是起步值需自行调。
- **较低/需接入前再核实**：**多家云厂商单价**（Replicate flux-pulid $0.029、InstantID $0.066；Stability credit 价；OpenAI $0.011–$0.25；Leonardo ~$0.02/张；fal 的 PuLID/InstantID 单价）——这些官方定价页对抓取工具返回 **403**，数字来自搜索摘要/聚合站，**接入前请到官方页面确认**。
- **条款歧义**：**fal.ai** 是否拿客户输入训练表述模糊("基于客户输入派生 Usage Data 来开发 AI 模型"，ToS 2026-03-03)；介意就走 Replicate 或看企业条款。
- **模型阵容更新快**：OpenAI 图像模型在迭代(gpt-image-1 将于 2026-10-23 弃用，现以 1.5/2 为主)；Google Gemini 图像(Nano Banana / 3.x)在快速更新——接入时请再核实模型 ID 与价格。
- **PhotoMaker v1 许可**：架构上确认 v1 仅用 CLIP(对商用更友好)、v2 加了 InsightFace；但未逐字读 v1 的 LICENSE 文件，商用前请自行核对。
