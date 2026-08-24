import pandas as pd
import pytest

from src.etl.validate import DataValidator


class TestDataValidator:
    """
    Testes unitários da classe DataValidator.
    """

    def test_validar_colunas_ok(self):
        """
        Deve validar corretamente quando todas
        as colunas obrigatórias existem.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "name": ["Gabriel"],
                "email": ["gabriel@email.com"],
            }
        )

        DataValidator.validar_colunas(
            df,
            ["id", "name", "email"],
        )

    def test_validar_colunas_faltando(self):
        """
        Deve lançar exceção quando faltar
        alguma coluna obrigatória.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "name": ["Gabriel"],
            }
        )

        with pytest.raises(ValueError):

            DataValidator.validar_colunas(
                df,
                ["id", "name", "email"],
            )

    def test_validar_nulos_ok(self):
        """
        Não deve lançar exceção
        quando não existirem nulos.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "nome": ["Gabriel"],
            }
        )

        DataValidator.validar_nulos(df)

    def test_validar_nulos_erro(self):
        """
        Deve lançar exceção
        quando existirem valores nulos.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "nome": [None],
            }
        )

        with pytest.raises(ValueError):

            DataValidator.validar_nulos(df)

    def test_validar_duplicados_ok(self):
        """
        Não deve lançar exceção
        quando não houver duplicados.
        """

        df = pd.DataFrame(
            {
                "id": [1, 2],
                "nome": ["A", "B"],
            }
        )

        DataValidator.validar_duplicados(df)

    def test_validar_duplicados_erro(self):
        """
        Deve lançar exceção
        quando houver duplicados.
        """

        df = pd.DataFrame(
            {
                "id": [1, 1],
                "nome": ["A", "A"],
            }
        )

        with pytest.raises(ValueError):

            DataValidator.validar_duplicados(df)

    def test_resumo(self):
        """
        Deve executar o resumo
        sem gerar exceções.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "nome": ["Gabriel"],
            }
        )

        DataValidator.resumo(df)