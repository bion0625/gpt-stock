import requests, json, os
from bs4 import BeautifulSoup

PORTFOLIO_FILE = "portfolio.json"

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

# 서버 시작 시 포트폴리오 불러오기
def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 포트폴리오 저장
def save_portfolio(portfolio: dict):
    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        json.dump(portfolio, f, indent=2, ensure_ascii=False)