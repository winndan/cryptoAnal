from pydantic import BaseModel
from typing import Optional

# Market data model
class MarketData(BaseModel):
    timestamp: str
    symbol: str
    price: float
    volume: float
    market_cap: Optional[float] = None

# Trading strategy model
class TradingStrategy(BaseModel):
    strategy_id: str
    symbol: str
    action: str  # Buy, Sell, Hold
    quantity: float
    target_price: float
    stop_loss: Optional[float] = None

# Trade execution model
class TradeExecution(BaseModel):
    trade_id: str
    strategy_id: str
    symbol: str
    action: str
    quantity: float
    executed_price: float
    timestamp: str

# Feedback model
class Feedback(BaseModel):
    trade_id: str
    success: bool
    profit_loss: float
    feedback: str