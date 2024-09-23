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

    def handle_file(self, **kwargs):
        """파일 업로드
        vedio, image 변수
        """
        valid_keys = {"vedio", "image"}  # 허용되는 키 리스트

        for key in kwargs:
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}")

        vedio = kwargs.get("vedio", None)  # 키 'vedio'가 없으면 기본값 None
        image = kwargs.get("image", None)  # 키 'image'가 없으면 기본값 None

        self.util.wait_and_click(
            '//*[@id="main-menu"]/li[2]/ul/li[3]/a'
        )  # 컨텐츠 관리 버튼
        self.util.wait_and_click('//*[@id="vueapp"]/div[1]/button[1]')  # 추가 버튼
        # self.util.click('//*[@id="menu_idx"]')                      # 메뉴 선택 버튼
        self.util.wait_and_click('//*[@id="menu_idx"]/option[2]')  # 주일 예배 선택
        self.util.click("subject")  # 제목 입력 클릭
        self.util.input_text("뭔가 텍스트")  # 입력하기
        self.util.click(
            '//*[@id="vueapp"]/div/div/div/form/div[3]/div/div[2]/label/input'
        )  # 영상 종류 mp4
        self.util.send_key("video_value", vedio)  # mp4 파일
        self.util.send_key("img_file", image)  # 이미지 파일
        self.util.click(
            '//*[@id="vueapp"]/div/div/div/form/div[9]/div/button[1]'
        )  # 저장 버튼

        # 대기를 얼마나 하지?
        self.util.sleep(60)
