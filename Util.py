import time, datetime, os
import pyperclip
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from Setting import Setting
from File import File


class Util:
    def __init__(self) -> None:
        self.setting = Setting()
        self.timeout = self.setting.timeout

    def set_driver(self, driver):
        self.driver = driver

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

    def sleep(self, sleep_time):
        time.sleep(sleep_time)

    def send_key(self, find_target, send_content):
        """셀레니움"""
        target = self.driver.find_element(By.ID, find_target)
        target.send_keys(send_content)

    def enter(self):
        """현재 포커스된 요소에 엔터 키 입력"""
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER).perform()

    def get_date_and_type(self):
        """오늘 날짜 기준 예배 종류 반환"""

        # 주어진 날짜의 요일을 계산 (0: 월, 1: 화, ..., 6: 일)
        date = datetime.datetime.now()
        weekday = date.weekday()

        # 해당 주에 일, 수, 금의 날짜를 구하기 위해 날짜 조정
        if weekday in [0, 1]:  # 월, 화 -> 일요일
            target_date = date - datetime.timedelta(days=weekday + 1)
            type = "주일예배"
        elif weekday in [2, 3]:  # 수, 목 -> 수요일
            target_date = date - datetime.timedelta(days=weekday - 2)
            type = "수요예배"
        elif weekday in [4, 5]:  # 금, 토 -> 금요일
            target_date = date - datetime.timedelta(days=weekday - 4)
            type = "금요기도회"
        else:  # 일요일은 그대로
            target_date = date
            type = "주일예배"

        return target_date, type

    def check_one_file(self, file_list) -> bool:
        if isinstance(file_list, list):
            if len(file_list) == 1:
                return True
        messagebox.showinfo("알림", "파일이 없거나 여러개 입니다.")
        return False

    def is_under_file_size(self, file, target_file_size) -> bool:
        if isinstance(file, File):
            if file.get_file_size() < target_file_size:
                return True

        messagebox.showinfo("알림", "파일 크기가 500MB를 초과하여 전송이 불가능합니다.")
        return False

    def rename(self, old_name, new_name):
        os.rename(old_name, new_name)

    def create_new_folder(self, folder_path, folder_name_year, folder_name_month):
        """폴더 없을 때 생성"""
        # 경로 합치기: 년도와 월 폴더 결합. 문자형 년도와 mm 형식 달
        full_path = os.path.join(
            folder_path, str(folder_name_year), f"{folder_name_month:02d}"
        )

        # 폴더 존재 여부 확인 및 생성
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)

    def check_info(self, **kwargs):
        """정보 체크하는 함수
        date(날짜), type(예배 종류), subject(주제), name(설교자)

        where => 어느 함수에서 호출했는지. 각 버튼 실행에 따라 검사해야하는 조건 상이
        """
        valid_keys = {"date", "type", "subject", "name"}  # 허용되는 키 리스트

        for key in kwargs:
            if key not in valid_keys:
                raise ValueError(f"Invalid key: {key}")

        date = kwargs.get("date", None)
        type = kwargs.get("type", None)
        subject = kwargs.get("subject", None)
        name = kwargs.get("name", None)

    def create_files(self, file_paths):
        """파일 경로 리스트를 받아서 File 객체로 만들어 file list로 반환"""
        result = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            file_path = os.path.dirname(file_path)
            file_obj = File(file_name, file_path)
            result.append(file_obj)
        return result
