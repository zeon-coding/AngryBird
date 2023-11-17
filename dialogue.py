from flask import Flask, request, jsonify
from konlpy.tag import Komoran
from sentence_transformers import SentenceTransformer, util
import csv

with open('user_data.csv', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        user_name = row['User Name']

komoran = Komoran()

# SentenceTransformers 모델 로드
model = SentenceTransformer("distiluse-base-multilingual-cased")


app = Flask(__name__)

# app.py에서 대화 내용을 받아서 처리하는 엔드포인트
@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    content = data.get('content')

    # 문장과 단어와의 유사도 비교
    test_sentence = content
    test_words = ["라인", "놀러가자", "사귈래", "http"]
    # SentenceTransformers 모델 로드
    model = SentenceTransformer("distiluse-base-multilingual-cased")

    def calculate_similarity(sentence, words):
        # 문장 토큰화
        sentence_tokens = komoran.morphs(sentence)
        
        # 문장 임베딩 생성
        sentence_embedding = model.encode(sentence, convert_to_tensor=True)
        
        for word in words:
            # 단어 임베딩 생성
            word_embedding = model.encode(word, convert_to_tensor=True)
            
            # 코사인 유사도 계산
            cosine_score = util.pytorch_cos_sim(sentence_embedding, word_embedding)
            
            # 백분율로 변환하여 출력
            similarity_percentage = (cosine_score.item() + 1) * 50  # [0, 100] 범위로 변환
            print(f"단어 '{word}'와 문장 '{sentence}' 간의 유사도: {similarity_percentage:.2f}%")

            if similarity_percentage >= 80:
                            send_capture_request(sentence)

    # 유사도 계산 및 출력
    calculate_similarity(test_sentence, test_words)
    return jsonify({'message': "received"})

# app.py로 캡처 요청 보내는 함수
def send_capture_request(captured_sentence):
    print(user_name, "아동의 대화중에 의심되는문장",captured_sentence, "가 나왔습니다. 어린이와 천천히 대화를 잘해보세요")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)