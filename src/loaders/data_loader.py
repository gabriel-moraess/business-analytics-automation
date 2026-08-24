from __future__ import annotations

from src.models.data_model import DataModel
from src.utils.logger import logger


class DataLoader:

    def __init__(self, source):
        self.source = source

    def carregar(
        self,
        orders: str,
        order_items: str,
        customers: str,
        products: str,
        payments: str,
        reviews: str,
        sellers: str,
        geolocation: str,
    ) -> DataModel:

        logger.info("=" * 60)
        logger.info("CARREGANDO DATASETS")
        logger.info("=" * 60)

        self.source.connect()

        model = DataModel()

        # =====================================================
        # ORDERS
        # =====================================================

        logger.info("Carregando orders...")

        model.orders = self.source.read(orders)

        logger.info(
            "%s registros carregados em 'orders'.",
            len(model.orders),
        )

        # =====================================================
        # ORDER ITEMS
        # =====================================================

        logger.info("Carregando order_items...")

        model.order_items = self.source.read(order_items)

        logger.info(
            "%s registros carregados em 'order_items'.",
            len(model.order_items),
        )

        # =====================================================
        # CUSTOMERS
        # =====================================================

        logger.info("Carregando customers...")

        model.customers = self.source.read(customers)

        logger.info(
            "%s registros carregados em 'customers'.",
            len(model.customers),
        )

        # =====================================================
        # PRODUCTS
        # =====================================================

        logger.info("Carregando products...")

        model.products = self.source.read(products)

        logger.info(
            "%s registros carregados em 'products'.",
            len(model.products),
        )

        # =====================================================
        # PAYMENTS
        # =====================================================

        logger.info("Carregando payments...")

        model.payments = self.source.read(payments)

        logger.info(
            "%s registros carregados em 'payments'.",
            len(model.payments),
        )

        # =====================================================
        # REVIEWS
        # =====================================================

        logger.info("Carregando reviews...")

        model.reviews = self.source.read(reviews)

        logger.info(
            "%s registros carregados em 'reviews'.",
            len(model.reviews),
        )

        # =====================================================
        # SELLERS
        # =====================================================

        logger.info("Carregando sellers...")

        model.sellers = self.source.read(sellers)

        logger.info(
            "%s registros carregados em 'sellers'.",
            len(model.sellers),
        )

        # =====================================================
        # GEOLOCATION
        # =====================================================

        logger.info("Carregando geolocation...")

        model.geolocation = self.source.read(geolocation)

        logger.info(
            "%s registros carregados em 'geolocation'.",
            len(model.geolocation),
        )

        self.source.disconnect()

        logger.info("=" * 60)
        logger.info("DATASETS CARREGADOS")
        logger.info("=" * 60)

        return model