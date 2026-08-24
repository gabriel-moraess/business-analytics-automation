import os
from pathlib import Path

from dotenv import load_dotenv

# ==========================================================
# VARIÁVEIS DE AMBIENTE
# ==========================================================

load_dotenv()

# ==========================================================
# INFORMAÇÕES DO PROJETO
# ==========================================================

PROJECT_NAME = "Olist Finance Automation"

PROJECT_VERSION = "1.0.0"

# ==========================================================
# DIRETÓRIOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DADOS_BRUTO = BASE_DIR / "dados" / "bruto"

DADOS_TRATADO = BASE_DIR / "dados" / "tratado"

DATABASE = BASE_DIR / "database"

DASHBOARD = BASE_DIR / "dashboard"

LOGS = BASE_DIR / "logs"

# Cria automaticamente as pastas do projeto

for pasta in (
    DADOS_BRUTO,
    DADOS_TRATADO,
    DATABASE,
    DASHBOARD,
    LOGS,
):
    pasta.mkdir(
        parents=True,
        exist_ok=True,
    )

# ==========================================================
# SQLITE
# ==========================================================

DATABASE_NAME = "olist.db"

DEFAULT_TABLE = "usuarios"

SQLITE_MODE = "replace"

# ==========================================================
# EXPORTAÇÃO
# ==========================================================

DEFAULT_EXPORT_NAME = "usuarios"

EXPORT_CSV = True

EXPORT_EXCEL = True

EXPORT_PARQUET = True

# ==========================================================
# DASHBOARD
# ==========================================================

DASHBOARD_TEMPLATE = "Dashboard_Template.xlsx"

DASHBOARD_OUTPUT = "Dashboard.xlsx"

# ==========================================================
# API
# ==========================================================

API_TIMEOUT = 30

API_RETRY = 3

OLIST_TOKEN = os.getenv("OLIST_TOKEN")

OLIST_URL = os.getenv("OLIST_URL")

# ==========================================================
# LOG
# ==========================================================

LOG_LEVEL = "INFO"