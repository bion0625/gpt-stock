from pydantic import BaseModel

class StockBase(BaseModel):
    name: str
    symbol: str
    market: str
    
    class Config:
        orm_mode = True