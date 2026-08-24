from __future__ import annotations

import logging
import re
import time
from pathlib import Path

import pandas as pd

from src.analytics.metrics import Metrics
from src.analytics.fact_sales import FactSales
from src.analytics.insights import Insights

from src.integration.order_integrator import OrderIntegrator

from src.loaders.data_loader import DataLoader

from src.sources.csv_source import CSVSource

from src.exporters.excel_exporter import ExcelExporter
from src.exporters.dashboard_excel import DashboardExcel


# =========================================================
# BUSINESS ANALYTICS AUTOMATION
# SPRINT 5.11
# INSIGHTS GERENCIAIS AVANÇADOS
# =========================================================


# =========================================================
# CONFIGURAÇÕES DO CLIENTE
# =========================================================

CLIENTE_NOME = "Gabriel Tecnologia LTDA"


# =========================================================
# CONFIGURAÇÕES DO PERÍODO
# =========================================================

PERIODO_INICIO = None

PERIODO_FIM = None


# =========================================================
# DIRETÓRIOS
# =========================================================

DIRETORIO_RAW = Path(
    "dados/raw/olist"
)

DIRETORIO_SAIDA = Path(
    "dados/processed"
)


# =========================================================
# ARQUIVOS OBRIGATÓRIOS
# =========================================================

ARQUIVOS_OBRIGATORIOS = {

    "orders": "olist_orders_dataset.csv",

    "order_items": "olist_order_items_dataset.csv",

    "customers": "olist_customers_dataset.csv",

    "products": "olist_products_dataset.csv",

    "payments": "olist_order_payments_dataset.csv",

    "reviews": "olist_order_reviews_dataset.csv",

    "sellers": "olist_sellers_dataset.csv",

    "geolocation": "olist_geolocation_dataset.csv",
}


# =========================================================
# ABAS ESPERADAS NO EXCEL
# =========================================================

ABAS_ESPERADAS = [

    "Dashboard",

    "Resumo",

    "Top_Sellers",

    "Frete",

    "Preco_Medio",

    "Por_Estado",

    "Financeiro",

    "Margem_Sellers",

    "Financeiro_Estados",

    "Insights",

    "Fato_Vendas",
]


# =========================================================
# LOG
# =========================================================

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def limpar_nome_arquivo(
    nome: str,
) -> str:

    nome = str(nome).strip()

    nome = re.sub(
        r'[<>:"/\\|?*]',
        "",
        nome,
    )

    nome = re.sub(
        r"\s+",
        " ",
        nome,
    )

    nome = nome.replace(
        " ",
        "_",
    )

    nome = nome.rstrip(
        ". "
    )

    if not nome:

        nome = "Cliente"

    return nome


# =========================================================

def validar_formato_periodo(
    periodo: str,
) -> bool:

    if not isinstance(
        periodo,
        str,
    ):

        return False

    return bool(
        re.fullmatch(
            r"\d{4}-\d{2}",
            periodo,
        )
    )


# =========================================================

def converter_periodo(
    periodo: str,
) -> pd.Period:

    if not validar_formato_periodo(
        periodo
    ):

        raise ValueError(
            f"Período inválido: "
            f"'{periodo}'. "
            "Utilize YYYY-MM."
        )

    try:

        return pd.Period(
            periodo,
            freq="M",
        )

    except Exception as erro:

        raise ValueError(
            f"Período inválido: "
            f"'{periodo}'."
        ) from erro


# =========================================================

def obter_periodo_disponivel(
    fato_vendas: pd.DataFrame,
) -> tuple[str, str]:

    if fato_vendas.empty:

        raise ValueError(
            "A Fato_Vendas está vazia."
        )

    coluna_data = (
        "order_purchase_timestamp"
    )

    if coluna_data not in fato_vendas.columns:

        raise ValueError(
            "A Fato_Vendas não possui "
            f"a coluna '{coluna_data}'."
        )

    datas = pd.to_datetime(

        fato_vendas[
            coluna_data
        ],

        errors="coerce",
    )

    datas = datas.dropna()

    if datas.empty:

        raise ValueError(
            "Não existem datas válidas "
            "na Fato_Vendas."
        )

    return (

        datas.min().strftime(
            "%Y-%m"
        ),

        datas.max().strftime(
            "%Y-%m"
        ),
    )


# =========================================================

