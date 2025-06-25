import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Ensure the logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Basic logger config
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbosity
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ryde_api")