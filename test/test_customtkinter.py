import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark") # Dark mode
ctk.set_default_color_theme("dark-blue") # Dark blue theme
purple = "#570091"

def btn_callback():
    print("Button pressed")

# Create window, set title, and set size
app = ctk.CTk()
app.title("Test")
app.geometry("1280x720")
btn = ctk.CTkButton(app, text="Test", fg_color=purple, font=("Arial", 20), cursor="hand2", command=btn_callback)
btn.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()