from Website import Website


class Gm(Website):
    def __init__(self, address, id, password) -> None:
        super().__init__(address, id, password)

    def login(self):
        super().login(
            "login_form_userid",
            "login_form_password",
            '//*[@id="tab-login"]/div/div/div/div[3]/button',
        )

    def handle_file(self, file):
        """파일 업로드"""
        # 뜰 때까지 기다리고
        self.util.click('//*[@id="main-menu"]/li[2]/ul/li[3]/a')  # 컨텐츠 관리 버튼
        # 여기서 뜰 때까지 기다려야할듯
        self.util.click('//*[@id="vueapp"]/div[1]/button[1]')  # 추가 버튼
        # 여기서도 뜰 때까지 기다리기
        # self.util.click('//*[@id="menu_idx"]')                      # 메뉴 선택 버튼
        self.util.click('//*[@id="menu_idx"]/option[2]')  # 주일 예배 선택
        self.util.click("subject")  # 제목 입력 클릭
        self.util.input_text("뭔가 텍스트")  # 입력하기
        self.util.click(
            '//*[@id="vueapp"]/div/div/div/form/div[3]/div/div[2]/label/input'
        )  # 영상 종류 mp4
        self.util.click("file_01")  # 파일 선택 클릭
        # 파일 선택 창에다 주소 붙여넣어주고 이름 입력해주고 하는거
        self.util.click(
            '//*[@id="vueapp"]/div/div/div/form/div[9]/div/button[1]'
        )  # 저장 버튼
        # 대기해야하고
        # 그러고 확인하고 끝인듯?
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
        self.util.click("")  #
