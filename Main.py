from GUI import GUI
from tkinterdnd2 import TkinterDnD, DND_FILES

root = TkinterDnD.Tk()
gui = GUI(root)
gui.show()

gui.root.mainloop()
