# 🚀 智能金融产品推荐平台

> 基于深度学习和大语言模型的个性化金融产品推荐平台，集成 AI 聊天助手、社区讨论和投资教育资源

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 亮点速览

- 🧠 **深度学习推荐引擎**：基于 TensorFlow 构建的神经网络，智能分析用户画像
- 🤖 **本地大模型集成**：集成 Ollama API，支持离线 AI 对话和金融咨询
- 📊 **多维度用户画像**：考虑年龄、性别、教育、婚姻、资产类别等多重因素
- 💬 **实时智能客服**：支持上下文记忆的多轮对话，24/7 金融问答
- 🏠 **社区讨论平台**：用户互动评论系统，支持点赞和嵌套回复
- 📚 **投资教育中心**：整合优质金融学习资源和工具平台
- 🔧 **RESTful API**：完整的 API 接口，支持第三方集成

## 🏗️ 技术架构

### 核心技术栈
- **后端框架**: Flask (轻量级 Web 框架)
- **数据库**: SQLite (轻量级关系型数据库)
- **机器学习**: TensorFlow 2.15 + Scikit-learn + NumPy
- **数据处理**: Pandas (数据分析与处理)
- **AI 集成**: Ollama API (本地大语言模型)
- **前端**: Bootstrap 5 + 原生 JavaScript
- **ORM**: SQLAlchemy (数据库对象关系映射)

### 推荐算法特色
- **深度神经网络**：多层感知机架构，自动学习用户-产品关联
- **特征工程**：标准化数值特征 + One-Hot 编码分类特征
- **置信度评分**：为每个推荐结果提供可解释的置信度分数
- **模型持久化**：训练完成的模型自动保存，支持快速加载

## 🚀 快速开始 (Windows)

### 环境准备
```powershell
# 检查 Python 版本 (需要 3.12+)
python --version

# 克隆项目
git clone https://github.com/LingmaFuture/financial-recommender.git
cd financial_recommender1

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

### 启动应用
```powershell
# 进入应用目录
cd notebooks

# 启动 Flask 应用
python app.py
```

应用将在 `http://localhost:8080` 启动，自动初始化数据库和推荐模型。

### Ollama 大模型配置 (可选)
```powershell
# 安装 Ollama (访问 https://ollama.ai 下载)
# 拉取推荐模型
ollama pull llama2
# 或者
ollama pull qwen:7b

# 启动 Ollama 服务 (默认端口 11434)
ollama serve
```

## 📖 核心功能详解

### 🎯 智能推荐系统
- **个性化算法**：基于用户画像的深度学习推荐
- **实时推荐**：毫秒级响应，支持在线推理
- **多产品支持**：自动识别数据集中的所有产品类型
- **可解释性**：提供推荐理由和置信度评分

**支持的用户特征**：
- 基础信息：年龄、性别、婚姻状况、子女情况
- 教育背景：学历水平
- 投资偏好：风险偏好、资产类别倾向

### 🤖 AI 智能客服
- **自然语言理解**：支持中文金融问答
- **上下文记忆**：维护会话历史，支持连续对话
- **多模型支持**：兼容 Ollama 生态的各种开源大模型
- **会话管理**：基于 Session ID 的多用户并发支持

### 💬 社区讨论平台
- **评论系统**：支持发布、回复、点赞功能
- **数据持久化**：基于 SQLAlchemy 的完整 CRUD 操作
- **实时交互**：Ajax 异步加载，无刷新用户体验
- **分页加载**：高效处理大量评论数据

### 📚 投资教育中心
精选金融学习资源，包括：
- 📈 股票市场分析工具
- 💰 加密货币交易平台
- 📊 投资研究报告
- 🎓 金融知识学习平台

## 🔌 API 接口文档

### 推荐接口
```powershell
# 获取个性化推荐 (PowerShell 示例)
$headers = @{"Content-Type" = "application/json"}
$body = @{
    "AGE" = 30
    "GENDER" = "M"
    "MARITAL" = "Single"
    "HAVE_CHILD" = "No"
    "EDU_LEVEL" = "Bachelor"
    "ASSET_CLASS" = "Stocks"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/recommend" -Method POST -Headers $headers -Body $body
```

