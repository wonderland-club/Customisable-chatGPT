import os  # 导入操作系统相关的库
from openai import AzureOpenAI  # 导入 Azure OpenAI 客户端
from flask import Flask, request, jsonify, render_template, session  # 导入 Flask 及其相关模块
from flask_session import Session  # 导入 Flask-Session 扩展
from uuid import uuid4  # 导入生成唯一标识符的模块

# 创建一个 Flask 应用实例
app = Flask(__name__)

# 设置 Flask 的密钥，用于会话数据的加密
app.secret_key = os.urandom(24)

# 配置 Flask-Session 扩展
app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系统来存储会话数据
app.config['SESSION_FILE_DIR'] = './flask_session'  # 指定会话数据的存储目录
app.config['SESSION_PERMANENT'] = False  # 设置会话不过期
app.config['SESSION_USE_SIGNER'] = True  # 使用签名对会话数据进行保护
app.config['SESSION_KEY_PREFIX'] = 'session:'  # 会话数据的键前缀
Session(app)  # 将会话配置应用到 Flask 应用实例中

# 创建 Azure OpenAI 客户端实例
client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),  # 从环境变量中获取 API 密钥
    api_version="2024-02-01",  # 设置 API 版本
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')  # 从环境变量中获取 Azure 端点
)

@app.route('/')  # 定义根路径的路由
def home():
    # 每次访问首页时，重置会话
    session['conversation_id'] = str(uuid4())  # 生成一个唯一的会话 ID
    session['conversation'] = [
        {"role": "system", "content": "你是一位中文养生顾问！在所有情况下，你都必须使用简体中文进行沟通，确保对话中不使用英文或包含任何英文词汇。你可以提供健康评估、饮食调理、运动指导、心理调适、睡眠管理、中医养生、健康教育和康复指导等方面的专业养生建议。你应与客户建立信任关系，清晰地解释健康问题和养生方案。你不得提供与养生无关的建议或回答其他问题。如果用户询问超出养生范围的问题，你应说明这不在你的服务范围内，并重申只提供养生建议。请确保你在对话中遵守以上规则。"}
    ]  # 初始化会话内容
    return render_template('index.html')  # 渲染首页模板

@app.route('/chat', methods=['POST'])  # 定义 /chat 路由，处理 POST 请求
def chat():
    user_input = request.form['user_input']  # 获取用户输入
    conversation = session.get('conversation', [])  # 获取当前会话内容，如果不存在则返回空列表
    conversation.append({"role": "user", "content": user_input})  # 将用户输入添加到会话内容中
    
    # 调用 Azure OpenAI API 获取模型回复
    response = client.chat.completions.create(
        model="syncport-gpt4-32k-0613",  # 指定使用的模型
        messages=conversation  # 提供会话内容
    )
    
    # 获取助手的回复内容
    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})  # 将助手回复添加到会话内容中
    print(session['conversation_id'], " : ", user_input, " : ", assistant_message)  # 打印会话 ID、用户输入和助手回复

    session['conversation'] = conversation  # 更新会话内容
    return jsonify({"response": assistant_message})  # 以 JSON 格式返回助手回复

if __name__ == '__main__':  # 确保该模块是作为主程序运行
    app.run(host='0.0.0.0', port=3000)  # 启动 Flask 应用，监听所有主机的 3000 端口