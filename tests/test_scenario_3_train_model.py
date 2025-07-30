import allure
import pytest
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.training_page import TrainingPage
from config.config import USERNAME, PASSWORD
from utils.helpers import save_training_script_from_clipboard
from test_data.model_training_data import model_training_data as data
import subprocess

def trigger_external_agent():
    filename = save_training_script_from_clipboard()
    subprocess.run(["pip", "install", "-U", "ultralytics"], check=True)
    subprocess.run(["python", filename], check=True)
    # subprocess.run(["python", "utils/cli_connection.py"], check=True)

@pytest.mark.order(3)
@pytest.mark.regression
# @allure.title("Train a Model")
def test_train_model(page):
    train_model_setup(page)

def train_model_setup(page):
    allure.dynamic.title("Train a Model")
    login_page = LoginPage(page)
    projects_page = ProjectsPage(page)
    training_page = TrainingPage(page)

    login_page.navigate_to_login()
    login_page.do_login(USERNAME, PASSWORD)

    projects_page.navigate_to_projects_tab()
    projects_page.create_new_project(data.project_name, data.project_description)
    assert projects_page.is_project_created(data.project_name), f"Project '{data.project_name}' not found"

    training_page.navigate_to_model_tab()
    training_page.click_train_model_button()
    training_page.select_dataset()
    training_page.select_project_from_dropdown_and_provide_model_name(data.project_name, data.model_name)
    training_page.set_model_config(data.model_arch, data.epoch_value)

    training_page.train_your_model()
    training_page.copy_content_from_step2()
    trigger_external_agent()
    training_page.verify_connection()
    training_page.click_on_done_button()
    assert training_page.has_training_started(), "Training did not start as expected"

    return {
        "project_name": data.project_name,
        "model_name": data.model_name,
    }
