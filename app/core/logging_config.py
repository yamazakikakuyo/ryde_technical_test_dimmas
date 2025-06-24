import logging

# Basic logger config
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbosity
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.logs"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ryde_api")