import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, bindparam
from app.models import StockData, Stock
from app.database import async_session_maker
from typing import List
from pykrx import stock
import pandas as pd

async def get_all_stocks(db: AsyncSession):
    result = await db.execute(select(Stock))
    records = result.scalars().all()
    return records

async def search_stocks(db: AsyncSession, query: str):
    stmt = select(Stock).where(
        Stock.name.ilike(bindparam("query")) | Stock.symbol.ilike(bindparam("query")))
    result = await db.execute(stmt.params(query=f"%{query}%"))
    records = result.scalars().all()
    return records

async def load_krx_stocks():
    markets = ["KOSPI", "KOSDAQ", "ETF"]
    async with async_session_maker() as session:
        for market in markets:
            tickers = stock.get_market_ticker_list(market=market)
            for symbol in tickers:
                name = stock.get_market_ticker_name(symbol)
                result = await session.execute(
                    select(Stock).where(Stock.symbol == symbol)
                )
                existing = result.scalar_one_or_none()
                if existing:
                    continue
                
                stock_record = Stock(
                    name=name,
                    symbol=symbol,
                    market=market
                )
                
                session.add(stock_record)
            await session.commit()
        print("✅ 한국 KRX 종목 데이터 적제 완료!")
        
if __name__ == "__main__":
    asyncio.run(load_krx_stocks())
        

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