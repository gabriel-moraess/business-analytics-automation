from pathlib import Path


# ============================================================
# CONFIGURAÇÕES DO PROJETO
# ============================================================

CLIENTE = "Olist"

NOME_PROJETO = "Business Analytics"


# ============================================================
# PERÍODO ANALISADO
# ============================================================

PERIODO_INICIAL = "2017-01-01"

PERIODO_FINAL = "2018-12-31"


# ============================================================
# DIRETÓRIOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DADOS_DIR = BASE_DIR / "dados"

RAW_DIR = DADOS_DIR / "raw"

PROCESSED_DIR = DADOS_DIR / "processed"


# ============================================================
# ARQUIVO DE SAÍDA
# ============================================================

def gerar_nome_arquivo() -> str:

    cliente = CLIENTE.replace(" ", "_")

    periodo_inicial = PERIODO_INICIAL.replace("-", "")

    periodo_final = PERIODO_FINAL.replace("-", "")

    return (
        f"{cliente}_"
        f"{NOME_PROJETO.replace(' ', '_')}_"
        f"{periodo_inicial}_a_{periodo_final}.xlsx"
    )


OUTPUT_FILE = PROCESSED_DIR / gerar_nome_arquivo()