from http.server import BaseHTTPRequestHandler
import json
import os
from google import genai
from google.genai import types
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email_direct(to_email, job, skills, experience, ai_result):
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASSWORD", "")
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.naver.com")
    try:
        smtp_port = int(os.environ.get("SMTP_PORT", "465"))
    except:
        smtp_port = 465
        
    # 미구성 시 예외 없이 종료
    if not smtp_user or not smtp_pass or not to_email:
        return
        
    subject = "[Career Carrier] AI 커리어 브랜딩 코칭 분석 리포트"
    body = (
        f"안녕하세요! Career? Carrier! 커리어 분석 코치입니다.\n\n"
        f"요청하신 AI 커리어 코칭 피드백 결과 리포트를 직접 전송해 드립니다.\n\n"
        f"■ 신청 정보\n"
        f"- 희망 직무: {job}\n"
        f"- 보유 기술: {skills}\n"
        f"- 핵심 경험: {experience}\n\n"
        f"-------------------------------------------------------------\n"
        f"■ AI 분석 리포트 본문\n"
        f"-------------------------------------------------------------\n"
        f"{ai_result}\n\n"
        f"-------------------------------------------------------------\n"
        f"본 메일은 Career? Carrier! Vercel 서버리스 엔진을 통해 자동으로 직접 발신되었습니다.\n"
    )
    
    try:
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        from_domain = "naver.com" if "naver" in smtp_server else "gmail.com"
        msg['From'] = f"Career Carrier <{smtp_user}@{from_domain}>"
        msg['To'] = to_email
        
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(f"{smtp_user}@{from_domain}", [to_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(f"{smtp_user}@{from_domain}", [to_email], msg.as_string())
        print(f"[SMTP Success] Email sent directly to {to_email}")
    except Exception as e:
        print(f"[SMTP Error] Failed to send email via SMTP: {str(e)}")

def trigger_automation_webhook(email, job, skills, experience, ai_result):
    # 환경 변수 "AUTO_WEBHOOK_URL"에 설정된 Discord Webhook 또는 Make.com Webhook 주소를 읽어옵니다.
    # 미구성 시 에러 없이 통과 처리하여 의존성을 제거합니다.
    webhook_url = os.environ.get("AUTO_WEBHOOK_URL", "")
    if not webhook_url:
        return
        
    ai_summary = ai_result[:300] + "..." if len(ai_result) > 300 else ai_result
    
    payload = {
        "event": "AI_Career_Coaching_Success",
        "email": email,
        "job": job,
        "skills": skills,
        "experience": experience,
        "ai_result_summary": ai_summary
    }
    
    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        # 서비스 성능 유지를 위해 2.5초 타임아웃 제한
        with urllib.request.urlopen(req, timeout=2.5) as response:
            pass
    except Exception as e:
        print(f"[Webhook Integration Ignored] {str(e)}")

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
            email = data.get('email', '').strip()
            
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
                model='gemini-3.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            # 4.5. 외부 노코드/알림 Webhook 트리거 실행
            trigger_automation_webhook(email, job, skills, experience, response.text)
            
            # 4.6. 외부 도구 없이 백엔드 자체 SMTP 직접 이메일 발송 실행
            send_email_direct(email, job, skills, experience, response.text)
            
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
