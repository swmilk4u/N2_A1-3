from http.server import BaseHTTPRequestHandler
import json
import os
from google import genai
from google.genai import types

# 🌟 Load environment variables from .env if present (self-sufficient backend loading)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                val = val.strip().strip('"').strip("'")
                os.environ[key.strip()] = val

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # CORS preflight 대응
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # 1. Content-Length 헤더로부터 데이터 크기 획득
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "detail": "요청 본문이 비어 있습니다."}).encode('utf-8'))
            return

        post_data = self.rfile.read(content_length)
        
        try:
            # 2. JSON 데이터 파싱
            data = json.loads(post_data.decode('utf-8'))
            job = data.get('job', '').strip()
            skills = data.get('skills', '').strip()
            experience = data.get('experience', '').strip()
            
            # 필수 데이터 검증
            if not job or not skills or not experience:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "detail": "직무, 기술 스택, 핵심 경험 정보를 모두 입력해야 합니다."}).encode('utf-8'))
                return

            # 3. GEMINI API 키 로드
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "detail": "서버에 GEMINI_API_KEY 환경 변수가 구성되지 않았습니다. Vercel 설정 혹은 로컬 env 설정을 확인하세요."}).encode('utf-8'))
                return
            
            # 4. google-genai Client 초기화 및 호출
            client = genai.Client(api_key=api_key)
            
            system_instruction = (
                "당신은 IT/Tech 분야 전문 헤드헌터이자 커리어 브랜딩 코치입니다. "
                "사용자가 제공한 [희망 직무], [보유 기술], [주요 프로젝트/경험] 내용을 기반으로 "
                "서류 전형을 압도할 수 있는 자기소개서 초안과 포트폴리오 기획 전략을 작성해야 합니다. "
                "규칙:\n"
                "1. 전문적이고 트렌디하면서도, 구직자의 잠재력을 최대한 이끌어내는 신뢰도 높고 따뜻한 조언의 톤앤매너를 유지하세요.\n"
                "2. 두 개의 섹션으로 구분하여 Markdown 형식으로 친절하고 가독성 좋게 출력해 주세요:\n"
                "   - '✨ 자기소개서 강점 기술 초안 (500자 내외)': 단순 나열이 아닌 Star 기법(상황-과제-행동-결과)을 녹여낸 매력적인 문장\n"
                "   - '🚀 포트폴리오 빌드업 스토리라인 전략': 보유 기술이 돋보이도록 프로젝트를 구조화하는 로드맵과 팁\n"
                "3. 한국어로 작성해 주세요."
            )
            
            prompt = (
                f"[희망 직무]\n{job}\n\n"
                f"[보유 기술 스택]\n{skills}\n\n"
                f"[주요 프로젝트 및 경험]\n{experience}\n\n"
                "위 정보를 바탕으로 자기소개서 강점 기술 초안과 포트폴리오 가이드를 멋지게 작성해 주세요."
            )
            
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            # 5. 정상 응답 반환
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_payload = {
                "success": True,
                "result": response.text
            }
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "detail": f"AI 코치 분석 중 오류가 발생했습니다: {str(e)}"}).encode('utf-8'))
