import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Касса")
        self.geometry("1100x700")
        self.resizable(False, False)

        self._build_nav()
        self._build_container()

        self.show_frame("sale")

    def _build_nav(self):
        nav = tk.Frame(self, bg="#2c3e50", width=160)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)

        buttons = [
            ("🛒 Продажа",  "sale"),
            ("📊 Отчёт",    "report"),
            ("📦 Остатки",  "stock"),
        ]

        for text, name in buttons:
            btn = tk.Label(
                nav, text=text,
                bg="#2c3e50", fg="white",
                pady=12, padx=8,
                font=("Montserrat", 11),
                cursor="hand2"
            )
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, n=name: self.show_frame(n))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#34495e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2c3e50"))

    def _build_container(self):
        self.container = tk.Frame(self, bg="#ecf0f1")
        self.container.pack(side="right", fill="both", expand=True)

    def show_frame(self, name):
        for widget in self.container.winfo_children():
            widget.destroy()

        if name == "sale":
            from gui.sale_screen import SaleScreen
            SaleScreen(self.container).pack(fill="both", expand=True)
        elif name == "report":
            from gui.report_screen import ReportScreen
            ReportScreen(self.container).pack(fill="both", expand=True)
        elif name == "stock":
            from gui.stock_screen import StockScreen
            StockScreen(self.container).pack(fill="both", expand=True)

if __name__ == '__main__':
    app = App()
    app.mainloop()