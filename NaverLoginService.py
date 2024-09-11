import time
import pyperclip
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class NaverLoginService:
    def __init__(self):
        self.driver = None

    def open_web_mode(self):
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
        self.driver.set_page_load_timeout(10)

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def login(self):
        self.driver.get("https://nid.naver.com/nidlogin.login")
        time.sleep(2)

        test_id = "cbs970524"
        test_passwd = "tlrksdmfdkRlwk"

        id_input = self.driver.find_element(By.ID, "id")
        id_input.click()
        pyperclip.copy(test_id)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        time.sleep(1)

        pw_input = self.driver.find_element(By.ID, "pw")
        pw_input.click()
        pyperclip.copy(test_passwd)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        time.sleep(1)

        self.driver.find_element(By.ID, "log.login").click()

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.btn_cancel"))
            )
            element.click()
        except:
            print("기기 등록 '등록안함' 버튼을 찾을 수 없습니다.")


if __name__ == "__main__":
    naver_service = NaverLoginService()
    naver_service.open_web_mode()
    naver_service.login()
    time.sleep(10)
    naver_service.close_browser()
