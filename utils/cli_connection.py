from ultralytics import YOLO, checks, hub
import logging

logger = logging.getLogger(__name__)

def connect_to_ultralytics_cli():
    logger.info(f"Before Checks")
    checks()
    logger.info(f"After Checks and before hub login")
    hub.login("c55fb1fd4cf34f70352479ce8090c6d64c0331f0a6")
    logger.info(f"After Hub Login")
    
    model = YOLO("https://hub.ultralytics.com/models/yalmIHDr0PzIbryOj5Ay")
    logger.info(f"Before training model")
    results = model.train()
    logger.info(f"After training model")
    return results

if __name__ == "__main__":
    logger.info(f"Connecting to ultralytics method")
    connect_to_ultralytics_cli()