def definir_periodo_analise(
    fato_vendas: pd.DataFrame,
    periodo_inicio: str | None,
    periodo_fim: str | None,
) -> tuple[str, str]:

    (
        periodo_disponivel_inicio,
        periodo_disponivel_fim,
    ) = obter_periodo_disponivel(
        fato_vendas
    )

    inicio_disponivel = converter_periodo(
        periodo_disponivel_inicio
    )

    fim_disponivel = converter_periodo(
        periodo_disponivel_fim
    )

    if (
        periodo_inicio is None
        and periodo_fim is None
    ):

        return (

            periodo_disponivel_inicio,

            periodo_disponivel_fim,
        )

    if (
        periodo_inicio is None
        or periodo_fim is None
    ):

        raise ValueError(
            "PERIODO_INICIO e PERIODO_FIM "
            "devem ser preenchidos juntos."
        )

    inicio = converter_periodo(
        periodo_inicio
    )

    fim = converter_periodo(
        periodo_fim
    )

    if inicio > fim:

        raise ValueError(
            "O período inicial não pode "
            "ser maior que o período final."
        )

    if inicio < inicio_disponivel:

        raise ValueError(
            f"O período inicial "
            f"({periodo_inicio}) está antes "
            f"do período disponível "
            f"({periodo_disponivel_inicio})."
        )

    if fim > fim_disponivel:

        raise ValueError(
            f"O período final "
            f"({periodo_fim}) está depois "
            f"do período disponível "
            f"({periodo_disponivel_fim})."
        )

    return (
        periodo_inicio,
        periodo_fim,
    )


# =========================================================

def filtrar_periodo(
    fato_vendas: pd.DataFrame,
    periodo_inicio: str,
    periodo_fim: str,
) -> pd.DataFrame:

    dados = fato_vendas.copy()

    coluna_data = (
        "order_purchase_timestamp"
    )

    if coluna_data not in dados.columns:

        raise ValueError(
            f"A coluna '{coluna_data}' "
            "não existe na Fato_Vendas."
        )

    datas = pd.to_datetime(

        dados[
            coluna_data
        ],

        errors="coerce",
    )

    periodos = datas.dt.to_period(
        "M"
    )

    inicio = converter_periodo(
        periodo_inicio
    )

    fim = converter_periodo(
        periodo_fim
    )

    filtro = (

        (periodos >= inicio)

        &

        (periodos <= fim)
    )

    return dados.loc[
        filtro
    ].copy()


# =========================================================

def gerar_nome_arquivo(
    cliente: str,
    inicio_periodo: str,
    fim_periodo: str,
) -> str:

    cliente_limpo = (
        limpar_nome_arquivo(
            cliente
        )
    )

    return (

        "Business_Analytics_"

        f"{cliente_limpo}_"

        f"{inicio_periodo}_a_"

        f"{fim_periodo}.xlsx"
    )


# =========================================================

def validar_configuracoes() -> None:

    logger.info(
        "ETAPA ATUAL: "
        "Validação das configurações"
    )

    if not CLIENTE_NOME.strip():

        raise ValueError(
            "CLIENTE_NOME não pode estar vazio."
        )

    if (
        PERIODO_INICIO is None
        and PERIODO_FIM is None
    ):

        logger.info(
            "Período configurado: automático."
        )

        return

    if (
        PERIODO_INICIO is None
        or PERIODO_FIM is None
    ):

        raise ValueError(
            "PERIODO_INICIO e PERIODO_FIM "
            "devem ser preenchidos juntos."
        )

    converter_periodo(
        PERIODO_INICIO
    )

    converter_periodo(
        PERIODO_FIM
    )

    if (
        converter_periodo(PERIODO_INICIO)
        >
        converter_periodo(PERIODO_FIM)
    ):

        raise ValueError(
            "PERIODO_INICIO não pode ser "
            "maior que PERIODO_FIM."
        )


# =========================================================

def validar_arquivos_fonte() -> None:

    logger.info(
        "ETAPA ATUAL: "
        "Validação dos arquivos de fonte"
    )

    faltantes = []

    for nome_arquivo in (
        ARQUIVOS_OBRIGATORIOS.values()
    ):

        caminho = (
            DIRETORIO_RAW
            / nome_arquivo
        )

        if not caminho.exists():

            faltantes.append(
                str(caminho)
            )

    if faltantes:

        raise FileNotFoundError(
            "Arquivos CSV obrigatórios "
            "não encontrados:\n"
            + "\n".join(faltantes)
        )

    logger.info(
        "Todos os arquivos CSV "
        "obrigatórios foram encontrados."
    )


