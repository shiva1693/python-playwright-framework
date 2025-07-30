import time
import logging
from utils.helpers import take_screenshot
from playwright.sync_api import expect
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class ProjectsPage(BasePage):
    """
    Page object for the Projects section, including navigation and project creation actions.
    """

    PROJECTS_TAB = 'a[href="/projects"] > div.name.animate-slide'
    NEW_PROJECT_BUTTON = 'button#Quick-Action.primary-btn.light.quick-action'
    PROJECT_NAME_INPUT = 'input[placeholder^="Project"][type="text"]'
    PROJECT_DESCRIPTION_INPUT = 'label:has(div:has-text("Description")) input[type="text"]'
    CREATE_BUTTON = 'button.primary-btn.light:has-text("Create") >> nth=1'

    def __init__(self, page):
        """Initializes the ProjectsPage with the given Playwright page."""
        super().__init__(page)

    def navigate_to_projects_tab(self):
        """Navigates to the Projects tab and waits for the new project button to appear."""
        logger.info("Navigating to Projects tab")
        self.click(self.PROJECTS_TAB)
        self.wait_for_element(self.NEW_PROJECT_BUTTON)

    def create_new_project(self, project_name: str, project_description: str):
        """Creates a new project with the given name and description."""
        logger.info(f"Creating project: {project_name}")
        self.click(self.NEW_PROJECT_BUTTON)

        expect(self.page.locator(self.PROJECT_NAME_INPUT)).to_be_visible(timeout=5000)
        self.type(self.PROJECT_NAME_INPUT, project_name)
        self.type(self.PROJECT_DESCRIPTION_INPUT, project_description)

        self.click(self.CREATE_BUTTON)
        expect(self.page.locator(f"text={project_name}")).to_be_visible(timeout=10000)

    def is_project_created(self, project_name: str) -> bool:
        """Checks if the project with the given name is visible on the page."""
        logger.info(f"Project is created : {project_name}")
        return self.is_visible(f"text={project_name}")


    