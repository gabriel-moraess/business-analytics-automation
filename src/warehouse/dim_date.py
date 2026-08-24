from __future__ import annotations

import pandas as pd


class DimDate:
    """
    Constrói a Dimensão Tempo.

    A dimensão tempo permite análises temporais
    utilizadas pelo Dashboard Executivo.
    """

    def __init__(
        self,
        df: pd.DataFrame,
    ) -> None:

        self.df = df.copy()

    def construir(self) -> pd.DataFrame:
        """
        Constrói a dimensão Tempo.

        Returns:
            DataFrame contendo os atributos de calendário.
        """

        coluna_data = self._identificar_coluna_data()

        if coluna_data is None:
            return pd.DataFrame()

        datas = pd.to_datetime(
            self.df[coluna_data],
            errors="coerce",
        )

        dim = pd.DataFrame()

        dim["data"] = datas

        dim["ano"] = datas.dt.year

        dim["semestre"] = datas.dt.month.apply(
            lambda mes: 1 if pd.notna(mes) and mes <= 6 else (
                2 if pd.notna(mes) else None
            )
        )

        dim["trimestre"] = datas.dt.quarter

        dim["mes"] = datas.dt.month

        dim["nome_mes"] = datas.dt.month_name(locale="pt_BR")

        dim["semana"] = datas.dt.isocalendar().week.astype("Int64")

        dim["dia"] = datas.dt.day

        dim["dia_semana"] = datas.dt.dayofweek + 1

        dim["nome_dia"] = datas.dt.day_name(locale="pt_BR")

        dim["fim_de_semana"] = (
            datas.dt.dayofweek >= 5
        )

        dim = dim.drop_duplicates()

        dim = dim.sort_values("data")

        dim = dim.reset_index(drop=True)

        return dim

    # =====================================================

    def _identificar_coluna_data(
        self,
    ) -> str | None:
        """
        Identifica automaticamente a melhor coluna de data.
        """

        prioridades = [

            "purchase_timestamp",

            "order_purchase_timestamp",

            "data_pedido",

            "data",

            "data_coleta",

            "data_processamento",

        ]

        for coluna in prioridades:

            if coluna in self.df.columns:

                return coluna

        return None