import tkinter as tk

class StockScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Экран остатков", font=("Montserrat", 16)).pack(pady=20)