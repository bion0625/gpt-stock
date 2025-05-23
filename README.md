# 📈 주식 종목 분석 웹 서비스 프로젝트

이 프로젝트는 **탑다운(top-down) 방식의 종목 분석** → **추천 전략 제공** → **사용자별 포트폴리오 관리** → **자동화·배포** → **출간용 콘텐츠 제작**까지 목표로 하는 학습·실전 프로젝트입니다.

---

## 🎯 최종 목표

- 실제 동작하는 주식 추천 서비스 완성
- Python, FastAPI, React, CI/CD, DevOps 등 전방위 실력 강화
- 출간용 콘텐츠 (책, 강의, 블로그, 노션)로 정리

---

## 📦 전체 기술 스택

| 영역        | 기술 스택                                                                                     |
|------------|---------------------------------------------------------------------------------------------|
| **백엔드** | Python, FastAPI, SQLAlchemy, PostgreSQL (SQLite → 전환), Pydantic, Alembic, Celery, Redis (비동기) |
| **프론트** | React, TypeScript, TailwindCSS, Axios, Recharts, React Query, Vite                             |
| **데이터** | pykrx, yfinance, pandas, numpy, dart-fss (예정), 업종·섹터 데이터                              |
| **인프라** | Docker, Nginx, GitHub Actions, CI/CD, Swagger/OpenAPI, Flower (비동기 모니터링)                |
| **테스트** | Pytest (백엔드), React Testing Library (프론트), Postman (통합 테스트)                          |

---

## 🏗️ 단계별 진행 상황

✅ **1단계: 프로젝트 초기 설계 및 백엔드 구축**
- FastAPI 기본 구조 (`main.py`, `routers`, `schemas`, `services`, `crud`)
- JWT 회원가입·로그인 (`/register`, `/token`)
- PostgreSQL (초기 SQLite)로 사용자·포트폴리오 데이터 관리
- Swagger UI API 문서화

✅ **2단계: 종목 데이터 수집 및 저장**
- pykrx로 한국 시장 종목 수집
- yfinance로 주요 종목 수집
- pandas 가공 후 DB 저장

✅ **3단계: 추천 API 예제 구축**
- `/recommend/{symbol}` API
- 20일 이동평균, 14일 RSI 계산
- BUY / HOLD / SELL 추천

✅ **4단계: 프론트엔드 React 개발**
- Vite + React + TypeScript
- Tailwind CSS 적용
- 포트폴리오 리스트·상세 + Recharts 차트

🟡 **5단계 (현재 진행 중): 프론트·백 고도화 및 리팩토링**
- 종목명 ↔ 심볼 매핑
- 전체 종목 리스트, 검색 API
- Axios 글로벌 에러·로딩 UX 개선
- 코드 리팩토링

✅ **6단계 (완료): UX/보안 고도화**
- 포트폴리오 추가 여부 표시
- 로그인 상태에 따라 메뉴·UX 동적 변경
- 로그아웃 기능 구현

🟣 **8단계 (앞당겨 완료): 비동기 및 주기적 데이터 갱신**
- Celery + Redis로 하루 1~2회 주기 갱신
- 실시간 상세 조회 시 장중 가격 최신화
- Flower로 비동기 작업 모니터링

🔵 **7단계 (다음 예정): 추천 기능 및 전략 고도화**
- 업종별, 수익률별, 위험도별 추천 강화
- 전략: 트레일링 스톱, 볼린저 밴드, MACD, EMA
- 추천 신뢰도·이유·시각적 설명 추가

🔒 **9단계: 데이터베이스 전환 및 마이그레이션**
- PostgreSQL 전환 (Docker or RDS)
- Alembic으로 마이그레이션 관리
- 환경변수 설정 강화

⚙ **10단계: 전략 시뮬레이션 및 자동화**
- 자동 전략 백테스트
- Celery로 과거 데이터 기반 시뮬레이션

🚀 **11단계: 배포 및 인프라 구축**
- Docker Compose로 백·프론트·DB 통합
- Nginx + HTTPS 적용
- GitHub Actions로 CI/CD 파이프라인 구축

📚 **12단계: 테스트 및 품질 관리**
- Pytest, React Testing Library, Postman 테스트
- 커버리지 관리, 코드 품질 개선

📝 **13단계: 문서화 및 출간 준비**
- Swagger API 문서 최종 정리
- GitHub Wiki, Notion 개발 노트
- 출간용 원고 (기획, 설계, 개발, 배포, 회고) 정리

---

## ✨ 현재 진행 요약

✅ **1~4단계 완료**  
🟡 **5단계 고도화 작업 진행 중**  
✅ **6단계 UX/보안 완료**  
🟣 **8단계 비동기 갱신 앞당겨 완료**  
🔜 **7단계 추천 고도화 및 9단계 이후로 확장 예정**

---

## 📌 실행·운영

- **백엔드 실행**
    ```
    cd backend
    uvicorn app.main:app --reload
    ```

- **프론트 실행**
    ```
    cd frontend
    npm install
    npm run dev
    ```

- **비동기 작업 실행**
    ```
    cd backend
    celery -A app.celery_worker.celery_app worker --loglevel=info --pool=solo
    celery -A app.celery_worker.celery_app beat --loglevel=info
    ```

- **DB 마이그레이션 (PostgreSQL 전환 후 예정)**
    ```
    alembic upgrade head
    ```
