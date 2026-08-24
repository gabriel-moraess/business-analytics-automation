import pandas as pd
import logging


logger = logging.getLogger(__name__)


def calcular_kpis(fato_vendas: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula os principais KPIs comerciais e financeiros
    a partir da Fato_Vendas.
    """

    if fato_vendas.empty:
        raise ValueError("Fato_Vendas está vazia.")

    df = fato_vendas.copy()

    # ---------------------------------------------------------
    # PREPARAÇÃO
    # ---------------------------------------------------------

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce"
    )

    df["receita_item"] = pd.to_numeric(
        df["receita_item"],
        errors="coerce"
    ).fillna(0)

    df["frete_item"] = pd.to_numeric(
        df["frete_item"],
        errors="coerce"
    ).fillna(0)

    # Receita + frete
    df["receita_total_item"] = (
        df["receita_item"] + df["frete_item"]
    )

    # ---------------------------------------------------------
    # KPIs GERAIS
    # ---------------------------------------------------------

    receita = df["receita_item"].sum()

    frete = df["frete_item"].sum()

    receita_total = df["receita_total_item"].sum()

    pedidos = df["order_id"].nunique()

    clientes = df["customer_unique_id"].nunique()

    sellers = df["seller_id"].nunique()

    itens = len(df)

    ticket_medio = (
        receita / pedidos
        if pedidos > 0
        else 0
    )

    frete_percentual = (
        frete / receita
        if receita > 0
        else 0
    )

    itens_por_pedido = (
        itens / pedidos
        if pedidos > 0
        else 0
    )

    receita_por_cliente = (
        receita / clientes
        if clientes > 0
        else 0
    )

    # ---------------------------------------------------------
    # TABELA DE KPIs
    # ---------------------------------------------------------

    kpis = pd.DataFrame(
        {
            "Indicador": [
                "Receita",
                "Frete",
                "Receita + Frete",
                "Pedidos",
                "Clientes",
                "Sellers",
                "Itens vendidos",
                "Ticket médio",
                "Frete % da receita",
                "Itens por pedido",
                "Receita por cliente",
            ],
            "Valor": [
                receita,
                frete,
                receita_total,
                pedidos,
                clientes,
                sellers,
                itens,
                ticket_medio,
                frete_percentual,
                itens_por_pedido,
                receita_por_cliente,
            ],
        }
    )

    return kpis


def calcular_vendas_mensais(
    fato_vendas: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula evolução mensal de vendas.
    """

    df = fato_vendas.copy()

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce"
    )

    df["receita_item"] = pd.to_numeric(
        df["receita_item"],
        errors="coerce"
    ).fillna(0)

    df["frete_item"] = pd.to_numeric(
        df["frete_item"],
        errors="coerce"
    ).fillna(0)

    df["mes"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    mensal = (
        df.groupby("mes")
        .agg(
            Receita=("receita_item", "sum"),
            Frete=("frete_item", "sum"),
            Pedidos=("order_id", "nunique"),
            Itens=("order_id", "count"),
        )
        .reset_index()
    )

    mensal["Receita_Total"] = (
        mensal["Receita"] + mensal["Frete"]
    )

    mensal["Ticket_Medio"] = (
        mensal["Receita"] / mensal["Pedidos"]
    )

    mensal["Frete_Percentual"] = (
        mensal["Frete"] / mensal["Receita"]
    )

    mensal = mensal.sort_values("mes")

    return mensal


def calcular_vendas_por_estado(
    fato_vendas: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula vendas por estado do cliente.
    """

    df = fato_vendas.copy()

    df["receita_item"] = pd.to_numeric(
        df["receita_item"],
        errors="coerce"
    ).fillna(0)

    df["frete_item"] = pd.to_numeric(
        df["frete_item"],
        errors="coerce"
    ).fillna(0)

    estado = (
        df.groupby("customer_state")
        .agg(
            Receita=("receita_item", "sum"),
            Frete=("frete_item", "sum"),
            Pedidos=("order_id", "nunique"),
            Clientes=("customer_unique_id", "nunique"),
        )
        .reset_index()
    )

    estado["Receita_Total"] = (
        estado["Receita"] + estado["Frete"]
    )

    estado["Ticket_Medio"] = (
        estado["Receita"] / estado["Pedidos"]
    )

    estado["Frete_Percentual"] = (
        estado["Frete"] / estado["Receita"]
    )

    estado = estado.sort_values(
        "Receita",
        ascending=False
    )

    return estado


def calcular_vendas_por_categoria(
    fato_vendas: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula vendas por categoria de produto.
    """

    df = fato_vendas.copy()

    # Utiliza a coluna enriquecida pela integração com produtos
    coluna_categoria = "product_category_name_produto"

    if coluna_categoria not in df.columns:
        coluna_categoria = "product_category_name"

    df["receita_item"] = pd.to_numeric(
        df["receita_item"],
        errors="coerce"
    ).fillna(0)

    df["frete_item"] = pd.to_numeric(
        df["frete_item"],
        errors="coerce"
    ).fillna(0)

    df[coluna_categoria] = (
        df[coluna_categoria]
        .fillna("Sem categoria")
        .replace("", "Sem categoria")
    )

    categoria = (
        df.groupby(coluna_categoria)
        .agg(
            Receita=("receita_item", "sum"),
            Frete=("frete_item", "sum"),
            Pedidos=("order_id", "nunique"),
            Itens=("order_id", "count"),
        )
        .reset_index()
    )

    categoria = categoria.rename(
        columns={
            coluna_categoria: "Categoria"
        }
    )

    categoria["Receita_Total"] = (
        categoria["Receita"] + categoria["Frete"]
    )

    categoria["Ticket_Medio"] = (
        categoria["Receita"] / categoria["Pedidos"]
    )

    categoria["Frete_Percentual"] = (
        categoria["Frete"] / categoria["Receita"]
    )

    categoria = categoria.sort_values(
        "Receita",
        ascending=False
    )

    return categoria


def calcular_vendas_por_seller(
    fato_vendas: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula desempenho dos sellers.
    """

    df = fato_vendas.copy()

    df["receita_item"] = pd.to_numeric(
        df["receita_item"],
        errors="coerce"
    ).fillna(0)

    df["frete_item"] = pd.to_numeric(
        df["frete_item"],
        errors="coerce"
    ).fillna(0)

    seller = (
        df.groupby("seller_id")
        .agg(
            Receita=("receita_item", "sum"),
            Frete=("frete_item", "sum"),
            Pedidos=("order_id", "nunique"),
            Itens=("order_id", "count"),
            Avaliacao_Media=("review_score", "mean"),
        )
        .reset_index()
    )

    seller["Receita_Total"] = (
        seller["Receita"] + seller["Frete"]
    )

    seller["Ticket_Medio"] = (
        seller["Receita"] / seller["Pedidos"]
    )

    seller["Frete_Percentual"] = (
        seller["Frete"] / seller["Receita"]
    )

    seller = seller.sort_values(
        "Receita",
        ascending=False
    )

    return seller


def gerar_analises(
    fato_vendas: pd.DataFrame
) -> dict:
    """
    Executa todas as análises e retorna
    os DataFrames organizados.
    """

    logger.info("Iniciando camada de Analytics.")

    resultados = {
        "KPIs": calcular_kpis(fato_vendas),
        "Vendas_Mensais": calcular_vendas_mensais(
            fato_vendas
        ),
        "Vendas_Estado": calcular_vendas_por_estado(
            fato_vendas
        ),
        "Vendas_Categoria": calcular_vendas_por_categoria(
            fato_vendas
        ),
        "Vendas_Seller": calcular_vendas_por_seller(
            fato_vendas
        ),
    }

    logger.info(
        "Camada de Analytics concluída."
    )

    return resultados