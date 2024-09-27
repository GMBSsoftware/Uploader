import tkinter as tk
import os, datetime
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

from Setting import Setting
from Util import Util
from File import File
from Naver import Naver
from Gm import Gm


class GUI:
    def __init__(self, root) -> None:
        self.version = "Ver1.0"
        self.root = root
        # 생성할 프로그램 가로 세로 크기
        self.app_width = 400
        self.app_height = 250
        # 현재 화면을 나타내는 프레임
        self.current_frame = None
        self.file_list = []
        self.util = Util()
        self.util.create_new_folder(
            setting.nas_path,
            datetime.datetime.now().year,
            datetime.datetime.now().month,
        )
        self.date, self.type = self.util.get_date_and_type()
        self.entry_widgets_setting = []  # 엔트리 위젯(설정 값)을 저장할 리스트 추가
        self.entry_widgets_home = (
            []
        )  # 엔트리 위젯(홈에서 날짜, 요일, 주제 등)을 저장할 리스트 추가
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
        self.util.create_new_folder(
            setting.nas_path,
            datetime.datetime.now().year,
            datetime.datetime.now().month,
        )
        self.page_home()

    def on_setting_click(self):
        self.page_setting()

    def show(self):
        self.page_home()

    def frame_drag_and_drop(self):
        # 엔트리 위젯 추가를 위한 데이터
        entries = [
            ("날짜", self.date.strftime("%Y-%m-%d")),
            ("예배 종류", self.type),
            ("주제", ""),
            ("설교자(신급)", "주중심 목사" if self.type != "금요기도회" else ""),
        ]

        for i, (label_text, default_value) in enumerate(entries):
            # 레이블 추가
            entry_label = tk.Label(self.root, text=label_text)
            entry_label.place(x=50, y=20 + (i * 30), anchor="nw")  # y 좌표 조정

            # 엔트리 추가
            entry = tk.Entry(self.root, width=40, justify="left")
            entry.place(x=200, y=20 + (i * 30))  # y 좌표 조정
            entry.insert(0, default_value)  # 기본값 설정
            self.entry_widgets_home.append(entry)  # 엔트리 위젯 저장

        # 파일 드래그 앤 드롭을 위한 리스트박스
        self.listbox = tk.Listbox(self.root, width=60, height=10)
        self.listbox.place(x=50, y=150)

        # 드래그 앤 드롭 기능을 리스트박스에 추가
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.on_file_drop)

        # 실행 버튼
        self.run_button = tk.Button(
            self.root, text="실행", command=self.on_run, relief="groove"
        )
        self.run_button.place(x=520, y=150, width=70, height=70)

        # 목록 지우기 버튼
        self.delete_button = tk.Button(
            self.root, text="목록\n지우기", command=self.on_delete, relief="groove"
        )
        self.delete_button.place(x=520, y=250, width=70, height=70)

        # 홈페이지 업로드 버튼
        self.upload_button = tk.Button(
            self.root, text="홈페이지\n업로드", command=self.on_upload, relief="groove"
        )
        self.upload_button.place(x=120, y=330, width=50, height=50)

        # 메일 전송 버튼
        self.send_email_button = tk.Button(
            self.root, text="메일\n전송", command=self.on_send_email, relief="groove"
        )
        self.send_email_button.place(x=220, y=330, width=50, height=50)

        # 나스 이동 버튼
        self.file_move_button = tk.Button(
            self.root, text="나스\n이동", command=self.on_file_move, relief="groove"
        )
        self.file_move_button.place(x=320, y=330, width=50, height=50)

    def frame_setting(self):
        # 설정 프레임 내의 라벨 추가
        label = tk.Label(self.root, text="설정 값", font=30)
        label.place(x=70, y=30)

        # 엔트리 위젯 추가를 위한 데이터
        entries = [
            ("광명 홈페이지 아이디", setting.id_gm),
            ("광명 홈페이지 비밀번호", setting.password_gm),
            ("네이버 아이디", setting.id_naver),
            ("네이버 비밀번호", setting.password_naver),
            ("메일 받는 사람", setting.receive_email),
            ("저장할 나스 위치", setting.nas_path),
            ("주일 타이틀 이미지", setting.title_image_sunday),
            ("수요 타이틀 이미지", setting.title_image_wednesday),
        ]

        for i, (label_text, default_value) in enumerate(entries):
            # 레이블 추가
            entry_label = tk.Label(self.root, text=label_text)
            entry_label.place(x=50, y=90 + (i * 30), anchor="nw")  # y 좌표 조정

            # 엔트리 추가
            entry = tk.Entry(self.root, width=40, justify="left")
            entry.place(x=200, y=90 + (i * 30))  # y 좌표 조정
            entry.insert(0, default_value)  # 기본값 설정
            self.entry_widgets_setting.append(entry)  # 엔트리 위젯 저장

    def save_settings(self):
        """엔트리 값을 setting에 저장하는 함수"""
        setting.id_gm = self.entry_widgets_setting[0].get()
        setting.password_gm = self.entry_widgets_setting[1].get()
        setting.id_naver = self.entry_widgets_setting[2].get()
        setting.password_naver = self.entry_widgets_setting[3].get()
        setting.receive_email = self.entry_widgets_setting[4].get()
        setting.nas_path = self.entry_widgets_setting[5].get()
        setting.title_image_sunday = self.entry_widgets_setting[6].get()
        setting.title_image_wednesday = self.entry_widgets_setting[7].get()

    def save_info(self):
        """날짜, 타입, 주제, 설교자 등 정보를 저장하는 함수"""
        self.date = datetime.datetime.strptime(
            self.entry_widgets_home[0].get(), "%Y-%m-%d"
        )
        self.type = self.entry_widgets_home[1].get()
        self.subject = self.entry_widgets_home[2].get()
        self.name = self.entry_widgets_home[3].get()

    def clear_widgets(self):
        self.entry_widgets_setting.clear()

    def on_file_drop(self, event):
        """파일 드롭 시 호출되는 함수"""
        files = self.root.tk.splitlist(event.data)  # 여러 파일 드롭 가능
        for file in files:
            self.listbox.insert(tk.END, file)  # 드롭된 파일 경로 추가

    def on_run(self):
        self.file_list = self.util.create_files(self.listbox.get(0, tk.END))
        if not self.util.check_count_file(self.file_list, 3):
            return None
        self.save_info()
        file_name = self.util.check_info_and_get_name(
            date=self.date,
            type=self.type,
            subject=self.subject,
            name=self.name,
            what=all,
        )
        if file_name is None:
            return None
        self.file_list = self.util.sort_files_by_size(self.file_list)
        # 오름차순이래

    def on_delete(self):
        """리스트박스의 모든 항목을 지우는 함수"""
        self.listbox.delete(0, tk.END)  # 리스트박스의 모든 항목 삭제
        self.file_list.clear()

    def on_upload(self):
        new_file = self.preprocess(1, "gm", 1610666666)  # 1.5GB
        if new_file is None:
            return
        gm = Gm(setting.address_gm, setting.id_gm, setting.password_gm)
        gm.login()
        if self.type == "주일예배":
            image = setting.title_image_sunday
        elif self.type == "수요예배":
            image = setting.title_image_wednesday
        result = gm.handle_file(file=new_file, image=image)
        if result:
            messagebox.showinfo("알림", "광명 홈페이지에 업로드를 완료했습니다.")
        self.on_delete()

    def on_send_email(self):
        new_file = self.preprocess(1, "naver", 524288000)  # 500MB
        if new_file is None:
            return
        naver = Naver(setting.address_naver, setting.id_naver, setting.password_naver)
        naver.login()
        result = naver.handle_file(file=new_file, receiver=setting.receive_email)
        if result:
            messagebox.showinfo("알림", "메일 전송을 완료했습니다.")
        self.on_delete()

    def on_file_move(self):
        new_file = self.preprocess(1, "nas", None)
        if new_file is None:
            return
        self.util.moveTo(
            new_file,
            os.path.join(
                setting.nas_path, str(self.date.year), f"{self.date.month:02d}"
            ),
        )
        self.on_delete()

    def preprocess(self, file_count, what_button, file_size):
        """각 버튼 눌렀을 때 처리 과정. 새 파일 리턴

        file_count : 파일 개수가 몇 개여야하는지.
        what_button : 어느 버튼을 누른것인지. (all, gm, nas, naver)
        file_size : 초과하면 안 되는 파일 사이즈

        파일 생성, 개수 체크, 크기 체크, 정보 저장, 정보 체크 및 이름, 파일명 체크, 이름 변경, File 형으로 생성
        """
        self.file_list = self.util.create_files(self.listbox.get(0, tk.END))
        if not self.util.check_count_file(self.file_list, file_count):
            return None
        if file_size and not self.util.is_under_file_size(self.file_list[0], file_size):
            messagebox.showinfo("알림", f"파일 크기가 {file_size}를 초과하였습니다.")
            return None
        self.save_info()
        file_name = self.util.check_info_and_get_name(
            date=self.date,
            type=self.type,
            subject=self.subject,
            name=self.name,
            what=what_button,
        )
        if file_name is None:
            return None
        new_file_path = self.util.rename(
            self.file_list[0].file_path, self.file_list[0].file_name, file_name
        )
        new_file = File(new_file_path)
        return new_file


setting = Setting()
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    gui = GUI(root)
    gui.show()

    gui.root.mainloop()
