from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.collect_utils import fetch_stock_data
from app.services import save_stock_data

router = APIRouter()

@router.post("/collect/{symbol}")
async def collect_stock_data(symbol: str, db: AsyncSession = Depends(get_db)):
    try:
        df = fetch_stock_data(symbol)
        await save_stock_data(symbol, df, db)
        return {"message": f"{symbol} 데이터 수집 및 저장 완료", "count": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))