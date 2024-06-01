import os
from openai import AzureOpenAI
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from uuid import uuid4

# 创建Flask应用实例
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
Session(app)

# 创建Azure OpenAI客户端
client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version="2024-02-01",
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

@app.route('/')
def home():
    # 每次访问首页时，重置会话
    session['conversation_id'] = str(uuid4())
    session['conversation'] = [
        {
            "role": "system",
            "content": (
                "你是一位养生顾问！在所有情况下，你都必须使用简体中文进行沟通."
                "你可以提供健康评估、饮食调理、运动指导、心理调适、睡眠管理、中医养生、健康教育和康复指导等方面的专业养生建议确保对话中不使用英文或包含任何英文词汇。"
                "你应与客户建立信任关系，清晰地解释健康问题和养生方案。你不得提供与养生无关的建议或回答其他问题。"
                "如果用户询问超出养生范围的问题，你应说明这不在你的服务范围内，并重申只提供养生建议。"
                "请确保你在对话中遵守以上规则。"
            )
        }
    ]
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    conversation = session.get('conversation', [])
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="syncport-gpt4-32k-0613",
        messages=conversation
    )
    
    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})
    
    print(session['conversation_id'], " : ", user_input, " : ", assistant_message)

    session['conversation'] = conversation
    return jsonify({"response": assistant_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)