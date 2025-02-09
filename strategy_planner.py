from pydantic_ai import PydanticAI
from models import MarketData, TradingStrategy
from logging_config import logger

class StrategyPlannerAgent:
    def __init__(self, api_key: str):
        self.ai = PydanticAI(api_key=api_key)
        logger.info("StrategyPlannerAgent initialized")

    def create_strategy(self, market_data: MarketData) -> TradingStrategy:
        """Create a trading strategy using Pydantic AI."""
        logger.info("Creating trading strategy...")
        try:
            prompt = f"""
            Analyze the following market data and create a trading strategy:
            {market_data.json()}
            """
            strategy = self.ai.generate(
                prompt=prompt,
                output_model=TradingStrategy,
                system_prompt="You are a crypto trading strategist.",
            )
            logger.info(f"Successfully created strategy: {strategy}")
            return strategy
        except Exception as e:
            logger.error(f"Failed to create strategy: {e}")
            raise