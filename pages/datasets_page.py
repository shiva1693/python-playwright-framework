import os
import time

from pages.base_page import BasePage
from playwright.sync_api import expect
from playwright.sync_api import Page
import logging
logger = logging.getLogger(__name__)

class DatasetsPage(BasePage):

    DATASETS_TAB = 'a[href="/datasets"] > div.name.animate-slide'
    UPLOAD_BUTTON = 'button#Quick-Action'
    DATASET_NAME_INPUT = 'input[type="text"][placeholder^="Dataset"]'
    FILE_INPUT = 'div.drop-zone input[type="file"]'
    DATASET_ENTRY = 'text=firstDataset'
    CREATE_BUTTON = 'button.primary-btn.light:has-text("Create")'
     # UPLOAD_FILE_RECORD = 'div.dataset-details p.name:has-text("firstDataset")'
    DELETE_DATA_OPTION = 'ul.options li'
    UPLOADED_DATASET_LABEL = 'div.dataset-details p.name'

    def __init__(self, page):
        super().__init__(page)
        self.fName = "firstDataset_" + time.strftime("%Y%m%d-%H%M%S")
        self.TARGET_3_DOTS = f'div.dataset-details:has(p:has-text("{self.fName}"))'


    def navigate_to_datasets_tab(self):
        self.click(self.DATASETS_TAB)
        self.wait_for_element(self.UPLOAD_BUTTON)

    def upload_dataset(self, file_path):
        self.click(self.UPLOAD_BUTTON)
        self.type(self.DATASET_NAME_INPUT, self.fName)
        absolute_path = os.path.abspath(file_path)
        self.page.wait_for_selector(self.FILE_INPUT, timeout=5000, state="attached")
        self.page.set_input_files(self.FILE_INPUT, absolute_path)
        self.click(self.CREATE_BUTTON)
        logger.info(f"Dataset '{self.fName}' in the process of uploading...")

    def validate_success_upload(self):
        self.page.wait_for_timeout(10000) 
        self.page.wait_for_selector(self.UPLOADED_DATASET_LABEL, timeout=10000, state="visible")
        assert self.page.locator(self.UPLOADED_DATASET_LABEL, has_text=self.fName).is_visible(), "Dataset upload failed"
        logger.info(f"Dataset '{self.fName}' uploaded successfully.")

    # def deleteDataset(self):
    #     # self.click(self.threeDots)
    #     self.page.locator(target_dataset_locator).locator('xpath=../../..').locator('div.dropdown .icon-button').click()
    #     self.page.locator(self.deleteData).filter(has_text="Delete").first.click()
    #     # self.click(self.deleteData)
    #     # logger.info(f"Dataset '{self.fName}' deleted successfully.")
    #     time.sleep(15)  
