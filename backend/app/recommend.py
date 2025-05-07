from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import StockData
from app.utils import compute_rsi
from app.utils import check_korea_market_open, get_price
import pandas as pd
from types import SimpleNamespace
from datetime import datetime, timezone

router = APIRouter()

@router.get("/recommend/{symbol}")
async def recommand_stock(symbol: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StockData).where(StockData.symbol == symbol)
    )
    records = result.scalars().all()
    
    if not records:
        raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")
    
    # 데이터프레임으로 변환
    df = pd.DataFrame([{
        "date": r.date,
        "close": r.close
    } for r in records])

    if check_korea_market_open():
        latest_price = get_price(symbol.split('.')[0])

        new_row = pd.DataFrame([{
            "date": datetime.now(timezone.utc).date(),
            "close": latest_price
        }])

        df = pd.concat([df, new_row], ignore_index=True)

    df.sort_values("date", inplace=True)
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["rsi14"] = compute_rsi(df["close"], 14)
    
    current_price = df["close"].iloc[-1]
    moving_average_20 = df["ma20"].iloc[-1]
    rsi_14 = df["rsi14"].iloc[-1]
    
    # 간단한 추천 로직 예제
    if current_price > moving_average_20 and rsi_14 < 70:
        recommandation = "BUY"
        reason = "현재 가격이 20일 이동평균선을 상향 돌파했습니다."
    elif rsi_14 > 70:
        recommandation = "SELL"
        reason = "RSI가 과매수 영역에 진입했습니다."
    else:
        recommandation = "HOLD"
        reason = "특별한 매수/매도 신호가 없습니다."
    
    return {
        "symbol": symbol,
        "recommandation": recommandation,
        "reason": reason,
        "details": {
            "current_price": current_price,
            "moving_average_20": moving_average_20,
            "rsi_14": rsi_14
        }
    }