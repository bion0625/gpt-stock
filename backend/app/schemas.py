from pydantic import BaseModel

class StockBase(BaseModel):
    name: str
    symbol: str
    market: str
    is_in_portfolio: bool
    
    class Config:
        orm_mode = True