# =========================================================

def validar_fato_vendas(
    fato_vendas: pd.DataFrame,
) -> None:

    logger.info(
        "ETAPA ATUAL: "
        "Validação da Fato_Vendas"
    )

    colunas_obrigatorias = [

        "order_id",

        "order_item_id",

        "product_id",

        "seller_id",

        "order_purchase_timestamp",

        "price",

        "freight_value",

        "receita_item",

        "frete_item",
    ]

    erros = []

    if fato_vendas.empty:

        erros.append(
            "Fato_Vendas não possui registros."
        )

    faltantes = [

        coluna

        for coluna in colunas_obrigatorias

        if coluna not in fato_vendas.columns
    ]

    if faltantes:

        erros.append(
            "Colunas obrigatórias ausentes: "
            + str(faltantes)
        )

    if all(

        coluna in fato_vendas.columns

        for coluna in [
            "order_id",
            "order_item_id",
        ]
    ):

        duplicados = (
            fato_vendas
            .duplicated(
                subset=[
                    "order_id",
                    "order_item_id",
                ]
            )
            .sum()
        )

        if duplicados > 0:

            erros.append(
                "Existem "
                f"{duplicados} duplicidades "
                "na chave "
                "order_id + order_item_id."
            )

    if (
        "order_purchase_timestamp"
        in fato_vendas.columns
    ):

        datas = pd.to_datetime(

            fato_vendas[
                "order_purchase_timestamp"
            ],

            errors="coerce",
        )

        if datas.isna().any():

            erros.append(
                "Existem datas inválidas."
            )

    for coluna, nome in [

        (
            "receita_item",
            "Receita",
        ),

        (
            "frete_item",
            "Frete",
        ),
    ]:

        if coluna in fato_vendas.columns:

            serie = pd.to_numeric(

                fato_vendas[
                    coluna
                ],

                errors="coerce",
            )

            if serie.isna().any():

                erros.append(
                    f"{nome} possui "
                    "valores nulos."
                )

            if (serie < 0).any():

                erros.append(
                    f"{nome} possui "
                    "valores negativos."
                )

    if erros:

        raise ValueError(
            "Validação da Fato_Vendas "
            "falhou:\n"
            + "\n".join(erros)
        )

    logger.info(
        "Fato_Vendas validada com sucesso."
    )

    logger.info(
        "Registros validados: "
        f"{len(fato_vendas):,}"
    )


# =========================================================

def validar_periodo_analisado(
    fato_vendas: pd.DataFrame,
) -> None:

    logger.info(
        "ETAPA ATUAL: "
        "Validação do período analisado"
    )

    if fato_vendas.empty:

        raise ValueError(
            "O período selecionado "
            "não possui registros."
        )

    datas = pd.to_datetime(

        fato_vendas[
            "order_purchase_timestamp"
        ],

        errors="coerce",
    )

    receita = pd.to_numeric(

        fato_vendas[
            "receita_item"
        ],

        errors="coerce",
    ).sum()

    frete = pd.to_numeric(

        fato_vendas[
            "frete_item"
        ],

        errors="coerce",
    ).sum()

    logger.info(
        f"Primeira venda: {datas.min()}"
    )

    logger.info(
        f"Última venda: {datas.max()}"
    )

    logger.info(
        f"Pedidos únicos: "
        f"{fato_vendas['order_id'].nunique():,}"
    )

    logger.info(
        f"Sellers únicos: "
        f"{fato_vendas['seller_id'].nunique():,}"
    )

    logger.info(
        f"Receita: R$ {receita:,.2f}"
    )

    logger.info(
        f"Frete: R$ {frete:,.2f}"
    )


# =========================================================
# INTEGRIDADE DA EXPORTAÇÃO
# =========================================================

