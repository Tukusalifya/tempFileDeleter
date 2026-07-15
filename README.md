# TempFileDeleter

## Introduction / Summary

TempFileDeleter is a Windows-focused Python utility that scans the system temporary-files location and removes unnecessary temporary files to reclaim disk space. Temporary data can accumulate as applications run; this tool automates the cleanup process.

## Packages Used

TempFileDeleter requires Python **3.12 or later**.

The project declares the following dependencies:

```cmd
alive-progress>=3.3.0
rich>=14.2.0
winotify>=1.1.0
```

- `alive-progress` provides progress-display functionality.
- `rich` provides formatted console output.
- `winotify` provides Windows notification functionality.

## Installation

1. Install `uv` with `pip`:

   ```cmd
   py -m pip install uv
   ```

2. From the project directory, install the project dependencies:

   ```cmd
   cd C:\Users\YourUser\path\to\tempFileDeleter
   uv sync
   ```

3. Edit the project's `.bat` launcher so that the script path points to the location of TempFileDeleter on your machine. For example:

   ```cmd
	@echo off
	REM Navigate to your project directory
	cd /d "C:\Users\YourUser\path\to\tempFileDeleter"

	REM Activate the venv and run your main script
	call .venv\Scripts\activate
	python -m src.main %*
   ```

4. Create a dedicated Scripts folder, then copy the `.bat` launcher into it:

   ```cmd
   mkdir "%USERPROFILE%\Scripts"
   copy "C:\Users\YourUser\path\to\tempFileDeleter\script\tempdel.bat" "%USERPROFILE%\Scripts\"
   ```

5. Add the Scripts folder to the Windows `PATH` environment variable so the launcher can be used from any terminal.

   **Environment Variables dialog**

   1. Open Start, search for **Environment Variables**, and select **Edit the system environment variables**.
   2. Select **Environment Variables**.
   3. Under **User variables**, select `Path` and choose **Edit**.
   4. Select **New**, enter the following folder, then confirm the dialogs:

      ```cmd
      C:\Users\YourUser\Scripts
      ```

   **CMD alternative**

   ```cmd
   setx PATH "%PATH%;%USERPROFILE%\Scripts"
   ```

   Open a new Command Prompt after changing `PATH`.

## Usage

After adding the Scripts folder to `PATH`, run the batch launcher from any Command Prompt window:

```cmd
tempdel
```

The utility scans the Windows temporary-files location and performs its cleanup operation. The console may show formatted output and progress information; Windows notifications may also be used by the tool.

### Alternative Usage

To run TempFileDeleter automatically when Windows starts, use either Task Scheduler or the Startup folder.

**Task Scheduler**

1. Open **Task Scheduler**.
2. Select **Create Basic Task**.
3. Name the task `TempFileDeleter`.
4. Choose **When the computer starts** as the trigger.
5. Choose **Start a program** as the action.
6. Browse to and select the `.bat` launcher in your Scripts folder.
7. Complete the wizard.

**Startup folder**

1. Press `Win + R`.
2. Enter the following command:

   ```cmd
   shell:startup
   ```

3. Create a shortcut to the `.bat` launcher in the folder that opens.

The launcher will run automatically when you sign in to Windows.