from Website import Website


class Gm(Website):
    def __init__(self, address, id, password) -> None:
        super().__init__(address, id, password)

    def login(self, id, password):
        return super().login(id, password)

    def upload(self, file):
        pass
