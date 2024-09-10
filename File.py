class File:
    def __init__(self, file_name, location) -> None:
        self.file_name = file_name
        self.file_location = location
        self.file_size = 0

    def moveTo(self, file, location_to_move):
        pass

    def get_file_size(self, file):
        return self.file_size

    def check_file_size_under_max_size(self, file, max_size) -> bool:
        if isinstance(file, File):
            return file.get_file_size <= max_size
        else:
            TypeError
