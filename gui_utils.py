from tkinter import Tk, filedialog


def choose_directory() -> str:
    root = Tk()
    root.withdraw()  # Hide main window
    directory = filedialog.askdirectory(title="Select Folder")
    root.destroy()
    return directory
