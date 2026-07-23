# 🌌 Career? Carrier! — AI 커리어 코칭 웹 서비스

> 서비스 슬로건: **"당신의 커리어에 우아한 빛을 더하다."**
>
> 희망 직무와 보유 기술, 프로젝트 경험을 입력하면 AI가 자기소개서 초안과 포트폴리오 전략을 즉시 생성해주는 AI 웹 서비스입니다.

---

| 항목 | 내용 |
|---|---|
| 🌐 **배포 URL** | [https://swmilk4u-1.vercel.app](https://swmilk4u-1.vercel.app) |
| 💾 **GitHub 저장소** | [https://github.com/swmilk4u/N2_A1-3](https://github.com/swmilk4u/N2_A1-3) |
| 📋 **노션 DB (AI 분석 결과 저장)** | [노션 데이터베이스 바로가기](https://app.notion.com/p/3a5ce80de197806ab961ce5eadeb72bd?v=3a5ce80de19780ff89e9000c9baf8581) |

---

## 📑 목차

1. [서비스 기획서](#1-서비스-기획서)
2. [AI 기능 설계 (입력 / 출력 / 실패 처리)](#2-ai-기능-설계)
3. [기술 스택](#3-기술-스택)
4. [프로젝트 폴더 구조](#4-프로젝트-폴더-구조)
5. [로컬에서 직접 실행하기](#5-로컬에서-직접-실행하기)
6. [Vercel 배포 방법 및 환경 변수 설정](#6-vercel-배포-방법-및-환경-변수-설정)
7. [보너스 과제 구현 내용](#7-보너스-과제-구현-내용)
8. [과제 목표 자체 검증 (Q&A)](#8-과제-목표-자체-검증)
9. [AI 코딩 도구 활용 증빙](#9-ai-코딩-도구-활용-증빙)
10. [서비스 동작 스크린샷](#10-서비스-동작-스크린샷)

---

## 1. 서비스 기획서

### 🎯 서비스 목적

취업 준비생과 이직 희망자 대부분이 "내용은 있는데 어떻게 써야 할지 모르겠다"는 어려움을 겪습니다.
**Career? Carrier!** 는 사용자가 입력한 경험과 기술 키워드를 AI가 분석해 **자기소개서 초안**과 **포트폴리오 구성 전략**을 바로 제안해 줍니다.

### 👥 타겟 사용자

| 사용자 유형 | 어려움 | 서비스가 해결하는 것 |
|---|---|---|
| 신입 개발자 / 디자이너 | 포트폴리오 구성 전략이 막막함 | AI가 강점 중심 스토리라인 제안 |
| 이직 준비생 (주니어/미들) | 기존 경험을 어떻게 표현할지 모름 | 채용 공고 트렌드에 맞는 언어로 번역 |
| 비전공자 / 부트캠프 수료생 | 프로젝트 경험을 자소서에 녹이기 어려움 | STAR 기법 기반 초안 자동 생성 |

### 🎨 페이지 구성 (3개 섹션 이상)

| 섹션 | 내용 | 이동 방법 |
|---|---|---|
| **① Home / Hero** | 서비스 소개 + 실시간 트렌드 뉴스룸 | 상단 네비게이션 |
| **② AI 코칭 빌더** | 입력 폼 + AI 분석 결과 카드 | 상단 메뉴 또는 스크롤 |
| **③ FAQ & Guides** | 자주 묻는 질문 아코디언 | 상단 메뉴 |

> 상단 네비게이션 바를 통해 각 섹션으로 바로 이동할 수 있으며, 다크/라이트 테마 토글 버튼으로 화면 분위기를 바꿀 수 있습니다.

### 📱 반응형 대응

- **데스크톱** (1200px 이상): 좌우 2컬럼 레이아웃
- **태블릿** (768px ~ 1199px): 1컬럼으로 자동 전환
- **모바일** (767px 이하): 입력 폼, 결과 카드 모두 전체 너비로 표시
- CSS Media Query로 구현, 직접 2가지 화면 크기에서 확인 완료

---

## 2. AI 기능 설계

### ✅ 입력 (Input) — 사용자가 입력하는 것

| 필드 | 예시 | 필수 여부 |
|---|---|---|
| 희망 직무 | `React 프론트엔드 개발자` | ✅ 필수 |
| 보유 기술 스택 | `React, TypeScript, TailwindCSS` | ✅ 필수 |
| 주요 프로젝트 및 경험 | `3개월간 오픈마켓 토이 프로젝트 제작. CORS 오류 해결 후 성공적으로 런칭` | ✅ 필수 |
| 결과를 받을 이메일 | `user@example.com` | 선택 (입력 시 이메일 자동 발송) |

### ✅ 출력 (Output) — AI가 생성해주는 것

1. **✨ 자기소개서 강점 기술 초안** (500자 내외)
   - STAR 기법(상황-과제-행동-결과)을 활용한 구조화된 자소서 본문
2. **🚀 포트폴리오 빌드업 전략**
   - 보유 기술이 돋보이는 프로젝트 구성 가이드 (Markdown 형식)

> 결과는 화면 우측 카드에 마크다운 렌더링으로 표시되며, 상단 **복사하기** 버튼으로 전체 복사가 가능합니다.

### ⚠️ 실패 처리 (3가지 모두 구현)

> 과제 요구사항: "아래 실패 처리 중 최소 1개 이상" → **3가지 모두 구현 완료**

| 실패 유형 | 언제 발생하나? | 사용자에게 보여주는 것 |
|---|---|---|
| **① 빈 입력 차단** | 필수 항목을 비운 채 제출 버튼을 누를 때 | 적색 에러 배너 + 우측 하단 토스트 팝업 |
| **② API 오류 처리** | 서버에서 500 오류 또는 AI API 장애 발생 시 | 적색 경고 배너에 상세 에러 메시지 표시 |
| **③ 타임아웃 방지** | AI 응답이 60초를 초과하는 경우 | 요청 자동 취소(AbortController) + 안내 문구 표시 |

### 🧪 테스트 시나리오

| 케이스 | 입력값 | 기대 결과 |
|---|---|---|
| 정상 입력 | 직무/기술/경험 모두 입력 | 스켈레톤 로딩 후 AI 결과 카드 출력 |
| 빈 입력 | 아무것도 입력 안 함 | 전송 차단 + 에러 메시지 표시 |
| 긴 입력 / 지연 | 1000자 이상 텍스트 | 60초 초과 시 자동 취소 + 타임아웃 안내 |

---

## 3. 기술 스택

| 구분 | 기술 | 사용한 이유 |
|---|---|---|
| **프론트엔드** | 순수 HTML5 + CSS3 + JavaScript | 과제 조건 (React 등 프레임워크 사용 금지) |
| **백엔드** | Python 3.12 (Vercel Serverless) | 과제 조건 (api/ 폴더에 Python 함수) |
| **AI 연동** | Google Gemini API (`google-genai`) | Gemini Flash 모델로 자소서 및 포트폴리오 전략 생성 |
| **마크다운 렌더링** | Marked.js | AI 응답(마크다운)을 웹 화면에 보기 좋게 표시 |
| **폰트 / 아이콘** | Google Fonts (Outfit, Inter) + FontAwesome 6 | 프리미엄 디자인 구현 |

> **AI 모델 Fallback 전략**: gemini-2.0-flash → gemini-flash-latest 순서로 자동 전환됩니다. 하나가 실패해도 다음 모델이 자동으로 응답합니다.

---

## 4. 프로젝트 폴더 구조

```text
N2_A1-3_AI website/
│
├── index.html               ← 웹 페이지 본체 (프론트엔드)
├── README.md                ← 지금 보고 있는 이 파일 (보고서)
├── requirements.txt         ← Python 패키지 목록 (Vercel 빌드 시 자동 설치됨)
├── vercel.json              ← Vercel 배포 라우팅 설정
├── .gitignore               ← API 키 등 민감 파일이 GitHub에 올라가지 않도록 제외
│
├── api/                     ← 백엔드 (Vercel Serverless Functions)
│   ├── coach.py             ← AI 코칭 분석 엔드포인트 (/api/coach)
│   └── news.py              ← 실시간 뉴스 RSS 파서 엔드포인트 (/api/news)
│
├── 02_source/               ← 프론트엔드 정적 파일 및 로컬 개발 도구
│   ├── dev_server.py        ← 로컬 테스트용 개발 서버
│   ├── css/
│   │   └── style.css        ← 글래스모피즘 테마 + 반응형 레이아웃 스타일
│   └── js/
│       └── main.js          ← 폼 제출, fetch 호출, 에러 처리, 타임아웃 로직
│
└── 01_document/             ← 과제 제출용 문서 및 증빙 자료
    ├── N2_A1-3 과제미션.txt
    ├── ai_chat_history.md   ← AI 코딩 도구 협업 과정 증빙
    └── screenshots/         ← 스크린샷 증빙 이미지
        ├── desktop_view.png
        ├── mobile_view.PNG
        ├── ai_function_view.png
        ├── empty_1.png
        └── ai_function_error.png
```

> **핵심 구조 설명**: 프론트엔드(`index.html`, `css/`, `js/`)와 백엔드(`api/`)가 명확하게 분리되어 있습니다. Vercel은 `api/` 폴더 안의 Python 파일을 자동으로 서버리스 함수로 인식합니다.

---

## 5. 로컬에서 직접 실행하기

> 인터넷 없이 내 컴퓨터에서 직접 테스트하고 싶을 때 사용합니다.

### Step 1. 코드 내려받기 (Clone)

```bash
git clone https://github.com/swmilk4u/N2_A1-3.git
cd N2_A1-3
```

### Step 2. Python 패키지 설치

```bash
pip install -r 02_source/requirements.txt
```

> `pip`이 없다면 먼저 Python 3.9 이상을 설치해 주세요.

### Step 3. 환경 변수(.env) 파일 설정

프로젝트 루트에 `.env` 파일을 만들고 아래와 같이 입력합니다.

```env
# 필수
GEMINI_API_KEY=여기에_본인의_Gemini_API_키를_입력하세요

# 선택 (노션 DB 자동 저장 사용 시)
NOTION_API_KEY=여기에_노션_통합_토큰을_입력하세요
NOTION_DATABASE_ID=여기에_노션_DB_아이디를_입력하세요

# 선택 (이메일 자동 발송 사용 시)
SMTP_USER=yourmail@gmail.com
SMTP_PASSWORD=구글_앱_비밀번호
```

> ⚠️ `.env` 파일은 절대 GitHub에 올리면 안 됩니다. `.gitignore`에 이미 등록되어 있어 자동으로 제외됩니다.

### Step 4. 로컬 서버 실행

```bash
python 02_source/dev_server.py
```

브라우저에서 `http://localhost:8080` 으로 접속하면 됩니다.

---

## 6. Vercel 배포 방법 및 환경 변수 설정

> Vercel은 GitHub와 연동하면 코드를 push할 때마다 자동으로 전 세계에 배포해 주는 무료 호스팅 서비스입니다.

### Step 1. GitHub에 코드 올리기

```bash
git add .
git commit -m "feat: 기능 개발 완료"
git push origin main
```

### Step 2. Vercel과 GitHub 연동

1. [vercel.com](https://vercel.com) 에 로그인
2. **Add New > Project** 클릭
3. GitHub 저장소(`N2_A1-3`) 선택 후 **Import**

### Step 3. 환경 변수 등록

> **왜 환경 변수로 관리하나요?**
> API 키를 코드에 직접 넣으면 GitHub에 공개되어 해킹 위험이 있습니다. Vercel의 환경 변수 기능을 사용하면 키를 안전하게 서버 내부에만 보관할 수 있습니다.

Vercel 프로젝트 설정 → **Environment Variables** 탭에서 아래 항목을 추가합니다:

| Key (변수 이름) | 필수 여부 | 설명 |
|---|---|---|
| `GEMINI_API_KEY` | ✅ 필수 | Google AI Studio에서 발급한 Gemini API 키 |
| `NOTION_API_KEY` | 선택 | Notion Integrations에서 발급한 `ntn_...` 토큰 |
| `NOTION_DATABASE_ID` | 선택 | 연동할 노션 DB의 ID (URL에서 확인 가능, 32자리) |
| `SMTP_USER` | 선택 | 발신용 Gmail 주소 (예: `yourmail@gmail.com`) |
| `SMTP_PASSWORD` | 선택 | Gmail 앱 비밀번호 (2단계 인증 후 발급) |
| `SMTP_SERVER` | 선택 | 기본값: `smtp.gmail.com` |
| `SMTP_PORT` | 선택 | 기본값: `587` (TLS) |
| `AUTO_WEBHOOK_URL` | 선택 | Discord/Slack/Make.com Webhook 주소 |

### Step 4. Deploy!

**Deploy** 버튼을 클릭하면 약 30~60초 후 고유한 URL이 생성됩니다.

> 이후 `git push`만 하면 자동으로 재배포됩니다.

---

## 7. 보너스 과제 구현 내용

### 🏆 보너스 ①: 운영 자동화 — 3중 파이프라인 구현

> 사용자가 AI 코칭을 받으면 → 자동으로 저장하고 알림을 보내는 흐름

#### 📋 노션 DB 자동 적재 (Notion Database Integration)

- AI 분석 완료 시 Notion API로 결과가 자동으로 노션 데이터베이스에 새 페이지로 저장됩니다.
- 저장 항목: 희망 직무, 보유 기술, 경험 요약, AI 분석 결과 전문
- [노션 DB에서 직접 확인하기](https://app.notion.com/p/3a5ce80de197806ab961ce5eadeb72bd?v=3a5ce80de19780ff89e9000c9baf8581)
- 환경 변수: `NOTION_API_KEY`, `NOTION_DATABASE_ID`

> **어떻게 동작하나?**: `api/coach.py` → `requests.post("https://api.notion.com/v1/pages", ...)` 로 노션 서버에 직접 데이터를 전송합니다.

#### 📧 이메일 자동 발송 (SMTP)

- 사용자가 이메일 주소를 입력하면 AI 분석 결과가 해당 이메일로 자동 발송됩니다.
- Python 내장 `smtplib` 라이브러리를 사용 (외부 서비스 불필요)
- 환경 변수: `SMTP_USER`, `SMTP_PASSWORD`

#### 🔔 Webhook 알림

- `AUTO_WEBHOOK_URL`을 설정하면 Discord/Slack으로 실시간 알림이 전송됩니다.

> **안전 설계**: 환경 변수가 설정되어 있지 않으면 해당 기능만 조용히 건너뛰고 나머지 서비스는 정상 작동합니다.

---

### 🏆 보너스 ②: UX 고도화

#### 🎲 예시 랜덤입력 자동 완성

- 폼 상단의 **🎲 예시 랜덤입력** 버튼을 클릭하면 4가지 직군(프론트엔드/백엔드/데이터엔지니어/디자이너) 중 하나가 무작위로 자동 완성됩니다.
- 처음 사용하는 사람도 어떻게 입력해야 하는지 바로 감을 잡을 수 있습니다.

#### 🌐 실시간 트렌드 뉴스룸

- 구글 뉴스 RSS를 백엔드(`/api/news`)에서 실시간으로 가져와 화면에 표시합니다.
- `이직 OR 창업 OR 채용` 키워드, `when:14d` (최근 14일 이내) 필터 적용
- 네트워크 장애 시에도 모크업 데이터로 자동 대체(Fallback) 됩니다.

#### 🌙 다크 / 라이트 테마 토글

- 우측 상단 버튼으로 다크/라이트 테마를 전환할 수 있습니다.
- 선택한 테마는 브라우저에 저장(`localStorage`)되어 다음 방문 시에도 유지됩니다.

---

## 8. 과제 목표 자체 검증

### Q1. HTML / CSS / JavaScript는 각각 어떤 역할을 하나요?

| 기술 | 역할 | 이 프로젝트에서 한 일 |
|---|---|---|
| **HTML** | 웹페이지의 뼈대(구조) | 입력 폼, 결과 카드, FAQ 섹션 구조 작성 |
| **CSS** | 뼈대에 색깔과 레이아웃을 입히는 것 | 글래스모피즘 디자인, 애니메이션, 반응형 레이아웃 |
| **JavaScript** | 사용자의 행동에 반응해 동작하는 것 | 폼 제출, AI 호출(fetch), 에러 처리, 타임아웃 제어 |

### Q2. 사용자 입력 → AI 응답이 화면에 표시되는 흐름은?

```
[사용자 입력] → [JS: 폼 제출 이벤트 캐치]
→ [JS: 빈 값 검증] → [JS: fetch('/api/coach', POST)]
→ [백엔드 Python: Gemini API 호출]
→ [Python: 응답 반환] → [JS: marked.js로 마크다운 파싱]
→ [화면: 결과 카드에 렌더링]
```

### Q3. Vercel Serverless Functions란 무엇인가요?

- 일반 서버는 항상 켜져 있어야 하는데, **Serverless Functions**는 요청이 들어올 때만 잠깐 켜졌다가 꺼집니다.
- 이 프로젝트에서는 `api/coach.py`가 `/api/coach` 경로로 접근하면 자동으로 실행됩니다.
- 비용이 거의 없고, Vercel이 전 세계 서버에 자동으로 배포해 줍니다.

### Q4. 왜 API 키를 환경 변수로 관리해야 하나요?

- API 키를 코드에 직접 넣으면 GitHub에 공개되어 자동 봇이 몇 초 안에 탈취합니다.
- 탈취된 키로 수십만 원의 과금이 발생할 수 있습니다.
- `.env` 파일(로컬)과 Vercel 환경 변수(배포) 기능으로 키를 코드와 완전히 분리합니다.

### Q5. 로컬 환경과 배포 환경의 차이는?

| 구분 | 로컬 환경 | Vercel 배포 환경 |
|---|---|---|
| 접속 범위 | 나만 접속 가능 | 전 세계 누구나 접속 가능 |
| API 키 관리 | `.env` 파일 | Vercel 환경 변수 대시보드 |
| 코드 반영 | 저장 즉시 | `git push` 후 자동 재배포 |
| 의존성 설치 | 내가 직접 `pip install` | `requirements.txt` 보고 자동 설치 |

### Q6. AI 도구로 개발하다 오류가 발생했을 때 어떻게 해결했나요?

1. **Vercel 배포 오류 (No Python entrypoint)**: Vercel CLI v56 버전에서 Python 함수 인식 방식이 바뀐 것을 확인. `vercel.json`에 `builds` 설정을 명시하여 해결.
2. **Notion API 400 오류**: 존재하지 않는 속성(`이메일`)을 전송하고 있었음. DB 스키마를 동적으로 조회한 후 실제 존재하는 컬럼에만 데이터를 전송하도록 수정.
3. **환경 변수 미반영**: Vercel 프로젝트가 3개 생성되어 실제 서빙 중인 프로젝트(`n2-a1-3-9hlu`)가 다른 것임을 `vercel logs`로 확인. 올바른 프로젝트에 환경 변수 등록 후 재배포하여 해결.

---

## 9. AI 코딩 도구 활용 증빙

> AI 코딩 도구(Antigravity / Claude / Gemini)를 활용하여 개발한 과정의 협업 로그입니다.

📄 **AI 대화 로그 파일**: [01_document/ai_chat_history.md](01_document/ai_chat_history.md)

| 단계 | AI 도구 활용 내용 |
|---|---|
| 기획 | 서비스 아이디어 구체화 및 UX 설계 방향 자문 |
| 프론트엔드 | 글래스모피즘 CSS 스타일, 반응형 레이아웃, 마크다운 렌더링 구현 |
| 백엔드 | Gemini API 연동, Notion API 적재 로직, SMTP 이메일 발송 구현 |
| 배포 | Vercel 환경 변수 등록, vercel.json 설정, 배포 오류 디버깅 |

---

## 10. 서비스 동작 스크린샷

### 🖥️ 데스크톱 뷰 (Desktop View)

![데스크톱 뷰](01_document/screenshots/desktop_view.png)

### 📱 모바일 뷰 (Mobile View)

![모바일 뷰](01_document/screenshots/mobile_view.PNG)

### ⚙️ AI 기능 동작 화면 (AI Function View)

![AI 기능 분석 화면](01_document/screenshots/ai_function_view.png)

### ⚠️ 빈 입력 실패 처리 화면

> 필수값을 입력하지 않고 제출 시, 에러 배너 및 토스트 팝업으로 즉시 안내합니다.

![빈 입력 에러 화면](01_document/screenshots/empty_1.png)

### 🚫 API 오류 처리 화면

> API 오류(4xx/5xx) 발생 시 적색 경고 배너로 상세 에러 정보를 제공합니다.

![API 오류 에러 화면](01_document/screenshots/ai_function_error.png)
