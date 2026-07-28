import tkinter as tk
import os
import sys
from PIL import Image, ImageTk

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Splash:

    def __init__(self):

        self.root = tk.Tk()

        self.root.overrideredirect(True)

        image = Image.open(resource_path("static/splash.jpg"))
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.root, image=photo)
        label.image = photo
        label.pack()

        width = image.width
        height = image.height

        x = (self.root.winfo_screenwidth()-width)//2
        y = (self.root.winfo_screenheight()-height)//2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show(self):

        self.root.update_idletasks()
        self.root.update()

    def close(self):

        self.root.destroy()