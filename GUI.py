import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES


class GUI:
    def __init__(self, root) -> None:
        self.version = "Ver1.0"
        self.root = root
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 400
        self.app_height = 250
        # 현재 화면을 나타내는 프레임
        self.current_frame = None

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

    def frame_home(self):
        self.frame_remove()

        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        self.current_frame.place(
            x=0, y=0, width=self.frame_width, height=self.frame_height
        )

    def frame_home_and_setting(self):
        # 프레임 생성
        self.current_frame = tk.Frame(self.root)
        self.current_frame.place(x=0, y=0, width=self.frame_width, height=80)

        button_home = tk.Button(
            self.current_frame, text="홈", command=self.on_home_click, relief="groove"
        )
        button_home.place(x=self.frame_width - 40 - 35, y=35, width=40, height=40)

        button_setting = tk.Button(
            self.current_frame,
            text="설정",
            command=self.on_setting_click,
            relief="groove",
        )
        button_setting.place(
            x=self.frame_width - 40 - 35 - 70, y=35, width=40, height=40
        )

    def frame_remove(self):
        # 현재 프레임이 있으면 제거
        if self.current_frame:
            self.current_frame.destroy()

    def on_home_click(self):
        self.frame_home()

    def on_setting_click(self):
        messagebox.showinfo("알림", "업데이트 예정")

    def show(self):
        self.frame_base()
        self.frame_home_and_setting()
        self.frame_drag_and_drop()

    def frame_drag_and_drop(self):
        # 파일 드래그 앤 드롭을 위한 리스트박스
        self.listbox = tk.Listbox(self.root, width=60, height=10)
        self.listbox.pack(pady=20)

        # 드래그 앤 드롭 기능을 리스트박스에 추가
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.on_file_drop)

    def on_file_drop(self, event):
        """파일 드롭 시 호출되는 함수"""
        files = self.root.tk.splitlist(event.data)  # 여러 파일 드롭 가능
        for file in files:
            self.listbox.insert(tk.END, file)  # 드롭된 파일 경로 추가
