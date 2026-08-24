from __future__ import annotations

import pandas as pd


class DataModel:
    """
    Modelo central de dados da aplicação.

    Centraliza todas as entidades carregadas pelo Pipeline.
    """

    def __init__(self) -> None:

        self.orders = pd.DataFrame()
        self.order_items = pd.DataFrame()
        self.customers = pd.DataFrame()
        self.products = pd.DataFrame()
        self.payments = pd.DataFrame()
        self.reviews = pd.DataFrame()
        self.sellers = pd.DataFrame()
        self.geolocation = pd.DataFrame()

    @property
    def total_tabelas(self) -> int:
        """
        Quantidade total de entidades do modelo.
        """
        return 8

    def carregar(
        self,
        nome: str,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Carrega um DataFrame em uma entidade do modelo.

        Exemplo:
            model.carregar("orders", df)
        """

        if not hasattr(self, nome):

            raise AttributeError(
                f"Entidade '{nome}' não existe no DataModel."
            )

        setattr(self, nome, dataframe)

    def obter(
        self,
        nome: str,
    ) -> pd.DataFrame:
        """
        Retorna uma entidade do modelo.
        """

        if not hasattr(self, nome):

            raise AttributeError(
                f"Entidade '{nome}' não existe."
            )

        return getattr(self, nome)

    def resumo(self) -> pd.DataFrame:
        """
        Resumo das entidades carregadas.
        """

        return pd.DataFrame(
            {
                "Entidade": [
                    "orders",
                    "order_items",
                    "customers",
                    "products",
                    "payments",
                    "reviews",
                    "sellers",
                    "geolocation",
                ],
                "Registros": [
                    len(self.orders),
                    len(self.order_items),
                    len(self.customers),
                    len(self.products),
                    len(self.payments),
                    len(self.reviews),
                    len(self.sellers),
                    len(self.geolocation),
                ],
            }
        )

    def limpar(self) -> None:
        """
        Limpa todas as entidades carregadas.
        """

        self.__init__()