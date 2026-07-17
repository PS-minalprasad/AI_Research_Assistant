import logging
import os

from utils.constants import LOG_FOLDER

os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(LOG_FOLDER, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)