import os
import pathlib
from datetime import datetime
from pathlib import Path
import logging


def delete_log_files():
    """
    Loops through the logs directory and checks if the creation date for the log
    files has passed 4 if so the files are deleted.
    This function ensures the log files don't pile up and take space.

    """
    try:
        logs_dir = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), f"logs"))
        os.makedirs(name=logs_dir, exist_ok=True)

        for path in logs_dir.rglob('*'):
            if path.is_file():
                try:
                    filename = path.stem

                    file_date = datetime.strptime(filename, "%d-%m-%Y")
                    today = datetime.now()
                    days_passed = (today - file_date).days

                    if days_passed > 4:
                        path.unlink()

                    else:
                        logging.log(logging.INFO, "Days passed are not greater than 4")

                except ValueError:
                    logging.log(logging.ERROR, f"Filename: {filename} is not the expected date format.")

    except Exception as e:
        logging.log(logging.ERROR, f"An unexpected error has occurred while trying to delete the log files: {e}")
