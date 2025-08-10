import logging
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fix_client import fix_client

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()

@app.on_event("startup")
def startup_event():
    """Connect to FIX server on startup."""
    try:
        fix_client.connect()
    except Exception as e:
        logger.error(f"FIX connection error: {e}")

@app.on_event("shutdown")
def shutdown_event():
    """Disconnect from FIX server on shutdown."""
    fix_client.disconnect()

# Market Data Request
@app.get("/market_data/{symbol}")
def get_market_data(symbol: str):
    """Fetch market data for a given symbol."""
    try:
        response = fix_client.send_market_data_request(symbol)
        return {"symbol": symbol, "data": response}
    except Exception as e:
        return {"error": str(e)}

# Status Check
@app.get("/status")
def get_status():
    """Check if FIX connection is alive."""
    return {"status": "connected" if fix_client.is_connected() else "disconnected"}

# Order Model
class OrderRequest(BaseModel):
    symbol: str
    side: str  # "buy" or "sell"
    quantity: int
    price: float
    order_type: str  # "market" or "limit"

# Place Order
@app.post("/place_order/")
def place_order(order: OrderRequest):
    """Place a trade order."""
    try:
        order_id = fix_client.send_new_order(
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            price=order.price,
            order_type=order.order_type
        )
        return {"status": "Order placed", "order_id": order_id}
    except Exception as e:
        return {"error": str(e)}

# WebSocket for real-time market data
@app.websocket("/ws/market_data/{symbol}")
async def market_data_stream(websocket: WebSocket, symbol: str):
    """WebSocket for live market data updates."""
    await websocket.accept()
    while True:
        try:
            data = fix_client.send_market_data_request(symbol)
            await websocket.send_json({"symbol": symbol, "data": data})
        except Exception as e:
            await websocket.send_json({"error": str(e)})
            break


# import logging
# from fastapi import FastAPI, WebSocket
# from pydantic import BaseModel
# from fix_client import pricing_client, trading_client

# # Logger setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # FastAPI app
# app = FastAPI()

# @app.on_event("startup")
# def startup_event():
#     """Connect to FIX servers on startup."""
#     try:
#         pricing_client.connect()
#         trading_client.connect()
#     except Exception as e:
#         logger.error(f"FIX connection error: {e}")

# @app.on_event("shutdown")
# def shutdown_event():
#     """Disconnect from FIX servers on shutdown."""
#     pricing_client.disconnect()
#     trading_client.disconnect()

# # Market Data Request
# @app.get("/market_data/{symbol}")
# def get_market_data(symbol: str):
#     """Fetch market data for a given symbol."""
#     return pricing_client.send_market_data_request(symbol)

# # Status Check
# @app.get("/status")
# def get_status():
#     """Check if FIX connections are alive."""
#     return {
#         "pricing_status": "connected" if pricing_client.is_connected() else "disconnected",
#         "trading_status": "connected" if trading_client.is_connected() else "disconnected"
#     }

# # Order Model
# class OrderRequest(BaseModel):
#     symbol: str
#     side: str
#     quantity: int
#     price: float
#     order_type: str

# # Place Order
# @app.post("/place_order/")
# def place_order(order: OrderRequest):
#     return trading_client.send_new_order(order.symbol, order.side, order.quantity, order.price, order.order_type)
