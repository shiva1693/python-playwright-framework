from utils.helpers import take_screenshot
from pages.base_page import BasePage
from config.config import BASE_URL
from playwright.sync_api import expect

class LoginPage(BasePage):

    EMAIL_INPUT = '//input[@type="email"]'
    PASSWORD_INPUT = '//input[@type="password"]'
    SIGN_IN_BUTTON = '//button[contains(@class, "primary-btn") and contains(.,"Sign In")]'
    SIGN_IN_TAB = '//div[contains(@class, "tab")]//div[@class="title" and contains(.,"Sign In")]'
    MAIN_PAGE_HEADING = 'div.breadcrumb-container > h1'

    def __init__(self, page):
        super().__init__(page)

    def navigate_to_login(self):
        self.page.goto(BASE_URL)
        self.page.wait_for_selector(self.SIGN_IN_TAB, state="visible")

    def do_login(self, username, password):
        self.click(self.SIGN_IN_TAB)
        self.type(self.EMAIL_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        with self.page.expect_navigation():
            self.click(self.SIGN_IN_BUTTON)
        return self.page.url