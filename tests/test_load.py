from pathlib import Path

import pandas as pd
import pytest

from src.etl.load import Load


class TestLoad:
    """
    Testes unitários da classe Load.
    """

    @pytest.fixture
    def dataframe(self) -> pd.DataFrame:
        """
        Retorna um DataFrame para testes.
        """

        return pd.DataFrame(
            {
                "id": [1, 2],
                "nome": ["Gabriel", "Maria"],
            }
        )

    @pytest.fixture
    def load(self, tmp_path: Path) -> Load:
        """
        Cria uma instância do Load utilizando
        um diretório temporário.
        """

        instancia = Load()

        instancia.output_dir = tmp_path

        return instancia

    def test_exportar_csv(
        self,
        load: Load,
        dataframe: pd.DataFrame,
    ):
        """
        Deve exportar um CSV.
        """

        caminho = load.exportar_csv(
            dataframe,
            "usuarios",
        )

        assert caminho.exists()

        assert caminho.suffix == ".csv"

    def test_exportar_excel(
        self,
        load: Load,
        dataframe: pd.DataFrame,
    ):
        """
        Deve exportar um Excel.
        """

        caminho = load.exportar_excel(
            dataframe,
            "usuarios",
        )

        assert caminho.exists()

        assert caminho.suffix == ".xlsx"

    def test_exportar_parquet(
        self,
        load: Load,
        dataframe: pd.DataFrame,
    ):
        """
        Deve exportar um Parquet.
        """

        caminho = load.exportar_parquet(
            dataframe,
            "usuarios",
        )

        assert caminho.exists()

        assert caminho.suffix == ".parquet"

    def test_exportar_todos(
        self,
        load: Load,
        dataframe: pd.DataFrame,
    ):
        """
        Deve exportar todos os formatos.
        """

        load.exportar_todos(
            dataframe,
            "usuarios",
        )

        assert (load.output_dir / "usuarios.csv").exists()

        assert (load.output_dir / "usuarios.xlsx").exists()

        assert (load.output_dir / "usuarios.parquet").exists()