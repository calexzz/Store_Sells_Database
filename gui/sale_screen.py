import tkinter as tk

class SaleScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Экран продажи", font=("Montserrat", 16)).pack(pady=20)