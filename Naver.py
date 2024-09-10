from Website import Website


class Naver(Website):
    def __init__(self, address, id, password) -> None:
        super().__init__(address, id, password)

    def login(self, id, password):
        return super().login(id, password)

    def send_email(self, file):
        pass
