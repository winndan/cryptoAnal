from market_observer import MarketObserverAgent
from strategy_planner import StrategyPlannerAgent
from execution_trader import ExecutionTraderAgent
from feedback_agent import FeedbackAgent
from logging_config import logger

def main():
    logger.info("Starting Crypto Trading System")
    try:
        # Initialize agents
        observer = MarketObserverAgent(api_url="https://api.cryptomarket.com")
        planner = StrategyPlannerAgent(api_key="your-pydantic-ai-key")
        trader = ExecutionTraderAgent()
        feedback_agent = FeedbackAgent()

        # Run the system
        symbol = "BTC"
        logger.info(f"Observing market for {symbol}...")
        market_data = observer.fetch_market_data(symbol)

        logger.info("Creating trading strategy...")
        strategy = planner.create_strategy(market_data)

        logger.info("Executing trade...")
        trade = trader.execute_trade(strategy)

        logger.info("Collecting feedback...")
        feedback = feedback_agent.collect_feedback(trade)

        logger.info(f"Feedback: {feedback}")
    except Exception as e:
        logger.error(f"System encountered an error: {e}")
    finally:
        logger.info("Crypto Trading System stopped")

if __name__ == "__main__":
    main()