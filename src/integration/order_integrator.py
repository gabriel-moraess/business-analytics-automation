from __future__ import annotations

import pandas as pd

from src.utils.logger import logger


class OrderIntegrator:
    """
    Responsável pelas integrações entre os datasets da Olist.
    """

    @staticmethod
    def adicionar_itens(
        orders: pd.DataFrame,
        order_items: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO PEDIDOS + ITENS")
        logger.info("=" * 60)

        resumo_itens = (
            order_items
            .groupby("order_id")
            .agg(
                receita_total=("price", "sum"),
                frete_total=("freight_value", "sum"),
                quantidade_itens=("order_item_id", "count"),
            )
            .reset_index()
        )

        resultado = orders.merge(
            resumo_itens,
            on="order_id",
            how="left",
        )

        logger.info(
            "%s pedidos enriquecidos com itens.",
            len(resultado),
        )

        return resultado

    @staticmethod
    def adicionar_clientes(
        orders: pd.DataFrame,
        customers: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO PEDIDOS + CLIENTES")
        logger.info("=" * 60)

        clientes = customers[
            [
                "customer_id",
                "customer_unique_id",
                "customer_city",
                "customer_state",
            ]
        ].copy()

        resultado = orders.merge(
            clientes,
            on="customer_id",
            how="left",
        )

        logger.info(
            "%s pedidos enriquecidos com clientes.",
            len(resultado),
        )

        return resultado

    @staticmethod
    def adicionar_produtos(
        order_items: pd.DataFrame,
        products: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO ITENS + PRODUTOS")
        logger.info("=" * 60)

        produtos = products[
            [
                "product_id",
                "product_category_name",
            ]
        ].copy()

        resultado = order_items.merge(
            produtos,
            on="product_id",
            how="left",
        )

        logger.info(
            "%s itens enriquecidos com produtos.",
            len(resultado),
        )

        return resultado

    @staticmethod
    def adicionar_pagamentos(
        orders: pd.DataFrame,
        payments: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO PEDIDOS + PAGAMENTOS")
        logger.info("=" * 60)

        pagamentos = (
            payments
            .groupby("order_id")
            .agg(
                payment_value=("payment_value", "sum"),
                payment_installments=(
                    "payment_installments",
                    "max",
                ),
                payment_sequential=(
                    "payment_sequential",
                    "max",
                ),
                payment_type=(
                    "payment_type",
                    "first",
                ),
            )
            .reset_index()
        )

        resultado = orders.merge(
            pagamentos,
            on="order_id",
            how="left",
        )

        logger.info(
            "%s pedidos enriquecidos com pagamentos.",
            len(resultado),
        )

        return resultado

    @staticmethod
    def adicionar_reviews(
        orders: pd.DataFrame,
        reviews: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO PEDIDOS + REVIEWS")
        logger.info("=" * 60)

        reviews_resumo = (
            reviews
            .sort_values("review_creation_date")
            .drop_duplicates(
                subset=["order_id"],
                keep="last",
            )
            [
                [
                    "order_id",
                    "review_id",
                    "review_score",
                    "review_creation_date",
                    "review_answer_timestamp",
                ]
            ]
        )

        resultado = orders.merge(
            reviews_resumo,
            on="order_id",
            how="left",
        )

        logger.info(
            "%s pedidos enriquecidos com reviews.",
            len(resultado),
        )

        return resultado

    @staticmethod
    def adicionar_sellers(
        order_items: pd.DataFrame,
        sellers: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO ITENS + SELLERS")
        logger.info("=" * 60)

        sellers_resumo = sellers[
            [
                "seller_id",
                "seller_zip_code_prefix",
                "seller_city",
                "seller_state",
            ]
        ].copy()

        resultado = order_items.merge(
            sellers_resumo,
            on="seller_id",
            how="left",
        )

        logger.info(
            "%s itens enriquecidos com sellers.",
            len(resultado),
        )

        return resultado

    @staticmethod
    def adicionar_geolocation_sellers(
        sellers: pd.DataFrame,
        geolocation: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO SELLERS + GEOLOCATION")
        logger.info("=" * 60)

        geo = (
            geolocation
            .groupby("geolocation_zip_code_prefix")
            .agg(
                geolocation_lat=("geolocation_lat", "mean"),
                geolocation_lng=("geolocation_lng", "mean"),
                geolocation_city=("geolocation_city", "first"),
                geolocation_state=("geolocation_state", "first"),
            )
            .reset_index()
        )

        resultado = sellers.merge(
            geo,
            left_on="seller_zip_code_prefix",
            right_on="geolocation_zip_code_prefix",
            how="left",
        )

        logger.info(
            "%s sellers enriquecidos com geolocation.",
            len(resultado),
        )

        return resultado

    @staticmethod
    def adicionar_geolocation_clientes(
        customers: pd.DataFrame,
        geolocation: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info("=" * 60)
        logger.info("INTEGRANDO CLIENTES + GEOLOCATION")
        logger.info("=" * 60)

        geo = (
            geolocation
            .groupby("geolocation_zip_code_prefix")
            .agg(
                customer_latitude=("geolocation_lat", "mean"),
                customer_longitude=("geolocation_lng", "mean"),
            )
            .reset_index()
        )

        clientes = customers.copy()

        if "customer_zip_code_prefix" not in clientes.columns:
            logger.warning(
                "customer_zip_code_prefix não encontrado nos customers."
            )
            return clientes

        resultado = clientes.merge(
            geo,
            left_on="customer_zip_code_prefix",
            right_on="geolocation_zip_code_prefix",
            how="left",
        )

        logger.info(
            "%s clientes enriquecidos com geolocation.",
            len(resultado),
        )

        return resultado