# TODO List

## Feature: 로그인/인증 시스템

### DB 작업

- [ ] User 테이블 모델 생성
  - [ ] 사용자 기본 정보 필드 (id, username, email)
  - [ ] 비밀번호 해싱 필드 (hashed_password)
  - [ ] 타임스탬프 필드 (created_at, updated_at)
  - [ ] 활성화 상태 필드 (is_active)

- [ ] User CRUD 함수 생성
  - [ ] 사용자 생성 함수 (create_user)
  - [ ] 이메일로 사용자 조회 함수 (get_user_by_email)
  - [ ] username으로 사용자 조회 함수 (get_user_by_username)
  - [ ] ID로 사용자 조회 함수 (get_user_by_id)

### BE 작업

- [ ] 인증 관련 Pydantic 스키마 생성
  - [ ] UserCreate (회원가입 요청)
  - [ ] UserLogin (로그인 요청)
  - [ ] UserResponse (사용자 정보 응답)
  - [ ] Token (JWT 토큰 응답)

- [ ] 인증 유틸리티 함수 구현
  - [ ] 비밀번호 해싱 함수
  - [ ] 비밀번호 검증 함수
  - [ ] JWT 토큰 생성 함수
  - [ ] JWT 토큰 검증 함수
  - [ ] 현재 사용자 가져오기 의존성

- [ ] 인증 API 엔드포인트 생성
  - [ ] POST /api/auth/signup (회원가입)
  - [ ] POST /api/auth/login (로그인)
  - [ ] GET /api/auth/me (현재 사용자 조회)
  - [ ] POST /api/auth/logout (로그아웃 - 선택사항)

### FE 작업

- [ ] 회원가입 페이지 구현
  - [ ] 회원가입 폼 컴포넌트 (username, email, password)
  - [ ] 폼 유효성 검증
  - [ ] 회원가입 API 호출 함수
  - [ ] 에러 처리 및 사용자 피드백

- [ ] 로그인 페이지 구현
  - [ ] 로그인 폼 컴포넌트 (email/username, password)
  - [ ] 폼 유효성 검증
  - [ ] 로그인 API 호출 함수
  - [ ] 에러 처리 및 사용자 피드백

- [ ] 인증 상태 관리
  - [ ] 토큰 저장 (localStorage/cookie)
  - [ ] 인증 상태 Context/Store 구현
  - [ ] 자동 로그인 (토큰 유효성 확인)
  - [ ] 로그아웃 기능

- [ ] 보호된 라우트 구현
  - [ ] 인증 체크 미들웨어/컴포넌트
  - [ ] 미인증 시 로그인 페이지 리다이렉트
  - [ ] 네비게이션 바에 로그인 상태 표시

---

## 작업 순서 (권장)

1. **DB 작업** (db-agent)
   - User 모델 및 CRUD 함수 생성

2. **BE 작업** (be-agent)
   - 스키마 및 유틸리티 함수 구현
   - API 엔드포인트 생성

3. **FE 작업** (fe-agent)
   - 회원가입/로그인 페이지 구현
   - 인증 상태 관리 및 보호된 라우트 구현
