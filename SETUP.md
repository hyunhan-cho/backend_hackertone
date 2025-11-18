# 🚀 백엔드 프로젝트 세팅 가이드

## 1. `.env` 파일 만들기

`.env.template` 파일을 `.env`로 복사해서 사용하세요:

```bash
cd modelproject
cp .env.template .env
```

**또는 직접 만들기:**

`modelproject/.env` 파일을 생성하고 아래 내용을 붙여넣으세요:

```env
# Django 시크릿 키 (개발용)
SECRET_KEY=dev-secret-key-change-me-in-production-abc123xyz

# --- Supabase 전용 DB 설정 ---
# 이 프로젝트 전용 새 Supabase DB (절대 운영 DB 아님)
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=chanjoon1221!
SUPABASE_DB_HOST=db.epaezvnftiuiedehgkfe.supabase.co
SUPABASE_DB_PORT=5432

# --- 선택: 카카오/Gemini API (나중에 필요시 채우기) ---
# KAKAO_REST_API_KEY=
# GEMINI_API_KEY=
```

---

## 2. 의존성 설치

Python 3.13 이상 환경에서:

```bash
cd modelproject
pip install -r requirements.txt
```

또는 `uv`를 사용한다면:

```bash
uv sync
```

---

## 3. 데이터베이스 마이그레이션 (새 Supabase DB에만 적용)

⚠️ **절대 기존 운영 DB에는 영향 없습니다.** `SUPABASE_DB_*` 정보로만 연결됩니다.

```bash
cd modelproject
python manage.py migrate --settings=modelproject.supabase_settings
```

---

## 4. 개발 서버 실행

```bash
cd modelproject
python manage.py runserver 0.0.0.0:8000 --settings=modelproject.supabase_settings
```

서버가 뜨면 http://127.0.0.1:8000 에서 확인할 수 있습니다.

---

## 5. (선택) 관리자 계정 만들기

```bash
cd modelproject
python manage.py createsuperuser --settings=modelproject.supabase_settings
```

이후 http://127.0.0.1:8000/admin 에서 로그인 가능합니다.

---

## 6. API 문서 확인

서버가 실행 중일 때:

- Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/
- ReDoc: http://127.0.0.1:8000/api/schema/redoc/
- OpenAPI JSON: http://127.0.0.1:8000/api/schema/

---

## 📝 주요 설정 파일

- `modelproject/supabase_settings.py`: Supabase PostgreSQL 전용 설정
- `modelproject/local_settings.py`: 로컬 개발용 SQLite 설정
- `modelproject/deploy_settings.py`: 배포용 MySQL 설정 (S3 제거됨)
- `.env`: 환경변수 (SECRET_KEY, DB 접속 정보 등)

---

## 🗄️ 데이터 초기화

### 법정동 주소 데이터

`modelproject/data/locations.json`에 전국 시/군/구/동 주소 목록이 이미 있습니다.

### 가게(Place) 데이터 넣기

가게 정보를 CSV로 준비한 뒤 Django shell에서 로드할 수 있습니다:

```bash
python manage.py shell --settings=modelproject.supabase_settings
```

```python
import csv
from django.utils.dateparse import parse_time
from couponbook.models import LegalDistrict, Place

with open("places.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        district = LegalDistrict.objects.get(
            province=row["province"],
            city=row["city"],
            district=row["district"],
        )
        Place.objects.create(
            name=row["name"],
            address_district=district,
            address_rest=row["address_rest"],
            image_url=row["image_url"],
            opens_at=parse_time(row["opens_at"]),
            closes_at=parse_time(row["closes_at"]),
            last_order=parse_time(row["last_order"]),
            tel=row["tel"],
            tags=row.get("tags", ""),
        )
```

---

## ⚠️ 주의사항

1. `.env` 파일은 **절대 Git에 커밋하지 마세요** (이미 `.gitignore`에 포함)
2. `supabase_settings.py`는 `SUPABASE_DB_*` 키만 읽으므로, 기존 운영 DB와 완전히 분리됩니다
3. 프로덕션 배포 시에는 `SECRET_KEY`를 반드시 새로 생성하세요

