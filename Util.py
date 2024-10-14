import time, datetime, os, shutil, ctypes, pyperclip, threading
import tkinter as tk
from tkinter import ttk
from ctypes import wintypes
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

    def check_count_file(self, file_list, target_num) -> bool:
        """파일이 몇 개인지 체크"""
        if isinstance(file_list, list):
            if len(file_list) == target_num:
                return True
        messagebox.showinfo(
            "알림",
            f"{target_num}개의 파일만 넣어주세요.\n\n실행 버튼 : (파일 크기 작은 순) 1. 메일 전송 2. 홈페이지 업로드 3. 나스 이동\n\n하단 개별 기능 버튼 : 1개 파일.",
        )
        return False

    def is_under_file_size(self, file, target_file_size) -> bool:
        if isinstance(file, File):
            if file.get_file_size() < target_file_size:
                return True
        return False

    def rename(self, path, old_name, new_name):
        # old_name에서 확장자 추출
        _, extension = os.path.splitext(old_name)

        # new_name에 확장자를 추가
        new_name_with_extension = new_name + extension

        # 파일 이름 변경
        os.rename(
            os.path.join(path, old_name), os.path.join(path, new_name_with_extension)
        )
        return os.path.join(path, new_name_with_extension)

    def create_new_folder(self, folder_path, folder_name_year, folder_name_month):
        """폴더 없을 때 생성"""
        # 경로 합치기: 년도와 월 폴더 결합. 문자형 년도와 mm 형식 달
        full_path = os.path.join(
            folder_path, str(folder_name_year), f"{folder_name_month:02d}"
        )

        # 폴더 존재 여부 확인 및 생성
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)

    def check_info(self, info, what_button):
        """정보 체크하는 함수

        what => 어느 함수에서 호출했는지. 각 버튼 실행에 따라 검사해야하는 조건 상이
        """

        if not self.check_date_format(
            str(info.date.date())
        ):  # 시간 정보 빼고 날짜만 들어가게
            return False

        if what_button == "nas" or what_button == "all":
            if info.type == "금요기도회":
                if info.date == "" or info.type == "" or info.subject == "":
                    messagebox.showinfo(
                        "알림", "설교자를 제외한 모든 정보를 입력해주세요."
                    )
                    return False
            elif (
                info.date == ""
                or info.type == ""
                or info.subject == ""
                or info.name == ""
            ):
                messagebox.showinfo("알림", "모든 정보를 입력해주세요.")
                return False
        elif what_button == "gm":
            if info.date == "" or info.type == "" or info.subject == "":
                messagebox.showinfo("알림", "설교자를 제외한 모든 정보를 입력해주세요.")
                return False
        elif what_button == "naver":
            if info.date == "" or info.type == "" or info.name == "":
                messagebox.showinfo("알림", "모든 정보를 입력해주세요.")
                return False

        return True

    def get_names(self, info, what_button):
        name_gm, name_nas, name_naver = None, None, None
        if what_button == "all":
            name_gm = (
                info.date.strftime("%Y년 %m월 %d일".encode("unicode-escape").decode())
                .encode()
                .decode("unicode-escape")
            )
            name_nas = (
                info.date.strftime("%Y%m%d")
                + "_"
                + info.type
                + "_"
                + info.subject
                + "_"
                + info.name
            )
            name_naver = (
                info.date.strftime("%y%m%d")
                + "_"
                + info.type
                + "_서울광명_"
                + info.name
            )
        elif what_button == "gm":
            name_gm = (
                info.date.strftime("%Y년 %m월 %d일".encode("unicode-escape").decode())
                .encode()
                .decode("unicode-escape")
            )
        elif what_button == "nas":
            name_nas = (
                info.date.strftime("%Y%m%d")
                + "_"
                + info.type
                + "_"
                + info.subject
                + "_"
                + info.name
            )
        elif what_button == "naver":
            name_naver = (
                info.date.strftime("%y%m%d")
                + "_"
                + info.type
                + "_서울광명_"
                + info.name
            )
        return name_gm, name_nas, name_naver

    def check_date_format(self, date):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            messagebox.showinfo(
                "알림", "올바른 날짜를 입력해주세요. 날짜 형식 YYYY-mm-dd"
            )
            return False

    def create_files(self, file_paths):
        """파일 경로 리스트를 받아서 File 객체로 만들어 file list로 반환"""
        result = []
        for file_path in file_paths:
            file_obj = File(file_path)
            result.append(file_obj)
        return result

    def moveTo(self, file, path_to_move):
        if isinstance(file, File):
            if os.path.isfile(file.full_path):
                try:
                    shutil.move(
                        file.full_path, os.path.join(path_to_move, file.file_name)
                    )
                    # messagebox.showinfo("알림", "파일이 이동되었습니다.")
                except FileNotFoundError as e:
                    pass
                    # messagebox.showinfo("알림", "파일을 찾을 수 없습니다")
                except Exception as e:
                    pass
                    # messagebox.showinfo("알림", "예상치 못한 오류 발생")
            """else:
                messagebox.showinfo("알림", "파일이 존재하지 않습니다")
        else:
            messagebox.showinfo("알림", "파일 관련 오류 발생")"""

    def move_file_with_progress(self, src, dst):
        file_path = src.full_path
        dst = os.path.join(dst, src.file_name)
        total_size = os.path.getsize(file_path)
        copied_size = 0
        block_size = 1024 * 1024  # 1MB 블록 단위

        root = tk.Tk()
        root.title("File Move Progress")

        # 진행률 바 설정
        progress_bar = ttk.Progressbar(
            root, orient="horizontal", length=300, mode="determinate"
        )
        progress_bar.pack(pady=20)

        status_label = tk.Label(root, text="Moving file...")
        status_label.pack()

        with open(file_path, "rb") as fsrc, open(dst, "wb") as fdst:
            while True:
                buffer = fsrc.read(block_size)
                if not buffer:
                    break
                fdst.write(buffer)
                copied_size += len(buffer)

                # 진행률 계산
                progress = (copied_size / total_size) * 100
                progress_bar["value"] = progress
                status_label.config(text=f"Progress: {progress:.2f}%")
                root.update_idletasks()  # UI 업데이트

        status_label.config(text="File move complete!")

    def sort_files_by_size(self, file_list, reverse=False):
        """
        파일 리스트를 파일 크기 기준으로 정렬하는 함수.

        Args:
            file_list (list): File 객체를 포함하는 리스트.
            reverse (bool): True면 내림차순, False면 오름차순으로 정렬. 기본값은 False.

        Returns:
            list: 정렬된 File 객체 리스트.
        """
        # file_list가 File 인스턴스들로 구성되어 있는지 확인
        if all(isinstance(file, File) for file in file_list):
            return sorted(file_list, key=lambda x: x.file_size, reverse=reverse)
        else:
            raise TypeError("file_list 내의 모든 요소는 File 객체여야 합니다.")

    def move_to_trash_windows(self, file_path):
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            print(f"{file_path} 파일이 존재하지 않습니다.")
            return

        # NULL 문자로 끝나는 유니코드 문자열로 경로 변환
        file_path_w = file_path + "\0"

        # SHFILEOPSTRUCT 구조체 초기화
        shfo = SHFILEOPSTRUCT()
        shfo.wFunc = FO_DELETE  # 파일 삭제
        shfo.pFrom = file_path_w  # 파일 경로 설정
        shfo.fFlags = FOF_ALLOWUNDO  # 휴지통으로 이동

        # SHFileOperation 호출하여 파일을 휴지통으로 이동
        try:
            result = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(shfo))
            if result == 0:
                print(f"{file_path} 파일을 휴지통으로 이동했습니다.")
            else:
                print(f"파일을 이동하는 중 오류 발생, 오류 코드: {result}")
        except Exception as e:
            print(f"파일 이동 중 오류가 발생했습니다: {e}")


# SHFILEOPSTRUCT 구조체 정의
class SHFILEOPSTRUCT(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("wFunc", wintypes.UINT),
        ("pFrom", wintypes.LPCWSTR),  # 유니코드 문자열
        ("pTo", wintypes.LPCWSTR),
        ("fFlags", wintypes.UINT),
        ("fAnyOperationsAborted", wintypes.BOOL),
        ("hNameMappings", wintypes.LPVOID),
        ("lpszProgressTitle", wintypes.LPCWSTR),
    ]


FO_DELETE = 0x0003
FOF_ALLOWUNDO = 0x0040
