from tkinter import *
from functools import partial


def myclick():
    label = Label(root, text=e.get())
    print(e.get())
    label.pack()


root = Tk()
e = Entry(root, width=50)
e.pack()
text = e.get()
mybtn = Button(root, text="click me", padx=50, command=myclick)
mybtn.pack()
root.mainloop()
