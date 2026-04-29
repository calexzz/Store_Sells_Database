import tkinter as tk
from tkinter import ttk
import datetime
from services.report_service import ReportService

BG      = "#34495e"
BG_DARK = "#2c3e50"
FG      = "#ecf0f1"
ACCENT  = "#27ae60"

class ReportScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.report_service = ReportService()

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
        self._build_bottom()

    def _build_top(self):
        top = tk.Frame(self, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(top, text="Дата:", bg=BG, fg=FG, font=("Arial", 11)).pack(side="left")

        self.date_var = tk.StringVar(value=datetime.date.today().strftime("%d.%m.%Y"))
        tk.Entry(top, textvariable=self.date_var, width=12,
                 bg=BG_DARK, fg=FG, insertbackground=FG,
                 font=("Arial", 11)).pack(side="left", padx=8)

        tk.Label(top, text="(дд.мм.гггг)", bg=BG,
                 fg="#95a5a6", font=("Arial", 9)).pack(side="left")

        btn = tk.Label(top, text="Показать", bg=ACCENT, fg=FG,
                       padx=16, pady=6, cursor="hand2", font=("Arial", 10, "bold"))
        btn.pack(side="left", padx=12)
        btn.bind("<Button-1>", lambda e: self._load_report())

    def _build_table(self):
        mid = tk.Frame(self, bg=BG)
        mid.grid(row=1, column=0, sticky="nsew", padx=10, pady=4)
        mid.rowconfigure(0, weight=1)
        mid.columnconfigure(0, weight=1)

        self.table = ttk.Treeview(mid, columns=("name", "qty", "total"), show="headings")
        self.table.heading("name",  text="Товар")
        self.table.heading("qty",   text="Кол-во")
        self.table.heading("total", text="Сумма")
        self.table.column("name",  width=300)
        self.table.column("qty",   width=100)
        self.table.column("total", width=120)
        self.table.grid(row=0, column=0, sticky="nsew")

    def _build_bottom(self):
        bottom = tk.Frame(self, bg=BG_DARK)
        bottom.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        tk.Label(bottom, text="Выручка за день:", bg=BG_DARK,
                 fg=FG, font=("Arial", 12)).pack(side="left", padx=12, pady=8)

        self.revenue_var = tk.StringVar(value="—")
        tk.Label(bottom, textvariable=self.revenue_var, bg=BG_DARK,
                 fg=ACCENT, font=("Arial", 14, "bold")).pack(side="left", pady=8)

    def _load_report(self):
        try:
            date = datetime.datetime.strptime(self.date_var.get(), "%d.%m.%Y").date()
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Неверный формат даты. Используйте дд.мм.гггг")
            return

        report = self.report_service.daily_report(date)

        for row in self.table.get_children():
            self.table.delete(row)

        for item in report['items']:
            self.table.insert("", "end", values=(
                item['name_of_product'],
                item['quantity'],
                f"{item['total']:.2f} ₽"
            ))

        self.revenue_var.set(f"{report['revenue']:.2f} ₽")