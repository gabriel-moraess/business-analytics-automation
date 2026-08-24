from __future__ import annotations

import pandas as pd


class DimRegion:
    """
    Constrói a Dimensão Região.

    Centraliza as informações geográficas para análises
    por cidade, estado e região.
    """

    def __init__(
        self,
        df: pd.DataFrame,
    ) -> None:

        self.df = df.copy()

    def construir(self) -> pd.DataFrame:
        """
        Constrói a dimensão Região.

        Returns:
            DataFrame contendo os dados geográficos.
        """

        dim = pd.DataFrame()

        # ==========================================
        # LOCALIZAÇÃO
        # ==========================================

        dim["cidade"] = self._obter_coluna("address_city")

        dim["estado"] = self._obter_coluna("state")

        dim["cep"] = self._obter_coluna("address_zipcode")

        dim["latitude"] = self._obter_coluna("address_geo_lat")

        dim["longitude"] = self._obter_coluna("address_geo_lng")

        # ==========================================
        # REGIÃO (placeholder)
        # ==========================================

        dim["regiao"] = self._obter_coluna(
            "region",
            default="Não Informada",
        )

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

        Caso contrário retorna uma série contendo
        o valor default.
        """

        if coluna in self.df.columns:
            return self.df[coluna]

        return pd.Series(
            [default] * len(self.df),
            index=self.df.index,
        )