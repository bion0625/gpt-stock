from fastapi import FastAPI
from pydantic import BaseModel
import requests 
from bs4 import BeautifulSoup

# 실행 코드
# 기본
#  .\.venv\Scripts\activate
# 서버버
# uvicorn main:app --reload

app = FastAPI()

portfolio = {}

class StockItem(BaseModel):
    symbol: str
    amount: int

# 종목 추가
@app.post("/portfolio")
def add_stock(item: StockItem):
    if item.symbol in portfolio:
        portfolio[item.symbol] += item.amount
    else:
        portfolio[item.symbol] = item.amount
    return {"message": "추가 완료", "portfolio": portfolio}

# 실시간 주가 크롤링 함수
def get_price(symbol: str):
    url = f"https://finance.naver.com/item/main.nhn?code={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.select_one("p.no_today span.blind")
    return tag.text if tag else "조회 불가"

# 포트폴리오 조회
@app.get("/portfolio")
def get_portfolio():
    result = []
    for symbol, amount in portfolio.items():
        price = get_price(symbol)
        result.append({
            "symbol": symbol,
            "amount": amount,
            "price": price
        })
    return result

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