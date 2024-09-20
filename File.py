import os
import shutil


class File:
    def __init__(self, file_name, path) -> None:
        self.file_name = file_name
        self.file_path = path
        self.full_path = os.path.join(
            self.file_path, self.file_name
        )  # 전체 파일 경로 생성

        if os.path.isfile(self.full_path):  # 전체 경로로 파일 존재 여부 확인
            self.file_size = self.get_file_size(self.full_path)  # 파일 사이즈 초기화
        else:
            print(f"파일이 존재하지 않습니다: {self.full_path}")
            self.file_size = 0  # 파일이 존재하지 않을 경우 사이즈를 0으로 설정

    def moveTo(self, file, path_to_move):
        if isinstance(file, File):
            shutil.move(file.full_path, path_to_move + "/" + file.file_name)
        pass

    def get_file_size(self, full_path):
        """파일 크기를 바이트 단위로 반환하는 함수"""
        return os.path.getsize(full_path)

    def check_file_size_under_max_size(self, file, max_size) -> bool:
        if isinstance(file, File):
            return file.get_file_size() <= max_size
        else:
            raise TypeError("잘못된 인스턴스")

    def __str__(self):
        return f"파일명: {self.file_name}, 위치: {self.file_path}, 크기: {self.file_size} 바이트"
