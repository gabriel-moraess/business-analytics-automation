from pathlib import Path
import sqlite3

import pandas as pd

from src.utils.config import (
    DATABASE,
    DATABASE_NAME,
)
from src.utils.logger import logger


class SQLiteManager:
    """
    Gerencia a persistência de dados em banco SQLite.
    """

    MODOS_VALIDOS = {"replace", "append", "fail"}

    def __init__(
        self,
        db_path: Path | None = None,
    ) -> None:
        """
        Inicializa o gerenciador do banco SQLite.

        Args:
            db_path:
                Caminho opcional para um banco de dados.
                Caso não seja informado, utiliza o banco
                padrão definido em config.py.
        """

        if db_path is None:
            self.db_path = DATABASE / DATABASE_NAME
        else:
            self.db_path = Path(db_path)

    def salvar_dataframe(
        self,
        df: pd.DataFrame,
        tabela: str,
        if_exists: str = "replace",
    ) -> None:
        """
        Salva um DataFrame em uma tabela SQLite.

        Args:
            df:
                DataFrame a ser persistido.

            tabela:
                Nome da tabela.

            if_exists:
                Estratégia utilizada caso a tabela já exista.

                replace -> recria a tabela.

                append -> adiciona registros.

                fail -> gera erro.

        Raises:
            ValueError:
                Caso o modo informado seja inválido.
        """

        if if_exists not in self.MODOS_VALIDOS:

            raise ValueError(
                f"Modo '{if_exists}' inválido. "
                f"Utilize um dos seguintes: "
                f"{sorted(self.MODOS_VALIDOS)}"
            )

        logger.info(
            "Salvando %s registros na tabela '%s' (%s)...",
            len(df),
            tabela,
            if_exists,
        )

        try:

            with sqlite3.connect(self.db_path) as conn:

                df.to_sql(
                    name=tabela,
                    con=conn,
                    if_exists=if_exists,
                    index=False,
                )

            logger.info(
                "Dados salvos com sucesso em '%s'.",
                self.db_path,
            )

        except Exception:

            logger.exception(
                "Erro ao salvar dados no SQLite."
            )

            raise