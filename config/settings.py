from pathlib import Path


# ============================================================
# CONFIGURAÇÕES DO CLIENTE
# ============================================================

CLIENTE_NOME = "Gabriel Tecnologia LTDA"


# ============================================================
# CONFIGURAÇÕES DO PROJETO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# DIRETÓRIOS
# ============================================================

DADOS_DIR = PROJECT_ROOT / "dados"

RAW_DIR = DADOS_DIR / "raw"

PROCESSED_DIR = DADOS_DIR / "processed"

LOG_DIR = PROJECT_ROOT / "logs"


# ============================================================
# DATASET OLIST
# ============================================================

OLIST_DIR = RAW_DIR / "olist"


# ============================================================
# ARQUIVOS DE ENTRADA
# ============================================================

ORDERS_FILE = OLIST_DIR / "olist_orders_dataset.csv"

ORDER_ITEMS_FILE = OLIST_DIR / "olist_order_items_dataset.csv"

CUSTOMERS_FILE = OLIST_DIR / "olist_customers_dataset.csv"

PRODUCTS_FILE = OLIST_DIR / "olist_products_dataset.csv"

PAYMENTS_FILE = OLIST_DIR / "olist_order_payments_dataset.csv"

REVIEWS_FILE = OLIST_DIR / "olist_order_reviews_dataset.csv"

SELLERS_FILE = OLIST_DIR / "olist_sellers_dataset.csv"

GEOLOCATION_FILE = OLIST_DIR / "olist_geolocation_dataset.csv"


# ============================================================
# CONFIGURAÇÕES DE EXPORTAÇÃO
# ============================================================

OUTPUT_PREFIX = "Business_Analytics"


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def nome_cliente_arquivo() -> str:
    """
    Converte o nome do cliente para um formato seguro para nome de arquivo.
    """

    caracteres_invalidos = '<>:"/\\|?*'

    nome = CLIENTE_NOME

    for caractere in caracteres_invalidos:
        nome = nome.replace(caractere, "_")

    nome = nome.strip()

    return nome.replace(" ", "_")


def garantir_diretorios() -> None:
    """
    Cria os diretórios necessários caso ainda não existam.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def gerar_nome_arquivo(periodo_inicio: str, periodo_fim: str) -> str:
    """
    Gera o nome padronizado do arquivo Excel.

    Exemplo:

    Business_Analytics_Gabriel_Tecnologia_LTDA_2016-09_a_2018-09.xlsx
    """

    cliente = nome_cliente_arquivo()

    return (
        f"{OUTPUT_PREFIX}_"
        f"{cliente}_"
        f"{periodo_inicio}_a_{periodo_fim}.xlsx"
    )


def gerar_caminho_saida(
    periodo_inicio: str,
    periodo_fim: str
) -> Path:
    """
    Retorna o caminho completo do arquivo Excel de saída.
    """

    nome_arquivo = gerar_nome_arquivo(
        periodo_inicio,
        periodo_fim
    )

    return PROCESSED_DIR / nome_arquivo