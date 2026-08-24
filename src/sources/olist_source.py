from __future__ import annotations

from typing import Any

from src.sources.base_source import BaseSource


class OlistSource(BaseSource):
    """
    Fonte oficial da API Olist.

    Implementação futura.
    """

    def __init__(self) -> None:
        pass

    def get_data(
        self,
        endpoint: str,
    ) -> list[dict[str, Any]]:

        raise NotImplementedError(
            "Integração com a API da Olist ainda não implementada."
        )