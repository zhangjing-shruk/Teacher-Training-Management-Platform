

### **AI 教师培训平台 - 技术需求文档 V1.0**

#### **1. 项目/功能概述 (Overview)**

本项目旨在开发一个集成了人工智能的 Web 应用，为在线英语教育的新任教师提供一个标准化的、可反复练习的在线试讲（磨课）平台。系统通过模拟学生互动和提供多维度即时反馈，旨在大幅提升培训效率，确保教学质量，并为大规模教师招聘与上岗提供有力支持。

#### **2. 核心功能点 (Core Features)**

* **多角色用户系统:**
    * **新老师 (Trainee):** 拥有独立的学习和练习空间。
    * **管理员 (Manager/Trainer):** 监督所有新老师的进度，并进行人工审核。
* **标准化培训流程:**
    * **学习中心:** 新老师可在线阅读或下载 PDF 格式的教学材料。
    * **SOP 流程学习:** 培训通过后，系统引导老师学习上课平台使用、排课规则等标准化操作流程。
* **AI 赋能的试讲练习:**
    * **AI 互动模拟:** （高级功能）老师在试讲时，系统可模拟学生进行基本问答互动。
    * **视频录制与上传:** 支持老师在网页端直接录制或上传自己的试讲视频。
    * **多维度 AI 分析:** 系统从发音、流畅度、能量与热情、内容覆盖度、互动性五个维度对视频进行自动分析，并生成量化分数和文字建议。
    * **练习次数限制:** 每位老师有 5 次提交 AI 分析的机会，鼓励其在得到反馈后进行优化。
* **高效的管理后台:**
    * **进度追踪看板:** 管理员可一览所有新老师的状态（学习中、已提交、待审核、已通过、未通过）。
    * **一体化审核界面:** 管理员可在同一页面观看老师的试讲视频、查看 AI 分析报告，并填写最终的人工评语和审核结果（通过/不通过）。

#### **3. 技术规格 (Technical Specifications)**

##### **前端 (Frontend)**

* **页面/组件 (Pages/Components):**
    * `LoginPage`: 统一登录页面。
    * `TeacherDashboardPage`: 新老师的个人中心，展示培训流程和状态。
    * `ManagerDashboardPage`: 管理员主页，用列表/看板展示所有新老师的进度。
    * `TrainingMaterialPage`: 用于展示和下载 PDF 教材的页面。
    * `TrialLecturePage`: **核心页面**，包含：
        * `VideoRecorder` (视频录制组件): 调用摄像头和麦克风进行录制。
        * `VideoUploader` (视频上传组件): 用于上传本地视频文件。
        * `AIStudentSimulator` (AI 模拟学生组件): （可选高级功能）一个简单的聊天窗口，可根据预设脚本与老师互动。
    * `FeedbackReportPage`: 展示 AI 分析结果（分数、图表、建议）和管理员的最终评语。
    * `SOPPage`: 培训通过后解锁的页面，展示 SOP 内容。
页面配色简洁、高级、现代，交互平滑不死板。
* **用户流程 (User Flow):**
    1.  **新老师:** 登录 -> 进入个人中心 -> 查看教材 -> 进入试讲页面录制/上传视频 -> 提交给 AI 分析 -> 查看反馈报告 -> 若未通过，可重复练习（最多5次） -> 若通过，进入 SOP 学习页面 -> 完成培训。
    2.  **管理员:** 登录 -> 进入管理看板 -> 点击“待审核”的老师 -> 进入审核页面 -> 观看视频、阅读 AI 报告 -> 填写评语并点击“通过”/“不通过” -> 系统状态更新。
* **数据交互 (Data Interaction):**
    * 登录时，向后端发送用户名和密码，获取 `token` (一种用户身份令牌)。
    * 在试讲页，将录制好的视频文件 **POST** 到后端接口。
    * 在反馈页，通过老师 ID 和练习 ID，**GET** 对应的 AI 分析数据和管理员评语。
    * 在管理看板，**GET** 所有新老师的列表及其当前状态。

##### **后端 (Backend)**

* **API 接口 (API Endpoints):** (采用 RESTful 设计风格)
    * **用户认证:**
        * `POST /api/auth/login`: 用户登录。
    * **老师端接口:**
        * `GET /api/teacher/me`: 获取当前老师的个人信息和培训状态。
        * `GET /api/materials`: 获取培训资料列表。
        * `POST /api/lectures`: 上传一个新的试讲视频并发起 AI 分析。
        * `GET /api/lectures`: 获取历史提交的试讲记录及反馈。
    * **管理员端接口:**
        * `GET /api/manager/trainees`: 获取所有新老师的列表及进度。
        * `GET /api/manager/lectures/{lecture_id}`: 获取指定一次试讲的详细信息（视频、AI报告）。
        * `POST /api/manager/lectures/{lecture_id}/review`: 提交对某次试讲的人工审核结果。
