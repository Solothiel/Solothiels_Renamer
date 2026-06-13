import ttkbootstrap as tb
from gui import RenamerGui
from tkinterdnd2 import TkinterDnD


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("Solothiel's Renamer")

    style = tb.Style("cyborg")

    app = RenamerGui(root)

    root.mainloop()

    root.mainloop()