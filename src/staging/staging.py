from __future__ import annotations

import pandas as pd

from src.database.sqlite_manager import SQLiteManager
from src.utils.logger import logger


class Staging:
    """
    Responsável por armazenar os dados brutos no banco SQLite.

    Nenhuma transformação é realizada nesta etapa.
    """

    def __init__(
        self,
        database: SQLiteManager,
    ) -> None:

        self.database = database

    def salvar(
        self,
        df: pd.DataFrame,
        tabela: str,
    ) -> None:
        """
        Salva um DataFrame bruto na camada Staging.

        Parameters
        ----------
        df
            Dados brutos.

        tabela
            Nome da tabela de staging.
        """

        tabela = f"stg_{tabela}"

        logger.info(
            "Salvando dados brutos na tabela '%s'...",
            tabela,
        )

        self.database.salvar_dataframe(
            df=df,
            tabela=tabela,
            if_exists="replace",
        )

        logger.info(
            "Tabela %s criada com sucesso.",
            tabela,
        )