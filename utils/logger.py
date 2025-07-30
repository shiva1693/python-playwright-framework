import logging
import os

def setup_logger():
    """
    Sets up logging configuration with both file and console output.
    Logs are saved to 'reports/test_execution.log', and the 'reports' folder is created if it doesn't exist.
    Log messages include timestamp, log level, and the message content.
    """
    os.makedirs("reports", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("reports/test_execution.log"),
            logging.StreamHandler()
        ]
    )