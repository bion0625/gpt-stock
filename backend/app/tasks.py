import asyncio
import requests

# 정기 작업 명령어 순서
# root
# cd backend
# docker-compose up -d
# .\.venv\Scripts\activate
# 창 두개 아래 각각각
# celery -A app.celery_worker.celery_app worker --loglevel=info --pool=solo
# Celery -A app.celery_worker.celery_app beat --loglevel=info

async def update_all_stocks():
    print("⏰ stating stock date update...")
    
    url = f"http://localhost:8000/collect/krx/all"
    response = requests.post(url)
    if response.status_code == 200:
        print(f"✅ 데이터 수집 성공: {response.json()}")
    else:
        print(f"❌ 데이터 수집 실패: {response.status_code} - {response.text}")
    
    url = f"http://localhost:8000/collect/all"
    response = requests.post(url)
    if response.status_code == 200:
        print(f"✅ 데이터 수집 성공: {response.json()}")
    else:
        print(f"❌ 데이터 수집 실패: {response.status_code} - {response.text}")
                    
    print(f"✅ All stock updates completed.")