from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import xml.etree.ElementTree as ET
import ssl

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # CORS preflight 대응
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # CORS 헤더와 JSON 헤더 설정
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        # 구글 뉴스 실시간 RSS 피드 URL (검색어: 이직 OR 창업 OR 채용, 14일 이내 최신 기사)
        url = "https://news.google.com/rss/search?q=%EC%9D%B4%EC%A7%81+OR+%EC%B0%BD%EC%97%85+OR+%EC%B2%B4%EC%9A%A9+when:14d&hl=ko&gl=KR&ceid=KR:ko"

        try:
            # 1. SSL 인증서 만료 및 불일치 에러 우회를 위한 미인증 컨텍스트 생성
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # 2. 봇 탐지 회피용 임의의 User-Agent 주입 헤더 구성
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )

            # 3. HTTP 요청 수행
            with urllib.request.urlopen(req, context=ctx, timeout=8) as response:
                xml_data = response.read()

            # 4. XML 데이터 트리 파싱
            root = ET.fromstring(xml_data)
            news_items = []

            # 5. 최신 8개 기사 획득 및 텍스트 데이터 정제
            for item in root.findall('.//item')[:8]:
                title = item.find('title').text if item.find('title') is not None else '커리어 트렌드 기사'
                link = item.find('link').text if item.find('link') is not None else '#'
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                source = item.find('source').text if item.find('source') is not None else '트렌드 뉴스'

                # 구글 뉴스 타이틀 포맷 ("뉴스 제목 - 언론사") 정제
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0].strip()
                    source = parts[1].strip()

                news_items.append({
                    "title": title,
                    "link": link,
                    "pubDate": pub_date,
                    "source": source
                })

            response_body = {"success": True, "news": news_items, "fallback": False}
            self.wfile.write(json.dumps(response_body, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            # 6. 네트워크 타임아웃 등 예외 발생 시 반환할 우아한 Fallback 모크업 데이터셋
            mock_news = [
                {
                    "title": "2026 하반기 채용 트렌드: AI 기술 면접 대비와 돋보이는 포트폴리오 기획법",
                    "link": "https://www.wanted.co.kr",
                    "pubDate": "Sun, 12 Jul 2026",
                    "source": "원티드"
                },
                {
                    "title": "성공적인 연봉 협상과 커리어 퀀텀 점프를 위한 이직 시나리오 가이드",
                    "link": "https://www.rememberapp.co.kr",
                    "pubDate": "Sat, 11 Jul 2026",
                    "source": "리멤버"
                },
                {
                    "title": "1인 테크 창업 및 사이드 프로젝트로 완성하는 나만의 포트폴리오 노하우",
                    "link": "https://www.wanted.co.kr",
                    "pubDate": "Fri, 10 Jul 2026",
                    "source": "스타트업레시피"
                },
                {
                    "title": "트렌디한 IT 기업 채용 담당자들이 눈여겨보는 자기소개서 첫 문장 꿀팁",
                    "link": "https://www.wanted.co.kr",
                    "pubDate": "Thu, 09 Jul 2026",
                    "source": "디캠프"
                },
                {
                    "title": "비전공자 주니어 개발자의 생존 전략: 성장 기록 블로그와 깃허브 브랜딩 요령",
                    "link": "https://www.wanted.co.kr",
                    "pubDate": "Wed, 08 Jul 2026",
                    "source": "커리어저널"
                }
            ]
            response_body = {
                "success": True,
                "news": mock_news,
                "fallback": True,
                "detail": str(e)
            }
            self.wfile.write(json.dumps(response_body, ensure_ascii=False).encode('utf-8'))
