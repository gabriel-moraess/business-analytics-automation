from __future__ import annotations

import pandas as pd

from src.sources.base_source import BaseSource
from src.utils.logger import logger


class Extract:
    """
    Responsável pela etapa de extração.

    Independente da origem dos dados.
    """

    def __init__(
        self,
        source: BaseSource,
    ) -> None:

        self.source = source

    def executar(
        self,
        resource: str,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Executa a leitura dos dados.

        Parameters
        ----------
        resource
            Nome do recurso.

        Returns
        -------
        pd.DataFrame
        """

        logger.info("=" * 60)
        logger.info("INICIANDO EXTRAÇÃO")
        logger.info("=" * 60)

        self.source.connect()

        try:

            df = self.source.read(
                resource,
                **kwargs,
            )

            logger.info(
                "%s registros extraídos.",
                len(df),
            )

            return df

        finally:

            self.source.disconnect()