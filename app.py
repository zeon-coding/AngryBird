from flask import Flask, render_template, request, jsonify
import openai
import requests
import json  # JSON 모듈을 추가

app = Flask(__name__)

# OpenAI API 키 설정
api_key = "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"

# Flask 애플리케이션에서 openai 모듈사용
openai.api_key = api_key

# 채팅 기록을 저장할 리스트
conversation_history = []

# detect.py로 대화 내용을 보내는 함수
def send_to_dialogue(content):
    url = "http://localhost:5001/receive"
    data = {"content": content}
    requests.post(url, json=data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        user_input = request.form['user_input']
    except KeyError:
        return jsonify({'message': "사용자 입력이 없습니다."})
    
    if user_input == "잘 가":
        response = "챗봇: 안녕히 가세요!"
    else:
        # 사용자 입력을 대화 기록에 추가
        conversation_history.append({"role": "user", "content": user_input})
        
        # OpenAI에 사용자 입력을 보내고 챗봇 응답을 받음
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        
        # 챗봇 응답을 대화 기록에 추가
        chatbot_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": chatbot_response})
        
        # 대화 내용을 dialogue.py로 보냄
        send_to_dialogue(user_input)
        send_to_dialogue(chatbot_response)
    
    # JSON 형식으로 응답을 반환
    return jsonify({'message': chatbot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)