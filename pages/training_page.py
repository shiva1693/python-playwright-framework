import time
import logging
from playwright.sync_api import expect
from pages.base_page import BasePage
from utils.helpers import take_screenshot

logger = logging.getLogger(__name__)

class TrainingPage(BasePage):

    MODEL_TAB ='li#Models a[href="/models"]'
    TRAIN_MODEL_BUTTON = "//button[@id='Quick-Action' and .//div[contains(text(),'Train Model')]]"
    DATASET_SEARCHBAR = "(//input[@type='text' and @placeholder='Search' and contains(@class, 'search')])[2]"
    MODEL_TYPE_SELECTOR = "//p[text()='COCO8']//ancestor::div[@class='content-wrapper']"
    CONTINUE_BUTTON = "//div[text()=' Continue']//ancestor::button[@class='primary-btn light']"
    PROJECT_DROPDOWN_TRIGGER = "//div[text()='Project']//ancestor::label//child::div[@class='select']"
    PROJECT_OPTION_LOCATOR_TEMPLATE ="//li[normalize-space()='{project_name}']"
    MODEL_NAME="//div[text()='Model name']//following-sibling::input"
    MODEL_ARCHITECTURE="(//p[text()='{model_arch}'])[2]"
    ADV_MODEL_CONFIG_TEXT="//p[normalize-space(text())='Advanced Model Configuration']"
    EPOCHS_INPUT="//p[normalize-space(.)='Epochs']/following::input[@type='number'][1]"
    IMAGE_SIZE="//p[normalize-space(.)='Image size']/following::input[@type='number'][1]"
    BRING_OWN_AGENT="//p[normalize-space(.)='Bring your own agent']"
    CONNECTED_TEXT="//p[normalize-space(.)='Connected']"
    DONE_BUTTON="//button[.//div[normalize-space(text())='Done']]"
    STEP2_COPY_TEXT="//div[contains(@class, 'wrapper multiline')]//pre//code"
    TRAIN_TAB="//p[normalize-space(.)='Train']"
    CONFIGURATION_TAB="//p[normalize-space(.)='Configuration']"
    CHARTS_TAB="//p[normalize-space(.)='Charts']"
    PREVIEW_TAB="//p[normalize-space(.)='Preview']"
    DEPLOY_TAB="//p[normalize-space(.)='Deploy']"

    def __init__(self, page):
        super().__init__(page)

    def navigate_to_model_tab(self):
        logger.info("Navigating to Model tab")
        self.click(self.MODEL_TAB)

    def click_train_model_button(self):
        logger.info("Clicking on Train Model button")
        self.click(self.TRAIN_MODEL_BUTTON)

    def select_dataset(self, dataset_name: str = "coco8"):
        logger.info(f"Selecting dataset: {dataset_name}")
        self.wait_for_element(self.DATASET_SEARCHBAR)
        self.type(self.DATASET_SEARCHBAR, dataset_name)
        self.click(self.MODEL_TYPE_SELECTOR)
        self.click(self.CONTINUE_BUTTON)
        # time.sleep(10)  

    def select_project_from_dropdown_and_provide_model_name(self, project_name: str, model_name: str):
        logger.info(f"Selecting project from dropdown: {project_name}")
        self.click(self.PROJECT_DROPDOWN_TRIGGER)
        project_locator = self.PROJECT_OPTION_LOCATOR_TEMPLATE.format(project_name=project_name)
        self.wait_for_element(project_locator)
        self.click(project_locator)
        self.type(self.MODEL_NAME,model_name)
    
    def set_model_config(self, model_arch : str = "YOLO11n", epochs: str = "5"):
        logger.info(f"Setting Model Configuratuions")
        model_arch = self.MODEL_ARCHITECTURE.format(model_arch=model_arch)
        self.wait_for_element(model_arch)
        self.click(model_arch)
        self.click(self.ADV_MODEL_CONFIG_TEXT)
        self.clear_and_fill_input(self.EPOCHS_INPUT, epochs)  
        self.click(self.IMAGE_SIZE)
        self.click(self.CONTINUE_BUTTON)
        # time.sleep(10)  

    def train_your_model(self):
        logger.info("Training your model")
        self.click(self.BRING_OWN_AGENT)

    def copy_content_from_step2(self):
        self.page.click(self.STEP2_COPY_TEXT)
        logger.info("Content copied from Step 2.")
          
    def verify_connection(self, timeout: int = 10):
        logger.info("Verifying if connection is established (i.e., 'Connected' message appears)")
        # time.sleep(20)
        try:
            locator = self.page.locator(self.CONNECTED_TEXT)
            expect(locator).to_be_visible(timeout=timeout)
            logger.info("'Connected' text is visible – connection established successfully.")
        except Exception as e:
            logger.error(f"Connection verification failed. 'Connected' text not visible within {timeout}ms.")
            raise AssertionError("Expected 'Connected' status not visible on the page.") from e

        logger.info("Clicking on the 'Done' button to finish the training step.")
        
    def click_on_done_button(self):
        logger.info("Clicking on the 'Done' button")
        self.wait_for_element(self.DONE_BUTTON)
        self.click(self.DONE_BUTTON)
        # time.sleep(15)

    def has_training_started(self):
        logger.info("Verifying if training has started")
        # time.sleep(10)
        return self.is_visible(self.TRAIN_TAB)
     
    