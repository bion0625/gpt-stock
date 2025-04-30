import requests, json, os
from bs4 import BeautifulSoup

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