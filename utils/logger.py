import logging
import os

def setup_logger():
    os.makedirs("reports", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("reports/test_execution.log"),
            logging.StreamHandler()
        ]
    )