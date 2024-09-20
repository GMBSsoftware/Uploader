import tkinter as tk
import os
from File import File
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

from Setting import Setting


class GUI:
    def __init__(self, root, setting) -> None:
        self.version = "Ver1.0"
        self.root = root
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 400
        self.app_height = 250
        # 현재 화면을 나타내는 프레임
        self.current_frame = None
        self.file_list = []
        self.setting = setting
        self.entry_widgets = []  # 엔트리 위젯(설정 값)을 저장할 리스트 추가
        self.frame_base()

    def frame_base(self):
        self.root.title("Uploader")

        # 화면 가로 세로 크기
        windows_width = self.root.winfo_screenwidth()
        windows_height = self.root.winfo_screenheight()
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 800
        self.app_height = 500
        # 화면 중앙에 위치 시키기
        center_width = (windows_width / 2) - (self.app_width / 2)
        center_height = (windows_height / 2) - (self.app_height / 2)
        # 가로x세로+x위치+y위치
        self.root.geometry(
            f"{self.app_width}x{self.app_height}+{int(center_width)}+{int(center_height)}"
        )
        # 창 크기 변경 (x, y)
        self.root.resizable(False, False)

        # 하단 라벨
        label = tk.Label(
            self.root,
            text=f"{self.version}    Made by\n광명방송국 개발팀",
            justify="right",
        )
        # label.pack(side="bottom", anchor="se")  # 하단에 정렬
        label.place(x=self.app_width - 120, y=self.app_height - 50)

        # 라벨 구간 뺀 크기
        self.frame_width = self.app_width
        self.frame_height = self.app_height - 60

    def create_frame(self):
        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.place(
            x=0, y=0, width=self.frame_width, height=self.frame_height
        )

    def page_home(self):
        self.frame_remove()
        self.create_frame()
        self.button_change_page("home")
        self.frame_drag_and_drop()

    def page_setting(self):
        self.frame_remove()
        self.clear_widgets()
        self.create_frame()
        self.button_change_page("setting")
        self.frame_setting()

    def button_change_page(self, current_page):
        """홈이면 설정 버튼, 설정 페이지면 홈"""

        text = "설정" if current_page == "home" else "홈"
        command = (
            self.on_setting_click if current_page == "home" else self.on_home_click
        )

        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(x=0, y=0, width=self.frame_width, height=80)

        button_change_page = tk.Button(
            self.current_frame,
            text=text,
            command=command,
            relief="groove",
        )
        button_change_page.place(
            x=self.frame_width - 40 - 35, y=35, width=40, height=40
        )

    def frame_remove(self):
        # 현재 프레임이 있으면 제거
        if self.current_frame:
            self.current_frame.destroy()

    def on_home_click(self):
        self.save_settings()
        self.page_home()

    def on_setting_click(self):
        self.page_setting()

    def show(self):
        self.page_home()

    def frame_drag_and_drop(self):
        # 파일 드래그 앤 드롭을 위한 리스트박스
        self.listbox = tk.Listbox(self.root, width=60, height=10)
        self.listbox.place(x=50, y=100)

        # 드래그 앤 드롭 기능을 리스트박스에 추가
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.on_file_drop)

        # 업로드 버튼
        self.upload_button = tk.Button(
            self.root, text="업로드", command=self.on_upload, relief="groove"
        )
        self.upload_button.place(x=520, y=100, width=70, height=70)

        # 목록 지우기 버튼
        self.delete_button = tk.Button(
            self.root, text="목록\n지우기", command=self.on_delete, relief="groove"
        )
        self.delete_button.place(x=520, y=200, width=70, height=70)

    def frame_setting(self):
        # 설정 프레임 내의 라벨 추가
        label = tk.Label(self.root, text="설정 값", font=30)
        label.place(x=70, y=30)

        # 엔트리 위젯 추가를 위한 데이터
        entries = [
            ("광명 홈페이지 아이디", self.setting.id_gm),
            ("광명 홈페이지 비밀번호", self.setting.password_gm),
            ("네이버 아이디", self.setting.id_naver),
            ("네이버 비밀번호", self.setting.password_naver),
            ("메일 받는 사람", self.setting.receive_email),
            ("저장할 나스 위치", self.setting.nas_path),
            ("타이틀 이미지", self.setting.title_image),
        ]

        for i, (label_text, default_value) in enumerate(entries):
            # 레이블 추가
            entry_label = tk.Label(self.root, text=label_text)
            entry_label.place(x=50, y=90 + (i * 30), anchor="nw")  # y 좌표 조정

            # 엔트리 추가
            entry = tk.Entry(self.root, width=40, justify="left")
            entry.place(x=200, y=90 + (i * 30))  # y 좌표 조정
            entry.insert(0, default_value)  # 기본값 설정
            self.entry_widgets.append(entry)  # 엔트리 위젯 저장

    def save_settings(self):
        """엔트리 값을 setting에 저장하는 함수"""
        self.setting.id_gm = self.entry_widgets[0].get()
        self.setting.password_gm = self.entry_widgets[1].get()
        self.setting.id_naver = self.entry_widgets[2].get()
        self.setting.password_naver = self.entry_widgets[3].get()
        self.setting.receive_email = self.entry_widgets[4].get()
        self.setting.nas_path = self.entry_widgets[5].get()
        self.setting.title_image = self.entry_widgets[6].get()

    def clear_widgets(self):
        self.entry_widgets.clear()

    def on_file_drop(self, event):
        """파일 드롭 시 호출되는 함수"""
        files = self.root.tk.splitlist(event.data)  # 여러 파일 드롭 가능
        for file in files:
            self.listbox.insert(tk.END, file)  # 드롭된 파일 경로 추가

    def on_upload(self):
        self.file_list = self.create_files_from_list(
            self.listbox.get(0, tk.END)
        )  # 리스트박스의 파일 경로로 File 객체 리스트 생성
        for file in self.file_list:
            print("file : ", file)  # File 객체의 __str__ 메서드 호출로 파일 정보 출력

    def on_delete(self):
        """리스트박스의 모든 항목을 지우는 함수"""
        self.listbox.delete(0, tk.END)  # 리스트박스의 모든 항목 삭제

    def create_files_from_list(self, file_paths):
        """파일 경로 리스트를 받아서 File 객체 리스트를 반환하는 함수"""
        file_objects = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            file_path = os.path.dirname(file_path)
            file_obj = File(file_name, file_path)
            file_objects.append(file_obj)
        return file_objects


setting = Setting()
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    gui = GUI(root, setting)
    gui.show()

    gui.root.mainloop()
