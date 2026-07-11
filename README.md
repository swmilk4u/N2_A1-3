# 🌌 AI Career Oasis (퍼스널 커리어 & 포트폴리오 코치)

> **"당신의 커리어에 우아한 빛을 더하다."**  
> AI Career Oasis는 구직자 및 이직 희망자의 핵심 경험과 기술 스택을 분석하여, 서류 전형을 압도할 수 있는 매력적인 자기소개서 초안과 단계별 포트폴리오 스토리라인 전략을 실시간으로 제안해 주는 프리미엄 AI 웹 서비스입니다.
> 
> * **배포 URL:** [https://n2-a1-3-ai-website.vercel.app](https://n2-a1-3-ai-website.vercel.app) *(실제 배포된 Vercel URL 기입란)*
> * **GitHub 저장소:** [https://github.com/swmilk4u/N2_A1-3](https://github.com/swmilk4u/N2_A1-3)

---

## 📑 목차
1. [서비스 기획서 (Service Plan)](#1-서비스-기획서-service-plan)
2. [핵심 AI 기능 및 UX 설계](#2-핵심-ai-기능-및-ux-설계)
3. [기술 스택 (Tech Stack)](#3-기술-스택-tech-stack)
4. [프로젝트 구조 (Project Directory)](#4-프로젝트-구조-project-directory)
5. [로컬 실행 방법 (Local Run)](#5-로컬-실행-방법-local-run)
6. [배포 및 환경 변수 설정 (Deployment & Env)](#6-배포-및-환경-변수-설정-deployment--env)

---

## 1. 서비스 기획서 (Service Plan)

### 🎯 서비스 목적 및 가치
많은 구직자가 자신의 훌륭한 프로젝트 경험과 기술을 가지고 있음에도 불구하고, 자기소개서의 첫 문장을 설계하거나 포트폴리오의 구조를 잡는 데 심각한 어려움(공백 공포증)을 겪습니다. 
**AI Career Oasis**는 사용자의 단편적인 경험 키워드들을 전문 컨설턴트 수준의 스토리텔링과 로드맵으로 변환하여 구직 준비 시간을 단축하고 자신감을 불어넣어 줍니다.

### 👥 타겟 사용자
* **신입 개발자 / 디자이너**: 첫 포트폴리오를 제작하려 하나 구성 전략이 막막한 취업 준비생.
* **이직 준비생 (주니어/미들)**: 기존 경험을 최신 트렌드에 맞게 브랜딩하고자 하는 직장인.
* **비전공자 및 부트캠프 수료생**: 프로젝트 경험은 있으나 기술적 강점을 자소서에 자연스럽게 녹여내기 힘든 지원자.

### 🎨 UX 디자인 콘셉트: '리퀴드글래스(Liquid Glass)'
* **비주얼 엑셀런스**: 어두운 심해를 연상시키는 딥 바이올렛 테마 위에 유기적으로 흐르는 유체 그라데이션 구체(Liquid Blobs)들이 몽환적이고 우아한 깊이감을 자아냅니다.
* **글래스모피즘(Glassmorphism)**: 반투명하고 매끄러운 유리 재질 질감(`backdrop-filter: blur(16px)`)을 카드 레이아웃에 적극 활용하여 극도의 모던함과 프리미엄 감성을 제공합니다.
* **다크/라이트 하이브리드 테마**: 상단 라이트 스위치 토글을 누르면 화사하면서도 부드러운 화이트 캔버스 스타일의 글래스모피즘으로 변환됩니다. (쿠키 기반 상태 보존 및 트랜지션 애니메이션 적용)
* **페이지 구성 (3개 섹션 이상)**:
  1. **Home / Hero**: 서비스 가치 전달 및 웅장한 디자인의 시각 효과 섹션.
  2. **AI 코칭 빌더 (Coaching Builder)**: 본문 입력 폼 및 AI 실시간 분석 결과 렌더링 카드 섹션.
  3. **FAQ & Guides**: 아코디언 컴포넌트를 활용한 매끄러운 정보 제공 섹션.

---

## 2. 핵심 AI 기능 및 UX 설계

### 🛠️ AI 기능 입출력 명세
* **사용자 입력 (Input)**:
  * **희망 직무** (예: `React 프론트엔드 개발자`)
  * **보유 기술 및 핵심 스택** (예: `React, TypeScript, TailwindCSS, Jest`)
  * **주요 프로젝트 및 경험 요약** (예: `3개월간 오픈마켓 토이 프로젝트 제작. 결제 API 연동 시 CORS 오류를 해결하여 성공적으로 런칭함`)
* **AI 출력 (Output)**:
  * **✨ 자기소개서 강점 기술 초안 (500자 내외)**: Star 기법(상황-과제-행동-결과)을 차용하여 매끄럽게 다듬은 자소서 본문.
  * **🚀 포트폴리오 빌드업 스토리라인 전략**: 보유한 스택과 경험이 돋보이게 프로젝트를 구조화하는 맞춤형 가이드 라인(Markdown 형식).
* **AI 백엔드 연동**:
  * 프론트엔드에서 `/api/coach`로 비동기 POST 전송.
  * Vercel Serverless Function(Python) 내부에서 `google-genai` 라이브러리를 통해 최신 **Gemini 3.5 Flash** 모델 호출.

### ⚠️ 예외 및 실패 처리 (UX 안전장치)
1. **빈 입력 차단**: 필수 항목 중 하나라도 비어 있거나 공백만 전송될 시, 전송을 중단하고 경고 창(Toast 및 Error Banner)을 띄워 사용자 피드백을 제공합니다.
2. **API 및 네트워크 에러 핸들링**: 백엔드에서 500 오류가 반환되거나 API 서버에 에러가 났을 때, 적색의 경고 배너를 띄워 상세 에러 정보와 함께 우아하게 에러 메시지("AI 코치 분석 중 오류가 발생했습니다")를 노출합니다.
3. **타임아웃(Timeout) 방지**: 응답이 지연되는 경우(25초 경과 시) JavaScript `AbortController`가 작동하여 비동기 fetch 요청을 자동 취소하고 지연 예외 안내를 화면에 제공합니다.
4. **로딩(Skeleton UI) 피드백**: AI가 분석을 수행하는 동안 오른쪽 결과창에 물결치는 듯한 스켈레톤 애니메이션(Liquid Skeleton Loader)과 로딩 상태 문구를 노출하여 화면이 멈춘 것 같은 불안감을 최소화합니다.

---

## 3. 기술 스택 (Tech Stack)

| 구분 | 기술 스택 | 비고 / 라이브러리 |
| :--- | :--- | :--- |
| **Frontend** | Pure HTML5, CSS3, Vanilla JS | 프레임워크(React/Vue 등) 미사용, CSS 변수/Media Query 반응형 적용 |
| **Backend** | Python 3.9+ (Vercel Serverless) | `BaseHTTPRequestHandler` 기반 경량 API 라우팅 (멀티스레딩 적용) |
| **AI Integration** | Google GenAI SDK | `google-genai` (최신 플래그십 Gemini 3.5 Flash 모델) |
| **Libraries** | Marked.js | AI의 마크다운 응답을 웹 화면에 실시간 HTML 파싱 및 바인딩 |
| **Aesthetics** | FontAwesome 6, Google Fonts | Outfit & Inter 폰트, 프리미엄 벡터 아이콘 |

---

## 4. 프로젝트 구조 (Project Directory)

```text
├── index.html               # 메인 웹 페이지 마크업 (정적 리소스 로드)
├── vercel.json              # Vercel 서버리스 빌드 및 API 라우팅 재정의 설정 파일
├── README.md                # 서비스 소개 및 최종보고서
├── .gitignore               # Git 버전 관리 추적 제외 설정 파일
├── .env                     # 로컬 전용 API 보안 환경 변수 파일
├── 01_document/
│   └── N2_A1-3 과제미션.txt  # 과제 요구사항 명세서
├── 02_source/               # 모든 실행용 소스 파일 및 개발 스크립트 모음 폴더
│   ├── requirements.txt     # 백엔드 Python 의존성 파일 (google-genai)
│   ├── dev_server.py        # 로컬 통합 테스트용 멀티스레드(Threading) 개발 서버
│   ├── css/
│   │   └── style.css        # 리퀴드글래스 테마 및 반응형 레이아웃 스타일시트
│   ├── js/
│   │   └── main.js          # 타임아웃 60초 및 캐시 무효화가 적용된 UI 제어 로직
│   └── api/
│       └── coach.py         # Vercel Serverless Function (Gemini 3.5 Flash 호출 핸들러)
└── 03_etc/                  # 비어 있는 디렉토리 (명세 요구사항용 보존)
```

---

## 5. 로컬 실행 방법 (Local Run)

로컬 개발 서버(`dev_server.py`)를 이용하면 Vercel CLI나 추가 빌드 과정 없이 정적 파일 서빙과 Python API 엔드포인트를 로컬에서 동시에 손쉽게 테스트할 수 있습니다.

### Step 1. 의존성 패키지 설치
터미널을 열고 Python 패키지들을 설치해 주세요. (가상환경 사용 권장)
```bash
pip install -r 02_source/requirements.txt
```

### Step 2. 환경 변수 설정
Gemini API 키를 프로젝트 루트의 `.env` 파일에 기록하거나 시스템 환경 변수에 등록합니다.
* **프로젝트 루트의 `.env` 파일에 직접 설정**:
  ```env
  GEMINI_API_KEY="본인의_실제_GEMINI_API_KEY_값"
  ```
* **Windows (PowerShell)**:
  ```powershell
  $env:GEMINI_API_KEY="본인의_실제_GEMINI_API_KEY_값"
  ```
* **macOS / Linux**:
  ```bash
  export GEMINI_API_KEY="본인의_실제_GEMINI_API_KEY_값"
  ```

### Step 3. 로컬 서버 실행
프로젝트 루트에서 아래 명령을 실행합니다.
```bash
python 02_source/dev_server.py
```
서버가 시작되면 웹 브라우저를 열고 `http://localhost:8000`에 접속하여 서비스를 테스트할 수 있습니다.

---

## 6. 배포 및 환경 변수 설정 (Deployment & Env)

### Vercel 배포 방법
1. 본 프로젝트의 수정 내역을 본인 GitHub 저장소에 커밋 및 푸시합니다.
   ```bash
   git add .
   git commit -m "feat: AI Career Oasis 개발 완료 및 히스토리 정리"
   git push origin main
   ```
2. [Vercel Dashboard](https://vercel.com/dashboard)에 로그인한 뒤 **Add New > Project**를 선택하고, 본인의 GitHub 저장소(`N2_A1-3`)를 연동합니다.
3. 빌드 설정은 기본값으로 유지하되, **Environment Variables** 항목에 다음과 같이 변수를 추가해 줍니다.
   * **Key**: `GEMINI_API_KEY`
   * **Value**: *본인의 실제 Gemini API Key 값*
4. **Deploy** 버튼을 클릭하면 수초 내에 배포가 완료되며 고유한 Vercel URL이 생성됩니다!

---
> [!NOTE]
> **보안 유의사항**: API 키는 절대 코드나 Public GitHub 저장소에 직접 노출하지 마세요. 반드시 Vercel 환경 변수 기능이나 시스템 환경 변수를 통해서만 관리해야 합니다.
