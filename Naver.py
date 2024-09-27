from Website import Website


class Naver(Website):
    def __init__(self, address, id, password) -> None:
        super().__init__(address, id, password)

    def login(self):
        super().login("id", "pw", "log.login")

        # 기기 등록 페이지 처리 -> 계정에서 설정 안하면 됨
        """try:
            element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.btn_cancel"))
            )
            element.click()
        except:
            print("기기 등록 '등록안함' 버튼을 찾을 수 없습니다.")"""

    def handle_file(self, **kwargs):
        """메일 전송
        file, receiver 변수 (receiver는 전송 받을 메일)
        """
        valid_keys = {"file", "receiver"}  # 허용되는 키 리스트

        for key in kwargs:
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}")

        file = kwargs.get("file", None)  # 키 'file'가 없으면 기본값 None
        receiver = kwargs.get("receiver", None)  # 키 'image'가 없으면 기본값 None

        print(receiver, " 에게 ", file, " 전송")

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
        self.util.send_key("ATTACH_LOCAL_FILE_ELEMENT_ID", str(file))  # 파일 첨부
        # 뭔가 파일 로딩 될 때까지 기다려야되나?
        self.util.wait_and_click(
            '//*[@id="content"]/div[2]/div[1]/div/button[1]'
        )  # 보내기 버튼 클릭

        result=self.util.wait_for_element(
            '//*[@id="content"]/div[2]/div/div[1]/div[2]/a[1]'
        )  # 전송 완료 후 메일 목록 버튼 뜰 시 메일 성공적 전송

        # 작업이 끝나면 원래 탭으로 돌아오기
        self.driver.close()  # 현재 탭 닫기
        self.driver.switch_to.window(original_window)  # 원래 탭으로 전환
        self.driver.close()  # 원래 탭도 닫기

        if result!=False:
            return True
        else:
            return False
