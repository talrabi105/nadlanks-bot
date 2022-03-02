import tkinter as tk
from tkinter import PhotoImage
import win32api
import os
from PIL import Image, ImageTk, ImageGrab


def choose_new_pic(window, names_list, msg, place):
    window.destroy()
    if os.path.exists('img/image1.jpg'):
        os.remove('img/image1.jpg')
    win32api.MessageBox(0, "העתק תמונה ללוח", "bot", 0)
    im = ImageGrab.grabclipboard()
    im.save("img/image1.jpg")
    start_msg(names_list, msg, place)


def remove_pic(window, names_list, msg, place):
    window.destroy()
    os.remove('img/image1.jpg')
    start_msg(names_list, msg, place)


def send(window):
    window.destroy()
    os.environ["nadlanks-bot"] = '1'


def cancel(window):
    window.destroy()
    os.environ["nadlanks-bot"] = '0'


def start_msg(names_list, msg, place):
    window = tk.Tk()
    window.title('נדל"ן כפר סבא')
    window.iconbitmap('logo.ico')

    window.attributes("-topmost", True)
    tk.Label(window, text=place, fg="blue").pack()

    tk.Label(window, text=msg).pack()

    for name in names_list:
        tk.Label(window, text=name, fg="blue").pack()

    if len(os.listdir("img")) == 0:
        l2 = tk.Label(window, text="הוסף תמונה מהלוח", cursor="hand2")
        l2.pack()
        l2.bind("<Button-1>", lambda a: choose_new_pic(window, names_list, msg, place))
    elif len(os.listdir("img")) == 1:
        image1 = Image.open("img/image1.jpg")
        ri = image1.resize((200, 100), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(ri)

        limg = tk.Label(window, image=test)
        limg.image = test
        limg.pack()

        l2 = tk.Label(window, text="החלף תמונה", cursor="hand2")
        l2.pack()
        l2.bind("<Button-1>", lambda a: choose_new_pic(window, names_list, msg, place))

        l3 = tk.Label(window, text="הסר תמונה", cursor="hand2")
        l3.pack()
        l3.bind("<Button-1>", lambda a: remove_pic(window, names_list, msg, place))

    b1 = tk.Button(window, text="שלח", command=lambda: send(window))
    b1.pack()

    b2 = tk.Button(window, text="ביטול", command=lambda: cancel(window))
    b2.pack()

    window.mainloop()
