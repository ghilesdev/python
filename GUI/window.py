import tkinter
from tkinter import messagebox
from tkinter import *


window=tkinter.Tk()
#put the code between tkinter.tk and window.mainloop

# def Popupfunc():
#     msg=messagebox.showinfo("popup title", "message of the popup")
#
# frame=Frame(window)
# frame.pack()
#
# #label
# str_var=StringVar()
# lbl=Label(frame, textvariable=str_var)
# str_var.set("label")
# lbl.pack()
#
# #button
# button_widget=tkinter.Button(frame, text="click me", command=Popupfunc)
# button_widget.pack(side=LEFT)
#
# #checkbutton
# cv=IntVar()
# cb=Checkbutton(frame, text='check', variable=cv, onvalue=1, offvalue=0, height=20, width=20)
# cb.pack()
#
# #text field
# entry=Entry(frame, bd=3)
# entry.pack()
#
# #listbox
# lbox=Listbox(frame)
# lbox.insert(1, 'item 1')
# lbox.insert(2, 'item 2')
# lbox.insert(3, 'item 3')
# lbox.insert(4, 'item 4')
# lbox.insert(5, 'item 5')
# lbox.pack()

#menu button
# m_button=Menubutton(window, text="click me")
# m_button.grid()
# m_button.menu=Menu(m_button)
# m_button['menu']=m_button.menu
# m_button.menu.add_checkbutton(label='item1')
# m_button.menu.add_checkbutton(label='item2')
# m_button.menu.add_checkbutton(label='item3')
# m_button.menu.add_checkbutton(label='item4')
# m_button.pack()

# #canvas
# canvas_widget=tkinter.Canvas(window, bg='red', width=512, height=512)
# coord=10,50, 512, 512
# #creating forms that will be placed in the canvas using pack()
# arc_object=canvas_widget.create_arc(coord, start=0, extent=270, fill='white')
# line_object=canvas_widget.create_line(75, 20, 30, 100, fill='black')
# canvas_widget.pack()

#menu bar
def func():
    print("button new clicked")


def func2():
    print("button  clicked")


menu_bar=Menu(window)
menu1=Menu(menu_bar)
menu1.add_command(label='new', command=func)
menu1.add_separator()
menu1.add_command(label='exit', command=window.quit)
menu_bar.add_cascade(label="file", menu= menu1)

menu2=Menu(menu_bar)
menu2.add_command(label='edit', command=func2)
menu2.add_separator()
menu2.add_command(label='undo', command=func2)
menu_bar.add_cascade(label="more", menu=menu2)

window.config(menu=menu_bar)

#radio button
def select():
    selection='selected option number'+str(var.get())
    label.config(text=selection)

var=IntVar()
radio1=Radiobutton(window, text='option 1', variable=var, value=1, command=select)
radio2=Radiobutton(window, text='option 2', variable=var, value=2, command=select)
radio3=Radiobutton(window, text='option 3', variable=var, value=3, command=select)
radio1.pack(anchor=W)
radio2.pack(anchor=W)
radio3.pack(anchor=W)
label=Label(window)
label.pack()


#scaler
# var2=DoubleVar()
# scale=Scale(window, variable=var2)
# scale.pack()

#scroll bar
scroll_bar=Scrollbar(window)
scroll_bar.pack(side=RIGHT, fill= Y)

mylist=Listbox(window, yscrollcommand=scroll_bar.set)

for line in range(1000):
    mylist.insert(END, "ROW: " +str(line+1))
mylist.pack()
scroll_bar.config(command=mylist.yview())

#spin box
spin_box=Spinbox(window, from_ =0, to = 5)
spin_box.pack()
window.mainloop()