import logging
import datetime as dt
import os

today = dt.datetime.today()
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"logs")
os.makedirs(name=logs_dir, exist_ok=True)

logs_path = os.path.join(logs_dir, f"{today.day:02d}-{today.month:02d}-{today.year}.log")

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("TEMPFILE_DELETER")

file_handler = logging.FileHandler(logs_path)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
