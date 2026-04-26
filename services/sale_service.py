import time
from repositories.receipt_repo import ReceiptRepository
from repositories.sale_item_repo import SaleItemRepository
from repositories.product_repo import ProductRepository

class SaleService:
    def __init__(self):
        self.receipt_repo = ReceiptRepository()
        self.sale_item_repo = SaleItemRepository()
        self.product_repo = ProductRepository()

    def create_sale(self, id_cashier, items):
        """
        items - список словарей: [{'id_product': 1, 'quantity': 2}, ...]
        """
        # Проверяем, что всего хватает на складе
        for item in items:
            available = self.product_repo.get_quantity(item['id_product'])
            if available < item['quantity']:
                raise ValueError(f"Недостаточно товара на складе: id {item['id_product']}")

        # Создаём чек
        created_at = time.time()
        id_check = self.receipt_repo.create(created_at, id_cashier)

        # Записываем позиции и списываем остатки
        self.sale_item_repo.create_many(id_check, items)
        for item in items:
            self.product_repo.decrease_quantity(item['id_product'], item['quantity'])

        return id_check