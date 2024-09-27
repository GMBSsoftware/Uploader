from Website import Website
import os

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
        valid_keys = {"vedio", "image","type"}  # 허용되는 키 리스트

        for key in kwargs:
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}")

        vedio = kwargs.get("vedio", None)  # 키 'vedio'가 없으면 기본값 None
        image = kwargs.get("image", None)  # 키 'image'가 없으면 기본값 None
        type = kwargs.get("type", None)  # 키 'type'가 없으면 기본값 None

        self.util.wait_and_click('/html/body/div[1]/div[1]/div/header/div[2]/a')    # 메뉴바 열기
        self.util.wait_and_click(
            '//*[@id="main-menu"]/li[2]/ul/li[3]/a/span'
        )  # 컨텐츠 관리 버튼
        self.util.wait_and_click('//*[@id="vueapp"]/div[1]/button[1]')  # 추가 버튼
        # self.util.click('//*[@id="menu_idx"]')                      # 메뉴 선택 버튼
        
        if type=="주일예배":
            self.util.wait_and_click('//*[@id="menu_idx"]/option[2]')  # 주일 예배 선택
        elif type=="수요예배":
            self.util.wait_and_click('//*[@id="menu_idx"]/option[3]')  # 수요 예배 선택
        self.util.click("subject")  # 제목 입력 클릭

        title, extension = os.path.splitext(vedio.file_name)
        self.util.input_text(title)  # 입력하기
        self.util.click(
            '//*[@id="vueapp"]/div/div/div/form/div[3]/div/div[2]/label/input'
        )  # 영상 종류 mp4
        self.util.send_key("video_value", str(vedio))  # mp4 파일
        self.util.send_key("img_file", str(image))  # 이미지 파일
        self.util.click(
            '//*[@id="vueapp"]/div/div/div/form/div[10]/div/button[1]'
        )  # 저장 버튼

        # alert 객체로 전환
        alert = self.util.driver.switch_to.alert

        # alert 확인 (확인 버튼 클릭)
        alert.accept()

        result=self.util.wait_for_element(
            '//*[@id="btn_delete"]'
        )  # 삭제 버튼 나오면 정상 업로드 완료.
        
        self.driver.close()

        if result!=False:
            return True
        else:
            return False