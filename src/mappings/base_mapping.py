from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseMapping(ABC):
    """
    Classe base para todos os mapeamentos de colunas.

    Cada fonte de dados deverá implementar um dicionário
    contendo a tradução entre os nomes originais das colunas
    e o padrão interno do projeto.
    """

    @property
    @abstractmethod
    def columns(self) -> dict[str, str]:
        """
        Retorna o dicionário de mapeamento.

        Exemplo:

        {
            "ORDER_ID": "order_id"
        }
        """
        ...