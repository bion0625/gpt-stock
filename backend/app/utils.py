import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, time, timezone

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

def check_korea_market_open():
    # 한국 증시는 보통 평일 오전 9시 ~ 오후 3시 30분
    korea_tz = timezone.utc # 단순 utc로 비교, 추후 pytz를 통한 Asia/Seoul로 할지 고민
    now = datetime.now(korea_tz)
    
    weekday = now.weekday()
    if weekday >= 5:
        return False
    
    market_open_time = time(0, 0) # UTC 기준: 한국 9시 = 0시
    market_close_time = time(6, 30) # UTC 기준: 한국 3:30 = 6:30
    
    return market_open_time <= now.time() <= market_close_time

def compute_rsi(series: pd.Series, period: int = 14):
    delta =series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi