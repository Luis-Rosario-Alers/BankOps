import logging.config
import os
import sys
from datetime import datetime


def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_filename = f"logs/BankOps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_filename),
        ],
    )


setup_logging()
logger = logging.getLogger("main")


def main():
    pass


if __name__ == "__main__":
    main()
