from __future__ import annotations

from src.analytics.metrics import BusinessMetrics
from src.integration.order_integrator import OrderIntegrator
from src.loaders.data_loader import DataLoader
from src.sources.base_source import BaseSource
from src.utils.logger import logger


class Pipeline:
    """
    Pipeline principal da aplicação.
    """

    def __init__(
        self,
        source: BaseSource,
    ) -> None:

        self.source = source
        self.loader = DataLoader(source)

    # =====================================================
    # EXECUÇÃO
    # =====================================================

    def executar(self):

        logger.info("=" * 80)
        logger.info("BUSINESS ANALYTICS AUTOMATION")
        logger.info("=" * 80)

        model = self._carregar()

        model = self._integrar(model)

        self._calcular_kpis(model)

        logger.info("=" * 80)
        logger.info("PIPELINE FINALIZADO")
        logger.info("=" * 80)

        return model

    # =====================================================
    # CARREGAMENTO
    # =====================================================

    def _carregar(self):

        logger.info("=" * 60)
        logger.info("CARREGANDO DATASETS")
        logger.info("=" * 60)

        return self.loader.carregar(

            orders="olist_orders_dataset.csv",

            order_items="olist_order_items_dataset.csv",

            customers="olist_customers_dataset.csv",

            products="olist_products_dataset.csv",

            payments="olist_order_payments_dataset.csv",

            reviews="olist_order_reviews_dataset.csv",

            sellers="olist_sellers_dataset.csv",

        )

    # =====================================================
    # INTEGRAÇÕES
    # =====================================================

    def _integrar(self, model):

        model.orders = OrderIntegrator.adicionar_itens(
            model.orders,
            model.order_items,
        )

        model.orders = OrderIntegrator.adicionar_clientes(
            model.orders,
            model.customers,
        )

        model.order_items = OrderIntegrator.adicionar_produtos(
            model.order_items,
            model.products,
        )

        model.orders = OrderIntegrator.adicionar_pagamentos(
            model.orders,
            model.payments,
        )

        model.orders = OrderIntegrator.adicionar_reviews(
            model.orders,
            model.reviews,
        )

        return model

    # =====================================================
    # KPIs
    # =====================================================

    def _calcular_kpis(self, model):

        metrics = BusinessMetrics(model)

        print()

        print("=" * 60)
        print("INDICADORES")
        print("=" * 60)

        for chave, valor in metrics.indicadores().items():
            print(f"{chave}: {valor}")

        print()

        print("=" * 60)
        print("TOP CATEGORIAS")
        print("=" * 60)

        print(metrics.top_categorias())

        print()

        print("=" * 60)
        print("RESUMO DO MODELO")
        print("=" * 60)

        print(model.resumo())

        print()

        print("=" * 60)
        print("ORDERS")
        print("=" * 60)

        print(model.orders.head())

        print()

        print(model.orders.columns.tolist())