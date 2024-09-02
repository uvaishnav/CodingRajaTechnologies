import os
import logging
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path = os.path.join("./logs", LOG_FILE)

os.makedirs(os.path.dirname(log_path), exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)