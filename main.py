import os
from pathlib import Path
from winotify import Notification


# Function to obtain the temp file directory path
def obtain_file_path():
    try:
        current_user_dir = Path.home()
        print(f"Current user's home directory: {current_user_dir}")

        tempfile_dir = current_user_dir / "AppData/Local/Temp"
        print(f"Temporary files directory: {tempfile_dir}")

        file_count = sum(1 for f in tempfile_dir.rglob('*') if f.is_file())
        print(f"Number of files in the temporary files directory: {file_count}")

        delete_files(tempfile_dir)

    except Exception as e:
        print(f"An unexpected error has occurred while obtaining the temp file directory path: {e}")


# Function to delete all files in the temp file directory
def delete_files(file_path):
    tempfile_count = 0
    file_size = 0

    try:
        for path in file_path.rglob('*'):
            if path.is_file():
                try:
                    path.unlink()
                    file_size += path.stat().st_size
                    tempfile_count += 1

                except PermissionError as e:
                    print(f"Permission denied while trying to delete files. {e}")
                    continue
                except OSError as e:
                    print(f"Skipped file due to an OS error: {e}")
                    continue

            elif path.is_dir():
                continue

        print(f"Total number of files deleted: {tempfile_count}")
        print(f"Total size of deleted files: {file_size / 1024:.2f} KB")

        delete_empty_dirs(file_path, tempfile_count, file_size)

    except Exception as e:
        print(f"An unexpected error has occurred while executing the delete files function: {e}")


# Function to delete empty directories
def delete_empty_dirs(file_path, tempfile_count, file_size):
    dir_count = 0

    try:
        for path in sorted(file_path.rglob('*'), reverse=True):
            if path.is_dir() and not any(f.is_file() for f in path.iterdir()):
                try:
                    path.rmdir()
                    dir_count += 1

                except PermissionError as e:
                    print(f"Permission denied while trying to delete files. {e}")
                    continue
                except OSError as e:
                    print(f"Skipped file due to an OS error: {e}")
                    continue
            else:
                continue

        print(f"Total number of empty directories deleted: {dir_count}")

        icon_path = os.path.join(os.path.dirname(__file__), "trash.png")
        toast = Notification(app_id="TempFile Deleter",
                             title="Temporary Files Deletion Complete",
                             msg=""
                                 f"Deleted {tempfile_count} files ({file_size / 1024 / 1024:.2f} MB) and "
                                 f"{dir_count} empty directories.",
                             icon=icon_path)

        toast.show()

    except Exception as e:
        print(f"An unexpected error has occurred deleting empty directories: {e}")


if __name__ == "__main__":
    obtain_file_path()
