import tkinter as tk

def main():
    window = tk.Tk()
    window.title("New Window")
    window.geometry("400x250")
    window.resizable(False, False)

    label = tk.Label(
        window,
        text="This is a new window",
        font=("Arial", 14)
    )
    label.pack(expand=True)

    button = tk.Button(
        window,
        text="Close",
        command=window.destroy
    )
    button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
