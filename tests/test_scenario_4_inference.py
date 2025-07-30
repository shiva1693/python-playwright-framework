# Verify model inference functionality with confidence threshold adjustment.

import allure
import pytest
import logging
from pages.login_page import LoginPage
from pages.models_page import ModelsPage
from utils.helpers import take_screenshot
from config.config import USERNAME, PASSWORD, YOLO11_URL
from test_data.model_interence_data import ModelInferenceData

TEST_PAGE_NAME = "model_inference_page"
logger = logging.getLogger(__name__)

@pytest.mark.order(4)
@pytest.mark.functional
@pytest.mark.parametrize("data", [ ModelInferenceData() ])
# @allure.title("Test Inference on YOLO11n Model")
def test_model_inference(page,data: ModelInferenceData):
    allure.dynamic.title(f"Test Inference on YOLO11n Model")
    login_page = LoginPage(page)
    models_page = ModelsPage(page)
     
    try:
        logger.info("Login to Ultralytics Hub")
        login_page.navigate_to_login()
        login_page.do_login(USERNAME, PASSWORD)

        logger.info("Navigate to YOLO11n model page")
        models_page.navigate_to_url(YOLO11_URL)
        models_page.open_model_preview()

        logger.info("Upload image for inference")
        #### models_page.upload_image_for_inference(data.github_image_url)
        models_page.upload_image_for_inference()

        logger.info(f"Verify these objects are detected: {data.expected_objects}")
        try:
            assert models_page.are_expected_objects_visible(data.expected_objects), f"Expected objects {data.expected_objects} not detected"
        except AssertionError as assertion_error:
            take_screenshot(page, TEST_PAGE_NAME, "initial_detection_failed")
            raise assertion_error
        
        logger.info(f"Adjust confidence threshold to {data.confidence_threshold}")
        models_page.adjust_confidence_threshold(data.confidence_threshold)
        
        logger.info(f"Verify objects after threshold adjustment: {data.expected_objects_after_adjustment}")
        try:
            assert models_page.are_expected_objects_visible(data.expected_objects_after_adjustment), \
                f"Expected objects {data.expected_objects_after_adjustment} not visible after threshold adjustment"
        except AssertionError as assertion_error:
            take_screenshot(page, TEST_PAGE_NAME, f"threshold_{data.confidence_threshold}_failed")
            raise assertion_error
        
        logger.info("Test Scenario 4 passed successfully")
        
    except Exception as e:
        logger.exception(f"Unexpected error in test scenario 4: {e}")
        take_screenshot(page, TEST_PAGE_NAME, "unexpected_error")
        raise
    