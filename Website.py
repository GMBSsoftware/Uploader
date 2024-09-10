from abc import ABC, abstractmethod


class Website(ABC):
    def __init__(self, address, id, password) -> None:
        self.address = address
        self.id = id
        self.password = password

    @abstractmethod
    def login(self, id, password):
        pass
