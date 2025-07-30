import os
import shutil
import pytest
from utils.helpers import take_screenshot, attach_video_to_allure

# folders for storing videos and screenshots
VIDEO_DIR = "videos"
SCREENSHOT_DIR = "screenshots"


def pytest_sessionstart(scope="session"):
    for folder in [VIDEO_DIR, SCREENSHOT_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

# @pytest.fixture(scope="session")
# def browser():
#     from playwright.sync_api import sync_playwright
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)  # show browser while running
#         yield browser
#         browser.close()

# this runs for each test and sets up a new page with video recording
@pytest.fixture(scope="function")
def page(browser, request):
    context = browser.new_context(record_video_dir=VIDEO_DIR)
    page = context.new_page()
    yield page 
    test_name = request.node.name  # get test name for file naming
    # if the test failed, take a screenshot and attach it to the report
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        take_screenshot(page, test_page_name="models_page", step_name=test_name)
    # attach the video for this test (whether it passed or failed)
    attach_video_to_allure(page, name=f"{test_name}_video")
    context.close()  # important to close so video gets saved


@pytest.fixture(scope="session")
def browser_context_args():
    download_path = "downloads/model_export"
    os.makedirs(download_path, exist_ok=True)
    print(f"[Playwright] Download path set to: {os.path.abspath(download_path)}")
    return {
        "accept_downloads": True,
        "downloads_path": os.path.abspath(download_path),
        "viewport": None
    }