def validar_integridade_exportacao(
    fato_vendas: pd.DataFrame,
    caminho_excel: Path,
) -> None:

    logger.info(
        "ETAPA ATUAL: "
        "Validação de integridade da exportação"
    )

    fato_excel = pd.read_excel(

        caminho_excel,

        sheet_name="Fato_Vendas",
    )

    erros = []

    if len(fato_vendas) != len(fato_excel):

        erros.append(
            "Quantidade de registros "
            "diferente entre origem e Excel."
        )

    if list(fato_vendas.columns) != list(
        fato_excel.columns
    ):

        erros.append(
            "Estrutura das colunas "
            "diferente entre origem e Excel."
        )

    receita_origem = pd.to_numeric(

        fato_vendas[
            "receita_item"
        ],

        errors="coerce",
    ).sum()

    receita_excel = pd.to_numeric(

        fato_excel[
            "receita_item"
        ],

        errors="coerce",
    ).sum()

    if abs(
        receita_origem
        -
        receita_excel
    ) > 0.01:

        erros.append(
            "Receita diferente "
            "entre origem e Excel."
        )

    frete_origem = pd.to_numeric(

        fato_vendas[
            "frete_item"
        ],

        errors="coerce",
    ).sum()

    frete_excel = pd.to_numeric(

        fato_excel[
            "frete_item"
        ],

        errors="coerce",
    ).sum()

    if abs(
        frete_origem
        -
        frete_excel
    ) > 0.01:

        erros.append(
            "Frete diferente "
            "entre origem e Excel."
        )

    if erros:

        raise ValueError(
            "Falha na integridade "
            "da exportação:\n"
            + "\n".join(erros)
        )

    logger.info(
        "Integridade da exportação "
        "validada com sucesso."
    )


# =========================================================
# VALIDAÇÃO DO EXCEL
# =========================================================

def validar_arquivo_excel(
    caminho_excel: Path,
) -> None:

    logger.info(
        "ETAPA ATUAL: "
        "Validação do arquivo Excel"
    )

    excel = pd.ExcelFile(
        caminho_excel
    )

    abas_encontradas = (
        excel.sheet_names
    )

    faltantes = [

        aba

        for aba in ABAS_ESPERADAS

        if aba not in abas_encontradas
    ]

    if faltantes:

        raise ValueError(
            "Abas esperadas não encontradas: "
            f"{faltantes}"
        )

    abas_obrigatorias_com_dados = [

        "Fato_Vendas",

        "Financeiro",

        "Financeiro_Estados",

        "Insights",
    ]

    for aba in abas_obrigatorias_com_dados:

        dados = pd.read_excel(

            caminho_excel,

            sheet_name=aba,
        )

        if dados.empty:

            raise ValueError(
                f"A aba '{aba}' está vazia."
            )

    logger.info(
        "Todas as abas e estruturas "
        "foram validadas."
    )


# =========================================================
# RESUMO
# =========================================================

def exibir_resumo_execucao(
    cliente: str,
    periodo_inicio: str,
    periodo_fim: str,
    registros: int,
    caminho_excel: Path,
    tempo_execucao: float,
    indicadores_financeiros: dict,
    insights_df: pd.DataFrame,
) -> None:

    print()
    print("=" * 80)

    print(
        "RESUMO DA EXECUÇÃO — SPRINT 5.11"
    )

    print("=" * 80)

    print()

    print(
        f"Cliente: {cliente}"
    )

    print(
        f"Período: "
        f"{periodo_inicio} a {periodo_fim}"
    )

    print(
        f"Registros analisados: "
        f"{registros:,}"
    )

    print()

    print(
        "INDICADORES FINANCEIROS:"
    )

    print()

    print(
        f"Receita bruta: "
        f"R$ {indicadores_financeiros['receita_bruta']:,.2f}"
    )

    print(
        f"Frete total: "
        f"R$ {indicadores_financeiros['frete_total']:,.2f}"
    )

    print(
        f"Resultado após frete: "
        f"R$ {indicadores_financeiros['resultado_apos_frete']:,.2f}"
    )

    print(
        f"Frete sobre receita: "
        f"{indicadores_financeiros['frete_percentual']:.2f}%"
    )

    print(
        f"Margem após frete: "
        f"{indicadores_financeiros['margem_apos_frete']:.2f}%"
    )

    print(
        f"Total de pedidos: "
        f"{indicadores_financeiros['total_pedidos']:,}"
    )

    print(
        f"Ticket médio por pedido: "
        f"R$ {indicadores_financeiros['ticket_medio_pedido']:,.2f}"
    )

    print()

    print(
        f"Insights gerados: "
        f"{len(insights_df)}"
    )

    print()

    print(
        "Arquivo:"
    )

    print(
        caminho_excel
    )

    print()

    print(
        "VALIDAÇÕES:"
    )

    print(
        "✓ Fato_Vendas"
    )

    print(
        "✓ Período"
    )

    print(
        "✓ Excel"
    )

    print(
        "✓ Dashboard"
    )

    print(
        "✓ Financeiro"
    )

    print(
        "✓ Insights"
    )

    print(
        "✓ Integridade da exportação"
    )

    print()

    print(
        f"Tempo de execução: "
        f"{tempo_execucao:.2f}s"
    )

    print()

    print(
        "STATUS FINAL: OK"
    )

    print()

    print("=" * 80)

    print(
        "PIPELINE FINALIZADO COM SUCESSO"
    )

    print("=" * 80)


