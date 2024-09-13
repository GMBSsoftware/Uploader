import time
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from Setting import Setting


class Util:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.setting = Setting()
        self.timeout = self.setting.timeout

    def click(self, locator):
        # XPath로 시작하는 경우는 // 혹은 /로 구분
        if locator.startswith("/") or locator.startswith("//"):
            target = self.driver.find_element(By.XPATH, locator)
        else:
            target = self.driver.find_element(By.ID, locator)

        target.click()
        time.sleep(self.setting.sleep_time)

    def input_text(self, text):
        pyperclip.copy(text)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        time.sleep(self.setting.sleep_time)

    def wait_for_element(self, locator):
        """ID 또는 XPath로 타임아웃 내 반복적으로 요소를 찾음"""

        def locate_element(driver):
            try:
                # ID로 찾기 시도
                return driver.find_element(By.ID, locator)
            except:
                try:
                    # XPath로 찾기 시도
                    return driver.find_element(By.XPATH, locator)
                except:
                    return False  # 아직도 찾을 수 없으면 False 반환

        try:
            # 타임아웃 내에서 ID와 XPath 반복적으로 시도
            return WebDriverWait(self.driver, self.timeout).until(locate_element)
        except TimeoutException:
            print(
                f"Element with ID or XPath '{locator}' could not be found within {self.timeout} seconds."
            )
            return None

    def wait_and_click(self, locator):
        self.wait_for_element(locator)
        self.click(locator)
