`该项目使用是我与 chatGPT-4o 一起合作完成的，readme文档由chatGPT-4o编写，我有所修改`

当然，这里是一份详细的 README 文档，初学者也能看懂，从激活虚拟环境开始，涵盖所有步骤。

---

# Flask Azure OpenAI Chatbot

这个项目使用 Flask 框架和 Azure OpenAI 构建了一个简单的聊天机器人应用。以下是设置和运行该项目的详细步骤。

## 先决条件

- 安装了 [Anaconda](https://www.anaconda.com/products/distribution)
- Azure OpenAI 账户和 API 密钥

## 设置步骤

### 1. 创建和激活虚拟环境

首先，打开命令行窗口，创建并激活一个新的 Conda 虚拟环境：

```sh
# 创建虚拟环境，命名为 'flask_openai_env'
conda create --name flask_openai_env python=3.8

# 激活虚拟环境
conda activate flask_openai_env
```

### 2. 安装所需库

在激活的虚拟环境中，运行以下命令安装所需的 Python 库：

```sh
pip install openai flask Flask-Session
```

### 3. 配置环境变量

在系统的环境变量中添加以下内容，并替换为你自己的 Azure OpenAI API 密钥和端点：

```sh
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your_openai_endpoint_here
```

确保你将 `your_api_key_here` 和 `your_openai_endpoint_here` 替换为你实际的 API 密钥和端点。

### 4. 项目文件结构

确保你的项目文件结构如下：

```
project_root/
│
├── app.py
├── flask_session/
│   ├── ... (会话文件)
└── templates/
    └── index.html
```

### 5. 运行应用

在项目根目录下，运行以下命令启动 Flask 应用：

```sh
python app.py
```

### 6. 会话存储

会话数据将存储在项目根目录下的 `flask_session` 文件夹中。该文件夹由 `flask_session` 配置项指定。如果该文件夹不存在，Flask-Session 会自动创建。

### 7. 访问应用

打开浏览器，访问以下地址：

```
http://127.0.0.1:3000
```

你现在应该可以看到聊天应用的主页，并开始与 Azure OpenAI 机器人进行对话。
