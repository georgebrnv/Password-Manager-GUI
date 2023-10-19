from tkinter import *
from tkinter import messagebox
from screeninfo import get_monitors
import pyperclip
import json

FONT = "Courier"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_entry.delete(0, END)

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)

    # Insert generated password into Password entry box
    password_entry.insert(0, password)

    # Add password to clipboard (copy)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password
        }
    }

    # Check if entry boxes are empty
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please fill up all the fields.")
    else:
        try:
            # Try to open a file
            with open("data.json", "r") as data_file:
                # Reading file data
                data = json.load(data_file)
        except FileNotFoundError:
            # If it doesn't exist - create one
            with open("data.json", "w") as data_file:
                # Write data
                json.dump(new_data, data_file, indent=4)
        else:
            # If it exists - update it's data
            data.update(new_data)
            # Save data
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            # delete previous entry content
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            # put cursor in website entry box
            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
def data_search():
    website = website_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            # Read file
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message=f"No Data File found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f"{website.title()}",
                                message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showwarning(title="Error", message=f"No details for {website.title()} exists.")

# User's screen info
screens = get_monitors()
screen_width = screens[0].width
screen_height = screens[0].height

# Window set up
window = Tk()
window.title("Password Manager App")
window.config(padx=20, pady=20)
screen_x = int((screen_width - window.winfo_width()) // 2)
screen_y = int((screen_height - window.winfo_height()) // 2)
window.geometry(f"+{screen_x}+{screen_y}")

# Canvas and png
canvas = Canvas(width=200, height=200)
logo_png = PhotoImage(file="logo.png")
canvas_image = canvas.create_image(100, 100, image=logo_png)
canvas.grid(column=1, row=0)

# Labels
website_text = Label(text="Website: ", font=(FONT, 14))
website_text.grid(column=0, row=1)
email_username_text = Label(text="Email/Username: ", font=(FONT, 14))
email_username_text.grid(column=0, row=2)
password_text = Label(text="Password: ", font=(FONT, 14))
password_text.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_username_entry = Entry(width=36)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, "example@email.com")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
generate_password_button = Button(text="Generate Password", width=11, command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=34, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=11, command=data_search)
search_button.grid(column=2, row=1)


window.mainloop()
