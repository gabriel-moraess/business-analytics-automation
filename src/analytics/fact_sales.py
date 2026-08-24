from __future__ import annotations

import pandas as pd


class FactSales:

    @staticmethod
    def criar(
        orders: pd.DataFrame,
        order_items: pd.DataFrame,
        products: pd.DataFrame,
        customers: pd.DataFrame,
        payments: pd.DataFrame,
        reviews: pd.DataFrame,
    ) -> pd.DataFrame:

        fato = order_items.copy()

        # =====================================================
        # PEDIDOS
        # =====================================================

        fato = fato.merge(
            orders[
                [
                    "order_id",
                    "customer_id",
                    "order_status",
                    "order_purchase_timestamp",
                    "order_approved_at",
                    "order_delivered_carrier_date",
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date",
                ]
            ],
            on="order_id",
            how="left",
        )

        # =====================================================
        # PRODUTOS
        # =====================================================

        fato = fato.merge(
            products[
                [
                    "product_id",
                    "product_category_name",
                    "product_weight_g",
                    "product_length_cm",
                    "product_height_cm",
                    "product_width_cm",
                ]
            ],
            on="product_id",
            how="left",
            suffixes=("", "_produto"),
        )

        # =====================================================
        # CLIENTES
        # =====================================================

        fato = fato.merge(
            customers[
                [
                    "customer_id",
                    "customer_unique_id",
                    "customer_zip_code_prefix",
                    "customer_city",
                    "customer_state",
                ]
            ],
            on="customer_id",
            how="left",
            suffixes=("", "_cliente"),
        )

        # =====================================================
        # PAGAMENTOS
        # =====================================================

        pagamentos = (
            payments
            .groupby("order_id", as_index=False)
            .agg(
                valor_pagamento=("payment_value", "sum"),
                parcelas=("payment_installments", "max"),
                tipo_pagamento=("payment_type", "first"),
            )
        )

        fato = fato.merge(
            pagamentos,
            on="order_id",
            how="left",
        )

        # =====================================================
        # REVIEWS
        # =====================================================

        reviews_limpo = (
            reviews[
                [
                    "order_id",
                    "review_score",
                ]
            ]
            .drop_duplicates("order_id")
        )

        fato = fato.merge(
            reviews_limpo,
            on="order_id",
            how="left",
        )

        # =====================================================
        # MÉTRICAS
        # =====================================================

        fato["receita_item"] = fato["price"]

        fato["frete_item"] = fato["freight_value"]

        fato["receita_total_item"] = (
            fato["price"]
            + fato["freight_value"]
        )

        # =====================================================
        # RESULTADO
        # =====================================================

        return fato