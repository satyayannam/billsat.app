import tkinter as tk
from tkinter import messagebox

import open_admin_page

# Predefined user IDs and passwords
users = {
    "user": "password",

}

# Function to validate user ID and password
def login():
    user_id = entry_user_id.get()
    password = entry_password.get()

    if users.get(user_id) == password:
        messagebox.showinfo("Login", "Login successful")
        root.destroy()
        open_admin_page.MainApp()
    else:
        messagebox.showerror("Login", "Invalid User ID or Password")

root = tk.Tk()
root.title("Billsat")
icon_image = tk.PhotoImage(file="Bill.png")

# Set the icon for the window
root.iconphoto(True, icon_image)

# Create a frame for the login form
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Username label and entry
label_user_id = tk.Label(frame, text="User ID:")
label_user_id.grid(row=0, column=0, padx=5, pady=5)
entry_user_id = tk.Entry(frame)
entry_user_id.grid(row=0, column=1, padx=5, pady=5)

# Password label and entry
label_password = tk.Label(frame, text="Password:")
label_password.grid(row=1, column=0, padx=5, pady=5)
entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

# Login button
btn_login = tk.Button(frame, text="Login", command=login)
btn_login.grid(row=2, column=0, columnspan=2, pady=10)
root.minsize(height=800,width=800)
# Start the GUI event loop
root.mainloop()
