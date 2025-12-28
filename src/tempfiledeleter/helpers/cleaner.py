import logging

from pathlib import Path
from datetime import datetime

from src.tempfiledeleter.helpers.logger import logging_config

logger = logging_config("Cleaner", level=logging.DEBUG)


def delete_log_files():
    """
    Loops through the logs directory and checks if the creation date for the log
    files has passed 4 if so the files are deleted.
    This function ensures the log files don't pile up and take space.

    """
    try:
        logs_dir = Path(__file__).parent / "logs"
        logs_dir.mkdir(exist_ok=True)

        for path in logs_dir.rglob('*'):
            if path.is_file():
                try:
                    filename = path.stem

                    file_date = datetime.strptime(filename, "%d-%m-%Y")
                    today = datetime.now()
                    days_passed = abs((today - file_date).days)

                    if days_passed >= 4:
                        path.unlink()

                    else:
                        logger.debug("Days passed are not greater than 4")

                except ValueError:
                    logger.error(f"Filename: {filename} is not the expected date format.")

    except Exception as e:
        logging.critical(f"An unexpected error has occurred while trying to delete the log files: {e}")
