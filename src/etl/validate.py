from __future__ import annotations

import pandas as pd

from src.utils.logger import logger


class DataValidator:
    """
    Responsável pela validação dos dados.

    Todas as validações do projeto devem ser centralizadas
    nesta classe.
    """

    @staticmethod
    def validar_dataframe(
        df: pd.DataFrame,
        obrigatorias: list[str] | None = None,
    ) -> None:
        """
        Executa todas as validações do DataFrame.
        """

        logger.info("=" * 60)
        logger.info("INICIANDO VALIDAÇÃO")
        logger.info("=" * 60)

        DataValidator.validar_dataframe_vazio(df)

        DataValidator.validar_colunas(df)

        if obrigatorias:

            DataValidator.validar_colunas_obrigatorias(
                df,
                obrigatorias,
            )

        DataValidator.validar_nulos(df)

        DataValidator.validar_duplicados(df)

        DataValidator.resumo(df)

        logger.info(
            "Validação concluída com sucesso."
        )

    # ==========================================================
    # DATAFRAME
    # ==========================================================

    @staticmethod
    def validar_dataframe_vazio(
        df: pd.DataFrame,
    ) -> None:
        """
        Verifica se o DataFrame está vazio.
        """

        if df.empty:

            raise ValueError(
                "O DataFrame está vazio."
            )

        logger.info(
            "DataFrame contém %s registros.",
            len(df),
        )

    # ==========================================================
    # COLUNAS
    # ==========================================================

    @staticmethod
    def validar_colunas(
        df: pd.DataFrame,
        colunas_esperadas: list[str] | None = None,
    ) -> None:
        """
        Verifica se existem colunas.

        Se colunas_esperadas for informado,
        também valida se todas estão presentes.
        """

        if len(df.columns) == 0:

            raise ValueError(
                "O DataFrame não possui colunas."
            )

        if colunas_esperadas:

            faltando = [
                coluna
                for coluna in colunas_esperadas
                if coluna not in df.columns
            ]

            if faltando:

                raise ValueError(
                    "Colunas obrigatórias ausentes: "
                    f"{faltando}"
                )

        logger.info(
            "%s colunas encontradas.",
            len(df.columns),
        )

    @staticmethod
    def validar_colunas_obrigatorias(
        df: pd.DataFrame,
        obrigatorias: list[str],
    ) -> None:
        """
        Valida colunas obrigatórias.

        Mantém este método por compatibilidade
        com o restante do projeto.
        """

        DataValidator.validar_colunas(
            df,
            obrigatorias,
        )

        logger.info(
            "Todas as colunas obrigatórias "
            "estão presentes."
        )

    # ==========================================================
    # NULOS
    # ==========================================================

    @staticmethod
    def validar_nulos(
        df: pd.DataFrame,
    ) -> None:
        """
        Verifica valores nulos.

        Caso existam valores nulos, lança ValueError.
        """

        nulos = df.isnull().sum()

        nulos = nulos[nulos > 0]

        if len(nulos):

            logger.warning(
                "Valores nulos encontrados:"
            )

            logger.warning(
                "\n%s",
                nulos,
            )

            raise ValueError(
                "Valores nulos encontrados: "
                f"{nulos.to_dict()}"
            )

        logger.info(
            "Nenhum valor nulo encontrado."
        )

    # ==========================================================
    # DUPLICADOS
    # ==========================================================

    @staticmethod
    def validar_duplicados(
        df: pd.DataFrame,
    ) -> None:
        """
        Verifica registros duplicados.

        Caso existam registros duplicados,
        lança ValueError.
        """

        quantidade = df.duplicated().sum()

        if quantidade:

            logger.warning(
                "%s registros duplicados encontrados.",
                quantidade,
            )

            raise ValueError(
                f"{quantidade} registros duplicados encontrados."
            )

        logger.info(
            "Nenhum registro duplicado encontrado."
        )

    # ==========================================================
    # RESUMO
    # ==========================================================

    @staticmethod
    def resumo(
        df: pd.DataFrame,
    ) -> None:
        """
        Exibe resumo da validação.
        """

        logger.info("=" * 60)

        logger.info("RESUMO")

        logger.info(
            "Linhas: %s",
            len(df),
        )

        logger.info(
            "Colunas: %s",
            len(df.columns),
        )

        memoria = (
            df.memory_usage(
                deep=True
            ).sum()
            / 1024
        )

        logger.info(
            "Memória: %.2f KB",
            memoria,
        )

        logger.info("=" * 60)