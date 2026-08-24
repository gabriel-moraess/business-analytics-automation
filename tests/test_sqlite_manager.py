from pathlib import Path

import pandas as pd
import pytest

from src.database.sqlite_manager import SQLiteManager


class TestSQLiteManager:
    """
    Testes unitários da classe SQLiteManager.
    """

    @pytest.fixture
    def dataframe(self) -> pd.DataFrame:
        """
        Retorna um DataFrame simples para os testes.
        """

        return pd.DataFrame(
            {
                "id": [1, 2],
                "nome": ["Gabriel", "Maria"],
            }
        )

    @pytest.fixture
    def banco_temporario(self, tmp_path: Path) -> SQLiteManager:
        """
        Cria um banco SQLite temporário.
        """

        db_path = tmp_path / "teste.db"

        return SQLiteManager(db_path=db_path)

    def test_salvar_dataframe_replace(
        self,
        banco_temporario: SQLiteManager,
        dataframe: pd.DataFrame,
    ):
        """
        Deve criar uma tabela utilizando o modo replace.
        """

        banco_temporario.salvar_dataframe(
            df=dataframe,
            tabela="usuarios",
            if_exists="replace",
        )

    def test_salvar_dataframe_append(
        self,
        banco_temporario: SQLiteManager,
        dataframe: pd.DataFrame,
    ):
        """
        Deve permitir inserir registros utilizando append.
        """

        banco_temporario.salvar_dataframe(
            dataframe,
            "usuarios",
            "replace",
        )

        banco_temporario.salvar_dataframe(
            dataframe,
            "usuarios",
            "append",
        )

    def test_modo_invalido(
        self,
        banco_temporario: SQLiteManager,
        dataframe: pd.DataFrame,
    ):
        """
        Deve lançar exceção para modos inválidos.
        """

        with pytest.raises(ValueError):

            banco_temporario.salvar_dataframe(
                dataframe,
                "usuarios",
                "modo_invalido",
            )

    def test_banco_criado(
        self,
        tmp_path: Path,
    ):
        """
        Deve criar o arquivo do banco SQLite.
        """

        db_path = tmp_path / "teste.db"

        banco = SQLiteManager(db_path=db_path)

        banco.salvar_dataframe(
            pd.DataFrame({"id": [1]}),
            "teste",
        )

        assert db_path.exists()