import logging
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, page):
        self.page = page

    def click(self, selector: str, timeout: int = 5000):
        logger.info(f"Clicking element: {selector}")
        self.wait_for_element(selector, timeout)
        self.page.locator(selector).click()

    def type(self, selector: str, text: str):
        logger.info(f"Typing in element: {selector} -> '{text}'")
        self.page.locator(selector).fill(text)

    def wait_for_element(self, selector, timeout=5000):
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
        except Exception as e:
            self.page.screenshot(path="element_wait_failed.png")
            raise AssertionError(f"Element not found: {selector}") from e
    
    def get_text(self, selector: str) -> str:
        text = self.page.locator(selector).inner_text()
        logger.info(f"Text from element {selector}: {text}")
        return text

    def is_visible(self, selector: str) -> bool:
        visible = self.page.locator(selector).is_visible()
        logger.info(f"Element {selector} visibility: {visible}")
        return visible
    
    def scroll_to_element(self, selector: str, timeout: int = 100):
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            self.page.locator(selector).scroll_into_view_if_needed()
            logger.info(f"Scrolled to element: {selector}")
        except Exception as e:
            logger.error(f"Failed to scroll to element: {selector}. Error: {e}")
            raise

    def clear_and_fill_input(self, selector: str, value: str, timeout: int = 5000):
        try:
            input_field = self.page.locator(selector)
            logger.info(f"Attempting to clear and fill input: {selector} with value: {value}")
            input_field.wait_for(state="visible", timeout=timeout)
            input_field.click()
            input_field.press("Control+A")
            input_field.press("Backspace")
            input_field.fill(value)
            input_field.press("Enter")
            logger.info(f"Successfully filled input: {selector} with value: {value} and pressed Enter")
        
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while waiting for input field: {selector}")
            raise

        except Exception as e:
            logger.exception(f"Failed to clear and fill input field: {selector} due to error: {e}")
            raise

    def navigate_to_url(self, url: str, wait_for_element: str = None, timeout: int = 10000):
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)

        if wait_for_element:
            logger.info(f"Waiting for element: {wait_for_element}")
            self.wait_for_element(wait_for_element, timeout=timeout)


    def download_file_and_verify_extension(self, download_button_selector: str, expected_extension: str):
        with self.page.expect_download() as download_info:
            self.page.click(download_button_selector)
        download = download_info.value
        path = download.path()
        filename = download.suggested_filename

        logger.info(f"Downloaded file: {filename}")
        assert filename.endswith(expected_extension), f"Expected file to end with {expected_extension}, got {filename}"


    # def set_slider_value_to(self, selector: str, value: float)
    #     try:
    #         slider = self.page.locator(selector).element_handle()
    #         if not slider:
    #             raise Exception("Slider element not found.")

    #         self.page.evaluate(
    #             """([el, val]) => {
    #                 el.value = val.toFixed(2); 
    #                 el.dispatchEvent(new Event('input', { bubbles: true }));
    #                 el.dispatchEvent(new Event('change', { bubbles: true }));
    #             }""",
    #             [slider, value]
    #         )
    #         actual_val = self.page.evaluate("el => el.value", slider)
    #         logger.info(f"Slider set to: {actual_val} (target: {value})")
    #     except PlaywrightTimeoutError:
    #         logger.error(f"Timeout after waiting for slider: {selector}")
    #         raise
    #     except Exception as e:
    #         logger.error(f"Failed to set slider value for {selector}. Error: {str(e)}")
    #         raise
    
    
    def set_slider_value_to(self, slider_locator: str, percent: float):
        try:
            slider = self.page.locator(slider_locator)

            if not slider.is_visible():
                raise Exception(f"Slider not visible for locator: {slider_locator}")

            box = slider.bounding_box()
            if not box:
                raise Exception(f"Unable to get bounding box for slider: {slider_locator}. It may not be attached to the DOM.")

            slider_element = slider.element_handle()

            min_val = float(self.page.evaluate("el => parseFloat(el.min)", slider_element))
            max_val = float(self.page.evaluate("el => parseFloat(el.max)", slider_element))
            step_val = float(self.page.evaluate("el => parseFloat(el.step || 0.01)", slider_element))

            target_val = min_val + percent * (max_val - min_val)

            steps_total = round((max_val - min_val) / step_val)
            steps_to_target = round((target_val - min_val) / step_val)
            px_per_step = box["width"] / steps_total
            x_offset = px_per_step * steps_to_target
            y_offset = box["height"] / 2

            self.page.mouse.move(box["x"] + 1, box["y"] + y_offset)
            self.page.mouse.down()
            self.page.mouse.move(box["x"] + x_offset, box["y"] + y_offset)
            self.page.mouse.up()

            logger.info(f"Slider dragged exactly to value: {target_val:.2f} (requested {percent * 100:.0f}%)")

        except Exception as e:
            logger.error(f"Failed to drag slider to {percent * 100:.0f}%: {str(e)}")
            raise


    def check_expected_texts_visible(self, containers_locator, text_xpath: str, expected_texts: list[str]) -> bool:
        try:
            containers_locator.first.wait_for(timeout=5000)
            detected = set()

            count = containers_locator.count()
            for i in range(count):
                card = containers_locator.nth(i)
                if card.is_visible():
                    name_elements = card.locator(f"xpath={text_xpath}")
                    for j in range(name_elements.count()):
                        name = name_elements.nth(j).inner_text().strip().lower()
                        detected.add(name)

            expected_set = set(text.lower() for text in expected_texts)
            missing = expected_set - detected

            if missing:
                logger.warning(f"Missing expected objects: {missing}")
                logger.warning(f"Detected: {detected}")
                return False

            logger.info(f"All expected objects visible: {expected_texts}")
            return True

        except Exception as e:
            logger.error(f"Error in visibility check: {e}")
            return False
