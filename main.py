from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

FONT_NAME = "Courier New"
START_EMAIL = "anton.vagin87@gmail.com"
DATA_FILE = "data.json"


# ___________________________________-Search Engine-----------------------------
#
def search_engine(website):
    try:
        with open(DATA_FILE, "r") as file:
            data_s = json.load(file)
    except FileNotFoundError:
        data_valid = messagebox.showerror(title="Error", message="There is no saved password Yet!")
    try:
        password = data_s[website]["password"]
        email = data_s[website]["email"]
        data_valid = messagebox.showerror(title="Found Data", message=f"Email: {email}\n"
                                                                      f"Password: {password}")
        inp_email.delete(0, 'end')
        inp_pass.delete(0, 'end')
        inp_pass.insert(0, password)
        inp_email.insert(0, email)
    except KeyError:
        data_valid = messagebox.showerror(title="Error", message=f"There is no password for  '{website}'")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def pass_generator():
    inp_pass.delete(0, "end")
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for x in range(randint(8, 10))]
    password_list += [choice(symbols) for x in range(randint(2, 4))]
    password_list += [choice(numbers) for x in range(randint(2, 4))]
    shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    inp_pass.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data(website, email, password):
    website = website.strip()
    email = email.strip()
    password = password.strip()
    if website == '' and password == '':
        data_valid = messagebox.showerror(title="Error", message="Some of the fields are empty!\n"
                                                                 "Please check and try again")
    else:
        new_data = {
            website: {
                "email": email,
                "password": password,
            }

        }
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open(DATA_FILE, "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open(DATA_FILE, "w") as file:
                data.update(new_data)
                json.dump(data, file, indent=4)
        finally:
            inp_email.delete(0, 'end')
            inp_email.insert(0, START_EMAIL)
            inp_web.delete(0, 'end')
            inp_pass.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

myimg = PhotoImage(file='logo.png')

can = Canvas(width=200, height=200)
can.create_image(100, 100, image=myimg)
can.grid(column=1, row=0)

lab_web = Label(text="Website: ", font=(FONT_NAME, 12, "bold"))
lab_web.grid(column=0, row=1, sticky="e")

inp_web = Entry(width=24)
inp_web.grid(column=1, row=1)
inp_web.focus()

lab_email = Label(text="Email/Username: ", font=(FONT_NAME, 12, "bold"))
lab_email.grid(column=0, row=2, sticky="e")

inp_email = Entry(width=45)
inp_email.grid(column=1, row=2, columnspan=2)
inp_email.insert(0, START_EMAIL)

lab_pass = Label(text="Password:", font=(FONT_NAME, 12, "bold"))
lab_pass.grid(column=0, row=3, sticky="e")

inp_pass = Entry(width=24)
inp_pass.grid(column=1, row=3)

but_gen = Button(text="Generate Password", font=(FONT_NAME, 10, "bold"), command=pass_generator)
but_gen.grid(column=2, row=3)

but_add = Button(text="Add", width=44, command=lambda: save_data(inp_web.get(), inp_email.get(), inp_pass.get()))
but_add.grid(column=1, row=4, columnspan=2)

but_search = Button(text="Search", font=(FONT_NAME, 10, "bold"), width=17, command=lambda: search_engine(inp_web.get()))
but_search.grid(column=2, row=1)

window.mainloop()
