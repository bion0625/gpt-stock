from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth import get_current_user
from app.utils import get_price, load_portfolio, save_portfolio

router = APIRouter()
user_portfolios = load_portfolio()

class StockItem(BaseModel):
    symbol: str
    amount: int

# 종목 추가
@router.post("/portfolio")
def add_stock(item: StockItem, username: str = Depends(get_current_user)):
    user_portfolios.setdefault(username, {})
    if item.symbol in user_portfolios[username]:
        user_portfolios[username][item.symbol] += item.amount
    else:
        user_portfolios[username][item.symbol] = item.amount
    save_portfolio(user_portfolios)
    return {"message": "추가 완료", "portfolio": user_portfolios[username]}

# 종목 삭제
@router.delete("/portfolio/{symbol}")
def delete_stock(symbol: str, username: str = Depends(get_current_user)):
    if symbol in user_portfolios[username]:
        del user_portfolios[username][symbol]
        save_portfolio(user_portfolios)
        return {"message": f"{symbol} 삭제됨"}
    else:
        raise HTTPException(status_code=404, detail="종목이 포트폴리오에 없습니다.")

# 포트폴리오 조회
@router.get("/portfolio")
def get_portfolio(username: str = Depends(get_current_user)):
    result = []
    if not user_portfolios or not user_portfolios[username]:
        return []
    for symbol, amount in user_portfolios[username].items():
        price = get_price(symbol)
        result.append({
            "symbol": symbol,
            "amount": amount,
            "price": price
        })
    return result



# 총 평가금액 조회
@router.get("/portfolio/value")
def get_total_value(username: str = Depends(get_current_user)):
    total = 0
    details = []

    for symbol, amount in user_portfolios[username].items():
        price = get_price(symbol)
        total += price * amount
        details.append({
            "symbol": symbol,
            "price": price,
            "amount": amount,
            "value": price * amount
        })
    
    return {
        "total_value" : total,
        "details" : details
    }