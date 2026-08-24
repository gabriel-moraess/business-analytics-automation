from __future__ import annotations

import pandas as pd

from src.analytics.metrics import Metrics


class DashboardData:
    """
    Camada responsável por preparar os dados analíticos
    utilizados pelo Dashboard.

    As regras de negócio permanecem na classe Metrics.
    O Dashboard recebe os dados já processados,
    sem acessar diretamente as regras de negócio.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Inicializa a camada de dados do Dashboard.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame principal da Fato_Vendas.
        """

        self.df = df

    def dados(self) -> dict:
        """
        Retorna todos os conjuntos de dados necessários
        para alimentar o Dashboard Executivo.

        Returns
        -------
        dict
            Dicionário contendo KPIs, rankings,
            análises financeiras, análises por estado
            e análises temporais.
        """

        # =====================================================
        # ANÁLISE DE SELLERS
        # =====================================================

        desempenho_sellers = (
            Metrics.desempenho_sellers(
                self.df
            )
        )

        ranking_sellers = (
            Metrics.ranking_sellers(
                desempenho_sellers
            )
        )

        # =====================================================
        # ANÁLISE FINANCEIRA
        # =====================================================

        indicadores_financeiros = (
            Metrics.indicadores_financeiros(
                self.df
            )
        )

        financeiro_sellers = (
            Metrics.financeiro_sellers(
                self.df
            )
        )

        # =====================================================
        # ANÁLISE TEMPORAL
        # =====================================================

        evolucao_mensal = (
            Metrics.evolucao_mensal(
                self.df
            )
        )

        crescimento_mensal = (
            Metrics.crescimento_mensal(
                evolucao_mensal
            )
        )

        # =====================================================
        # RETORNO PARA O DASHBOARD
        # =====================================================

        return {

            # -------------------------------------------------
            # SELLERS
            # -------------------------------------------------

            "ranking_sellers": ranking_sellers,

            "ranking_frete": (
                Metrics.ranking_frete(
                    desempenho_sellers
                )
            ),

            "ranking_preco_medio": (
                Metrics.ranking_preco_medio(
                    desempenho_sellers
                )
            ),

            "desempenho_estados": (
                Metrics.desempenho_estados(
                    desempenho_sellers
                )
            ),

            "resumo_sellers": (
                Metrics.resumo_sellers(
                    desempenho_sellers
                )
            ),

            # -------------------------------------------------
            # FINANCEIRO
            # -------------------------------------------------

            "indicadores_financeiros": (
                indicadores_financeiros
            ),

            "financeiro_sellers": (
                financeiro_sellers
            ),

            "ranking_margem_sellers": (
                Metrics.ranking_margem_sellers(
                    financeiro_sellers
                )
            ),

            "financeiro_estados": (
                Metrics.financeiro_estados(
                    financeiro_sellers
                )
            ),

            # -------------------------------------------------
            # TEMPORAL
            # -------------------------------------------------

            "evolucao_mensal": (
                evolucao_mensal
            ),

            "crescimento_mensal": (
                crescimento_mensal
            ),

            "resumo_temporal": (
                Metrics.resumo_temporal(
                    evolucao_mensal
                )
            ),

            "ranking_mensal_receita": (
                Metrics.ranking_mensal_receita(
                    evolucao_mensal
                )
            ),

            "ranking_mensal_resultado": (
                Metrics.ranking_mensal_resultado(
                    evolucao_mensal
                )
            ),
        }