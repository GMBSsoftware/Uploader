from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from Setting import Setting
from Util import Util


class Website(ABC):
    def __init__(self, address, id, password) -> None:
        self.address = address
        self.id = id
        self.password = password
        setting = Setting()
        self.timeout = setting.timeout
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
        self.driver.set_page_load_timeout(self.timeout)
        self.util = Util()
        self.util.set_driver(self.driver)

    def login(self, id_text_locator, password_text_locator, login_btn_locator):
        """로그인"""

        # 로그인 페이지 접속
        self.driver.get(self.address)

        # 특정 요소(ID 입력 필드)가 로드될 때까지 대기
        self.util.wait_for_element(login_btn_locator)

        # id, password 입력
        self.util.wait_and_click(id_text_locator)
        self.util.input_text(self.id)
        self.util.click(password_text_locator)
        self.util.input_text(self.password)

        # 로그인 버튼 클릭
        self.util.click(login_btn_locator)

        self.util.sleep(1)

    @abstractmethod
    def handle_file(self, file):
        pass

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
