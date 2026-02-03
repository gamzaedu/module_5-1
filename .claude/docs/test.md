# 인증 시스템 테스트 체크리스트

이 문서는 로그인 및 인증 시스템 구현에 대한 테스트 항목을 정리한 문서입니다.

---

## 🗄️ DB (Database) 테스트

### User 모델 테스트
- [ ] User 테이블이 올바르게 생성되는가?
- [ ] id 필드가 Primary Key로 설정되는가?
- [ ] username 필드에 unique 제약조건이 있는가?
- [ ] email 필드에 unique 제약조건이 있는가?
- [ ] username과 email에 인덱스가 생성되는가?
- [ ] hashed_password 필드가 255자 제한을 가지는가?
- [ ] is_active 필드의 기본값이 True인가?
- [ ] created_at이 자동으로 설정되는가?
- [ ] updated_at이 업데이트 시 자동으로 변경되는가?

### User CRUD 함수 테스트
- [ ] get_user_by_id: 존재하는 ID로 사용자를 조회할 수 있는가?
- [ ] get_user_by_id: 존재하지 않는 ID일 때 None을 반환하는가?
- [ ] get_user_by_email: 존재하는 이메일로 사용자를 조회할 수 있는가?
- [ ] get_user_by_email: 존재하지 않는 이메일일 때 None을 반환하는가?
- [ ] get_user_by_username: 존재하는 username으로 사용자를 조회할 수 있는가?
- [ ] get_user_by_username: 존재하지 않는 username일 때 None을 반환하는가?
- [ ] create_user: 새로운 사용자를 정상적으로 생성할 수 있는가?
- [ ] create_user: 생성된 사용자의 모든 필드가 올바르게 저장되는가?
- [ ] create_user: 중복된 email로 생성 시 에러가 발생하는가?
- [ ] create_user: 중복된 username으로 생성 시 에러가 발생하는가?

---

## 🔧 BE (Backend) 테스트

### 인증 유틸리티 테스트
- [ ] get_password_hash: 비밀번호가 올바르게 해싱되는가?
- [ ] get_password_hash: 같은 비밀번호를 두 번 해싱하면 다른 결과가 나오는가? (salt)
- [ ] verify_password: 올바른 비밀번호 검증 시 True를 반환하는가?
- [ ] verify_password: 잘못된 비밀번호 검증 시 False를 반환하는가?
- [ ] create_access_token: JWT 토큰이 올바르게 생성되는가?
- [ ] create_access_token: 토큰에 만료 시간이 포함되는가?
- [ ] create_access_token: 생성된 토큰을 디코딩하면 원본 데이터가 나오는가?

### 회원가입 API 테스트
- [ ] POST /api/auth/signup: 유효한 데이터로 회원가입이 성공하는가?
- [ ] POST /api/auth/signup: 응답에 사용자 정보가 포함되는가? (비밀번호 제외)
- [ ] POST /api/auth/signup: HTTP 201 상태 코드를 반환하는가?
- [ ] POST /api/auth/signup: 중복된 이메일로 요청 시 400 에러를 반환하는가?
- [ ] POST /api/auth/signup: 중복된 username으로 요청 시 400 에러를 반환하는가?
- [ ] POST /api/auth/signup: 비밀번호가 6자 미만일 때 422 에러를 반환하는가?
- [ ] POST /api/auth/signup: 잘못된 이메일 형식일 때 422 에러를 반환하는가?
- [ ] POST /api/auth/signup: 필수 필드 누락 시 422 에러를 반환하는가?

### 로그인 API 테스트
- [ ] POST /api/auth/login: 유효한 자격증명으로 로그인이 성공하는가?
- [ ] POST /api/auth/login: 응답에 access_token이 포함되는가?
- [ ] POST /api/auth/login: 응답에 token_type이 "bearer"인가?
- [ ] POST /api/auth/login: HTTP 200 상태 코드를 반환하는가?
- [ ] POST /api/auth/login: 존재하지 않는 이메일로 요청 시 401 에러를 반환하는가?
- [ ] POST /api/auth/login: 잘못된 비밀번호로 요청 시 401 에러를 반환하는가?
- [ ] POST /api/auth/login: 필수 필드 누락 시 422 에러를 반환하는가?

