import os
from pages.base_page import BasePage
from utils.helpers import download_image, take_screenshot, save_download_and_get_extension_from_download,create_folder_if_not_exists


from playwright.sync_api import expect
import logging
import time

logger = logging.getLogger(__name__)
TEST_PAGE_NAME = "models_page"

class ModelsPage(BasePage):

    MODEL_TYPE = '//p[normalize-space(.)="YOLO11n"]//ancestor::div[@class="model-wrapper"]' 
    PREVIEW_TAB = '//p[normalize-space(.)="Preview"]//ancestor::div[@class="title"]'
    UPLOAD_INPUT = "input[type='file']"
    CONFIDENCE_SLIDER = 'input[type="range"]'
    CONFIDENCE_THRESHOLD_SLIDER="//div[contains(@class, 'option')]//div[text()='Confidence Threshold']/following-sibling::div//input[@type='range']"
    INFERENCE_SECTION_XPATH = "//h3[text()='Inference results']/ancestor::div[contains(@class, 'section')]"
    OBJECT_CONTAINER_XPATH = ".//div[contains(@class, 'option')]"
    OBJECT_TEXT_XPATH = ".//div[contains(@class, 'name')]"
    CUSTOM_MODEL_CLICKABLE = "//p[@title='Model name' and text()='{model_name}']"
    DEPLOY_TAB="//p[normalize-space(.)='Deploy']"
    EXPORT_SECTION="//h2[contains(@class, 'card-title') and normalize-space(text())='Export']"
    EXPORT_TEXT = "//div[contains(@class, 'export-item-wrapper') and .//div[@class='name' and normalize-space(.)='{model_card_name}']]//span[@class='text' and normalize-space(.)='Export']"
    DOWNLOAD_TEXT = "//div[contains(@class, 'export-item-wrapper') and .//div[@class='name' and contains(normalize-space(.), '{model_card_name}')]]//span[contains(@class, 'text') and contains(normalize-space(.), 'Download')]"
    LATEST_CREATED_MODEL="(//p[@title='Model name' and text()='{model_name}'])[1]"


    def __init__(self, page):
        super().__init__(page)

    def open_model_preview(self):  
        logger.info("Opening YOLO11n model preview")
        self.click(self.MODEL_TYPE)
        self.click(self.PREVIEW_TAB)
        # self.wait_for_element(self.upload_input)

    # def upload_image_for_inference(self, github_image_url):
    #     # image_path = download_image(github_image_url, filename="inference.jpg")
    #     # absolute_path = os.path.abspath(image_path)
    #     logger.info(f"Uploading image for inference: {absolute_path}")
    #     self.page.wait_for_selector(self.UPLOAD_INPUT, timeout=10000, state="attached")
    #     self.page.locator(self.UPLOAD_INPUT).set_input_files(image_path)
    #     time.sleep(100)

    def upload_image_for_inference(self):
        logger.info("Uploading the Image for Inference")
        rel_path="/test_data/inference.jpg"
        image_path = os.getcwd() + os.path.realpath(rel_path)
        logger.info(f"Uploading image for inference: {image_path}")
        self.page.wait_for_selector(self.UPLOAD_INPUT, timeout=10000, state="attached")
        self.page.locator(self.UPLOAD_INPUT).set_input_files(image_path)

    def is_object_detected(self, object_name):
        logger.info(f"Checking if '{object_name}' is getting detected")
       
    def are_expected_objects_visible(self, expected_objects: list[str]) -> bool:
        section = self.page.locator(f"xpath={self.INFERENCE_SECTION_XPATH}")
        containers = section.locator(f"xpath={self.OBJECT_CONTAINER_XPATH}")
        return self.check_expected_texts_visible(containers, self.OBJECT_TEXT_XPATH, expected_objects)
        
    def adjust_confidence_threshold(self, percent):
        # logger.info(f"Adjusting confidence threshold to: {threshold}")
        # self.set_slider_value_to(self.CONFIDENCE_THRESHOLD_SLIDER, threshold)
        # logger.info("Confidence threshold set successfully.")
        # time.sleep(1000)
        logger.info(f"Adjusting confidence threshold to: {percent}")
        self.set_slider_value_to(self.CONFIDENCE_THRESHOLD_SLIDER, percent)
        logger.info("Confidence threshold set successfully.")
    
    def is_object_detected(self, object_label):
        logger.info(f"Checking if object '{object_label}' was detected")
        return self.is_visible(f"text={object_label}")
    
    def click_on_latest_created_model(self, model_name):
        logger.info(f"Clicking on the latest created model: {model_name}")
        self.click(self.CUSTOM_MODEL_CLICKABLE.format(model_name=model_name))
        logger.info("Model clicked successfully.")
    
    def click_deploy_tab(self):
        logger.info("Clicking on the Deploy tab")
        self.wait_for_element(self.DEPLOY_TAB)
        # self.page.locator(self.DEPLOY_TAB).scroll_into_view_if_needed()
        self.click(self.DEPLOY_TAB)
        logger.info("Deploy tab clicked successfully.")
    
    def scroll_to_export_options_section(self):
        logger.info("Scrolling to the export options section")
        self.scroll_to_element(self.EXPORT_SECTION)
        logger.info("Scrolled to the export options section")
    
    def export_download_extract_fileExt(self, model_card_name: str):     
        try:
            logger.info(f"Starting export for model format: {model_card_name}")

            export_xpath = self.EXPORT_TEXT.format(model_card_name=model_card_name)
            download_xpath = self.DOWNLOAD_TEXT.format(model_card_name=model_card_name)

            if model_card_name != "PyTorch":
                logger.info(f"Clicking Export for: {model_card_name}")
                self.page.locator(export_xpath).click()

                logger.info(f"Waiting for Download button for: {model_card_name}")
                self.page.locator(download_xpath).wait_for(state="visible", timeout=600_000)

            else:
                logger.info(f"Model {model_card_name} does not require export. Proceeding directly.")
            self.page.wait_for_timeout(1000)  

            
            with self.page.expect_download(timeout=120_000) as download_info:
                logger.info(f"Clicking Download for: {model_card_name}")
                button = self.page.locator(download_xpath)
                button.wait_for(state="visible", timeout=10000)  
                button.click()

            download = download_info.value
            logger.info(f"Downloaded file for model: {model_card_name}")

            return save_download_and_get_extension_from_download(download, folder="downloads/model_export")

        except Exception as e:
            logger.error(f"Failed during export/download for '{model_card_name}': {e}")
            raise

    # def click_on_latest_created_model(self, model_name):
    #     logger.info(f"Clicking on the latest created model: {model_name}")
    #     selector = self.LATEST_CREATED_MODEL.format(model_name=model_name)
    #     self.click(selector)
    #     logger.info("Latest created model clicked successfully.")