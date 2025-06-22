# MOLA Backend API 문서

## 개요

MOLA (Mathematical Object Learning Assistant)는 수학 문제 학습을 돕는 AI 기반 백엔드 시스템입니다. 

### 주요 기능
- 🔐 **사용자 인증 및 관리** - JWT 기반 회원가입/로그인/프로필 관리
- 📷 **이미지 OCR 분석** - 수학 문제 이미지를 텍스트로 변환 및 구조화
- 🤖 **AI 문제 생성** - GPT를 활용한 다양한 수학 문제 자동 생성
- 📚 **문제 관리** - CRUD 기능을 통한 수학 문제 데이터 관리

## 서버 정보

- **Base URL**: `http://localhost:8000` (개발 환경)
- **API 문서**: `http://localhost:8000/swagger/` (Swagger UI)
- **인증 방식**: JWT Bearer Token

## 인증

인증이 필요한 API는 헤더에 JWT 액세스 토큰을 포함해야 합니다:

```http
Authorization: Bearer {your_access_token}
```

## API 엔드포인트

### 🔐 사용자 인증

#### 회원가입
- **POST** `/api/users/api/signup/`
- **설명**: 새로운 사용자 계정을 생성합니다.
- **인증**: 불필요
- **요청 필드**:
  - `username` (string, 필수): 사용자 아이디
  - `email` (string, 필수): 이메일 주소
  - `real_name` (string, 필수): 실명
  - `birthdate` (string, 필수): 생년월일 (YYYY-MM-DD)
  - `school` (string, 필수): 학교명
  - `student_number` (integer, 필수): 학번
  - `password` (string, 필수): 비밀번호
  - `password2` (string, 필수): 비밀번호 확인
  - `avatar` (file, 선택): 프로필 사진

#### 로그인
- **POST** `/api/users/api/login/`
- **설명**: 사용자 인증 후 JWT 토큰을 발급받습니다.
- **인증**: 불필요
- **요청 필드**:
  - `username` (string, 필수): 사용자 아이디
  - `password` (string, 필수): 비밀번호
- **응답**: 액세스 토큰, 리프레시 토큰, 사용자 정보

### 👤 사용자 프로필

#### 프로필 조회
- **GET** `/api/users/api/profile/`
- **설명**: 현재 로그인한 사용자의 프로필 정보를 조회합니다.
- **인증**: 필요

#### 프로필 수정
- **PATCH** `/api/users/api/profile/`
- **PUT** `/api/users/api/profile/`
- **설명**: 현재 로그인한 사용자의 프로필 정보를 수정합니다.
- **인증**: 필요
- **요청 필드**: 수정하고자 하는 필드만 전송 (PATCH) 또는 모든 필드 전송 (PUT)

#### 회원탈퇴
- **DELETE** `/api/users/api/profile/`
- **설명**: 현재 로그인한 사용자의 계정을 삭제합니다.
- **인증**: 필요
- **주의**: 이 작업은 되돌릴 수 없습니다.

### 📚 수학 문제 관리

#### 문제 목록 조회
- **GET** `/api/problems/list/`
- **설명**: 등록된 모든 수학 문제 목록을 최신순으로 조회합니다.
- **인증**: 필요

#### 문제 직접 생성
- **POST** `/api/problems/list/`
- **설명**: 이미지 없이 텍스트로 수학 문제를 직접 생성합니다.
- **인증**: 필요
- **요청 필드**:
  - `question` (string, 필수): 수학 문제 내용
  - `image_path` (string, 선택): 문제 이미지 경로

#### 이미지 업로드 및 분석
- **POST** `/api/problems/upload/`
- **설명**: 수학 문제 이미지를 업로드하여 OCR 및 AI 분석을 수행합니다.
- **인증**: 필요
- **Content-Type**: `multipart/form-data`
- **요청 필드**:
  - `image` (file, 필수): 분석할 수학 문제 이미지
- **처리 과정**:
  1. 이미지 파일 저장
  2. OCR을 통한 텍스트 추출
  3. LaTeX 수식 변환
  4. GPT를 통한 문제 구조화 분석
  5. 데이터베이스 저장
  6. JSON 파일 백업

#### 문제 상세 조회
- **GET** `/api/problems/{id}/`
- **설명**: 문제 ID를 통해 특정 수학 문제의 상세 정보를 조회합니다.
- **인증**: 필요

