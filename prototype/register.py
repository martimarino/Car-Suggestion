from tkinter import *
import re
from tkinter import messagebox
import sqlite3
import random
from email.message import EmailMessage
import smtplib

# Database
try:
    con = sqlite3.connect('website.db')

    con.execute('''create table if not exists users(
                fname text not null,
                lname text not null,
                email text not null,
                password text not null);      
    ''')
    con.close()

except Exception as ep:
    messagebox.showerror('', ep)

ws = Tk()
ws.title('Python Guides')
ws.geometry('500x400')
ws.config(bg="#447c84")
ws.attributes('-fullscreen', True)


# functions

def otp_gen():
    pass


cpy = ''


def sendOtp():
    otp_no = ''
    for _ in range(4):
        r = random.randint(0, 9)
        otp_no += str(r)

    global cpy
    cpy += otp_no
    sender = "codetestingemail6@gmail.com"
    reciever = em.get()
    password = "Cute...pie@0823"
    msg_body = f'otp is {cpy}'
    msg = EmailMessage()
    msg['subject'] = 'OTP'
    msg['from'] = sender
    msg['to'] = reciever
    msg.set_content(msg_body)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)

        smtp.send_message(msg)

    print(cpy)
    return cpy


def clr():
    fname.delete(0, END)
    lname.delete(0, END)
    em.delete(0, END)
    pwd.delete(0, END)


def submit():
    enteredOtp = otp.get()
    expectedOtp = cpy
    print(expectedOtp)

    fname_check = fname.get()
    lname_check = lname.get()
    em_check = em.get()
    pwd_check = pwd.get()
    otp_check = otp.get()
    check_count = 0

    if fname_check == "":
        warn = "First name can't be empty!"
    else:
        check_count += 1
    if lname_check == "":
        warn = "Last name can't be empty!"
    else:
        check_count += 1
    if em_check == "":
        warn = "Email can't be empty!"
    else:
        check_count += 1
    if pwd_check == "":
        warn = "Password can't be empty!"
    else:
        check_count += 1
    if otp_check == "":
        warn = "Otp can't be empty!"
    else:
        check_count += 1

    # if fname_check, lname_check, pwd_check, otp_check:
    if check_count == 5:
        if (expectedOtp == enteredOtp):
            con = sqlite3.connect('website.db')
            c = con.cursor()
            c.execute("insert into users VALUES (:fname, :lname, :em, :pwd)", {

                'fname': fname.get(),
                'lname': lname.get(),
                'em': em.get(),
                'pwd': pwd.get()
            })
            con.commit()

            ws.destroy()
            import app

        else:
            messagebox.showerror('', 'Incorrect Otp')
    else:
        messagebox.showerror('', warn)


# frames
frame = Frame(ws, padx=20, pady=20)
frame.pack(expand=True)

# labels
Label(
    frame,
    text="Create New Account",
    font=("Times", "24", "bold")
).grid(row=0, columnspan=3, pady=10)

Label(
    frame,
    text='First Name',
    font=("Times", "14")
).grid(row=1, column=0, pady=5)

Label(
    frame,
    text='Last Name',
    font=("Times", "14")
).grid(row=2, column=0, pady=5)

Label(
    frame,
    text='Email Address',
    font=("Times", "14")
).grid(row=3, column=0, pady=5)

Label(
    frame,
    text='Password',
    font=("Times", "14")
).grid(row=4, column=0, pady=5)

Label(
    frame,
    text='Enter OTP',
    font=("Times", "14")
).grid(row=5, column=0, pady=5)

# Entry
fname = Entry(frame, width=30)
lname = Entry(frame, width=30)
em = Entry(frame, width=30)
pwd = Entry(frame, width=30)
otp = Entry(frame, width=30)

fname.grid(row=1, column=1)
lname.grid(row=2, column=1)
em.grid(row=3, column=1)
pwd.grid(row=4, column=1)
otp.grid(row=5, column=1)

# button
clr = Button(frame, text="Clear", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=clr)
reg = Button(frame, text="Register", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"), command=submit)
ext = Button(frame, text="Exit", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"),
             command=lambda: ws.destroy())
otpp = Button(frame, text="verify email", padx=10, relief=RAISED, font=("Times", "10", "bold"), command=sendOtp)
clr.grid(row=6, column=0, pady=20)
reg.grid(row=6, column=1, pady=20)
ext.grid(row=6, column=2, pady=20)
otpp.grid(row=5, column=2)

ws.mainloop()