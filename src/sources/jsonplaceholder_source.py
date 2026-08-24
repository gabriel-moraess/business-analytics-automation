from __future__ import annotations

from typing import Any

from src.api.client import APIClient
from src.sources.base_source import BaseSource


class JsonPlaceholderSource(BaseSource):
    """
    Fonte de dados da API JsonPlaceholder.
    """

    def __init__(self, base_url: str) -> None:
        self.client = APIClient(base_url)

    def get_data(
        self,
        endpoint: str,
    ) -> list[dict[str, Any]]:

        return self.client.get(endpoint)