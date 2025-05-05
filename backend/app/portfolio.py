from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.auth import get_current_user
from app.models import Portfolio, Stock
from app.utils import get_price
from app.database import async_session_maker, get_db

router = APIRouter()

class StockItem(BaseModel):
    symbol: str
    amount: int

# 종목 추가
@router.post("/portfolio")
async def add_stock(
    item: StockItem, 
    user = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
    ):
    
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id, Portfolio.symbol == item.symbol)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.amount += item.amount
    else:
        new = Portfolio(symbol=item.symbol, amount=item.amount, user_id=user.id)
        db.add(new)
    
    await db.commit()
    return {"message": "추가 완료"}

# 종목 삭제
@router.delete("/portfolio/{symbol}")
async def delete_stock(
    symbol: str, 
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id, Portfolio.symbol == symbol)
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="해당 종목이 없습니다.")
    
    await db.delete(target)
    await db.commit()
    return {"message": f"{symbol} 삭제 완료"}

# 포트폴리오 조회
@router.get("/portfolio")
async def get_portfolio(
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id)
    )
    items = result.scalars().all()
    
    portfolio_data = []
    for item in items:
        stock_result = await db.execute(select(Stock).where(Stock.symbol == item.symbol.split('.')[0]))
        stock = stock_result.scalar_one_or_none()
        price = get_price(stock.symbol)
        portfolio_data.append({
            "symbol": item.symbol,
            "amount": item.amount,
            "name": stock.name,
            "price": price
        })
    
    return portfolio_data

@router.get("/portfolio/{symbol}")
async def get_stock_detail(
    symbol: str, 
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id, Portfolio.symbol == symbol)
    )
    portfolio_item = result.scalar_one_or_none()
    if not portfolio_item:
        raise HTTPException(status_code=404, detail="해당 종목이 없습니다.")
    
    return {
        "symbol": portfolio_item.symbol,
        "amount": portfolio_item.amount,
    }


# 총 평가금액 조회
@router.get("/portfolio/value")
async def get_total_value(
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id)
    )
    items = result.scalars().all()

    total = 0
    details = []

    for item in items:
        price = get_price(item.symbol)
        value = price * item.amount
        total += value
        details.append({
            "symbol": item.symbol,
            "price": price,
            "amount": item.amount,
            "value": value
        })
    
    return {
        "total_value" : total,
        "details" : details
    }