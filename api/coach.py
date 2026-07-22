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
        if "@" in smtp_user:
            sender_email = smtp_user
        else:
            from_domain = "naver.com" if "naver" in smtp_server else "gmail.com"
            sender_email = f"{smtp_user}@{from_domain}"
            
        msg['From'] = f"Career Carrier <{sender_email}>"
        msg['To'] = to_email
        
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender_email, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender_email, [to_email], msg.as_string())
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

def split_text_to_chunks(text, chunk_size=2000):
    if not text:
        return []
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

import re
import urllib.error
from datetime import datetime, timezone, timedelta

def extract_notion_db_id(raw_id):
    if not raw_id:
        return ""
    raw_id = raw_id.strip()
    # If full URL is passed, extract 32-character hex ID
    match = re.search(r'([a-f0-9]{32})', raw_id.replace('-', ''), re.IGNORECASE)
    if match:
        return match.group(1)
    return raw_id

def get_notion_db_schema(notion_token, notion_db_id):
    url = f"https://api.notion.com/v1/databases/{notion_db_id}"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28"
    }
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=3.0) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("properties", {})
    except Exception as e:
        print(f"[Notion Schema Inspection Warning] {e}")
        return None

def send_to_notion_database(email, job, skills, experience, ai_result):
    notion_token = (
        os.environ.get("NOTION_TOKEN", "") or 
        os.environ.get("NOTION_API_KEY", "") or 
        os.environ.get("NOTION_KEY", "")
    ).strip()
    
    raw_db_id = (
        os.environ.get("NOTION_DATABASE_ID", "") or 
        os.environ.get("NOTION_DB_ID", "") or
        "3a5ce80de197806ab961ce5eadeb72bd"
    ).strip()
    
    notion_db_id = extract_notion_db_id(raw_db_id)
    
    # Skip if credentials are not configured
    if not notion_token:
        print("[Notion Error] NOTION_API_KEY is missing in environment variables.")
        return
    if not notion_db_id:
        print("[Notion Error] NOTION_DATABASE_ID is missing.")
        return
        
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    children_blocks = []
    # Notion rich text has a 2000-character limit; chunk to 1800 safely
    for chunk in split_text_to_chunks(ai_result, 1800):
        if chunk.strip():
            children_blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": chunk
                            }
                        }
                    ]
                }
            })
            
    # Current KST time string for Date property
    kst_now = datetime.now(timezone(timedelta(hours=9))).isoformat()

    # 🌟 1. Dynamically inspect DB schema for robust column mapping
    db_schema = get_notion_db_schema(notion_token, notion_db_id)
    
    properties_payload = {}
    
    if db_schema:
        # Find Title property
        title_prop_name = None
        for prop_name, prop_meta in db_schema.items():
            if prop_meta.get("type") == "title":
                title_prop_name = prop_name
                break
        if not title_prop_name:
            title_prop_name = "Name"
            
        properties_payload[title_prop_name] = {
            "title": [{"text": {"content": job}}]
        }
        
        # Find Rich Text, Email, Date properties
        rich_text_props = [name for name, meta in db_schema.items() if meta.get("type") == "rich_text"]
        email_props = [name for name, meta in db_schema.items() if meta.get("type") == "email"]
        date_props = [name for name, meta in db_schema.items() if meta.get("type") == "date"]
        
        # Map Rich Text properties
        if "보유 기술" in rich_text_props:
            properties_payload["보유 기술"] = {"rich_text": [{"text": {"content": skills}}]}
        elif rich_text_props:
            properties_payload[rich_text_props[0]] = {"rich_text": [{"text": {"content": skills}}]}
            
        if "핵심 경험" in rich_text_props:
            properties_payload["핵심 경험"] = {"rich_text": [{"text": {"content": experience}}]}
        elif len(rich_text_props) > 1:
            properties_payload[rich_text_props[1]] = {"rich_text": [{"text": {"content": experience}}]}
            
        # Map Email property if present in DB
        if email:
            if "이메일" in email_props:
                properties_payload["이메일"] = {"email": email}
            elif email_props:
                properties_payload[email_props[0]] = {"email": email}
                
        # Map Date property if present in DB
        matched_date_prop = None
        for candidate in ["등록 날짜", "등록 일시", "생성 일시", "생성 날짜", "생성일", "등록일", "날짜", "Date", "Created Date"]:
            if candidate in date_props:
                matched_date_prop = candidate
                break
        if not matched_date_prop and date_props:
            matched_date_prop = date_props[0]
            
        if matched_date_prop:
            properties_payload[matched_date_prop] = {"date": {"start": kst_now}}
    else:
        # Fallback to standard property names
        properties_payload = {
            "희망 직무": {"title": [{"text": {"content": job}}]},
            "보유 기술": {"rich_text": [{"text": {"content": skills}}]},
            "핵심 경험": {"rich_text": [{"text": {"content": experience}}]}
        }
        if email:
            properties_payload["이메일"] = {"email": email}

    payload = {
        "parent": { "database_id": notion_db_id },
        "properties": properties_payload,
        "children": children_blocks
    }
        
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        # Timeout at 4.0s to avoid blocking responses
        with urllib.request.urlopen(req, timeout=4.0) as response:
            pass
        print("[Notion Success] AI coaching result integrated to Notion database successfully.")
    except urllib.error.HTTPError as http_err:
        try:
            err_body = http_err.read().decode('utf-8')
            print(f"[Notion Integration HTTP Error {http_err.code}] {err_body}")
        except Exception:
            print(f"[Notion Integration HTTP Error {http_err.code}] {str(http_err)}")
    except Exception as e:
        print(f"[Notion Integration Error] {str(e)}")

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
                model='gemini-2.5-flash',
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
            
            # 4.7. 노션 데이터베이스 결과 자동 적재 실행 (환경 변수 구성 시 작동)
            send_to_notion_database(email, job, skills, experience, response.text)
            
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
