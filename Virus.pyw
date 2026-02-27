import tkinter as tk

# Create window
window = tk.Tk()
window.title("My First Window")
window.geometry("400x300")

# Label
label = tk.Label(window, text="Hello World!", font=("Arial", 16))
label.pack(pady=20)

# Button
def close_window():
    window.destroy()

button = tk.Button(window, text="Close", command=close_window)
button.pack(pady=10)

# Start window loop
window.mainloop()