#### 문제 수정
- **PUT** `/api/problems/{id}/`
- **PATCH** `/api/problems/{id}/`
- **설명**: 문제 ID를 통해 특정 수학 문제의 정보를 수정합니다.
- **인증**: 필요

#### 문제 삭제
- **DELETE** `/api/problems/{id}/`
- **설명**: 문제 ID를 통해 특정 수학 문제를 삭제합니다.
- **인증**: 필요
- **주의**: 이 작업은 되돌릴 수 없습니다.

### 🤖 AI 문제 생성

#### AI 문제 생성
- **GET** `/api/ai/generate/`
- **POST** `/api/ai/generate/`
- **설명**: GPT를 활용하여 다양한 유형의 수학 문제를 자동으로 생성합니다.
- **인증**: 필요
- **지원 문제 유형**:
  - 이차방정식
  - 삼각함수
  - 미적분
  - 대수
  - 기하
  - 확률통계
- **응답 필드**:
  - `problem_type`: 문제 유형
  - `question`: 생성된 문제 내용
  - `latex`: LaTeX 형식 수식
  - `options`: 선택지 배열
  - `answer`: 정답
  - `explanation`: 해설
  - `difficulty`: 난이도
  - `category`: 카테고리

## 응답 코드

| 상태 코드 | 설명 |
|----------|------|
| 200 | 요청 성공 |
| 201 | 생성 성공 |
| 204 | 삭제 성공 (응답 본문 없음) |
| 400 | 잘못된 요청 (유효성 검사 실패) |
| 401 | 인증 실패 |
| 403 | 권한 없음 |
| 404 | 리소스를 찾을 수 없음 |
| 413 | 파일 크기 초과 |
| 500 | 서버 오류 |

## 에러 응답 형식

```json
{
  "detail": "에러 메시지",
  "field_name": ["필드별 에러 메시지"]
}
```

## 예시 요청/응답

### 회원가입 예시

**요청**:
```http
POST /api/users/api/signup/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "real_name": "홍길동",
  "birthdate": "2000-01-01",
  "school": "선린인터넷고등학교",
  "student_number": 1001,
  "password": "password123",
  "password2": "password123"
}
```

**응답**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "real_name": "홍길동",
  "birthdate": "2000-01-01",
  "school": "선린인터넷고등학교",
  "student_number": 1001,
  "avatar": "/media/avatars/default.jpg"
}
```

### 로그인 예시

**요청**:
```http
POST /api/users/api/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}
```

**응답**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "username": "john_doe",
    "real_name": "홍길동",
    "email": "john@example.com",
    "avatar": "/media/avatars/john_doe/profile.jpg"
  }
}
```

### AI 문제 생성 예시

**응답**:
```json
{
  "problem_type": "이차방정식",
  "question": "다음 이차방정식을 풀어보세요: 2x² - 7x + 3 = 0",
  "latex": "2x^2 - 7x + 3 = 0",
  "options": [
    "A) x = 3, x = 1/2",
    "B) x = -3, x = -1/2",
    "C) x = 2, x = 3/2",
    "D) x = -2, x = -3/2"
  ],
  "answer": "A) x = 3, x = 1/2",
  "explanation": "인수분해를 사용하면: (2x-1)(x-3) = 0이므로 x = 1/2 또는 x = 3입니다.",
  "difficulty": "medium",
  "category": "대수",
  "created_at": "2024-01-01T15:30:00Z"
}
```

## 개발 환경 설정

### 필요 조건
- Python 3.8+
- Django 5.2+
- Django REST Framework
- drf-yasg (Swagger 문서화)
- JWT 인증 라이브러리

### 환경 변수
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
OPENAI_API_KEY=your-openai-api-key
```

### 서버 실행
```bash
python manage.py runserver
```

## 참고사항

- 모든 날짜/시간은 ISO 8601 형식 (UTC)으로 제공됩니다.
- 이미지 업로드는 최대 10MB까지 지원됩니다.
- JWT 액세스 토큰의 유효기간은 24시간입니다.
- API 응답은 모두 JSON 형식으로 제공됩니다.
- 한글 인코딩은 UTF-8을 사용합니다.

## 문의사항

개발팀 연락처: contact@mola.example.com

---

**최종 업데이트**: 2024년 1월 1일
**API 버전**: v1
