from GUI import GUI
from tkinterdnd2 import TkinterDnD, DND_FILES
from Naver import Naver
from Gm import Gm
from Setting import Setting
import time

"""root = TkinterDnD.Tk()
gui = GUI(root)
gui.show()

gui.root.mainloop()"""

if __name__ == "__main__":
    setting = Setting()
    naver = Naver(setting.address_naver, setting.id_naver, setting.password_naver)
    naver.login()
    gm = Gm(setting.address_gm, setting.id_gm, setting.password_gm)
    gm.login()
    time.sleep(10)
    naver.close_browser()
    gm.close_browser()
