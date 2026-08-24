import pandas as pd

from src.etl.transform import Transform


class TestTransform:
    """
    Testes unitários da classe Transform.
    """

    def test_json_para_dataframe(self):
        """
        Deve converter uma lista de dicionários em DataFrame.
        """

        dados = [
            {
                "id": 1,
                "name": "Gabriel"
            }
        ]

        df = Transform.json_para_dataframe(dados)

        assert isinstance(df, pd.DataFrame)

        assert len(df) == 1

        assert "id" in df.columns

        assert "name" in df.columns

    def test_remover_duplicados(self):
        """
        Deve remover registros duplicados.
        """

        df = pd.DataFrame(
            {
                "id": [1, 1, 2],
                "nome": ["A", "A", "B"],
            }
        )

        df = Transform.remover_duplicados(df)

        assert len(df) == 2

    def test_padronizar_colunas(self):
        """
        Deve padronizar nomes das colunas.
        """

        df = pd.DataFrame(
            columns=[
                "Nome Cliente",
                "Data.Nascimento",
            ]
        )

        df = Transform.padronizar_colunas(df)

        assert "nome_cliente" in df.columns

        assert "data_nascimento" in df.columns

    def test_adicionar_metadados(self):
        """
        Deve adicionar colunas técnicas ao DataFrame.
        """

        df = pd.DataFrame(
            {
                "id": [1],
                "nome": ["Gabriel"],
            }
        )

        df = Transform.adicionar_metadados(df)

        assert "data_coleta" in df.columns

        assert "data_processamento" in df.columns

        assert pd.notna(df.loc[0, "data_coleta"])

        assert pd.notna(df.loc[0, "data_processamento"])