import ttkbootstrap as tb
from gui import RenamerGui


if __name__ == "__main__":
    root = tb.Window(themename="cyborg")
    app = RenamerGui(root)
    root.mainloop()

