import tkinter as tk
from tkinter import ttk, messagebox
from services.sale_service import SaleService
from repositories.product_repo import ProductRepository

class SaleScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ecf0f1")
        self.sale_service = SaleService()
        self.product_repo = ProductRepository()
        self.products = self.product_repo.get_all()
        self.cart = []

        self._build_ui()

    def _build_ui(self):
        # --- левая колонка: список товаров ---
        left = tk.Frame(self, bg="#ecf0f1")
        left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(left, text="Товары", font=("Arial", 13, "bold"), bg="#ecf0f1").pack(anchor="w")

        self.product_list = ttk.Treeview(left, columns=("name", "price", "stock"), show="headings")
        self.product_list.heading("name",  text="Название")
        self.product_list.heading("price", text="Цена")
        self.product_list.heading("stock", text="На складе")
        self.product_list.column("name",  width=200)
        self.product_list.column("price", width=80)
        self.product_list.column("stock", width=80)
        self.product_list.pack(fill="both", expand=True)
        self.product_list.bind("<Double-1>", self._on_product_select)

        for p in self.products:
            self.product_list.insert("", "end", iid=p['id_product'], values=(
                p['name_of_product'], f"{p['price']} ₽", p['quantity_at_storage']
            ))

        # --- средняя колонка: корзина ---
        mid = tk.Frame(self, bg="#ecf0f1")
        mid.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(mid, text="Корзина", font=("Arial", 13, "bold"), bg="#ecf0f1").pack(anchor="w")

        self.cart_list = ttk.Treeview(mid, columns=("name", "qty", "total"), show="headings")
        self.cart_list.heading("name",  text="Название")
        self.cart_list.heading("qty",   text="Кол-во")
        self.cart_list.heading("total", text="Сумма")
        self.cart_list.column("name",  width=180)
        self.cart_list.column("qty",   width=60)
        self.cart_list.column("total", width=80)
        self.cart_list.pack(fill="both", expand=True)

        tk.Button(mid, text="Удалить товар из корзины", command=self._remove_from_cart).pack(pady=4)
        tk.Button(mid, text="Очистить корзину", command=self._clear_cart).pack(pady=4)

        # --- правая колонка: итог ---
        right = tk.Frame(self, bg="#ecf0f1", width=180)
        right.pack(side="left", fill="y", padx=10, pady=10)
        right.pack_propagate(False)

        tk.Label(right, text="Итог", font=("Arial", 13, "bold"), bg="#ecf0f1").pack(anchor="w")

        self.total_var = tk.StringVar(value="0.00 ₽")
        tk.Label(right, textvariable=self.total_var, font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        tk.Label(right, text="Кассир ID:", bg="#ecf0f1").pack(anchor="w")
        self.cashier_var = tk.StringVar(value="1")
        tk.Entry(right, textvariable=self.cashier_var, width=10).pack(anchor="w", pady=4)

        tk.Button(
            right, text="Оформить продажу",
            font=("Arial", 11, "bold"),
            bg="#27ae60", fg="white",
            pady=10, command=self._checkout
        ).pack(fill="x", pady=20)

    def _clear_cart(self):
        self.cart = []
        self._refresh_cart()

    def _on_product_select(self, event):
        selected = self.product_list.focus()
        if not selected:
            return
        product = next(p for p in self.products if p['id_product'] == int(selected))

        # диалог ввода количества
        dialog = tk.Toplevel(self)
        dialog.title("Количество")
        dialog.geometry("250x120")
        dialog.resizable(False, False)

        tk.Label(dialog, text=f"{product['name_of_product']}", font=("Arial", 11)).pack(pady=8)
        tk.Label(dialog, text=f"Доступно: {product['quantity_at_storage']}").pack()

        qty_var = tk.StringVar(value="1")
        entry = tk.Entry(dialog, textvariable=qty_var, width=10)
        entry.pack(pady=4)
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

        tk.Button(dialog, text="Добавить", command=confirm).pack()
        dialog.bind("<Return>", lambda e: confirm())

    def _add_to_cart(self, product, qty):
        # считаем сколько уже в корзине
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
            'id_product': product['id_product'],
            'name_of_product': product['name_of_product'],
            'price': product['price'],
            'quantity': qty
        })
        self._refresh_cart()

    def _remove_from_cart(self):
        selected = self.cart_list.focus()
        if not selected:
            return
        self.cart = [i for i in self.cart if i['id_product'] != int(selected)]
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

        try:
            id_check = self.sale_service.create_sale(cashier_id, self.cart)
            messagebox.showinfo("Успешно", f"Чек #{id_check} оформлен!\nСумма: {self.total_var.get()}")
            self.cart = []
            self._refresh_cart()
            # обновляем остатки в списке товаров
            self.products = self.product_repo.get_all()
            for p in self.products:
                self.product_list.item(p['id_product'], values=(
                    p['name_of_product'], f"{p['price']} ₽", p['quantity_at_storage']
                ))
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))