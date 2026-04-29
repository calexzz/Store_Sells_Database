import tkinter as tk
from tkinter import ttk
from repositories.product_repo import ProductRepository

BG      = "#34495e"
BG_DARK = "#2c3e50"
FG      = "#ecf0f1"
LOW     = "#e74c3c"   # мало товара
OK      = "#ecf0f1"

class StockScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.product_repo = ProductRepository()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background=BG_DARK, foreground=FG,
            fieldbackground=BG_DARK, rowheight=25
        )
        style.configure("Treeview.Heading",
            background=BG_DARK, foreground=FG,
            font=("Arial", 10, "bold")
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._build_top()
        self._build_table()

    def _build_top(self):
        top = tk.Frame(self, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(top, text="Остатки на складе", font=("Arial", 13, "bold"),
                 bg=BG, fg=FG).pack(side="left")

        btn = tk.Label(top, text="Обновить", bg="#2980b9", fg=FG,
                       padx=12, pady=6, cursor="hand2", font=("Arial", 10))
        btn.pack(side="right")
        btn.bind("<Button-1>", lambda e: self._load())

    def _build_table(self):
        mid = tk.Frame(self, bg=BG)
        mid.grid(row=1, column=0, sticky="nsew", padx=10, pady=4)
        mid.rowconfigure(0, weight=1)
        mid.columnconfigure(0, weight=1)

        self.table = ttk.Treeview(mid,
            columns=("name", "category", "price", "qty"), show="headings")
        self.table.heading("name",     text="Название")
        self.table.heading("category", text="Категория")
        self.table.heading("price",    text="Цена")
        self.table.heading("qty",      text="Остаток")
        self.table.column("name",     width=250)
        self.table.column("category", width=150)
        self.table.column("price",    width=100)
        self.table.column("qty",      width=100)
        self.table.grid(row=0, column=0, sticky="nsew")

        self._load()

    def _load(self):
        for row in self.table.get_children():
            self.table.delete(row)

        products = self.product_repo.get_all()
        for p in products:
            tag = "low" if p['quantity_at_storage'] <= 10 else "ok"
            self.table.insert("", "end", values=(
                p['name_of_product'],
                p['name_of_category'],
                f"{p['price']} ₽",
                p['quantity_at_storage']
            ), tags=(tag,))

        self.table.tag_configure("low", foreground=LOW)
        self.table.tag_configure("ok",  foreground=OK)