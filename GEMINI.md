# BizTone Converter (업무 말투 변환기)

## 프로젝트 개요

BizTone Converter는 AI 기반의 웹 솔루션으로, 사용자의 일상적인 표현을 상사, 동료, 고객 등 특정 대상에 맞는 전문적인 비즈니스 말투로 자동 변환해 줍니다. 이 프로젝트는 직장인의 커뮤니케이션 효율성을 높이고, 조직 내외부 커뮤니케이션의 일관된 톤앤매너를 유지하며, 직원의 비즈니스 작문 교육을 보조하는 것을 목표로 합니다.

**주요 기술 스택:**
-   **프론트엔드**: HTML5, CSS3 (Tailwind CSS), JavaScript (ES6+)
-   **백엔드**: Python, Flask (RESTful API), Flask-CORS, python-dotenv
-   **AI**: Groq AI API (모델: `moonshotai/kimi-k2-instruct-0905`)
-   **배포**: Vercel (CI/CD 자동화)

**아키텍처:**
클라이언트 레이어(프론트엔드)는 Flask 기반의 REST API 서버(API 게이트웨이)와 통신하며, API 게이트웨이는 Groq AI API 서비스를 호출하여 자연어 변환을 처리합니다. 모든 민감 정보는 환경 변수로 관리되며, 반응형 웹 디자인을 통해 다양한 디바이스에서 최적화된 사용자 경험을 제공합니다.

## 빌드 및 실행

프로젝트를 로컬에서 빌드하고 실행하기 위한 단계는 다음과 같습니다.

### 1. 환경 설정

#### 1.1 Python 가상 환경 설정
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

#### 1.2 백엔드 의존성 설치
`backend/requirements.txt`에 명시된 Python 패키지를 설치합니다.
```bash
pip install -r backend/requirements.txt
```

#### 1.3 환경 변수 설정
프로젝트 루트 디렉토리(`.env` 파일과 같은 위치)에 `.env` 파일을 생성하고 Groq API 키를 추가합니다.
```
GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
```

### 2. 애플리케이션 실행

#### 2.1 백엔드 서버 실행
가상 환경이 활성화된 상태에서 `backend/app.py`를 실행하여 Flask 서버를 시작합니다.
```bash
python backend/app.py
```
서버는 기본적으로 `http://127.0.0.1:5000`에서 실행됩니다.

#### 2.2 프론트엔드 접근
백엔드 서버가 실행 중이면 웹 브라우저에서 `http://127.0.0.1:5000`에 접속하여 프론트엔드 UI에 접근할 수 있습니다. 프론트엔드 파일은 Flask 애플리케이션에 의해 정적으로 제공됩니다.

## 개발 컨벤션

### 1. Git 버전 관리
-   **브랜치 전략**: `main` (production), `develop`, `feature` 브랜치 전략을 사용합니다.
-   **코드 리뷰**: Pull Request를 통한 코드 리뷰를 필수로 합니다.
-   **커밋 메시지**: 의미 있는 커밋 메시지 컨벤션을 따릅니다.

### 2. 환경 변수 관리
-   모든 민감 정보 (예: Groq API 키)는 `.env` 파일에 저장하고 `python-dotenv`를 사용하여 로드합니다.
-   클라이언트 사이드에는 민감 정보가 노출되지 않도록 서버사이드에서만 접근 가능하도록 관리합니다.

### 3. 로깅
-   Python의 `logging` 모듈을 사용하여 애플리케이션의 오류 및 주요 이벤트를 기록합니다.
-   `logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')`와 같은 기본 설정을 따릅니다.
-   개인 정보가 포함되지 않도록 로깅 시 주의합니다.

### 4. 코드 스타일
-   Python 코드의 경우 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 가이드를 따릅니다.
-   프론트엔드 코드는 일관된 포맷팅을 유지합니다.

### 5. 테스트
-   현재 명시적인 테스트 프레임워크나 테스트 코드는 포함되어 있지 않습니다. 기능 개발 시 필요에 따라 통합 테스트 및 단위 테스트를 고려해야 합니다.

### 6. 배포
-   Vercel을 통한 CI/CD 자동화가 설정되어 있으며, `main` 브랜치 푸시 시 자동 배포가 트리거됩니다.
-   프리뷰 배포를 통해 개발 중 테스트 환경을 제공합니다.
