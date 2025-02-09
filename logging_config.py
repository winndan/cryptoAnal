import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to console
        logging.FileHandler("crypto_trading_system.log"),  # Log to file
    ],
)

# Create a logger for the system
logger = logging.getLogger("CryptoTraderSystem")