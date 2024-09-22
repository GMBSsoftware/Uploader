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

    def handle_file(self, **kwargs):
        """메일 전송
        vedio, receiver 변수 (receiver는 전송 받을 메일)
        """

        valid_keys = {'vedio', 'receiver'}  # 허용되는 키 리스트

        for key in kwargs:
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}")

        vedio = kwargs.get('vedio', None)  # 키 'vedio'가 없으면 기본값 None
        receiver = kwargs.get('receiver', None)  # 키 'image'가 없으면 기본값 None


        self.util.wait_and_click(
            '//*[@id="account"]/div[2]/div/div/ul/li[1]/a/span[1]'
        )  # 메일 클릭
        self.util.wait_and_click(
            '//*[@id="account"]/div[3]/div[2]/div[2]/a'
        )  # 메일쓰기 클릭
        # 대기

        # 현재 탭의 핸들을 저장
        original_window = self.driver.current_window_handle
        
        # 새 탭에서 작업 진행
        for handle in self.driver.window_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                break

        self.util.click('//*[@id="recipient_input_element"]')  # 받는 사람 선택
        self.util.input_text(receiver)  # 받는 사람 입력하기
        self.util.click(
            '//*[@id="content"]/div[3]/div/div[1]/div[6]/div/div[2]/div/label'
        )  # 파일 첨부
        self.util.sleep(1)
        self.util.input_text(vedio)  # 영상 파일 경로 입력
        self.util.enter()
        # 뭔가 파일 로딩 될 때까지 기다려야되나?
        self.util.click(
            '//*[@id="content"]/div[2]/div[1]/div/button[1]'
        )  # 보내기 버튼 클릭

        # 작업이 끝나면 원래 탭으로 돌아오기
        self.driver.close()  # 현재 탭 닫기
        self.driver.switch_to.window(original_window)  # 원래 탭으로 전환
        self.driver.close() # 원래 탭도 닫기