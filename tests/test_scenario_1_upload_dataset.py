import allure
import pytest
from pages.login_page import LoginPage
from pages.datasets_page import DatasetsPage
from config.config import USERNAME, PASSWORD,BASE_URL


@pytest.mark.order(1)
@pytest.mark.smoke
# @allure.title("Upload Dataset")
def test_upload_dataset(page):
    allure.dynamic.title("Upload Dataset")
    loginPage = LoginPage(page)
    datasetsPage = DatasetsPage(page)

    loginPage.navigate_to_login()
    loginPage.do_login(USERNAME, PASSWORD)
    page.wait_for_url(f"{BASE_URL}/home", timeout=10000)
    assert page.url == f"{BASE_URL}/home", "Login failed, URL mismatch after login."

    datasetsPage.navigate_to_datasets_tab()
    datasetsPage.upload_dataset("test_data/coco8.zip")
    datasetsPage.validate_success_upload()
    # datasetsPage.delete_dataset() 