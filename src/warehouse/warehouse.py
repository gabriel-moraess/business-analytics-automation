from __future__ import annotations

import pandas as pd

from src.warehouse.dim_customer import DimCustomer
from src.warehouse.dim_date import DimDate
from src.warehouse.dim_product import DimProduct
from src.warehouse.dim_region import DimRegion
from src.warehouse.fact_sales import FactSales


class Warehouse:
    """
    Responsável pela construção do Data Warehouse.

    A partir de um DataFrame tratado, gera todas as tabelas
    analíticas (Fato e Dimensões) utilizadas pelo Dashboard.
    """

    def __init__(
        self,
        df: pd.DataFrame,
    ) -> None:

        self.df = df

    def construir(self) -> dict[str, pd.DataFrame]:
        """
        Constrói todas as tabelas do Data Warehouse.

        Returns:
            Dicionário contendo todas as tabelas analíticas.
        """

        return {

            "fact_sales": FactSales(self.df).construir(),

            "dim_customer": DimCustomer(self.df).construir(),

            "dim_product": DimProduct(self.df).construir(),

            "dim_date": DimDate(self.df).construir(),

            "dim_region": DimRegion(self.df).construir(),

        }