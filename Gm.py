from Website import Website


class Gm(Website):
    def __init__(self, address, id, password) -> None:
        super().__init__(address, id, password)

    def login(self):
        super().login(
            "login_form_userid",
            "login_form_password",
            '//*[@id="tab-login"]/div/div/div/div[3]/button',
        )

    def handle_file(self, file):
        pass
