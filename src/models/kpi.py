from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class KPI:
    """
    Representa um indicador de negócio.

    Attributes:
        nome: Nome do indicador.
        valor: Valor principal.
        formato: Formato de exibição.
        variacao: Percentual de variação.
        tendencia: Direção da variação.
    """

    nome: str
    valor: float | int

    formato: str = "numero"

    variacao: float | None = None

    tendencia: str | None = None

    def formatado(self) -> str:
        """
        Retorna o valor formatado para exibição.
        """

        if self.formato == "moeda":
            return f"R$ {self.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        if self.formato == "percentual":
            return f"{self.valor:.2f}%"

        if self.formato == "inteiro":
            return f"{int(self.valor):,}".replace(",", ".")

        return str(self.valor)