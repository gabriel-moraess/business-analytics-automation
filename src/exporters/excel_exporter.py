from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Mapping

import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

from src.utils.logger import logger


class ExcelExporter:
    """
    Exporta os DataFrames processados para um arquivo Excel.

    Responsabilidades:

    - criar o arquivo Excel;
    - exportar os DataFrames;
    - aplicar formatação básica;
    - criar tabelas do Excel;
    - formatar valores monetários;
    - formatar percentuais;
    - ajustar largura das colunas;
    - realizar substituição segura do arquivo final.

    A criação do Dashboard é responsabilidade de outra classe.
    A validação do Excel também é responsabilidade de outra classe.
    """

    def __init__(
        self,
        output_path: str | Path,
    ) -> None:

        self.output_path = Path(output_path)

    # =========================================================
    # EXPORTAÇÃO
    # =========================================================

    def exportar(
        self,
        tabelas: Mapping[str, pd.DataFrame],
    ) -> Path:
        """
        Exporta os DataFrames para Excel.

        Utiliza um arquivo temporário para reduzir o risco de
        corromper ou perder o arquivo final caso ocorra algum erro.
        """

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "Iniciando exportação para Excel: %s",
            self.output_path,
        )

        arquivo_temporario = (
            self.output_path.with_name(
                f"{self.output_path.stem}_temp"
                f"{self.output_path.suffix}"
            )
        )

        self._remover_temporario(
            arquivo_temporario
        )

        try:

            self._criar_arquivo_base(
                arquivo_temporario,
                tabelas,
            )

            logger.info(
                "Arquivo base Excel criado."
            )

            self._formatar_excel(
                arquivo_temporario
            )

            self._substituir_arquivo(
                arquivo_temporario
            )

        except Exception:

            self._remover_temporario(
                arquivo_temporario,
                silencioso=True,
            )

            raise

        logger.info(
            "Arquivo Excel gerado com sucesso: %s",
            self.output_path,
        )

        return self.output_path

    # =========================================================
    # CRIAÇÃO DO ARQUIVO BASE
    # =========================================================

    def _criar_arquivo_base(
        self,
        arquivo_temporario: Path,
        tabelas: Mapping[str, pd.DataFrame],
    ) -> None:
        """
        Cria o arquivo Excel inicial contendo todas as abas.
        """

        with pd.ExcelWriter(
            arquivo_temporario,
            engine="openpyxl",
            mode="w",
        ) as writer:

            for nome_aba, dataframe in tabelas.items():

                logger.info(
                    "Exportando aba '%s' com %s registros.",
                    nome_aba,
                    len(dataframe),
                )

                dataframe.to_excel(
                    writer,
                    sheet_name=nome_aba,
                    index=False,
                )

    # =========================================================
    # REMOÇÃO DO TEMPORÁRIO
    # =========================================================

    @staticmethod
    def _remover_temporario(
        arquivo_temporario: Path,
        silencioso: bool = False,
    ) -> None:
        """
        Remove um arquivo temporário existente.
        """

        if not arquivo_temporario.exists():
            return

        try:

            arquivo_temporario.unlink()

        except PermissionError as erro:

            if silencioso:
                return

            raise PermissionError(
                "O arquivo temporário do Excel está "
                "sendo utilizado por outro processo. "
                "Feche o Excel e execute novamente."
            ) from erro

    # =========================================================
    # SUBSTITUIÇÃO SEGURA
    # =========================================================

    def _substituir_arquivo(
        self,
        arquivo_temporario: Path,
    ) -> None:
        """
        Substitui o arquivo final pelo temporário.

        No Windows, caso o arquivo esteja aberto no Excel,
        os.replace pode gerar PermissionError.
        """

        if not arquivo_temporario.exists():

            raise FileNotFoundError(
                "Arquivo temporário não encontrado: "
                f"{arquivo_temporario}"
            )

        # -----------------------------------------------------
        # ARQUIVO FINAL NÃO EXISTE
        # -----------------------------------------------------

        if not self.output_path.exists():

            try:

                os.replace(
                    arquivo_temporario,
                    self.output_path,
                )

                return

            except PermissionError as erro:

                raise PermissionError(
                    "Não foi possível criar o arquivo Excel. "
                    "Verifique se ele está aberto em outro "
                    "programa."
                ) from erro

        # -----------------------------------------------------
        # PRIMEIRA TENTATIVA
        # -----------------------------------------------------

        try:

            os.replace(
                arquivo_temporario,
                self.output_path,
            )

            logger.info(
                "Arquivo Excel anterior substituído."
            )

            return

        except PermissionError:

            logger.warning(
                "Arquivo Excel está em uso. "
                "Realizando nova tentativa."
            )

        # -----------------------------------------------------
        # SEGUNDA TENTATIVA
        # -----------------------------------------------------

        time.sleep(1)

        try:

            os.replace(
                arquivo_temporario,
                self.output_path,
            )

            logger.info(
                "Arquivo Excel substituído após nova tentativa."
            )

            return

        except PermissionError as erro:

            self._remover_temporario(
                arquivo_temporario,
                silencioso=True,
            )

            raise PermissionError(
                "\n"
                "Não foi possível atualizar o arquivo Excel.\n\n"
                f"Arquivo: {self.output_path}\n\n"
                "O arquivo provavelmente está aberto no "
                "Excel ou sendo utilizado por outro processo.\n\n"
                "Feche o arquivo Excel e execute novamente:\n"
                "python main.py"
            ) from erro

    # =========================================================
    # FORMATAÇÃO DO EXCEL
    # =========================================================

    def _formatar_excel(
        self,
        arquivo: Path | None = None,
    ) -> None:
        """
        Aplica a formatação em todas as abas do workbook.
        """

        logger.info(
            "Iniciando formatação do Excel."
        )

        caminho = (
            arquivo
            if arquivo is not None
            else self.output_path
        )

        workbook = load_workbook(
            filename=caminho,
            read_only=False,
            data_only=False,
        )

        try:

            for worksheet in workbook.worksheets:

                self._formatar_aba(
                    worksheet
                )

            workbook.save(
                caminho
            )

        finally:

            workbook.close()

        logger.info(
            "Formatação do Excel concluída."
        )

    # =========================================================
    # FORMATAÇÃO DA ABA
    # =========================================================

    def _formatar_aba(
        self,
        worksheet,
    ) -> None:
        """
        Aplica formatação padrão a uma aba.
        """

        # -----------------------------------------------------
        # CONFIGURAÇÕES GERAIS
        # -----------------------------------------------------

        worksheet.freeze_panes = "A2"

        worksheet.sheet_view.showGridLines = False

        # -----------------------------------------------------
        # CABEÇALHO
        # -----------------------------------------------------

        for cell in worksheet[1]:

            cell.font = Font(
                bold=True,
                color="FFFFFF",
            )

            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="1F4E78",
            )

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
            )

        worksheet.row_dimensions[1].height = 25

        # -----------------------------------------------------
        # TABELA
        # -----------------------------------------------------

        max_row = worksheet.max_row
        max_column = worksheet.max_column

        if (
            max_row >= 2
            and max_column >= 1
        ):

            referencia = (
                f"A1:"
                f"{get_column_letter(max_column)}"
                f"{max_row}"
            )

            nome_tabela = (
                "Tabela_"
                + "".join(
                    char
                    for char in worksheet.title
                    if char.isalnum()
                )
            )

            # Excel exige nomes únicos para tabelas.
            nome_tabela = nome_tabela[:250]

            tabela = Table(
                displayName=nome_tabela,
                ref=referencia,
            )

            estilo = TableStyleInfo(
                name="TableStyleMedium2",
                showFirstColumn=False,
                showLastColumn=False,
                showRowStripes=True,
                showColumnStripes=False,
            )

            tabela.tableStyleInfo = estilo

            worksheet.add_table(
                tabela
            )

        # -----------------------------------------------------
        # LARGURA DAS COLUNAS
        # -----------------------------------------------------

        self._ajustar_largura_colunas(
            worksheet
        )

        # -----------------------------------------------------
        # FORMATAÇÃO NUMÉRICA
        # -----------------------------------------------------

        self._formatar_valores_numericos(
            worksheet
        )

        # -----------------------------------------------------
        # ALINHAMENTO DO CABEÇALHO
        # -----------------------------------------------------

        for cell in worksheet[1]:

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
            )

    # =========================================================
    # LARGURA DAS COLUNAS
    # =========================================================

    @staticmethod
    def _ajustar_largura_colunas(
        worksheet,
    ) -> None:
        """
        Calcula uma largura adequada para cada coluna.

        Analisa no máximo 1000 células por coluna para evitar
        processamento excessivo em datasets grandes.
        """

        for column_cells in worksheet.columns:

            if not column_cells:
                continue

            max_length = 0

            column_letter = get_column_letter(
                column_cells[0].column
            )

            cells_to_check = column_cells[:1000]

            for cell in cells_to_check:

                if cell.value is None:
                    continue

                tamanho = len(
                    str(cell.value)
                )

                if tamanho > max_length:
                    max_length = tamanho

            largura = min(
                max(
                    max_length + 2,
                    12,
                ),
                35,
            )

            worksheet.column_dimensions[
                column_letter
            ].width = largura

    # =========================================================
    # FORMATAÇÃO NUMÉRICA
    # =========================================================

    @staticmethod
    def _formatar_valores_numericos(
        worksheet,
    ) -> None:
        """
        Aplica formatos numéricos de acordo com o nome da coluna.
        """

        colunas = {}

        for cell in worksheet[1]:

            if cell.value is not None:

                colunas[
                    cell.column
                ] = str(
                    cell.value
                ).lower()

        for numero_coluna, nome_coluna in colunas.items():

            # -------------------------------------------------
            # MONETÁRIO
            # -------------------------------------------------

            eh_monetario = any(
                palavra in nome_coluna
                for palavra in [
                    "receita",
                    "frete",
                    "preco",
                    "preço",
                    "ticket",
                    "price",
                    "valor_pagamento",
                    "valor pagamento",
                    "resultado",
                    "faturamento",
                    "custo",
                    "margem_valor",
                ]
            )

            # -------------------------------------------------
            # PERCENTUAL
            # -------------------------------------------------

            eh_percentual = (
                "percentual" in nome_coluna
                or nome_coluna.endswith("%")
                or "margem" in nome_coluna
            )

            # -------------------------------------------------
            # INTEIROS
            # -------------------------------------------------

            eh_inteiro = any(
                palavra in nome_coluna
                for palavra in [
                    "itens",
                    "sellers",
                    "ranking",
                    "parcelas",
                    "order_item_id",
                    "total_pedidos",
                    "total_orders",
                ]
            )

            # -------------------------------------------------
            # DEFINE FORMATO
            # -------------------------------------------------

            if eh_percentual and not eh_monetario:

                formato = "0.00%"

            elif eh_monetario:

                formato = 'R$ #,##0.00'

            elif eh_inteiro:

                formato = '#,##0'

            else:

                continue

            # -------------------------------------------------
            # APLICA FORMATO
            # -------------------------------------------------

            for row in worksheet.iter_rows(
                min_row=2,
                min_col=numero_coluna,
                max_col=numero_coluna,
            ):

                cell = row[0]

                if isinstance(
                    cell.value,
                    (int, float),
                ):

                    cell.number_format = formato