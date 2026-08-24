from __future__ import annotations

import pandas as pd


class DimCustomer:
    """
    Constrói a Dimensão Cliente.

    Centraliza todas as informações relacionadas aos clientes
    para utilização no Data Warehouse e no Dashboard.
    """

    def __init__(
        self,
        df: pd.DataFrame,
    ) -> None:

        self.df = df.copy()

    def construir(self) -> pd.DataFrame:
        """
        Constrói a dimensão de clientes.

        Returns:
            DataFrame contendo a dimensão Cliente.
        """

        dim = pd.DataFrame()

        # ==========================================
        # IDENTIFICADORES
        # ==========================================

        dim["cliente_id"] = self._obter_coluna("customer_id")

        # ==========================================
        # DADOS CADASTRAIS
        # ==========================================

        dim["nome"] = self._obter_coluna("name")

        dim["email"] = self._obter_coluna("email")

        dim["telefone"] = self._obter_coluna("phone")

        # ==========================================
        # LOCALIZAÇÃO
        # ==========================================

        dim["cidade"] = self._obter_coluna("address_city")

        dim["estado"] = self._obter_coluna("state")

        dim["cep"] = self._obter_coluna("address_zipcode")

        # ==========================================
        # REMOÇÃO DE DUPLICADOS
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

        Caso contrário, retorna uma série preenchida
        com o valor padrão.
        """

        if coluna in self.df.columns:
            return self.df[coluna]

        return pd.Series(
            [default] * len(self.df),
            index=self.df.index,
        )