import os


class File:
    def __init__(self, file_name, location) -> None:
        self.file_name = file_name
        self.file_location = location
        if os.path.isfile(self.file_location):
            self.file_size = self.get_file_size(
                self.file_location
            )  # 파일 사이즈 초기화
        else:
            print(f"파일이 존재하지 않습니다: {self.file_location}")
            self.file_size = 0  # 파일이 존재하지 않을 경우 사이즈를 0으로 설정

    def moveTo(self, file, location_to_move):
        pass

    def get_file_size(self, file):
        try:
            return os.path.getsize(file)
        except Exception as e:
            print(f"파일 사이즈를 가져오는 중 오류 발생: {e}")
            return 0

    def check_file_size_under_max_size(self, file, max_size) -> bool:
        if isinstance(file, File):
            return file.get_file_size() <= max_size
        else:
            raise TypeError("잘못된 인스턴스")

    def __str__(self):
        return f"파일명: {self.file_name}, 위치: {self.file_location}, 크기: {self.file_size} 바이트"
