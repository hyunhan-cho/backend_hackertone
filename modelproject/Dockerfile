FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # uv가 만든 .venv를 기본 PATH에 등록
    PATH="/app/.venv/bin:$PATH" \
    # 기본 settings를 Supabase로 설정 (필요 시 배포 환경에서 덮어쓰기 가능)
    DJANGO_SETTINGS_MODULE=modelproject.supabase_settings

WORKDIR /app

# 시스템 패키지
# - build-essential/gcc: C 확장 빌드
# - pkg-config: mysqlclient 빌드 시 라이브러리/헤더 탐색 (필수!)
# - default-libmysqlclient-dev: MySQL/MariaDB 클라이언트 개발 헤더
#   (MariaDB를 직접 쓰면 libmariadb-dev로 교체 가능)
# - curl/ca-certificates: 일반 유틸
# - vim: 선택(편의)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc pkg-config default-libmysqlclient-dev \
    curl ca-certificates vim \
 && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN python -m pip install --upgrade pip && pip install uv

# 의존성만 먼저 복사 → 레이어 캐시 극대화 (uv는 pyproject.toml/uv.lock 사용)
COPY pyproject.toml uv.lock* ./

# 프로덕션 의존성만 동기화(가상환경 .venv 생성)
# --frozen: uv.lock과 불일치 시 실패 → 재현 가능한 빌드
RUN uv sync --no-dev --extra prod --frozen

# 앱 소스 복사
COPY . .

WORKDIR /app

ENV PYTHONPATH=/app

# Cloudtype는 동적 포트($PORT)를 할당하므로 이를 바인드
# 컨테이너 시작 시 DB 마이그레이션 및 정적 파일 수집까지 수행
CMD ["/bin/sh", "-c", \
    "SUPABASE_DB_PORT=\${SUPABASE_DB_PORT_MIGRATE:-\${SUPABASE_DB_PORT}} python manage.py migrate --noinput && \
     python manage.py collectstatic --noinput && \
     gunicorn --chdir /app --bind 0.0.0.0:${PORT:-8000} modelproject.wsgi:application"]