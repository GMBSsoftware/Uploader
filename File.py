import os


class File:
    def __init__(self, file_name, location) -> None:
        self.file_name = file_name
        self.file_location = location
        self.file_size = self.get_file_size(file_name)  # 파일 사이즈 초기화

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