### 사용자 조회 API 테스트
- [ ] GET /api/auth/me: 유효한 토큰으로 현재 사용자 정보를 조회할 수 있는가?
- [ ] GET /api/auth/me: 응답에 사용자 정보가 올바르게 포함되는가?
- [ ] GET /api/auth/me: HTTP 200 상태 코드를 반환하는가?
- [ ] GET /api/auth/me: 토큰 없이 요청 시 401 에러를 반환하는가?
- [ ] GET /api/auth/me: 잘못된 토큰으로 요청 시 401 에러를 반환하는가?
- [ ] GET /api/auth/me: 만료된 토큰으로 요청 시 401 에러를 반환하는가?

### 스키마 검증 테스트
- [ ] UserCreate: 유효한 데이터를 올바르게 검증하는가?
- [ ] UserCreate: username이 3자 미만일 때 에러를 반환하는가?
- [ ] UserCreate: username이 50자 초과일 때 에러를 반환하는가?
- [ ] UserCreate: 잘못된 이메일 형식일 때 에러를 반환하는가?
- [ ] UserLogin: 유효한 데이터를 올바르게 검증하는가?
- [ ] Token: access_token과 token_type 필드를 가지는가?

---

## 🎨 FE (Frontend) 테스트

### AuthContext 테스트
- [ ] AuthContext가 초기 상태를 올바르게 설정하는가? (user: null, token: null, isLoading: true)
- [ ] localStorage에 토큰이 있을 때 자동으로 로그인하는가?
- [ ] signup 함수가 회원가입 API를 호출하는가?
- [ ] signup 성공 시 사용자 상태와 토큰이 업데이트되는가?
- [ ] login 함수가 로그인 API를 호출하는가?
- [ ] login 성공 시 사용자 상태와 토큰이 업데이트되는가?
- [ ] login 성공 시 localStorage에 토큰이 저장되는가?
- [ ] logout 함수가 사용자 상태를 초기화하는가?
- [ ] logout 시 localStorage에서 토큰이 제거되는가?
- [ ] useAuth 훅이 AuthContext 값을 올바르게 반환하는가?

### 회원가입 페이지 테스트
- [ ] 페이지가 올바르게 렌더링되는가?
- [ ] 모든 입력 필드가 표시되는가? (username, email, password, confirmPassword)
- [ ] 회원가입 버튼이 표시되는가?
- [ ] username 입력 시 상태가 업데이트되는가?
- [ ] email 입력 시 상태가 업데이트되는가?
- [ ] password 입력 시 상태가 업데이트되는가?
- [ ] confirmPassword 입력 시 상태가 업데이트되는가?
- [ ] 비밀번호가 일치하지 않을 때 에러 메시지를 표시하는가?
- [ ] 비밀번호가 6자 미만일 때 에러 메시지를 표시하는가?
- [ ] 이메일 형식이 올바르지 않을 때 에러 메시지를 표시하는가?
- [ ] 회원가입 성공 시 대시보드로 이동하는가?
- [ ] 회원가입 실패 시 에러 메시지를 표시하는가?
- [ ] 로그인 페이지 링크가 동작하는가?

### 로그인 페이지 테스트
- [ ] 페이지가 올바르게 렌더링되는가?
- [ ] 모든 입력 필드가 표시되는가? (email, password)
- [ ] 로그인 버튼이 표시되는가?
- [ ] email 입력 시 상태가 업데이트되는가?
- [ ] password 입력 시 상태가 업데이트되는가?
- [ ] 로그인 성공 시 대시보드로 이동하는가?
- [ ] 로그인 실패 시 에러 메시지를 표시하는가?
- [ ] 회원가입 페이지 링크가 동작하는가?

