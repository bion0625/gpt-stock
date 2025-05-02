from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.collect_utils import fetch_stock_data
from app.services import save_stock_data
from app.models import StockData
import app.services as services, app.schemas as schemas

router = APIRouter()

SYMBOL_LIST = {
    "AAPL",     # Apple
    "MSFT",     # Microsoft
    "005930.KQ" # 삼성전자
    # 필요시 더 추가
}

@router.get("/stocks/list", response_model=list[schemas.StockBase])
async def list_stocks(db: AsyncSession = Depends(get_db)):
    results = await services.get_all_stocks(db)
    if not results:
        raise HTTPException(status_code=404, detail="No Stocks found.")
    return results

@router.get("/stocks/search", response_model=list[schemas.StockBase])
async def search_stocks(q: str, db: AsyncSession = Depends(get_db)):
    results = await services.search_stocks(db, q)
    if not results:
        raise HTTPException(status_code=404, detail="No Stocks found.")
    return results

@router.post("/collect/all")
async def collect_all_stocks(db: AsyncSession = Depends(get_db)):
    results = []
    
    for symbol in SYMBOL_LIST:
        try:
            df = fetch_stock_data(symbol)
            await save_stock_data(symbol, df, db)
            results.append({"symbol": symbol, "status": "success", "count": len(df)})
        except Exception as e:
            results.append({"symbol": symbol, "status": "error", "error": str(e)})
    
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
        select(StockData).where(StockData.symbol == symbol)
    )
    records = result.scalars().all()
    
    if not records:
        raise HTTPException(status_code=404, detail="No data found for symbol")
    
    now = datetime.utcnow().date()
    if period == "7d":
        cutoff = now - timedelta(days=7)
    elif period == "1mo":
        cutoff = now - timedelta(days=30)
    elif period == "1y":
        cutoff = now - timedelta(days=365)
    else:
        raise HTTPException(status_code=400, detail="Invalid period parameter")
    
    records =[r for r in records if r.date >= cutoff]
    
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
        for record in records
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
        raise HTTPException(status_code=404, detail="No data found for symbol")
    
    return {
        "symbol": record.symbol,
        "date": record.date.isoformat(),
        "open": record.open,
        "high": record.high,
        "low": record.low,
        "close": record.close,
        "volume": record.volume
    }