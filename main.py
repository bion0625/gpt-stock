from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import requests, json, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 실행 코드
# 기본
# python -m venv .venv
# .\.venv\Scripts\activate
# pip install -r requirements.txt
# 서버
# uvicorn main:app --reload

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

app = FastAPI()

# 가상 유저 DB
fake_user_db = {
    "bion": {
        "username": "bion",
        "full_name": "Bion User",
        "hashed_password": "$2b$12$Yb9CdA7uoJ.qOMG6p/qVVOUh8kEFVMV9T.oIyXGGfHRIQ7Dr.9pwW", # "1234"
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)

def get_user(db, username: str):
    return db.get(username)

def authenticate_user(username: str, password: str):
    user = get_user(fake_user_db, username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user(fake_user_db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return username

PORTFOLIO_FILE = "portfolio.json"

# 서버 시작 시 포트폴리오 불러오기
def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 포트폴리오 저장
def save_portfolio():
    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        json.dump(user_portfolios, f, indent=2, ensure_ascii=False)

# portfolio = load_portfolio()

class StockItem(BaseModel):
    symbol: str
    amount: int

user_portfolios = load_portfolio()

# 종목 추가
@app.post("/portfolio")
def add_stock(item: StockItem, token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    user_portfolios.setdefault(username, {})
    if item.symbol in user_portfolios[username]:
        user_portfolios[username][item.symbol] += item.amount
    else:
        user_portfolios[username][item.symbol] = item.amount
    save_portfolio()
    return {"message": "추가 완료", "portfolio": user_portfolios[username]}

# 종목 삭제
@app.delete("/portfolio/{symbol}")
def delete_stock(symbol: str, token: str = Depends(oauth2_scheme)):
    username = get_current_user(token)
    if symbol in user_portfolios[username]:
        del user_portfolios[username][symbol]
        save_portfolio()
        return {"message": f"{symbol} 삭제됨"}
    else:
        raise HTTPException(status_code=404, detail="종목이 포트폴리오에 없습니다.")

# 포트폴리오 조회
@app.get("/portfolio")
def get_portfolio(token: str = Depends(oauth2_scheme)):
    result = []
    username = get_current_user(token)
    if not user_portfolios or not user_portfolios[username]:
        return []
    for symbol, amount in user_portfolios[username].items():
        price = get_price(symbol)
        result.append({
            "symbol": symbol,
            "amount": amount,
            "price": price
        })
    return result

# 실시간 주가 크롤링 함수
def get_price(symbol: str):
    url = f"https://finance.naver.com/item/main.nhn?code={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.select_one("p.no_today span.blind")

    if tag:
        try:
            return int(tag.text.replace(",",""))
        except ValueError:
            return 0
    return 0

# 총 평가금액 조회
@app.get("/portfolio/value")
def get_total_value(token: str = Depends(oauth2_scheme)):
    total = 0
    details = []
    username = get_current_user(token)

    for symbol, amount in user_portfolios[username].items():
        price = get_price(symbol)
        total += price * amount
        details.append({
            "symbol": symbol,
            "price": price,
            "amount": amount,
            "value": price * amount
        })
    
    return {
        "total_value" : total,
        "details" : details
    }

@app.get("/")
def read_root():
    return {"message": "주식 분석 API 서버에 오신 것을 환영합니다"}

@app.get("/stocks/{symbol}")
def get_stock(symbol: str):
    url = f"https://finance.naver.com/item/main.nhn?code={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"} # 봇 차단 우회용

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return {"error": "페이지 요청 실패"}
    
    soup = BeautifulSoup(res.text, "html.parser")
    price_tag = soup.select_one("p.no_today span.blind")

    if price_tag:
        return {"symbol": symbol, "price": price_tag.text}
    else:
        return {"error": "주가 정보를 찾을 수 없습니다."}