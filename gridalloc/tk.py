import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.geometry("300x200")
root.title("Login Page")
label = tk.Label(root, text="Login Page", font=("Arial", 14))
label.grid(row=0, column=1)
l1 = tk.Label(root, text="Username")
l1.grid(row=1, column=0)
username = tk.Entry(root, width=20)
username.grid(row=1, column=1)
l2 = tk.Label(root, text="Password")
l2.grid(row=2, column=0)
password = tk.Entry(root, width=20, show="*")
password.grid(row=2, column=1)
def login():
    user = username.get()
    pwd = password.get()
    if user == "admin" and pwd == "1234":
        messagebox.showinfo("Login", "Login Successful!")
    else:
        messagebox.showerror("Login", "Invalid Username or Password")
button = tk.Button(root, text="Login", command=login)
button.grid(row=3, column=1)
root.mainloop()
