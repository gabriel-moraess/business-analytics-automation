import logging
from pathlib import Path

from src.utils.config import LOGS

ARQUIVO_LOG = LOGS / "automacao.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(ARQUIVO_LOG, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("OlistAutomation")