### 대시보드 페이지 테스트
- [ ] 페이지가 올바르게 렌더링되는가?
- [ ] 인증된 사용자의 정보가 표시되는가? (username, email)
- [ ] 로그아웃 버튼이 표시되는가?
- [ ] 로그아웃 버튼 클릭 시 로그아웃되는가?
- [ ] 로그아웃 후 홈페이지로 이동하는가?

### ProtectedRoute 컴포넌트 테스트
- [ ] 인증된 사용자일 때 children을 렌더링하는가?
- [ ] 인증되지 않은 사용자일 때 로그인 페이지로 리다이렉트하는가?
- [ ] 로딩 중일 때 로딩 스피너를 표시하는가?

### Navbar 컴포넌트 테스트
- [ ] 컴포넌트가 올바르게 렌더링되는가?
- [ ] 미인증 상태에서 "로그인", "회원가입" 링크가 표시되는가?
- [ ] 인증 상태에서 "대시보드", "로그아웃" 버튼이 표시되는가?
- [ ] 인증 상태에서 사용자 이름이 표시되는가?
- [ ] 홈 링크가 항상 표시되는가?
- [ ] 로그아웃 버튼 클릭 시 로그아웃되는가?

### 홈 페이지 테스트
- [ ] 페이지가 올바르게 렌더링되는가?
- [ ] 미인증 상태에서 로그인/회원가입 링크가 표시되는가?
- [ ] 인증 상태에서 환영 메시지가 표시되는가?
- [ ] 인증 상태에서 사용자 이름이 표시되는가?

---

## 🔄 통합 테스트 (E2E)

### 회원가입 플로우
- [ ] 회원가입 페이지에서 정보 입력 후 제출할 수 있는가?
- [ ] 회원가입 후 자동으로 로그인되는가?
- [ ] 회원가입 후 대시보드로 이동하는가?
- [ ] 중복된 이메일로 회원가입 시 에러 메시지가 표시되는가?

### 로그인 플로우
- [ ] 로그인 페이지에서 자격증명 입력 후 로그인할 수 있는가?
- [ ] 로그인 후 대시보드로 이동하는가?
- [ ] localStorage에 토큰이 저장되는가?
- [ ] 잘못된 자격증명으로 로그인 시 에러 메시지가 표시되는가?

### 보호된 라우트 플로우
- [ ] 미인증 상태에서 대시보드 접근 시 로그인 페이지로 리다이렉트되는가?
- [ ] 인증 후 대시보드에 접근할 수 있는가?

### 토큰 영속성 플로우
- [ ] 로그인 후 페이지 새로고침 시 로그인 상태가 유지되는가?
- [ ] 브라우저를 닫았다 열어도 로그인 상태가 유지되는가? (localStorage 토큰이 유효한 경우)

### 로그아웃 플로우
- [ ] 로그아웃 버튼 클릭 시 로그아웃되는가?
- [ ] 로그아웃 후 localStorage에서 토큰이 제거되는가?
- [ ] 로그아웃 후 보호된 페이지에 접근할 수 없는가?

---

## 📊 테스트 실행 방법

### Backend 테스트
```bash
cd backend
pytest test/ -v
```

### Frontend 테스트
```bash
cd frontend
npm test
```

### Database 테스트
```bash
cd backend
pytest db/test/ -v
```

---

## 📝 테스트 커버리지 목표

- **Backend**: 80% 이상
- **Frontend**: 70% 이상
- **Database**: 90% 이상

---

## 🔍 테스트 우선순위

### P0 (필수)
- User 모델 생성 및 제약조건
- CRUD 함수 (create_user, get_user_by_email)
- 회원가입 API (성공/이메일 중복)
- 로그인 API (성공/실패)
- JWT 토큰 생성/검증
- AuthContext (login, logout, signup)
- ProtectedRoute (인증 체크)

### P1 (중요)
- 비밀번호 해싱/검증
- 사용자 조회 API
- 회원가입 페이지 (유효성 검증)
- 로그인 페이지
- 대시보드 페이지

### P2 (선택)
- 스키마 검증 세부사항
- Navbar 컴포넌트
- 홈 페이지
- E2E 통합 테스트
