import os
import logging # Import logging module
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
# 프론트엔드からの 모든 출처에서의 요청을 허용
CORS(app) 

groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    logging.error("Error: GROQ_API_KEY not found in environment variables.")
    groq_client = None
else:
    try:
        groq_client = Groq(api_key=groq_api_key)
        logging.info("Groq client initialized successfully.")
    except Exception as e:
        groq_client = None
        logging.error(f"Error initializing Groq client: {e}")

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    텍스트 변환을 위한 API 엔드포인트.
    Groq AI API를 활용하여 실제 변환 로직을 수행합니다.
    """
    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        logging.error("Missing 'text' or 'target' in request.")
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    # 대상별 프롬프트 정의
    prompts = {
        "Upward": f"다음 문장을 상사에게 보고하는 정중하고 격식 있는 보고 형식으로 변환해 주세요. 결론부터 명확하게 제시해 주세요: '{original_text}'",
        "Lateral": f"다음 문장을 타팀 동료에게 보내는 친절하고 상호 존중하는 협조 요청 형식으로 변환해 주세요. 요청 사항과 마감 기한을 명확히 전달해 주세요: '{original_text}'",
        "External": f"다음 문장을 고객에게 보내는 극존칭을 사용하며 전문성과 서비스 마인드를 강조하는 안내, 공지 또는 사과 형식으로 변환해 주세요: '{original_text}'"
    }

    system_message = "당신은 비즈니스 커뮤니케이션 전문가입니다. 사용자가 제공한 텍스트와 대상에 맞춰 가장 적절하고 전문적인 말투로 변환해 주세요."
    user_message = prompts.get(target)

    if not user_message:
        logging.error(f"Invalid target received: {target}")
        return jsonify({"error": "유효하지 않은 변환 대상입니다."}), 400

    if groq_client is None:
        logging.error("Groq client not initialized. GROQ_API_KEY might be missing or invalid.")
        return jsonify({"error": "Groq 클라이언트가 초기화되지 않았습니다. API 키를 확인해주세요."}), 500

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7, # 창의성 조절
            max_tokens=500,  # 최대 응답 길이
        )
        converted_text = chat_completion.choices[0].message.content
        logging.info("Text conversion successful.")
        
    except Exception as e:
        logging.error(f"Groq API 호출 오류: {e}")
        return jsonify({"error": "텍스트 변환 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}), 500

    response_data = {
        "original_text": original_text,
        "converted_text": converted_text,
        "target": target
    }
    
    return jsonify(response_data)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Add a route to serve other static files (CSS, JS)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)