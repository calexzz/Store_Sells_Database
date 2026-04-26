import tkinter as tk
from tkinter import ttk, messagebox
from services.sale_service import SaleService
from repositories.product_repo import ProductRepository

BG       = "#34495e"
BG_DARK  = "#2c3e50"
FG       = "#ecf0f1"
ACCENT   = "#27ae60"
DANGER   = "#e74c3c"
SELECTED = "#3498db"

class SaleScreen(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent)
        tk.Label(self, text="Экран продажи", font=("Montserrat", 16)).pack(pady=20)
        super().__init__(parent, bg=BG)
        self.sale_service = SaleService()
        self.product_repo = ProductRepository()
        self.products = self.product_repo.get_all()
        self.cart = []

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background=BG_DARK, foreground=FG,
            fieldbackground=BG_DARK, rowheight=25
        )
        style.configure("Treeview.Heading",
            background=BG_DARK, foreground=FG,
            font=("Montserrat", 10, "bold")
        )
        style.map("Treeview", background=[("selected", SELECTED)])

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_mid()
        self._build_right()

    def _build_left(self):
        left = tk.Frame(self, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        tk.Label(left, text="Товары", font=("Montserrat", 13, "bold"),
                 bg=BG, fg=FG).grid(row=0, column=0, sticky="w")

        self.product_list = ttk.Treeview(left, columns=("name", "price", "stock"), show="headings")
        self.product_list.heading("name",  text="Название")
        self.product_list.heading("price", text="Цена")
        self.product_list.heading("stock", text="На складе")
        self.product_list.column("name",  width=200)
        self.product_list.column("price", width=80)
        self.product_list.column("stock", width=80)
        self.product_list.grid(row=1, column=0, sticky="nsew")
        self.product_list.bind("<Double-1>", self._on_product_select)

        for p in self.products:
            self.product_list.insert("", "end", iid=p['id_product'], values=(
                p['name_of_product'], f"{p['price']} ₽", p['quantity_at_storage']
            ))

    def _build_mid(self):
        mid = tk.Frame(self, bg=BG)
        mid.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        mid.rowconfigure(1, weight=1)
        mid.columnconfigure(0, weight=1)

        tk.Label(mid, text="Корзина", font=("Montserrat", 13, "bold"),
                 bg=BG, fg=FG).grid(row=0, column=0, sticky="w")

        self.cart_list = ttk.Treeview(mid, columns=("name", "qty", "total"), show="headings")
        self.cart_list.heading("name",  text="Название")
        self.cart_list.heading("qty",   text="Кол-во")
        self.cart_list.heading("total", text="Сумма")
        self.cart_list.column("name",  width=180)
        self.cart_list.column("qty",   width=60)
        self.cart_list.column("total", width=80)
        self.cart_list.grid(row=1, column=0, sticky="nsew")

        btn_remove = tk.Label(mid, text="Удалить выбранное", bg=DANGER, fg=FG,
                              pady=6, cursor="hand2", font=("Montserrat", 10))
        btn_remove.grid(row=2, column=0, sticky="ew", pady=(4, 2))
        btn_remove.bind("<Button-1>", lambda e: self._remove_from_cart())

        btn_clear = tk.Label(mid, text="Очистить корзину", bg="#c0392b", fg=FG,
                             pady=6, cursor="hand2", font=("Montserrat", 10))
        btn_clear.grid(row=3, column=0, sticky="ew", pady=(2, 0))
        btn_clear.bind("<Button-1>", lambda e: self._clear_cart())

    def _build_right(self):
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        tk.Label(right, text="Итог", font=("Montserrat", 13, "bold"),
                 bg=BG, fg=FG).pack(anchor="w")

        self.total_var = tk.StringVar(value="0.00 ₽")
        tk.Label(right, textvariable=self.total_var, font=("Montserrat", 22, "bold"),
                 bg=BG, fg=FG).pack(pady=20)

        tk.Label(right, text="Кассир ID:", bg=BG, fg=FG).pack(anchor="w")
        self.cashier_var = tk.StringVar(value="1")
        tk.Entry(right, textvariable=self.cashier_var, width=10,
                 bg=BG_DARK, fg=FG, insertbackground=FG).pack(anchor="w", pady=4)

        btn = tk.Label(right, text="Оформить продажу", font=("Montserrat", 11, "bold"),
                       bg=ACCENT, fg=FG, pady=12, cursor="hand2")
        btn.pack(fill="x", pady=20)
        btn.bind("<Button-1>", lambda e: self._checkout())

    def _on_product_select(self, event):
        selected = self.product_list.focus()
        if not selected:
            return
        product = next(p for p in self.products if p['id_product'] == int(selected))

        dialog = tk.Toplevel(self)
        dialog.title("Количество")
        dialog.geometry("250x140")
        dialog.resizable(False, False)
        dialog.configure(bg=BG)

        tk.Label(dialog, text=product['name_of_product'], font=("Montserrat", 11),
                 bg=BG, fg=FG).pack(pady=8)
        tk.Label(dialog, text=f"Доступно: {product['quantity_at_storage']}",
                 bg=BG, fg=FG).pack()

        qty_var = tk.StringVar(value="1")
        entry = tk.Entry(dialog, textvariable=qty_var, width=10,
                         bg=BG_DARK, fg=FG, insertbackground=FG)
        entry.pack(pady=6)
        entry.focus()

        def confirm():
            try:
                qty = float(qty_var.get())
                if qty <= 0:
                    raise ValueError
                self._add_to_cart(product, qty)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное количество")

        btn = tk.Label(dialog, text="Добавить", bg=ACCENT, fg=FG,
                       pady=6, cursor="hand2", font=("Montserrat", 10))
        btn.pack(fill="x", padx=20)
        btn.bind("<Button-1>", lambda e: confirm())
        dialog.bind("<Return>", lambda e: confirm())

    def _add_to_cart(self, product, qty):
        in_cart = 0
        for item in self.cart:
            if item['id_product'] == product['id_product']:
                in_cart = item['quantity']
                break

        available = product['quantity_at_storage']
        if in_cart + qty > available:
            messagebox.showerror("Ошибка", f"Доступно только {available - in_cart} шт.")
            return

        for item in self.cart:
            if item['id_product'] == product['id_product']:
                item['quantity'] += qty
                self._refresh_cart()
                return

        self.cart.append({
            'id_product':      product['id_product'],
            'name_of_product': product['name_of_product'],
            'price':           product['price'],
            'quantity':        qty
        })
        self._refresh_cart()

    def _remove_from_cart(self):
        selected = self.cart_list.focus()
        if not selected:
            return
        self.cart = [i for i in self.cart if i['id_product'] != int(selected)]
        self._refresh_cart()

    def _clear_cart(self):
        self.cart = []
        self._refresh_cart()

    def _refresh_cart(self):
        for row in self.cart_list.get_children():
            self.cart_list.delete(row)
        total = 0
        for item in self.cart:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            self.cart_list.insert("", "end", iid=item['id_product'], values=(
                item['name_of_product'], item['quantity'], f"{subtotal:.2f} ₽"
            ))
        self.total_var.set(f"{total:.2f} ₽")

    def _checkout(self):
        if not self.cart:
            messagebox.showwarning("Корзина пуста", "Добавьте товары в корзину")
            return
        try:
            cashier_id = int(self.cashier_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ID кассира")
            return

        from repositories.employer_repo import EmployerRepository
        if not EmployerRepository().is_cashier(cashier_id):
            messagebox.showerror("Ошибка", f"Сотрудник с ID {cashier_id} не является кассиром")
            return

        try:
            id_check = self.sale_service.create_sale(cashier_id, self.cart)
            messagebox.showinfo("Успешно", f"Чек #{id_check} оформлен!\nСумма: {self.total_var.get()}")
            self.cart = []
            self._refresh_cart()
            self.products = self.product_repo.get_all()
            for p in self.products:
                self.product_list.item(p['id_product'], values=(
                    p['name_of_product'], f"{p['price']} ₽", p['quantity_at_storage']
                ))
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))