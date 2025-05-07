from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio
import pytz
from types import SimpleNamespace

from app.auth import get_current_user
from app.database import get_db
from app.collect_utils import fetch_stock_data
from app.services import save_stock_data, get_symbol_with_market
from app.models import StockData, Stock
from app.utils import get_price, check_korea_market_open
import app.services as services, app.schemas as schemas

router = APIRouter()

SYMBOL_LIST = {
    "AAPL",     # Apple
    "MSFT",     # Microsoft
    "005930.KQ" # 삼성전자
    # 필요시 더 추가
}

@router.get("/stocks/list", response_model=list[schemas.StockBase])
async def list_stocks(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    stocks = await services.get_all_stocks(db)
    if not stocks:
        raise HTTPException(status_code=404, detail="No Stocks found.")
    
    return await services.make_stock_list_with_portfolio(stocks, db, user)

@router.get("/stocks/search", response_model=list[schemas.StockBase])
async def search_stocks(q: str, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    stocks = await services.search_stocks(db, q)
    if not stocks:
        raise HTTPException(status_code=404, detail="No Stocks found.")
    
    return await services.make_stock_list_with_portfolio(stocks, db, user)


@router.post("/collect/sample/all")
async def collect_sample_all_stocks(db: AsyncSession = Depends(get_db)):
    results = []
    
    for symbol in SYMBOL_LIST:
        try:
            df = fetch_stock_data(symbol)
            await save_stock_data(symbol, df, db)
            results.append({"symbol": symbol, "status": "success", "count": len(df)})
        except Exception as e:
            results.append({"symbol": symbol, "status": "error", "error": str(e)})
    
    return {"results": results}

@router.post("/collect/krx/all")
async def collect_all_stocks(db: AsyncSession = Depends(get_db)):
    await services.load_krx_stocks()
    results = await services.get_all_stocks(db)
    if not results:
        raise HTTPException(status_code=404, detail="No Stocks found.")
    return results

@router.post("/collect/all")
async def collect_all_stocks(db: AsyncSession = Depends(get_db)):
    results = []
    
    result = await db.execute(select(Stock))
    stocks = result.scalars().all()
    
    stocks_data = [{"symbol": stock.symbol, "market": stock.market} for stock in stocks]
    
    for stock in stocks_data:
        symbolWithMarket = get_symbol_with_market(stock["symbol"], stock["market"])
        try:
            df = fetch_stock_data(symbolWithMarket)
            await save_stock_data(symbolWithMarket, df, db)
            results.append({"symbol": symbolWithMarket, "status": "success", "count": len(df)})
        except Exception as e:
            results.append({"symbol": symbolWithMarket, "status": "error", "error": str(e)})
        
        await asyncio.sleep(2)
    
    return {"results": results}

@router.post("/collect/{symbol}")
async def collect_stock_data(symbol: str, db: AsyncSession = Depends(get_db)):
    try:
        df = fetch_stock_data(symbol)
        await save_stock_data(symbol, df, db)
        return {"message": f"{symbol} 데이터 수집 및 저장 완료", "count": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/{symbol}/data")
async def get_stock_data(
    symbol: str,
    period: Optional[str] = Query("7d", description="기간 선택: 7d, 1mo, 1y"),
    db: AsyncSession = Depends(get_db)
    ):
    result = await db.execute(
        select(StockData).where(StockData.symbol == symbol).order_by(StockData.date.asc())
    )
    records = result.scalars().all()

    if not records:
        raise HTTPException(status_code=404, detail="No data found for symbol")
    
    if check_korea_market_open():
        latest_price = get_price(symbol.split('.')[0])

        fake_record = SimpleNamespace(
            symbol=symbol,
            date=datetime.now(timezone.utc).date(),
            open=latest_price,
            high=latest_price,
            low=latest_price,
            close=latest_price,
            volume=0
        )

        records.append(fake_record)
    
    now = datetime.now(timezone.utc).date()
    if period == "7d":
        cutoff = now - timedelta(days=7)
    elif period == "1mo":
        cutoff = now - timedelta(days=30)
    elif period == "1y":
        cutoff = now - timedelta(days=365)
    else:
        raise HTTPException(status_code=400, detail="Invalid period parameter")
    
    filtered =[r for r in records if r.date >= cutoff]
    
    # DB 객체 -> 딕셔너리로 변환
    data = [
        {
            "date": record.date.isoformat(),
            "pen": record.open,
            "high": record.high,
            "low": record.low,
            "close": record.close,
            "volume": record.volume,
        }
        for record in filtered
    ]
    
    return {"symbol":symbol, "count": len(data), "data": data}

@router.get("/stocks/{symbol}")
async def get_latest_stock_data(symbol: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StockData)
        .where(StockData.symbol == symbol)
        .order_by(StockData.date.desc())
        .limit(1)
    )
    record = result.scalar_one_or_none()
    
    if not record:
        df = fetch_stock_data(symbol, period="1y")
        await save_stock_data(symbol, df, db)
        result = await db.execute(
            select(StockData).where(StockData.symbol == symbol).order_by(StockData.date.desc()).limit(1)
        )
        record = result.scalar_one_or_none()
        if not record:
            raise HTTPException(status_code=404, detail="No data found for symbol")
        
    if check_korea_market_open():
        # 장 중이면 naver에서 가져온 가격을 종가에 적용(최신 가격)
        record.close = get_price(symbol.split('.')[0]) # todo 장 열리고 테스트 필요
        record.date = datetime.now(pytz.timezone('Asia/Seoul')).date()
    
    return {
        "symbol": record.symbol,
        "date": record.date.isoformat(),
        # "open": record.open,
        # "high": record.high,
        # "low": record.low,
        "close": record.close,
        # "volume": record.volume
    }