# =========================================================
# MAIN
# =========================================================

def main():

    inicio_execucao = time.perf_counter()

    print("=" * 80)

    print(
        "BUSINESS ANALYTICS AUTOMATION"
    )

    print("=" * 80)

    print()

    print(
        "SPRINT 5.11"
    )

    print()

    print(
        "CLIENTE:",
        CLIENTE_NOME,
    )

    print()

    print(
        "PERÍODO SOLICITADO:"
    )

    if (
        PERIODO_INICIO is None
        and PERIODO_FIM is None
    ):

        print(
            "AUTOMÁTICO"
        )

    else:

        print(
            f"{PERIODO_INICIO} "
            f"a "
            f"{PERIODO_FIM}"
        )

    print()

    # =====================================================
    # 1. CONFIGURAÇÕES
    # =====================================================

    validar_configuracoes()

    # =====================================================
    # 2. ARQUIVOS
    # =====================================================

    validar_arquivos_fonte()

    # =====================================================
    # 3. SOURCE
    # =====================================================

    logger.info(
        "ETAPA ATUAL: "
        "Inicialização da fonte CSV"
    )

    source = CSVSource(
        str(DIRETORIO_RAW)
    )

    loader = DataLoader(
        source
    )

    # =====================================================
    # 4. CARREGAMENTO
    # =====================================================

    logger.info(
        "ETAPA ATUAL: "
        "Carregamento dos datasets"
    )

    model = loader.carregar(

        orders=ARQUIVOS_OBRIGATORIOS[
            "orders"
        ],

        order_items=ARQUIVOS_OBRIGATORIOS[
            "order_items"
        ],

        customers=ARQUIVOS_OBRIGATORIOS[
            "customers"
        ],

        products=ARQUIVOS_OBRIGATORIOS[
            "products"
        ],

        payments=ARQUIVOS_OBRIGATORIOS[
            "payments"
        ],

        reviews=ARQUIVOS_OBRIGATORIOS[
            "reviews"
        ],

        sellers=ARQUIVOS_OBRIGATORIOS[
            "sellers"
        ],

        geolocation=ARQUIVOS_OBRIGATORIOS[
            "geolocation"
        ],
    )

    # =====================================================
    # 5. INTEGRAÇÕES
    # =====================================================

    model.orders = (
        OrderIntegrator.adicionar_itens(
            model.orders,
            model.order_items,
        )
    )

    model.orders = (
        OrderIntegrator.adicionar_clientes(
            model.orders,
            model.customers,
        )
    )

    model.order_items = (
        OrderIntegrator.adicionar_produtos(
            model.order_items,
            model.products,
        )
    )

    model.orders = (
        OrderIntegrator.adicionar_pagamentos(
            model.orders,
            model.payments,
        )
    )

    model.orders = (
        OrderIntegrator.adicionar_reviews(
            model.orders,
            model.reviews,
        )
    )

    model.order_items = (
        OrderIntegrator.adicionar_sellers(
            model.order_items,
            model.sellers,
        )
    )

    model.sellers = (
        OrderIntegrator.adicionar_geolocation_sellers(
            model.sellers,
            model.geolocation,
        )
    )

    # =====================================================
    # 6. FATO
    # =====================================================

    logger.info(
        "ETAPA ATUAL: "
        "Criação da Fato_Vendas"
    )

    fato_vendas = FactSales.criar(

        orders=model.orders,

        order_items=model.order_items,

        products=model.products,

        customers=model.customers,

        payments=model.payments,

        reviews=model.reviews,
    )

    print()
    print(
        f"Fato_Vendas: "
        f"{len(fato_vendas):,} registros"
    )

    # =====================================================
    # 7. VALIDAÇÃO
    # =====================================================

    validar_fato_vendas(
        fato_vendas
    )

    # =====================================================
    # 8. PERÍODO
    # =====================================================

    (
        periodo_disponivel_inicio,
        periodo_disponivel_fim,
    ) = obter_periodo_disponivel(
        fato_vendas
    )

    print()
    print(
        "PERÍODO DISPONÍVEL:"
    )

    print(
        f"{periodo_disponivel_inicio} "
        f"a "
        f"{periodo_disponivel_fim}"
    )

    (
        inicio_periodo,
        fim_periodo,
    ) = definir_periodo_analise(

        fato_vendas,

        PERIODO_INICIO,

        PERIODO_FIM,
    )

    # =====================================================
    # 9. FILTRO
    # =====================================================

    fato_vendas_filtrado = (
        filtrar_periodo(

            fato_vendas,

            inicio_periodo,

            fim_periodo,
        )
    )

    validar_periodo_analisado(
        fato_vendas_filtrado
    )

    # =====================================================
    # 10. MÉTRICAS SELLERS
    # =====================================================

    logger.info(
        "ETAPA ATUAL: "
        "Cálculo das métricas de sellers"
    )

    ranking_base = (
        Metrics.desempenho_sellers(
            fato_vendas_filtrado
        )
    )

    top_sellers = (
        Metrics.ranking_sellers(
            ranking_base
        )
    )

    frete_sellers = (
        Metrics.ranking_frete(
            ranking_base,
            minimo_itens=100,
        )
    )

    preco_medio_sellers = (
        Metrics.ranking_preco_medio(
            ranking_base,
            minimo_itens=100,
        )
    )

    sellers_estado = (
        Metrics.desempenho_estados(
            ranking_base
        )
    )

    resumo = (
        Metrics.resumo_sellers(
            ranking_base
        )
    )

    # =====================================================
    # 11. MÉTRICAS FINANCEIRAS
    # =====================================================

    logger.info(
        "ETAPA ATUAL: "
        "Cálculo dos indicadores financeiros"
    )

    indicadores_financeiros = (
        Metrics.indicadores_financeiros(
            fato_vendas_filtrado
        )
    )

    financeiro_sellers = (
        Metrics.financeiro_sellers(
            fato_vendas_filtrado
        )
    )

    ranking_margem_sellers = (
        Metrics.ranking_margem_sellers(
            financeiro_sellers,
            minimo_itens=100,
        )
    )

    financeiro_estados = (
        Metrics.financeiro_estados(
            financeiro_sellers
        )
    )

    # =====================================================
    # 12. INSIGHTS
    # =====================================================

    insights_df = Insights.gerar(

        fato_vendas=(
            fato_vendas_filtrado
        ),

        indicadores_financeiros=(
            indicadores_financeiros
        ),

        ranking_sellers=(
            top_sellers
        ),

        financeiro_sellers=(
            financeiro_sellers
        ),

        financeiro_estados=(
            financeiro_estados
        ),
    )

    # =====================================================
    # 13. RESUMO
    # =====================================================

    resumo_completo = {

        **resumo,

        "receita_bruta": (
            indicadores_financeiros[
                "receita_bruta"
            ]
        ),

        "frete_total": (
            indicadores_financeiros[
                "frete_total"
            ]
        ),

        "resultado_apos_frete": (
            indicadores_financeiros[
                "resultado_apos_frete"
            ]
        ),

        "frete_percentual": (
            indicadores_financeiros[
                "frete_percentual"
            ]
        ),

        "margem_apos_frete": (
            indicadores_financeiros[
                "margem_apos_frete"
            ]
        ),

        "total_pedidos": (
            indicadores_financeiros[
                "total_pedidos"
            ]
        ),

        "ticket_medio_pedido": (
            indicadores_financeiros[
                "ticket_medio_pedido"
            ]
        ),
    }

    resumo_df = pd.DataFrame(
        [resumo_completo]
    )

    # =====================================================
    # 14. DIRETÓRIO
    # =====================================================

    DIRETORIO_SAIDA.mkdir(

        parents=True,

        exist_ok=True,
    )

    # =====================================================
    # 15. ARQUIVO
    # =====================================================

    nome_arquivo = (
        gerar_nome_arquivo(

            CLIENTE_NOME,

            inicio_periodo,

            fim_periodo,
        )
    )

    caminho_excel = (
        DIRETORIO_SAIDA
        /
        nome_arquivo
    )

    print()
    print(
        "ARQUIVO DE SAÍDA:"
    )

    print(
        caminho_excel
    )

    # =====================================================
    # 16. EXPORTAÇÃO
    # =====================================================

    logger.info(
        "ETAPA ATUAL: "
        "Exportação do Excel"
    )

    exporter = ExcelExporter(
        caminho_excel
    )

    exporter.exportar({

        "Resumo": resumo_df,

        "Top_Sellers": (
            top_sellers.head(10)
        ),

        "Frete": (
            frete_sellers.head(10)
        ),

        "Preco_Medio": (
            preco_medio_sellers.head(10)
        ),

        "Por_Estado": (
            sellers_estado
        ),

        "Financeiro": (
            pd.DataFrame(
                [indicadores_financeiros]
            )
        ),

        "Margem_Sellers": (
            ranking_margem_sellers.head(10)
        ),

        "Financeiro_Estados": (
            financeiro_estados
        ),

        "Insights": (
            insights_df
        ),

        "Fato_Vendas": (
            fato_vendas_filtrado
        ),
    })

    # =====================================================
    # 17. DASHBOARD
    # =====================================================

    logger.info(
        "ETAPA ATUAL: "
        "Criação do Dashboard Excel"
    )

    dashboard = DashboardExcel(
        caminho_excel
    )

    dashboard.criar_dashboard(

        resumo=resumo_df,

        top_sellers=top_sellers,

        por_estado=sellers_estado,

        fato_vendas=fato_vendas_filtrado,
    )

    logger.info(
        "Dashboard Excel criado com sucesso."
    )

    # =====================================================
    # 18. VALIDAÇÃO EXCEL
    # =====================================================

    validar_arquivo_excel(
        caminho_excel
    )

    # =====================================================
    # 19. INTEGRIDADE
    # =====================================================

    validar_integridade_exportacao(

        fato_vendas_filtrado,

        caminho_excel,
    )

    # =====================================================
    # 20. FINAL
    # =====================================================

    tempo_execucao = (
        time.perf_counter()
        -
        inicio_execucao
    )

    exibir_resumo_execucao(

        cliente=CLIENTE_NOME,

        periodo_inicio=inicio_periodo,

        periodo_fim=fim_periodo,

        registros=len(
            fato_vendas_filtrado
        ),

        caminho_excel=caminho_excel,

        tempo_execucao=tempo_execucao,

        indicadores_financeiros=(
            indicadores_financeiros
        ),

        insights_df=insights_df,
    )


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    inicio = time.perf_counter()

    try:

        main()

    except KeyboardInterrupt:

        print()
        print(
            "PIPELINE INTERROMPIDO PELO USUÁRIO"
        )

        raise

    except FileNotFoundError as erro:

        tempo = (
            time.perf_counter()
            -
            inicio
        )

        logger.error(
            "ERRO DE ARQUIVO: %s",
            erro,
        )

        print()
        print("=" * 80)
        print(
            "PIPELINE FINALIZADO COM FALHA"
        )
        print("=" * 80)

        print()
        print(
            "Arquivo ou diretório não encontrado."
        )

        print(
            str(erro)
        )

        print(
            f"Tempo até a falha: "
            f"{tempo:.2f}s"
        )

        raise

    except ValueError as erro:

        tempo = (
            time.perf_counter()
            -
            inicio
        )

        logger.error(
            "ERRO DE VALIDAÇÃO: %s",
            erro,
        )

        print()
        print("=" * 80)
        print(
            "PIPELINE FINALIZADO COM FALHA"
        )
        print("=" * 80)

        print()
        print(
            "Validação ou configuração inválida."
        )

        print(
            str(erro)
        )

        print(
            f"Tempo até a falha: "
            f"{tempo:.2f}s"
        )

        raise

    except Exception as erro:

        tempo = (
            time.perf_counter()
            -
            inicio
        )

        logger.exception(
            "ERRO INESPERADO."
        )

        print()
        print("=" * 80)
        print(
            "PIPELINE FINALIZADO COM FALHA"
        )
        print("=" * 80)

        print()
        print(
            "Erro inesperado:"
        )

        print(
            str(erro)
        )

        print(
            f"Tempo até a falha: "
            f"{tempo:.2f}s"
        )

        raise