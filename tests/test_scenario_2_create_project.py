import allure
import pytest
import time
from pages.login_page import LoginPage
from pages.datasets_page import DatasetsPage
from pages.projects_page import ProjectsPage
from config.config import USERNAME, PASSWORD

@pytest.mark.order(2)
@pytest.mark.regression
# @allure.title("Create a Project and Verify It")
def test_create_project(page):
    allure.dynamic.title(f"Create a Project and Verify It")
    login_page = LoginPage(page)
    projects_page = ProjectsPage(page)
    project_name = f"auto_project_" + time.strftime("%Y%m%d-%H%M%S")
    # project_name="Test Project"
    project_description = "This is a test project description."

    login_page.navigate_to_login()
    login_page.do_login(USERNAME, PASSWORD)

    projects_page.navigate_to_projects_tab()
    projects_page.create_new_project(project_name, project_description)
    assert projects_page.is_project_created(project_name), f"Project '{project_name}' not found after creation"
