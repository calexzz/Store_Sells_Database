import tkinter as tk

class ReportScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Экран отчета", font=("Montserrat", 16)).pack(pady=20)