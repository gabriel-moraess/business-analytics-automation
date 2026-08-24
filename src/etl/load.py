from pathlib import Path

import pandas as pd

from src.utils.config import DADOS_TRATADO
from src.utils.logger import logger


class Load:
    """
    Responsável por exportar DataFrames para diferentes formatos.

    Atualmente suporta:

    - CSV
    - Excel
    - Parquet
    """

    def __init__(self) -> None:
        self.output_dir = DADOS_TRATADO

    def exportar_csv(
        self,
        df: pd.DataFrame,
        nome_arquivo: str
    ) -> Path:
        """
        Exporta o DataFrame para CSV.
        """

        caminho = self.output_dir / f"{nome_arquivo}.csv"

        logger.info(f"Exportando CSV: {caminho}")

        df.to_csv(
            caminho,
            index=False,
            encoding="utf-8-sig"
        )

        return caminho

    def exportar_excel(
        self,
        df: pd.DataFrame,
        nome_arquivo: str
    ) -> Path:
        """
        Exporta o DataFrame para Excel.
        """

        caminho = self.output_dir / f"{nome_arquivo}.xlsx"

        logger.info(f"Exportando Excel: {caminho}")

        df.to_excel(
            caminho,
            index=False
        )

        return caminho

    def exportar_parquet(
        self,
        df: pd.DataFrame,
        nome_arquivo: str
    ) -> Path:
        """
        Exporta o DataFrame para Parquet.
        """

        caminho = self.output_dir / f"{nome_arquivo}.parquet"

        logger.info(f"Exportando Parquet: {caminho}")

        df.to_parquet(
            caminho,
            index=False
        )

        return caminho

    def exportar_todos(
        self,
        df: pd.DataFrame,
        nome_arquivo: str
    ) -> None:
        """
        Exporta o DataFrame para todos os formatos suportados.
        """

        logger.info("Iniciando exportação dos arquivos...")

        self.exportar_csv(df, nome_arquivo)
        self.exportar_excel(df, nome_arquivo)
        self.exportar_parquet(df, nome_arquivo)

        logger.info("Exportações finalizadas com sucesso.")