from tkinter import *
from tkinter import messagebox

ws = Tk()
ws.title('Python Guides')
ws.geometry('500x300')
ws.config(bg="#447c84")
ws.attributes('-fullscreen', True)


# functions
def msg():
    return messagebox.showinfo('', 'Life is short, \n do what you love')


def logOut():
    resp = messagebox.askquestion('', 'Are you sure?')
    if resp == 'yes':
        ws.destroy()

    else:
        pass


# frames
frame = Frame(
    ws,
    padx=20,
    pady=20
)
frame.pack(expand=True)

# image
img = PhotoImage(file='img.png')

# labelslo
Label(
    frame,
    text="Congratulations!",
    font=("Times", "24", "bold")
).grid(row=0, columnspan=3)

Label(
    frame,
    text='Your Account is Active',
    fg='green',
    font=("Times", "14")
).grid(row=1, columnspan=3)

imglbl = Label(frame, image=img)
imglbl.grid(row=2, column=1)

# button
exp = Button(frame, text="open>>", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=msg)
logout = Button(frame, text="Logout", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=logOut)
exp.grid(row=2, column=1)
logout.grid(row=3, column=1)

ws.mainloop()