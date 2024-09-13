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
        self.util.wait_and_click(
            '//*[@id="account"]/div[2]/div/div/ul/li[1]/a/span[1]'
        )  # 메일 클릭
        self.util.wait_and_click(
            '//*[@id="account"]/div[3]/div[2]/div[2]/a'
        )  # 메일쓰기 클릭
        # 대기
        # 새창으로 뜨는데 이건 괜찮나?
        self.util.click("")  #
        # 받는 사람 자동으로 클릭되는데 크롬드라이버로 열어도 그런지 확인 필요.
        self.util.input_text("뭔가 텍스트")  # 받는 사람 입력하기
        self.util.click(
            '//*[@id="content"]/div[3]/div/div[1]/div[6]/div/div[2]/div/label'
        )  # 파일 첨부
        # 여기도 위치랑 파일명 정해주고 ㅇㅋ 해주는 부분
        # 뭔가 파일 로딩 될 때까지 기다려야되나?
        self.util.click(
            '//*[@id="content"]/div[2]/div[1]/div/button[1]'
        )  # 보내기 버튼 클릭
        # 이렇게하면 끝인듯
