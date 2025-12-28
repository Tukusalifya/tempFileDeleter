import os
import pathlib
import alive_progress

from src.tempfiledeleter.helpers.logger import *

from pathlib import Path
from winotify import Notification
from src.tempfiledeleter.helpers.cleaner import delete_log_files


logger = logging_config("Temp Deleter", level=logging.DEBUG)


def obtain_file_path():
    """
    Creates the Temp file directory path and counts the number of files in the directory.
    """
    delete_log_files()
    try:
        current_user_dir = Path.home()
        logger.debug(f"Current user's home directory: {current_user_dir}")

        tempfile_dir = current_user_dir / "AppData/Local/Temp"
        logger.debug(f"Temporary files directory: {tempfile_dir}")

        file_count = sum(1 for f in tempfile_dir.rglob('*') if f.is_file())
        logger.debug(f"Number of files in the temporary files directory: {file_count}")

        delete_files(tempfile_dir, file_count)

    except Exception as e:
        logger.critical(f"An unexpected error has occurred while obtaining the temp file directory path: {e}")


def delete_files(file_path: pathlib.Path, file_count: int):
    """
    Try to delete every file in the temp file directory.
    If successful the delete file count increases by one and the file size is
    added to the overall deleted temp files size.

    :param file_path: File path for temporary files
    :param file_count: Number of files in the directory
    """

    delfile_count = 0
    temp_files_size = 0

    try:
        with alive_progress.alive_bar(file_count, title="Deleting temporary files...", bar="blocks",
                                      spinner="waves") as bar:
            for path in file_path.rglob('*'):
                if path.is_file():
                    try:
                        file_size = path.stat().st_size
                        path.unlink()
                        delfile_count += 1
                        temp_files_size += file_size

                    except PermissionError as e:
                        logger.debug(f"Permission denied skipping file: {e}")
                        continue
                    except OSError as e:
                        logger.debug(f"OS error skipping file: {e}")
                        continue
                    finally:
                        bar()

                elif path.is_dir():
                    continue

        logger.info(f"Total number of files deleted: {delfile_count}/{file_count}")
        logger.info(f"Total size of deleted files: {temp_files_size / 1024 / 1024:.2f} MB\n")

        delete_empty_folders(file_path, delfile_count, file_count, temp_files_size)

    except Exception as e:
        logger.error(f"An unexpected error has occurred while executing the delete files function: {e}")


def delete_empty_folders(file_path: pathlib.Path, delfile_count: int, file_count: int, temp_files_size: float):
    """
    Try to delete every empty folder in the temp file directory.
    If successful the deleted folder count increases by one.
    Shows a toast notification after all folders are deleted with a summary of
    all deleted files(sizes included) and folders.

    :param file_path: File path for temporary files
    :param delfile_count: Number of files deleted
    :param file_count: Number of files in the directory before files and folders were deleted
    :param temp_files_size: Overall size of deleted files
    """
    dir_count = 0

    try:
        folder_count = sum(
            1 for file in file_path.rglob('*') if file.is_dir() and not any(f.is_file() for f in file.iterdir()))

        with alive_progress.alive_bar(folder_count, title="Deleting empty folders...", bar="blocks",
                                      spinner="waves") as bar:
            for path in sorted(file_path.rglob('*'), reverse=True):
                if path.is_dir() and not any(f.is_file() for f in path.iterdir()):
                    try:
                        path.rmdir()
                        dir_count += 1

                    except PermissionError as e:
                        logger.debug(f"Permission denied skipping folder: {e}")
                        continue
                    except OSError as e:
                        logger.debug(f"OS error skipping folder: {e}")
                        continue
                    finally:
                        bar()

                else:
                    continue

        logger.info(f"Total number of empty folders deleted: {dir_count}")
        # Show toast notification
        icon_path = Path(__file__).parent.parent / "assets/icons/trash.png"
        toast = Notification(app_id="TempFile Deleter",
                             title="Temporary Files Deleted Successfully",
                             msg=""
                                 f"Deleted {delfile_count}/{file_count} files ({temp_files_size / 1024 / 1024:.2f} MB) and "
                                 f"{dir_count} empty directories.",
                             icon=str(icon_path))

        toast.show()

    except Exception as e:
        logger.error(f"An unexpected error has occurred deleting empty folders: {e}")


if __name__ == "__main__":
    obtain_file_path()
