import logging
from time import sleep
import allure
import pytest
from config.config import MODEL_EXPORT_URL
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.training_page import TrainingPage
from config.config import USERNAME, PASSWORD
from pages.models_page import ModelsPage
from test_data.model_training_data import model_training_data
from test_data.model_export_data import ModelExportData
from utils.helpers import take_screenshot
from tests.test_scenario_3_train_model import train_model_setup 

logger = logging.getLogger(__name__)
TEST_PAGE_NAME = "model_export_page"

@allure.step("Setup for model export test")
def export_model_setup(page):
    logger.info("Run model training before export")
    train_model_setup(page)  
    # login_page = LoginPage(page)
    # training_page= TrainingPage(page)
    # login_page.navigate_to_login()
    # login_page.do_login(USERNAME, PASSWORD)
    training_page= TrainingPage(page)
    models_page = ModelsPage(page)
    return models_page, training_page

# @pytest.mark.parametrize("export_data", [ ModelExportData(...) ])
# @pytest.mark.parametrize("export_data", [
#     ModelExportData(name="PyTorch", expect_ext=".pt"),
#     ModelExportData(name="TorchScript", expect_ext=".torchscript.pt"),
#     ModelExportData(name="ONNX", expect_ext=".onnx"),
#     ModelExportData(name="OpenVINO", expect_ext="_openvino_model.zip"),
#     ModelExportData(name="TFLite", expect_ext=".tflite"),
# ])

@pytest.mark.order(5)
@pytest.mark.functional
# @allure.title("Export YOLO11n model in all supported formats")
def test_model_export_in_all_formats(page):
    allure.dynamic.title(f"Export YOLO11n model in all formats")
    models_page = export_model_setup(page)
    models_page = ModelsPage(page)
    # login_page = LoginPage(page)
    # training_page= TrainingPage(page)
    # login_page.navigate_to_login()
    # login_page.do_login(USERNAME, PASSWORD)
    # logger.info("Step 1: Navigate to Models tab")
    # training_page.navigate_to_model_tab()
    # logger.info("Step 2: Click on the latest created trained model")
    # models_page.click_on_latest_created_model(model_training_data.model_name)

    logger.info("Step 3 Navigate to Deploy tab")
    models_page.click_deploy_tab()

    logger.info("Step 4: Scroll dowmn to the export section")
    models_page.scroll_to_export_options_section()

    logger.info("Step 5: Export model in all supported formats")
    actual_ext = models_page.export_download_extract_fileExt(model_card_name="PyTorch")
    assert actual_ext == ".pt", f"Expected .pt file, but got {actual_ext}"
    actual_ext = models_page.export_download_extract_fileExt(model_card_name="TorchScript")
    assert actual_ext == ".pt", f"Expected .onnx file, but got {actual_ext}"
    actual_ext = models_page.export_download_extract_fileExt(model_card_name="ONNX")
    assert actual_ext == ".onnx", f"Expected .onnx file, but got {actual_ext}"
    actual_ext = models_page.export_download_extract_fileExt(model_card_name="OpenVINO")
    assert actual_ext == ".zip", f"Expected .tflite file, but got {actual_ext}"
    actual_ext = models_page.export_download_extract_fileExt(model_card_name="TensorRT")
    assert actual_ext == ".engine", f"Expected .tflite file, but got {actual_ext}"


