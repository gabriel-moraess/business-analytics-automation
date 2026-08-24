from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.sources.base_source import BaseSource
from src.utils.logger import logger


class CSVSource(BaseSource):
    """
    Fonte de dados baseada em arquivos CSV.

    Esta classe permite que o Pipeline leia qualquer arquivo CSV
    mantendo a mesma interface das demais fontes de dados.
    """

    def __init__(
        self,
        base_path: str | Path,
    ) -> None:

        self.base_path = Path(base_path)

    @property
    def source_name(self) -> str:
        return "CSV"

    def connect(self) -> None:
        """
        Não é necessário conectar em arquivos locais.
        """

        logger.info("Fonte CSV inicializada.")

    def disconnect(self) -> None:
        """
        Não há conexão para encerrar.
        """

        logger.info("Fonte CSV finalizada.")

    def read(
        self,
        resource: str,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Lê um arquivo CSV.

        Parameters
        ----------
        resource
            Nome do arquivo.

        Returns
        -------
        pd.DataFrame
        """

        arquivo = self.base_path / resource

        logger.info("Lendo arquivo: %s", arquivo)

        if not arquivo.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {arquivo}"
            )

        df = pd.read_csv(
            arquivo,
            **kwargs,
        )

        logger.info(
            "%s registros carregados.",
            len(df),
        )

        return df