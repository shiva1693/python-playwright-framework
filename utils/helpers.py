import os
import shutil
import time
import allure
import requests
import logging
import pyperclip

logger = logging.getLogger(__name__)

def download_image(github_url: str, download_dir: str = "test_data", filename: str = "sample.jpg"):
    """Downloads an image from a GitHub URL and saves it to the specified directory."""

    os.makedirs(download_dir, exist_ok=True)
    save_path = os.path.join(download_dir, filename)

    response = requests.get(github_url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
    else:
        raise Exception(f"Failed to download image: {response.status_code} - {github_url}")

def save_training_script_from_clipboard(file_path="model_scripts/train_model_script.py"):
    """Saves a YOLO training script from the clipboard to a file if it looks valid."""
    script_content = pyperclip.paste()
    if "from ultralytics" in script_content and "YOLO" in script_content:
        with open(file_path, "w") as f:
            f.write(script_content)
        return file_path
    else:
        raise ValueError("Copied content does not appear to be a valid training script.")

def take_screenshot(page, test_page_name: str, step_name: str, folder: str = "screenshots"):
    """Takes a screenshot of the page, saves it with a timestamp, and attaches it to Allure reports."""
    os.makedirs(folder, exist_ok=True)
    timestamp = int(time.time())
    filename = f"{folder}/{test_page_name}_{step_name}_{timestamp}.png"
    logger.info(f"Capturing screenshot: {filename}")
    page.screenshot(path=filename)

    with open(filename, "rb") as f:
        allure.attach(f.read(), name=f"{test_page_name}_{step_name}", attachment_type=allure.attachment_type.PNG)

def attach_video_to_allure(playwright_page, name="Test Video"):
    """Attaches the recorded video from a Playwright test to the Allure report."""
    try:   
        video_path = playwright_page.video.path()
        if os.path.exists(video_path):
            allure.attach.file(
                video_path,
                name=name,
                attachment_type=allure.attachment_type.MP4
            )
    except Exception as e:
        print(f"Failed to attach video: {e}")

def create_folder_if_not_exists(folder_path: str):
    """Creates a folder if it doesn't exist, otherwise prints that it already exists."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


def save_download_and_get_extension_from_download(download, folder: str = "downloads/model_export") -> str:
    """
    Saves the given download to the specified folder, ensures the file is fully written and valid.
    Verifies that the file exists and is not empty before proceeding.
    Returns the file extension (Ex., '.zip', '.pt') of the saved download.
    Raises an exception if the file is missing, empty, or if any error occurs during the process.
    """
    import os
    import time

    try:
        os.makedirs(folder, exist_ok=True)
        clear_directory(folder)

        filename = download.suggested_filename
        file_path = os.path.join(folder, filename)

        download.save_as(file_path)
        logger.info(f"Download complete and saved to: {file_path}")

        # Ensures OS writes file fully
        for _ in range(10):
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                break
            time.sleep(1)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Download file not found at: {file_path}")
        if os.path.getsize(file_path) == 0:
            raise IOError(f"Downloaded file is empty: {file_path}")

        return os.path.splitext(file_path)[-1]

    except Exception as e:
        logger.error(f"Failed to save or get file extension: {e}")
        raise

def clear_directory(path: str):
    """
    Clears all files from the specified directory.If the directory does not exist, it is created.
    Raises a RuntimeError if any file deletion or directory creation fails.
    """
    try:
        if os.path.exists(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(path)
    except Exception as e:
        raise RuntimeError(f"Failed to clear directory '{path}': {e}")
