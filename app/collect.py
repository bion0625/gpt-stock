from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.collect_utils import fetch_stock_data
from app.services import save_stock_data

router = APIRouter()

SYMBOL_LIST = {
    "AAPL",     # Apple
    "MSFT",     # Microsoft
    "005930.KQ" # 삼성전자
    # 필요시 더 추가
}

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