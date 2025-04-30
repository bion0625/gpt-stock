from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests, json, os
from bs4 import BeautifulSoup

# 실행 코드
# 기본
#  .\.venv\Scripts\activate
# 서버버
# uvicorn main:app --reload

app = FastAPI()

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
        json.dump(portfolio, f, indent=2, ensure_ascii=False)

portfolio = load_portfolio()

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
    save_portfolio()
    return {"message": "추가 완료", "portfolio": portfolio}

# 종목 삭제
@app.delete("/portfolio/{symbol}")
def delete_stock(symbol: str):
    if symbol in portfolio:
        del portfolio[symbol]
        save_portfolio()
        return {"message": f"{symbol} 삭제됨"}
    else:
        raise HTTPException(status_code=404, detail="종목이 포트폴리오에 없습니다.")

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
def get_total_value():
    total = 0
    details = []

    for symbol, amount in portfolio.items():
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