from __future__ import annotations

from datetime import datetime
import json

import pandas as pd

from src.utils.logger import logger


class Transform:
    """
    Responsável pelas transformações dos dados.

    Esta classe recebe um DataFrame proveniente da camada
    de Staging e aplica regras de padronização, limpeza
    e enriquecimento dos dados.
    """

    @staticmethod
    def json_para_dataframe(
        dados,
    ) -> pd.DataFrame:
        """
        Converte dados JSON em DataFrame.

        Aceita:
        - lista de dicionários
        - dicionário
        - string JSON
        """

        if isinstance(dados, str):
            try:
                dados = json.loads(dados)
            except json.JSONDecodeError as erro:
                raise ValueError(
                    "JSON inválido."
                ) from erro

        if isinstance(dados, pd.DataFrame):
            return dados.copy()

        if isinstance(dados, list):
            return pd.DataFrame(dados)

        if isinstance(dados, dict):
            return pd.DataFrame(dados)

        raise TypeError(
            "Os dados devem ser JSON, lista, "
            "dicionário ou DataFrame."
        )

    @staticmethod
    def remover_duplicados(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Remove registros duplicados.
        """

        quantidade = len(df)

        df = df.drop_duplicates().copy()

        removidos = quantidade - len(df)

        logger.info(
            "Duplicados removidos: %s",
            removidos,
        )

        return df

    @staticmethod
    def padronizar_colunas(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Padroniza os nomes das colunas.

        Regras:
        - remove espaços no início/fim
        - converte para minúsculas
        - substitui espaços por _
        - substitui hífens por _
        - substitui pontos por _
        """

        df = df.copy()

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
            .str.replace(".", "_", regex=False)
        )

        logger.info(
            "Colunas padronizadas."
        )

        return df

    @staticmethod
    def converter_datas(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Converte automaticamente colunas contendo
        'date' ou 'timestamp' para datetime.
        """

        df = df.copy()

        for coluna in df.columns:

            if (
                "date" in coluna
                or "timestamp" in coluna
            ):

                try:

                    df[coluna] = pd.to_datetime(
                        df[coluna],
                        errors="coerce",
                    )

                except Exception:

                    logger.warning(
                        "Não foi possível converter '%s' "
                        "para datetime.",
                        coluna,
                    )

        return df

    @staticmethod
    def adicionar_metadados(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Adiciona metadados ao DataFrame.
        """

        df = df.copy()

        agora = datetime.now()

        df["data_coleta"] = agora

        df["data_processamento"] = agora

        logger.info(
            "Metadados adicionados ao DataFrame."
        )

        return df

    @staticmethod
    def ordenar_colunas(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Ordena alfabeticamente as colunas.
        """

        return df.reindex(
            sorted(df.columns),
            axis=1,
        )

    @staticmethod
    def executar(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Executa todas as transformações do DataFrame.
        """

        logger.info("=" * 60)
        logger.info(
            "INICIANDO TRANSFORMAÇÕES"
        )
        logger.info("=" * 60)

        df = Transform.remover_duplicados(df)

        df = Transform.padronizar_colunas(df)

        df = Transform.converter_datas(df)

        df = Transform.adicionar_metadados(df)

        df = Transform.ordenar_colunas(df)

        logger.info(
            "Transformações finalizadas."
        )

        return df