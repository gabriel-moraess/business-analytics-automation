from __future__ import annotations

import pandas as pd


class Metrics:
    """
    Camada de métricas e análises do projeto.

    Centraliza os cálculos analíticos para evitar
    que regras de negócio fiquem dentro do main.py.

    Sprint 6.0:
    - KPIs de sellers
    - Rankings
    - Análise de frete
    - Análise por estado
    - Indicadores financeiros
    - Análise financeira por seller
    - Análise financeira por estado
    - Análise temporal
    - Crescimento mensal
    """

    # =====================================================
    # KPIs DOS SELLERS
    # =====================================================

    @staticmethod
    def desempenho_sellers(
        order_items: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calcula o desempenho individual dos sellers.
        """

        ranking = (
            order_items
            .groupby(
                [
                    "seller_id",
                    "seller_city",
                    "seller_state",
                ],
                as_index=False,
            )
            .agg(
                receita=("price", "sum"),
                frete=("freight_value", "sum"),
                itens=("order_item_id", "count"),
            )
        )

        ranking["preco_medio_item"] = (
            ranking["receita"]
            / ranking["itens"]
        )

        ranking["frete_medio_item"] = (
            ranking["frete"]
            / ranking["itens"]
        )

        ranking["frete_percentual"] = (
            ranking["frete"]
            / ranking["receita"]
            * 100
        )

        return ranking

    # =====================================================
    # RANKING DE RECEITA
    # =====================================================

    @staticmethod
    def ranking_sellers(
        ranking_sellers: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Retorna os sellers ordenados por receita.
        """

        ranking = (
            ranking_sellers
            .sort_values(
                "receita",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        ranking["ranking"] = (
            ranking.index + 1
        )

        return ranking

    # =====================================================
    # IMPACTO DO FRETE
    # =====================================================

    @staticmethod
    def ranking_frete(
        ranking_sellers: pd.DataFrame,
        minimo_itens: int = 100,
    ) -> pd.DataFrame:
        """
        Retorna sellers com maior impacto
        do frete sobre a receita.
        """

        return (
            ranking_sellers[
                ranking_sellers["itens"] >= minimo_itens
            ]
            .sort_values(
                "frete_percentual",
                ascending=False,
            )
            .reset_index(drop=True)
        )

    # =====================================================
    # PREÇO MÉDIO
    # =====================================================

    @staticmethod
    def ranking_preco_medio(
        ranking_sellers: pd.DataFrame,
        minimo_itens: int = 100,
    ) -> pd.DataFrame:
        """
        Retorna sellers com maior preço médio
        por item.
        """

        return (
            ranking_sellers[
                ranking_sellers["itens"] >= minimo_itens
            ]
            .sort_values(
                "preco_medio_item",
                ascending=False,
            )
            .reset_index(drop=True)
        )

    # =====================================================
    # DESEMPENHO POR ESTADO
    # =====================================================

    @staticmethod
    def desempenho_estados(
        ranking_sellers: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Consolida o desempenho dos sellers por estado.
        """

        estados = (
            ranking_sellers
            .groupby(
                "seller_state",
                as_index=False,
            )
            .agg(
                sellers=("seller_id", "nunique"),
                receita=("receita", "sum"),
                frete=("frete", "sum"),
                itens=("itens", "sum"),
            )
            .sort_values(
                "receita",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        estados["ticket_medio_item"] = (
            estados["receita"]
            / estados["itens"]
        )

        estados["frete_percentual"] = (
            estados["frete"]
            / estados["receita"]
            * 100
        )

        return estados

    # =====================================================
    # RESUMO GERAL DOS SELLERS
    # =====================================================

    @staticmethod
    def resumo_sellers(
        ranking_sellers: pd.DataFrame,
    ) -> dict:
        """
        Retorna os principais indicadores dos sellers.
        """

        receita = ranking_sellers["receita"].sum()

        frete = ranking_sellers["frete"].sum()

        itens = ranking_sellers["itens"].sum()

        return {
            "total_sellers": (
                ranking_sellers[
                    "seller_id"
                ].nunique()
            ),

            "receita_total": receita,

            "frete_total": frete,

            "total_itens": itens,

            "preco_medio_item": (
                receita / itens
                if itens > 0
                else 0
            ),

            "frete_percentual": (
                frete / receita * 100
                if receita > 0
                else 0
            ),
        }

    # =====================================================
    # ANÁLISE FINANCEIRA
    # =====================================================

    @staticmethod
    def indicadores_financeiros(
        order_items: pd.DataFrame,
    ) -> dict:
        """
        Calcula os principais indicadores financeiros
        disponíveis na base Olist.

        A base não possui custo de aquisição dos produtos
        nem despesas operacionais completas.

        Portanto, não é calculada aqui uma margem bruta
        ou líquida contábil real.

        O indicador "resultado_apos_frete" representa
        receita de produtos menos frete.
        """

        receita = (
            pd.to_numeric(
                order_items["price"],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

        frete = (
            pd.to_numeric(
                order_items["freight_value"],
                errors="coerce",
            )
            .fillna(0)
            .sum()
        )

        itens = len(order_items)

        pedidos = (
            order_items["order_id"]
            .nunique()
        )

        resultado_apos_frete = (
            receita - frete
        )

        frete_percentual = (
            frete / receita * 100
            if receita > 0
            else 0
        )

        margem_apos_frete = (
            resultado_apos_frete
            / receita
            * 100
            if receita > 0
            else 0
        )

        ticket_medio_item = (
            receita / itens
            if itens > 0
            else 0
        )

        ticket_medio_pedido = (
            receita / pedidos
            if pedidos > 0
            else 0
        )

        return {
            "receita_bruta": receita,

            "frete_total": frete,

            "resultado_apos_frete": (
                resultado_apos_frete
            ),

            "frete_percentual": (
                frete_percentual
            ),

            "margem_apos_frete": (
                margem_apos_frete
            ),

            "total_itens": itens,

            "total_pedidos": pedidos,

            "ticket_medio_item": (
                ticket_medio_item
            ),

            "ticket_medio_pedido": (
                ticket_medio_pedido
            ),
        }

    # =====================================================
    # ANÁLISE FINANCEIRA POR SELLER
    # =====================================================

    @staticmethod
    def financeiro_sellers(
        order_items: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calcula indicadores financeiros por seller.

        O resultado_apos_frete é uma métrica analítica:
        receita - frete.

        Não representa lucro contábil.
        """

        financeiro = (
            order_items
            .groupby(
                [
                    "seller_id",
                    "seller_city",
                    "seller_state",
                ],
                as_index=False,
            )
            .agg(
                receita=("price", "sum"),
                frete=("freight_value", "sum"),
                itens=("order_item_id", "count"),
            )
        )

        financeiro["resultado_apos_frete"] = (
            financeiro["receita"]
            - financeiro["frete"]
        )

        financeiro["frete_percentual"] = (
            financeiro["frete"]
            / financeiro["receita"]
            * 100
        )

        financeiro["margem_apos_frete"] = (
            financeiro["resultado_apos_frete"]
            / financeiro["receita"]
            * 100
        )

        financeiro["preco_medio_item"] = (
            financeiro["receita"]
            / financeiro["itens"]
        )

        financeiro["frete_medio_item"] = (
            financeiro["frete"]
            / financeiro["itens"]
        )

        return financeiro

    # =====================================================
    # RANKING FINANCEIRO DOS SELLERS
    # =====================================================

    @staticmethod
    def ranking_margem_sellers(
        financeiro_sellers: pd.DataFrame,
        minimo_itens: int = 100,
    ) -> pd.DataFrame:
        """
        Retorna sellers ordenados pela margem
        após frete.

        O filtro mínimo evita que sellers com poucos
        itens distorçam o ranking.
        """

        ranking = (
            financeiro_sellers[
                financeiro_sellers["itens"]
                >= minimo_itens
            ]
            .sort_values(
                "margem_apos_frete",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        ranking["ranking_margem"] = (
            ranking.index + 1
        )

        return ranking

    # =====================================================
    # ANÁLISE FINANCEIRA POR ESTADO
    # =====================================================

    @staticmethod
    def financeiro_estados(
        financeiro_sellers: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Consolida os indicadores financeiros por estado.
        """

        estados = (
            financeiro_sellers
            .groupby(
                "seller_state",
                as_index=False,
            )
            .agg(
                sellers=("seller_id", "nunique"),
                receita=("receita", "sum"),
                frete=("frete", "sum"),
                itens=("itens", "sum"),
            )
        )

        estados["resultado_apos_frete"] = (
            estados["receita"]
            - estados["frete"]
        )

        estados["frete_percentual"] = (
            estados["frete"]
            / estados["receita"]
            * 100
        )

        estados["margem_apos_frete"] = (
            estados["resultado_apos_frete"]
            / estados["receita"]
            * 100
        )

        estados["ticket_medio_item"] = (
            estados["receita"]
            / estados["itens"]
        )

        estados = (
            estados
            .sort_values(
                "resultado_apos_frete",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        return estados

    # =====================================================
    # ANÁLISE TEMPORAL
    # =====================================================

    @staticmethod
    def evolucao_mensal(
        order_items: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Consolida os principais indicadores por mês.

        Utiliza order_purchase_timestamp como referência
        temporal da venda.
        """

        dados = order_items.copy()

        dados["order_purchase_timestamp"] = (
            pd.to_datetime(
                dados["order_purchase_timestamp"],
                errors="coerce",
            )
        )

        dados = dados.dropna(
            subset=["order_purchase_timestamp"]
        )

        dados["mes"] = (
            dados["order_purchase_timestamp"]
            .dt.to_period("M")
            .astype(str)
        )

        mensal = (
            dados
            .groupby(
                "mes",
                as_index=False,
            )
            .agg(
                receita=("price", "sum"),
                frete=("freight_value", "sum"),
                itens=("order_item_id", "count"),
                pedidos=("order_id", "nunique"),
                sellers=("seller_id", "nunique"),
            )
        )

        mensal["resultado_apos_frete"] = (
            mensal["receita"]
            - mensal["frete"]
        )

        mensal["frete_percentual"] = (
            mensal["frete"]
            / mensal["receita"]
            * 100
        )

        mensal["margem_apos_frete"] = (
            mensal["resultado_apos_frete"]
            / mensal["receita"]
            * 100
        )

        mensal["ticket_medio_item"] = (
            mensal["receita"]
            / mensal["itens"]
        )

        mensal["ticket_medio_pedido"] = (
            mensal["receita"]
            / mensal["pedidos"]
        )

        mensal = (
            mensal
            .sort_values("mes")
            .reset_index(drop=True)
        )

        return mensal

    # =====================================================
    # CRESCIMENTO MENSAL
    # =====================================================

    @staticmethod
    def crescimento_mensal(
        evolucao_mensal: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calcula o crescimento mensal dos principais
        indicadores.

        O percentual compara cada mês com o mês anterior.
        """

        crescimento = evolucao_mensal.copy()

        crescimento = (
            crescimento
            .sort_values("mes")
            .reset_index(drop=True)
        )

        crescimento["crescimento_receita"] = (
            crescimento["receita"]
            .pct_change()
            * 100
        )

        crescimento["crescimento_pedidos"] = (
            crescimento["pedidos"]
            .pct_change()
            * 100
        )

        crescimento["crescimento_itens"] = (
            crescimento["itens"]
            .pct_change()
            * 100
        )

        crescimento["crescimento_frete"] = (
            crescimento["frete"]
            .pct_change()
            * 100
        )

        return crescimento

    # =====================================================
    # RESUMO TEMPORAL
    # =====================================================

    @staticmethod
    def resumo_temporal(
        evolucao_mensal: pd.DataFrame,
    ) -> dict:
        """
        Retorna os principais indicadores da evolução
        temporal do negócio.
        """

        if evolucao_mensal.empty:
            return {
                "melhor_mes_receita": None,
                "pior_mes_receita": None,
                "melhor_mes_resultado": None,
                "pior_mes_resultado": None,
                "crescimento_receita_total": 0,
                "meses_analisados": 0,
            }

        dados = (
            evolucao_mensal
            .sort_values("mes")
            .reset_index(drop=True)
        )

        melhor_receita = (
            dados.loc[
                dados["receita"].idxmax()
            ]
        )

        pior_receita = (
            dados.loc[
                dados["receita"].idxmin()
            ]
        )

        melhor_resultado = (
            dados.loc[
                dados["resultado_apos_frete"].idxmax()
            ]
        )

        pior_resultado = (
            dados.loc[
                dados["resultado_apos_frete"].idxmin()
            ]
        )

        primeira_receita = dados.iloc[0]["receita"]

        ultima_receita = dados.iloc[-1]["receita"]

        crescimento_total = (
            (
                ultima_receita
                / primeira_receita
            )
            - 1
        ) * 100 if primeira_receita > 0 else 0

        return {
            "melhor_mes_receita": (
                melhor_receita["mes"]
            ),

            "melhor_mes_receita_valor": (
                melhor_receita["receita"]
            ),

            "pior_mes_receita": (
                pior_receita["mes"]
            ),

            "pior_mes_receita_valor": (
                pior_receita["receita"]
            ),

            "melhor_mes_resultado": (
                melhor_resultado["mes"]
            ),

            "melhor_mes_resultado_valor": (
                melhor_resultado[
                    "resultado_apos_frete"
                ]
            ),

            "pior_mes_resultado": (
                pior_resultado["mes"]
            ),

            "pior_mes_resultado_valor": (
                pior_resultado[
                    "resultado_apos_frete"
                ]
            ),

            "crescimento_receita_total": (
                crescimento_total
            ),

            "meses_analisados": (
                len(dados)
            ),
        }

    # =====================================================
    # RANKING MENSAL
    # =====================================================

    @staticmethod
    def ranking_mensal_receita(
        evolucao_mensal: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Cria ranking dos meses por receita.
        """

        ranking = (
            evolucao_mensal
            .sort_values(
                "receita",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        ranking["ranking_receita"] = (
            ranking.index + 1
        )

        return ranking

    # =====================================================
    # RANKING MENSAL DE RESULTADO
    # =====================================================

    @staticmethod
    def ranking_mensal_resultado(
        evolucao_mensal: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Cria ranking dos meses pelo resultado
        após frete.
        """

        ranking = (
            evolucao_mensal
            .sort_values(
                "resultado_apos_frete",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        ranking["ranking_resultado"] = (
            ranking.index + 1
        )

        return ranking