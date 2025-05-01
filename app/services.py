from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import StockData
from typing import List
import pandas as pd

async def save_stock_data(symbol: str, df: pd.DataFrame, db: AsyncSession):
    """
    DataFrame 데이터를 StockData 테이블에 저장한다.
    동일한 (symbol, date) 데이터는 덮어쓰지 않는다.

    Args:
        symbol (str): 종목코드
        df (pd.DataFrame): yfinance에서 수집한 데이터프레임
        db (AsyncSession): 비동기 db 세션
    """
    
    for _, row in df.iterrows():
        # symbole, date 존재 여부 확인
        result = await db.execute(
            select(StockData).where(
                StockData.symbol == symbol,
                StockData.date == row['date'].date()
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            continue # 이미 있으면 스킵
        
        # 새 레코드 생성
        stock_record = StockData(
            symbol=symbol,
            date=row['date'].date(),
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume']
        )
        db.add(stock_record)
        
    await db.commit()