### 聊天接口
```powershell
# AI 聊天对话
$chatBody = @{
    "question" = "什么是基金定投？"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/chat" -Method POST -Headers $headers -Body $chatBody
```

### 评论接口
```powershell
# 获取所有评论
Invoke-RestMethod -Uri "http://localhost:8080/api/comments" -Method GET

# 发布新评论
$commentBody = @{
    "content" = "这个推荐系统很实用！"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/comments" -Method POST -Headers $headers -Body $commentBody
```

## 📁 项目结构

```
financial_recommender1/
├── data/                          # 数据文件
│   └── CUST_INVESTMENT.csv       # 客户投资数据集
├── models/                        # 训练模型存储
├── notebooks/                     # 主应用代码
│   ├── app.py                    # Flask 主应用
│   ├── recommender.py            # 推荐算法核心
│   ├── ollama.py                 # Ollama API 封装
│   ├── models.py                 # 数据库模型定义
│   ├── static/                   # 静态资源
│   └── templates/                # HTML 模板
│       ├── home.html            # 首页
│       ├── recommend.html       # 推荐页面
│       ├── chat.html            # AI 聊天
│       ├── discussion.html      # 讨论区
│       ├── education.html       # 教育中心
│       └── api.html             # API 文档
├── requirements.txt               # Python 依赖
└── readme.md                     # 项目文档
```

## 🛠️ 开发指南

### 数据格式要求
推荐系统支持的输入数据格式：
```javascript
{
  "AGE": 30,                    // 年龄 (数值)
  "GENDER": "M",                // 性别 (M/F)
  "MARITAL": "Single",          // 婚姻状况 (Single/Married)
  "HAVE_CHILD": "No",           // 是否有子女 (Yes/No)
  "EDU_LEVEL": "Bachelor",      // 学历 (High School/Bachelor/Master/PhD)
  "ASSET_CLASS": "Stocks"       // 资产类别偏好
}
```

**字段说明：**
- `AGE`: 用户年龄，数值类型
- `GENDER`: 性别，可选值：`"M"` (男性) 或 `"F"` (女性)
- `MARITAL`: 婚姻状况，可选值：`"Single"` (单身) 或 `"Married"` (已婚)
- `HAVE_CHILD`: 是否有子女，可选值：`"Yes"` 或 `"No"`
- `EDU_LEVEL`: 教育水平，可选值：`"High School"`, `"Bachelor"`, `"Master"`, `"PhD"`
- `ASSET_CLASS`: 资产类别偏好，根据数据集中的具体类别而定

### 模型训练与部署
```powershell
# 重新训练模型 (如果需要)
cd notebooks
python -c "
from recommender import FinancialRecommender
import pandas as pd
data = pd.read_csv('../data/CUST_INVESTMENT.csv')
model = FinancialRecommender()
X = data.drop(['CODE'], axis=1)
y = data['CODE']
model.train(X, y)
"
```

### 自定义配置
在 `notebooks/config.py` 中可以调整：
- 数据库连接配置
- Ollama 服务地址
- 模型参数设置
- 日志级别配置

## ❓ 常见问题

**Q: 为什么推荐结果不准确？**
A: 确保训练数据质量良好，数据量充足。可以通过增加训练数据或调整模型参数来改善。

**Q: Ollama 连接失败怎么办？**
A: 确保 Ollama 服务正在运行 (`ollama serve`)，并检查端口 11434 是否可访问。

**Q: 如何添加新的产品类型？**
A: 在 `data/CUST_INVESTMENT.csv` 中添加新的产品数据，重启应用会自动重新训练模型。

**Q: 支持哪些大语言模型？**
A: 支持所有 Ollama 兼容的模型，推荐使用 llama2、qwen、chatglm 等中文友好模型。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
