import requests
from models import MarketData
from logging_config import logger

class MarketObserverAgent:
    def __init__(self, api_url: str):
        self.api_url = api_url
        logger.info(f"MarketObserverAgent initialized with API URL: {api_url}")

    def fetch_market_data(self, symbol: str) -> MarketData:
        """Fetch market data for a given symbol."""
        logger.info(f"Fetching market data for symbol: {symbol}")
        try:
            response = requests.get(f"{self.api_url}/market-data?symbol={symbol}")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            logger.info(f"Successfully fetched market data: {data}")
            return MarketData(**data)
        except Exception as e:
            logger.error(f"Failed to fetch market data: {e}")
            raise