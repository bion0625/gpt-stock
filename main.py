from fastapi import FastAPI
import requests 
from bs4 import BeautifulSoup

app = FastAPI()

# MOCK_DATA = {
#     "005930":{"symbol":"005930", "name":"삼성전자", "price": 75200},
#     "000660":{"symbol":"000660", "name":"SK하이닉스", "price": 136500}
# }

@app.get("/")
def read_root():
    return {"message": "주식 분석 API 서버에 오신 것을 환영합니다"}

@app.get("/stocks/{symbol}")
def get_stock(symbol: str):
    # stock = MOCK_DATA.get(symbol)
    # if stock:
    #     return stock
    # else:
    #     return {"error": "해당 종목이 없습니다."}
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