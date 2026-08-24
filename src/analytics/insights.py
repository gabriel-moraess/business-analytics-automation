from __future__ import annotations

import logging
from typing import Any

import pandas as pd


logger = logging.getLogger(__name__)


class Insights:
    """
    Geração de Insights Gerenciais para o projeto
    Business Analytics Automation.

    Sprint 5.11
    """

    # =====================================================
    # CONFIGURAÇÕES
    # =====================================================

    LIMITE_FRETE_ALTO = 20.0

    LIMITE_FRETE_MUITO_ALTO = 25.0

    LIMITE_CONCENTRACAO = 50.0

    LIMITE_MARGEM_BAIXA = 70.0

    MINIMO_ITENS_SELLER = 100

    # =====================================================
    # MÉTODO PRINCIPAL
    # =====================================================

    @classmethod
    def gerar(
        cls,
        fato_vendas: pd.DataFrame,
        indicadores_financeiros: dict[str, Any],
        ranking_sellers: pd.DataFrame | None = None,
        financeiro_sellers: pd.DataFrame | None = None,
        financeiro_estados: pd.DataFrame | None = None,
    ) -> pd.DataFrame:

        """
        Gera um DataFrame estruturado contendo os
        principais insights gerenciais.

        Cada insight possui:

        - Categoria
        - Tipo
        - Título
        - Insight
        - Indicador
        - Valor
        - Recomendação
        """

        logger.info(
            "ETAPA ATUAL: "
            "Geração dos Insights Gerenciais"
        )

        insights: list[dict[str, Any]] = []

        # =================================================
        # 1. FINANCEIRO
        # =================================================

        insights.extend(
            cls._insights_financeiros(
                indicadores_financeiros
            )
        )

        # =================================================
        # 2. FRETE
        # =================================================

        insights.extend(
            cls._insights_frete(
                indicadores_financeiros
            )
        )

        # =================================================
        # 3. TICKET
        # =================================================

        insights.extend(
            cls._insights_ticket(
                indicadores_financeiros
            )
        )

        # =================================================
        # 4. SELLERS
        # =================================================

        insights.extend(
            cls._insights_sellers(
                ranking_sellers,
                financeiro_sellers,
            )
        )

        # =================================================
        # 5. ESTADOS
        # =================================================

        insights.extend(
            cls._insights_estados(
                financeiro_estados
            )
        )

        # =================================================
        # 6. CONCENTRAÇÃO
        # =================================================

        insights.extend(
            cls._insight_concentracao(
                financeiro_sellers,
                indicadores_financeiros,
            )
        )

        # =================================================
        # DATAFRAME FINAL
        # =================================================

        if not insights:

            return pd.DataFrame(
                columns=[
                    "Categoria",
                    "Tipo",
                    "Titulo",
                    "Insight",
                    "Indicador",
                    "Valor",
                    "Recomendacao",
                ]
            )

        resultado = pd.DataFrame(
            insights
        )

        logger.info(
            "Insights gerados: "
            f"{len(resultado)}"
        )

        cls._exibir_console(
            resultado
        )

        return resultado

    # =====================================================
    # FINANCEIRO
    # =====================================================

    @classmethod
    def _insights_financeiros(
        cls,
        indicadores: dict[str, Any],
    ) -> list[dict[str, Any]]:

        resultado = []

        receita = cls._numero(
            indicadores.get(
                "receita_bruta",
                0,
            )
        )

        resultado_frete = cls._numero(
            indicadores.get(
                "resultado_apos_frete",
                0,
            )
        )

        margem = cls._numero(
            indicadores.get(
                "margem_apos_frete",
                0,
            )
        )

        resultado.append(
            cls._criar_insight(
                categoria="Financeiro",
                tipo="Positivo",
                titulo="Resultado após frete",
                insight=(
                    "A operação apresentou "
                    f"R$ {receita:,.2f} de receita bruta "
                    "e "
                    f"R$ {resultado_frete:,.2f} "
                    "de resultado após frete, "
                    f"com margem de {margem:.2f}%."
                ),
                indicador="Margem após frete",
                valor=margem,
                recomendacao=(
                    "Manter o acompanhamento "
                    "da margem e avaliar "
                    "periodicamente a evolução "
                    "do custo logístico."
                ),
            )
        )

        return resultado

    # =====================================================
    # FRETE
    # =====================================================

    @classmethod
    def _insights_frete(
        cls,
        indicadores: dict[str, Any],
    ) -> list[dict[str, Any]]:

        resultado = []

        frete_percentual = cls._numero(
            indicadores.get(
                "frete_percentual",
                0,
            )
        )

        frete_total = cls._numero(
            indicadores.get(
                "frete_total",
                0,
            )
        )

        if frete_percentual >= cls.LIMITE_FRETE_MUITO_ALTO:

            tipo = "Crítico"

            recomendacao = (
                "Investigar imediatamente "
                "os principais componentes "
                "do custo logístico."
            )

        elif frete_percentual >= cls.LIMITE_FRETE_ALTO:

            tipo = "Atenção"

            recomendacao = (
                "Avaliar sellers, estados "
                "e categorias com maior "
                "impacto proporcional de frete."
            )

        else:

            tipo = "Normal"

            recomendacao = (
                "Continuar monitorando "
                "o custo de frete "
                "sobre a receita."
            )

        resultado.append(
            cls._criar_insight(
                categoria="Frete",
                tipo=tipo,
                titulo="Impacto do frete",
                insight=(
                    f"O frete total foi de "
                    f"R$ {frete_total:,.2f}, "
                    f"representando "
                    f"{frete_percentual:.2f}% "
                    "da receita."
                ),
                indicador="Frete sobre receita",
                valor=frete_percentual,
                recomendacao=recomendacao,
            )
        )

        return resultado

    # =====================================================
    # TICKET
    # =====================================================

    @classmethod
    def _insights_ticket(
        cls,
        indicadores: dict[str, Any],
    ) -> list[dict[str, Any]]:

        resultado = []

        ticket = cls._numero(
            indicadores.get(
                "ticket_medio_pedido",
                0,
            )
        )

        pedidos = int(
            cls._numero(
                indicadores.get(
                    "total_pedidos",
                    0,
                )
            )
        )

        resultado.append(
            cls._criar_insight(
                categoria="Ticket",
                tipo="Informativo",
                titulo="Ticket médio",
                insight=(
                    f"O ticket médio por pedido "
                    f"foi de R$ {ticket:,.2f}, "
                    f"considerando {pedidos:,} "
                    "pedidos analisados."
                ),
                indicador="Ticket médio por pedido",
                valor=ticket,
                recomendacao=(
                    "Avaliar oportunidades de "
                    "aumento de ticket por meio "
                    "de venda cruzada, kits e "
                    "produtos complementares."
                ),
            )
        )

        return resultado

    # =====================================================
    # SELLERS
    # =====================================================

    @classmethod
    def _insights_sellers(
        cls,
        ranking_sellers: pd.DataFrame | None,
        financeiro_sellers: pd.DataFrame | None,
    ) -> list[dict[str, Any]]:

        resultado = []

        # -------------------------------------------------
        # TOP SELLER
        # -------------------------------------------------

        if (
            ranking_sellers is not None
            and not ranking_sellers.empty
        ):

            dados = ranking_sellers.copy()

            coluna_receita = (
                cls._encontrar_coluna(
                    dados,
                    [
                        "receita_bruta",
                        "receita",
                        "total_receita",
                    ],
                )
            )

            coluna_seller = (
                cls._encontrar_coluna(
                    dados,
                    [
                        "seller_id",
                        "seller",
                    ],
                )
            )

            if (
                coluna_receita
                and coluna_seller
            ):

                dados[coluna_receita] = pd.to_numeric(
                    dados[coluna_receita],
                    errors="coerce",
                )

                dados = dados.dropna(
                    subset=[
                        coluna_receita
                    ]
                )

                if not dados.empty:

                    melhor = dados.sort_values(
                        coluna_receita,
                        ascending=False,
                    ).iloc[0]

                    seller = str(
                        melhor[
                            coluna_seller
                        ]
                    )

                    receita = cls._numero(
                        melhor[
                            coluna_receita
                        ]
                    )

                    resultado.append(
                        cls._criar_insight(
                            categoria="Sellers",
                            tipo="Positivo",
                            titulo="Seller líder em receita",
                            insight=(
                                f"O seller {seller} "
                                f"lidera o ranking com "
                                f"R$ {receita:,.2f} "
                                "em receita."
                            ),
                            indicador="Receita do líder",
                            valor=receita,
                            recomendacao=(
                                "Avaliar os fatores "
                                "que explicam o desempenho "
                                "do seller e verificar "
                                "se práticas semelhantes "
                                "podem ser replicadas."
                            ),
                        )
                    )

        # -------------------------------------------------
        # MARGEM
        # -------------------------------------------------

        if (
            financeiro_sellers is not None
            and not financeiro_sellers.empty
        ):

            dados = financeiro_sellers.copy()

            coluna_margem = (
                cls._encontrar_coluna(
                    dados,
                    [
                        "margem_percentual",
                        "margem",
                        "margem_apos_frete",
                    ],
                )
            )

            coluna_seller = (
                cls._encontrar_coluna(
                    dados,
                    [
                        "seller_id",
                        "seller",
                    ],
                )
            )

            if (
                coluna_margem
                and coluna_seller
            ):

                dados[coluna_margem] = pd.to_numeric(
                    dados[coluna_margem],
                    errors="coerce",
                )

                dados = dados.dropna(
                    subset=[
                        coluna_margem
                    ]
                )

                if not dados.empty:

                    melhor = dados.sort_values(
                        coluna_margem,
                        ascending=False,
                    ).iloc[0]

                    seller = str(
                        melhor[
                            coluna_seller
                        ]
                    )

                    margem = cls._numero(
                        melhor[
                            coluna_margem
                        ]
                    )

                    resultado.append(
                        cls._criar_insight(
                            categoria="Margem",
                            tipo="Positivo",
                            titulo="Maior margem entre sellers",
                            insight=(
                                f"O seller {seller} "
                                f"apresentou a maior margem "
                                f"observada, de "
                                f"{margem:.2f}%."
                            ),
                            indicador="Maior margem",
                            valor=margem,
                            recomendacao=(
                                "Investigar a composição "
                                "de preços, frete e mix "
                                "de produtos desse seller."
                            ),
                        )
                    )

                    # -------------------------------------
                    # SELLER COM BAIXA MARGEM
                    # -------------------------------------

                    menor = dados.sort_values(
                        coluna_margem,
                        ascending=True,
                    ).iloc[0]

                    seller_menor = str(
                        menor[
                            coluna_seller
                        ]
                    )

                    margem_menor = cls._numero(
                        menor[
                            coluna_margem
                        ]
                    )

                    if (
                        margem_menor
                        < cls.LIMITE_MARGEM_BAIXA
                    ):

                        resultado.append(
                            cls._criar_insight(
                                categoria="Margem",
                                tipo="Atenção",
                                titulo="Seller com baixa margem",
                                insight=(
                                    f"O seller "
                                    f"{seller_menor} "
                                    f"apresentou margem "
                                    f"de {margem_menor:.2f}%, "
                                    "abaixo do nível "
                                    "de referência."
                                ),
                                indicador="Menor margem",
                                valor=margem_menor,
                                recomendacao=(
                                    "Avaliar preços, "
                                    "frete e composição "
                                    "do mix de produtos "
                                    "desse seller."
                                ),
                            )
                        )

        return resultado

    # =====================================================
    # ESTADOS
    # =====================================================

    @classmethod
    def _insights_estados(
        cls,
        financeiro_estados: pd.DataFrame | None,
    ) -> list[dict[str, Any]]:

        resultado = []

        if (
            financeiro_estados is None
            or financeiro_estados.empty
        ):

            return resultado

        dados = financeiro_estados.copy()

        coluna_estado = (
            cls._encontrar_coluna(
                dados,
                [
                    "seller_state",
                    "state",
                    "estado",
                ],
            )
        )

        coluna_receita = (
            cls._encontrar_coluna(
                dados,
                [
                    "receita_bruta",
                    "receita",
                    "total_receita",
                ],
            )
        )

        if (
            coluna_estado
            and coluna_receita
        ):

            dados[coluna_receita] = pd.to_numeric(
                dados[coluna_receita],
                errors="coerce",
            )

            dados = dados.dropna(
                subset=[
                    coluna_receita
                ]
            )

            if not dados.empty:

                melhor = dados.sort_values(
                    coluna_receita,
                    ascending=False,
                ).iloc[0]

                estado = str(
                    melhor[
                        coluna_estado
                    ]
                )

                receita = cls._numero(
                    melhor[
                        coluna_receita
                    ]
                )

                resultado.append(
                    cls._criar_insight(
                        categoria="Geografia",
                        tipo="Positivo",
                        titulo="Estado líder em receita",
                        insight=(
                            f"O estado {estado} "
                            f"apresentou a maior receita, "
                            f"com R$ {receita:,.2f}."
                        ),
                        indicador="Maior receita estadual",
                        valor=receita,
                        recomendacao=(
                            "Avaliar a participação "
                            "do estado na estratégia "
                            "comercial e logística."
                        ),
                    )
                )

        return resultado

    # =====================================================
    # CONCENTRAÇÃO
    # =====================================================

    @classmethod
    def _insight_concentracao(
        cls,
        financeiro_sellers: pd.DataFrame | None,
        indicadores: dict[str, Any],
    ) -> list[dict[str, Any]]:

        resultado = []

        if (
            financeiro_sellers is None
            or financeiro_sellers.empty
        ):

            return resultado

        dados = financeiro_sellers.copy()

        coluna_receita = (
            cls._encontrar_coluna(
                dados,
                [
                    "receita_bruta",
                    "receita",
                    "total_receita",
                ],
            )
        )

        if not coluna_receita:

            return resultado

        dados[coluna_receita] = pd.to_numeric(
            dados[coluna_receita],
            errors="coerce",
        )

        dados = dados.dropna(
            subset=[
                coluna_receita
            ]
        )

        if dados.empty:

            return resultado

        receita_total = cls._numero(
            indicadores.get(
                "receita_bruta",
                0,
            )
        )

        if receita_total <= 0:

            return resultado

        top_10_receita = (
            dados
            .sort_values(
                coluna_receita,
                ascending=False,
            )
            .head(10)[
                coluna_receita
            ]
            .sum()
        )

        concentracao = (
            top_10_receita
            /
            receita_total
            *
            100
        )

        if (
            concentracao
            >= cls.LIMITE_CONCENTRACAO
        ):

            tipo = "Atenção"

            recomendacao = (
                "Avaliar risco de concentração "
                "e desenvolver estratégias "
                "para diversificar a base "
                "de sellers."
            )

        else:

            tipo = "Normal"

            recomendacao = (
                "Continuar monitorando "
                "a concentração da receita "
                "entre sellers."
            )

        resultado.append(
            cls._criar_insight(
                categoria="Concentração",
                tipo=tipo,
                titulo="Concentração nos Top 10 sellers",
                insight=(
                    f"Os 10 maiores sellers "
                    f"representam "
                    f"{concentracao:.2f}% "
                    "da receita total analisada."
                ),
                indicador="Receita Top 10",
                valor=concentracao,
                recomendacao=recomendacao,
            )
        )

        return resultado

    # =====================================================
    # CRIAÇÃO DO INSIGHT
    # =====================================================

    @staticmethod
    def _criar_insight(
        categoria: str,
        tipo: str,
        titulo: str,
        insight: str,
        indicador: str,
        valor: float,
        recomendacao: str,
    ) -> dict[str, Any]:

        return {

            "Categoria": categoria,

            "Tipo": tipo,

            "Titulo": titulo,

            "Insight": insight,

            "Indicador": indicador,

            "Valor": valor,

            "Recomendacao": recomendacao,
        }

    # =====================================================
    # UTILITÁRIOS
    # =====================================================

    @staticmethod
    def _numero(
        valor: Any,
    ) -> float:

        try:

            if pd.isna(valor):

                return 0.0

            return float(valor)

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # =====================================================

    @staticmethod
    def _encontrar_coluna(
        df: pd.DataFrame,
        possibilidades: list[str],
    ) -> str | None:

        for coluna in possibilidades:

            if coluna in df.columns:

                return coluna

        return None

    # =====================================================

    @staticmethod
    def _exibir_console(
        insights: pd.DataFrame,
    ) -> None:

        print()
        print("=" * 80)

        print(
            "INSIGHTS GERENCIAIS AVANÇADOS"
        )

        print("=" * 80)

        for indice, linha in insights.iterrows():

            print()

            print(
                f"{indice + 1}. "
                f"[{linha['Tipo']}] "
                f"{linha['Titulo']}"
            )

            print(
                f"   {linha['Insight']}"
            )

            print(
                f"   Recomendação: "
                f"{linha['Recomendacao']}"
            )

        print()