from __future__ import annotations

import pandas as pd


class FactSales:
    """
    Constrói a tabela fato de vendas.

    A FactSales concentra os principais eventos de negócio
    que serão utilizados pelo Dashboard Executivo.

    A estrutura foi projetada para receber futuramente
    os dados reais da API da Olist.
    """

    def __init__(
        self,
        df: pd.DataFrame,
    ) -> None:

        self.df = df.copy()

    def construir(self) -> pd.DataFrame:
        """
        Constrói a FactSales.

        Returns:
            DataFrame da tabela fato.
        """

        fact = pd.DataFrame()

        # ==========================================
        # IDENTIFICADORES
        # ==========================================

        fact["pedido_id"] = self._obter_coluna("id")

        fact["cliente_id"] = self._obter_coluna("customer_id")

        fact["produto_id"] = self._obter_coluna("product_id")

        # ==========================================
        # DATAS
        # ==========================================

        fact["data_pedido"] = self._obter_coluna("purchase_timestamp")

        # ==========================================
        # STATUS
        # ==========================================

        fact["status"] = self._obter_coluna("status")

        # ==========================================
        # MÉTRICAS
        # ==========================================

        fact["quantidade"] = self._obter_coluna(
            "quantity",
            default=1,
        )

        fact["preco_unitario"] = self._obter_coluna(
            "price",
            default=0.0,
        )

        fact["frete"] = self._obter_coluna(
            "freight_value",
            default=0.0,
        )

        fact["desconto"] = self._obter_coluna(
            "discount",
            default=0.0,
        )

        # Receita

        fact["receita"] = (
            fact["quantidade"]
            * fact["preco_unitario"]
        )

        # Custo (placeholder)

        fact["custo"] = 0.0

        # Lucro (placeholder)

        fact["lucro"] = (
            fact["receita"]
            - fact["custo"]
        )

        return fact

    # =====================================================

    def _obter_coluna(
        self,
        coluna: str,
        default=None,
    ) -> pd.Series:
        """
        Retorna uma coluna caso exista.

        Caso contrário retorna uma série contendo
        o valor default.
        """

        if coluna in self.df.columns:
            return self.df[coluna]

        return pd.Series(
            [default] * len(self.df),
            index=self.df.index,
        )