* **数据模型 (Data Models):** (数据库表结构设计)
    * **User (用户表):**
        * `id` (主键)
        * `email` (登录邮箱)
        * `password_hash` (加密后的密码)
        * `name` (姓名)
        * `role` (角色: `trainee` 或 `manager`)
    * **TrialLecture (试讲记录表):**
        * `id` (主键)
        * `trainee_id` (外键，关联用户表的 id)
        * `video_url` (视频存储地址)
        * `status` (状态: `processing`, `pending_review`, `passed`, `failed`)
        * `attempt_number` (尝试次数)
        * `created_at` (创建时间)
    * **FeedbackReport (反馈报告表):**
        * `id` (主键)
        * `lecture_id` (外键，关联试讲记录表)
        * `pronunciation_score` (发音分)
        * `fluency_score` (流畅度分)
        * `energy_score` (能量分)
        * `content_score` (内容分)
        * `interaction_score` (互动分)
        * `ai_suggestions` (AI 文字建议, JSON 格式)
        * `manager_feedback` (管理员评语)
        * `is_passed` (管理员最终决定是否通过)

#### **4. 技术栈建议 (Tech Stack Suggestion)**


* **前端:** **Vue.js 3** - 相比 React 更易上手，其“组合式 API”非常适合组织代码逻辑。
* **后端:** **Python (FastAPI)** - FastAPI 性能高，代码简洁，并且能自动生成交互式的 API 文档，对前后端联调极为友好。
* **数据库:** **PostgreSQL** - 功能强大且稳定，是生产环境的优秀选择。初期开发可用 **SQLite** (一个轻量级文件数据库) 以简化配置。
* **AI 服务:** **不建议自研模型。** 采用成熟的云服务 API，按量付费，快速实现功能。
    * **语音转文字及分析 (发音、流畅度):** Google Cloud Speech-to-Text 或 Microsoft Azure Speech Service。它们能提供每个单词的发音置信度和时间戳。
    * **情绪与能量分析:** 对转录后的文本和音频的音调进行分析。可使用 Amazon Comprehend 或 Azure Cognitive Services for Language。
    * **内容与互动分析:** 后端通过代码逻辑，对转录的文本进行关键词匹配（例如，是否提到了教材中的句子；是否使用了 "can you read it", "good" 等互动词）。

#### **5. 开发步骤建议 (Development Steps)**


1.  **环境搭建:** 安装 Python, Node.js, VSCode，并选择一个数据库。
2.  **后端先行 (API First):**
    * 使用 FastAPI 初始化项目。
    * 设计并创建上述三张数据库表。
    * 优先实现用户登录注册的 API 接口。
3.  **前端基础:**
    * 使用 Vite 创建一个 Vue.js 3 项目。
    * 搭建基础的页面路由（登录页、老师主页、管理员主页）。
    * 完成登录页与后端 API 的对接。
4.  **核心功能开发 - 视频上传:**
    * 前端实现一个简单的文件上传页面。
    * 后端实现接收视频文件并保存到服务器或云存储的接口。
5.  **集成第一个 AI 能力 (最关键的一步):**
    * 注册一个云服务商账号（如 Google Cloud）。
    * 在后端，编写代码调用“语音转文字”API。先实现将上传的视频转录成文字的功能。
6.  **构建分析与反馈流程:**
    * 在后端扩展代码，基于转录的文字和分析结果，计算出发音、内容等维度的分数。
    * 将分析结果存入 `FeedbackReport` 表。
    * 前端创建一个页面来展示这份报告。
7.  **完善管理后台:**
    * 开发管理员看板，列出所有待处理的试讲。
    * 开发审核页面，集成视频播放器和评语提交功能。
8.  **完善老师端流程:**
    * 实现 5 次机会的限制逻辑。
    * 开发 SOP 学习页面。
9.  **部署与测试:** 将应用部署到线上服务器，邀请真实用户进行测试。代码上传到github仓库，使用vercel进行部署，使用supbase进行数据储存，需要配置的环境变量有：
    * `DATABASE_URL`: 数据库连接字符串。
    * `GOOGLE_API_KEY`: Google Cloud Speech-to-Text API 密钥。
    * `AZURE_API_KEY`: Microsoft Azure Speech Service API 密钥。
    * `AZURE_API_REGION`: Azure 服务区域（例如，`westus2`）。这些环境变量需要在vercel的项目设置中配置。需要配置的时候找我提供相关信息

