from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class BaseSource(ABC):
    """
    Classe base para todas as fontes de dados.

    Qualquer origem (CSV, Excel, API, Banco de Dados)
    deve herdar desta classe.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """
        Nome da fonte de dados.
        """
        ...

    @abstractmethod
    def connect(self) -> None:
        """
        Estabelece conexão com a fonte.

        Para arquivos locais este método pode não realizar
        nenhuma ação, mas mantém a interface consistente.
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """
        Encerra a conexão.
        """
        ...

    @abstractmethod
    def read(
        self,
        resource: str,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Lê um recurso da fonte.

        Parameters
        ----------
        resource
            Nome do arquivo, endpoint, tabela etc.

        Returns
        -------
        pd.DataFrame
        """
        ...