from __future__ import annotations

import pandas as pd


class ManagementAnalytics:
    """
    Camada de analytics gerencial da Sprint 5.7.

    Responsável por gerar:
    - KPIs gerenciais
    - Evolução mensal
    - Análise por categoria
    """

    # =========================================================
    # VALIDAÇÃO
    # =========================================================

    @staticmethod
    def _validar_fato(
        fato_vendas: pd.DataFrame,
    ) -> None:
        """
        Valida se a Fato_Vendas possui as colunas
        necessárias para os cálculos gerenciais.
        """

        colunas_obrigatorias = [
            "order_id",
            "order_item_id",
            "seller_id",
            "order_purchase_timestamp",
            "price",
            "freight_value",
            "receita_item",
            "frete_item",
            "review_score",
        ]

        faltantes = [
            coluna
            for coluna in colunas_obrigatorias
            if coluna not in fato_vendas.columns
        ]

        if faltantes:
            raise ValueError(
                "A Fato_Vendas não possui todas as "
                f"colunas necessárias. Faltantes: {faltantes}"
            )

        if fato_vendas.empty:
            raise ValueError(
                "A Fato_Vendas está vazia."
            )

    # =========================================================
    # KPIs
    # =========================================================

    @staticmethod
    def calcular_kpis(
        fato_vendas: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calcula os principais KPIs gerenciais.
        """

        ManagementAnalytics._validar_fato(
            fato_vendas
        )

        dados = fato_vendas.copy()

        dados["receita_item"] = pd.to_numeric(
            dados["receita_item"],
            errors="coerce",
        ).fillna(0)

        dados["frete_item"] = pd.to_numeric(
            dados["frete_item"],
            errors="coerce",
        ).fillna(0)

        dados["review_score"] = pd.to_numeric(
            dados["review_score"],
            errors="coerce",
        )

        receita_total = (
            dados["receita_item"].sum()
        )

        frete_total = (
            dados["frete_item"].sum()
        )

        receita_com_frete = (
            receita_total + frete_total
        )

        pedidos = (
            dados["order_id"].nunique()
        )

        itens = len(dados)

        sellers = (
            dados["seller_id"].nunique()
        )

        avaliacao_media = (
            dados["review_score"].mean()
        )

        ticket_medio = (
            receita_total / pedidos
            if pedidos > 0
            else 0
        )

        receita_media_item = (
            receita_total / itens
            if itens > 0
            else 0
        )

        frete_medio_item = (
            frete_total / itens
            if itens > 0
            else 0
        )

        frete_percentual = (
            (frete_total / receita_total) * 100
            if receita_total > 0
            else 0
        )

        kpis = {
            "Receita Total": receita_total,
            "Frete Total": frete_total,
            "Receita + Frete": receita_com_frete,
            "Pedidos": pedidos,
            "Itens Vendidos": itens,
            "Sellers": sellers,
            "Ticket Médio": ticket_medio,
            "Receita Média por Item": receita_media_item,
            "Frete Médio por Item": frete_medio_item,
            "Avaliação Média": avaliacao_media,
            "Frete % Receita": frete_percentual,
        }

        resultado = pd.DataFrame(
            [
                {
                    "KPI": chave,
                    "Valor": valor,
                }
                for chave, valor in kpis.items()
            ]
        )

        return resultado

    # =========================================================
    # EVOLUÇÃO MENSAL
    # =========================================================

    @staticmethod
    def evolucao_mensal(
        fato_vendas: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calcula a evolução dos principais indicadores
        por mês.
        """

        ManagementAnalytics._validar_fato(
            fato_vendas
        )

        dados = fato_vendas.copy()

        dados["data_venda"] = pd.to_datetime(
            dados[
                "order_purchase_timestamp"
            ],
            errors="coerce",
        )

        dados = dados[
            dados["data_venda"].notna()
        ].copy()

        dados["receita_item"] = pd.to_numeric(
            dados["receita_item"],
            errors="coerce",
        ).fillna(0)

        dados["frete_item"] = pd.to_numeric(
            dados["frete_item"],
            errors="coerce",
        ).fillna(0)

        dados["review_score"] = pd.to_numeric(
            dados["review_score"],
            errors="coerce",
        )

        dados["Mes"] = (
            dados["data_venda"]
            .dt.to_period("M")
            .astype(str)
        )

        mensal = (
            dados
            .groupby("Mes")
            .agg(
                Pedidos=(
                    "order_id",
                    "nunique",
                ),
                Itens=(
                    "order_item_id",
                    "count",
                ),
                Receita=(
                    "receita_item",
                    "sum",
                ),
                Frete=(
                    "frete_item",
                    "sum",
                ),
                Avaliacao_Media=(
                    "review_score",
                    "mean",
                ),
            )
            .reset_index()
        )

        mensal["Receita_Mais_Frete"] = (
            mensal["Receita"]
            + mensal["Frete"]
        )

        mensal["Ticket_Medio"] = (
            mensal["Receita"]
            / mensal["Pedidos"]
        )

        mensal["Frete_Percentual"] = (
            mensal["Frete"]
            / mensal["Receita"]
            * 100
        )

        mensal["Crescimento_Receita"] = (
            mensal["Receita"]
            .pct_change()
            .fillna(0)
            * 100
        )

        mensal = mensal[
            [
                "Mes",
                "Pedidos",
                "Itens",
                "Receita",
                "Frete",
                "Receita_Mais_Frete",
                "Ticket_Medio",
                "Avaliacao_Media",
                "Frete_Percentual",
                "Crescimento_Receita",
            ]
        ]

        return mensal

    # =========================================================
    # ANÁLISE POR CATEGORIA
    # =========================================================

    @staticmethod
    def por_categoria(
        fato_vendas: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calcula indicadores de performance por categoria.
        """

        ManagementAnalytics._validar_fato(
            fato_vendas
        )

        dados = fato_vendas.copy()

        coluna_categoria = (
            "product_category_name"
        )

        if (
            coluna_categoria
            not in dados.columns
        ):
            coluna_categoria = (
                "product_category_name_produto"
            )

        if (
            coluna_categoria
            not in dados.columns
        ):
            raise ValueError(
                "A Fato_Vendas não possui coluna "
                "de categoria de produto."
            )

        dados[coluna_categoria] = (
            dados[coluna_categoria]
            .fillna("Sem Categoria")
            .astype(str)
            .str.strip()
        )

        dados.loc[
            dados[coluna_categoria] == "",
            coluna_categoria,
        ] = "Sem Categoria"

        dados["receita_item"] = pd.to_numeric(
            dados["receita_item"],
            errors="coerce",
        ).fillna(0)

        dados["frete_item"] = pd.to_numeric(
            dados["frete_item"],
            errors="coerce",
        ).fillna(0)

        categoria = (
            dados
            .groupby(coluna_categoria)
            .agg(
                Itens=(
                    "order_item_id",
                    "count",
                ),
                Pedidos=(
                    "order_id",
                    "nunique",
                ),
                Receita=(
                    "receita_item",
                    "sum",
                ),
                Frete=(
                    "frete_item",
                    "sum",
                ),
            )
            .reset_index()
        )

        categoria = categoria.rename(
            columns={
                coluna_categoria: "Categoria"
            }
        )

        categoria["Ticket_Medio"] = (
            categoria["Receita"]
            / categoria["Pedidos"]
        )

        receita_total = (
            categoria["Receita"].sum()
        )

        categoria["Participacao_Receita"] = (
            categoria["Receita"]
            / receita_total
            * 100
            if receita_total > 0
            else 0
        )

        categoria = categoria.sort_values(
            "Receita",
            ascending=False,
        )

        categoria = categoria.reset_index(
            drop=True
        )

        return categoria

    # =========================================================
    # RESUMO EXECUTIVO
    # =========================================================

    @staticmethod
    def resumo_executivo(
        fato_vendas: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Gera um resumo executivo simplificado
        para utilização futura no Dashboard.
        """

        kpis = (
            ManagementAnalytics.calcular_kpis(
                fato_vendas
            )
        )

        evolucao = (
            ManagementAnalytics.evolucao_mensal(
                fato_vendas
            )
        )

        categoria = (
            ManagementAnalytics.por_categoria(
                fato_vendas
            )
        )

        receita_total = (
            fato_vendas["receita_item"]
            .sum()
        )

        if not evolucao.empty:
            melhor_mes = evolucao.loc[
                evolucao["Receita"].idxmax(),
                "Mes",
            ]

            pior_mes = evolucao.loc[
                evolucao["Receita"].idxmin(),
                "Mes",
            ]

        else:
            melhor_mes = None
            pior_mes = None

        if not categoria.empty:
            melhor_categoria = categoria.iloc[
                0
            ]["Categoria"]

        else:
            melhor_categoria = None

        resultado = pd.DataFrame(
            [
                {
                    "Receita_Total": receita_total,
                    "Melhor_Mes": melhor_mes,
                    "Pior_Mes": pior_mes,
                    "Melhor_Categoria": melhor_categoria,
                    "Quantidade_Categorias": len(
                        categoria
                    ),
                }
            ]
        )

        return resultado