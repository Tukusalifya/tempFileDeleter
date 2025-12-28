from src.tempfiledeleter.helpers.logger import *


current_user_dir = Path.home()
logger.debug(f"Current user's home directory: {current_user_dir}")

tempfile_dir = current_user_dir / "AppData/Local/Temp"
logger.debug(f"Temporary files directory: {tempfile_dir}")

file_count = sum(1 for f in tempfile_dir.rglob('*') if f.is_file())
logger.info(f"Number of files in the temporary files directory: {file_count}")