from Website import Website
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Naver(Website):
    def __init__(self, address, id, password) -> None:
        super().__init__(address, id, password)

    def login(self):
        super().login("id", "pw", "log.login")

        # 기기 등록 페이지 처리
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.btn_cancel"))
            )
            element.click()
        except:
            print("기기 등록 '등록안함' 버튼을 찾을 수 없습니다.")

    def handle_file(self, file):
        """메일 전송"""
        # 뜰 때까지 기다리고
        self.util.click(
            '//*[@id="account"]/div[2]/div/div/ul/li[1]/a/span[1]'
        )  # 메일 클릭
        # 뜰 때가지 대기
        self.util.click('//*[@id="account"]/div[3]/div[2]/div[2]/a')  # 메일쓰기 클릭
        # 대기
        # 새창으로 뜨는데 이건 괜찮나?
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
