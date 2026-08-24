from __future__ import annotations

import pandas as pd


class DimProduct:
    """
    Constrói a Dimensão Produto.

    Centraliza todas as informações referentes aos produtos
    para utilização no Data Warehouse.
    """

    def __init__(
        self,
        df: pd.DataFrame,
    ) -> None:

        self.df = df.copy()

    def construir(self) -> pd.DataFrame:
        """
        Constrói a dimensão Produto.

        Returns:
            DataFrame contendo os produtos.
        """

        dim = pd.DataFrame()

        # ==========================================
        # IDENTIFICADORES
        # ==========================================

        dim["produto_id"] = self._obter_coluna("product_id")

        # ==========================================
        # DADOS DO PRODUTO
        # ==========================================

        dim["produto"] = self._obter_coluna("product_name")

        dim["categoria"] = self._obter_coluna("category")

        dim["marca"] = self._obter_coluna("brand")

        dim["fornecedor"] = self._obter_coluna("supplier")

        # ==========================================
        # CARACTERÍSTICAS
        # ==========================================

        dim["peso_g"] = self._obter_coluna("weight_g")

        dim["comprimento_cm"] = self._obter_coluna("length_cm")

        dim["altura_cm"] = self._obter_coluna("height_cm")

        dim["largura_cm"] = self._obter_coluna("width_cm")

        # ==========================================
        # REMOVER DUPLICADOS
        # ==========================================

        dim = dim.drop_duplicates()

        dim = dim.reset_index(drop=True)

        return dim

    # ==================================================

    def _obter_coluna(
        self,
        coluna: str,
        default=None,
    ) -> pd.Series:
        """
        Retorna uma coluna caso exista.
        Caso contrário, retorna uma série com o valor padrão.
        """

        if coluna in self.df.columns:
            return self.df[coluna]

        return pd.Series(
            [default] * len(self.df),
            index=self.df.index,
        )