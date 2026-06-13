import ttkbootstrap as tb
from gui import RenamerGui
from tkinterdnd2 import TkinterDnD


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("Solothiel's Renamer")

    root = tb.Window(themename="cyborg", master=root)

    app = RenamerGui(root)

    root.mainloop()