# ---------------------------------------------------------------------------
# task_id: LADE-20261111-921
# produced_by: software-engineer
# review_level: standard
# references: [.hermes/references/engineering/testing.md]
# adr: none
# gates: {safety: pass, dependencies: pass, git: na, documentation: na}
# status: IN_PROGRESS
# assumptions:
#   - Os testes são determinísticos: sem rede, relógio de parede ou aleatoriedade.
#   - A classe de erro ``TaskIdError`` é subclasse de ``ValueError``.
# ---------------------------------------------------------------------------
"""Testes unitários para ``lade.ids.parse_task_id``."""

from __future__ import annotations

import unittest
from datetime import date

from src.lade.ids import ParsedTaskId, TaskIdError, parse_task_id


class ParseTaskIdValidTests(unittest.TestCase):
    """Casos em que o identificador é válido."""

    def test_standard_id(self) -> None:
        """Identificador típico de tarefa é interpretado corretamente."""
        result: ParsedTaskId = parse_task_id("LADE-20261111-921")
        self.assertEqual(result.date, date(2026, 11, 11))
        self.assertEqual(result.sequence, 921)

    def test_minimal_sequence(self) -> None:
        """Sequência mínima de três dígitos (000) é aceita."""
        result: ParsedTaskId = parse_task_id("LADE-20260101-000")
        self.assertEqual(result.date, date(2026, 1, 1))
        self.assertEqual(result.sequence, 0)

    def test_max_sequence(self) -> None:
        """Sequência máxima de três dígitos (999) é aceita."""
        result: ParsedTaskId = parse_task_id("LADE-20261231-999")
        self.assertEqual(result.date, date(2026, 12, 31))
        self.assertEqual(result.sequence, 999)

    def test_leap_year_date(self) -> None:
        """29 de fevereiro em ano bissexto é aceito."""
        result: ParsedTaskId = parse_task_id("LADE-20240229-001")
        self.assertEqual(result.date, date(2024, 2, 29))
        self.assertEqual(result.sequence, 1)


class ParseTaskIdWrongPrefixTests(unittest.TestCase):
    """Casos em que o prefixo está errado."""

    def test_wrong_prefix(self) -> None:
        """Prefixo diferente de 'LADE-' é rejeitado."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("TASK-20261111-921")
        self.assertIn("Prefixo inválido", str(ctx.exception))

    def test_lowercase_prefix(self) -> None:
        """Prefixo em minúsculas é rejeitado (sensível a caixa)."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("lade-20261111-921")
        self.assertIn("Prefixo inválido", str(ctx.exception))

    def test_no_prefix(self) -> None:
        """String sem prefixo nenhum é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("20261111-921")
        self.assertIn("Prefixo inválido", str(ctx.exception))


class ParseTaskIdImpossibleDateTests(unittest.TestCase):
    """Casos em que a data é impossível no calendário gregoriano."""

    def test_february_30(self) -> None:
        """30 de fevereiro é rejeitado."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20250230-001")
        self.assertIn("Data impossível", str(ctx.exception))

    def test_month_13(self) -> None:
        """Mês 13 é rejeitado."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20261301-001")
        self.assertIn("Data impossível", str(ctx.exception))

    def test_non_leap_feb_29(self) -> None:
        """29 de fevereiro em ano não-bissexto é rejeitado."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20250229-001")
        self.assertIn("Data impossível", str(ctx.exception))

    def test_november_31(self) -> None:
        """31 de novembro é rejeitado."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20251131-001")
        self.assertIn("Data impossível", str(ctx.exception))


class ParseTaskIdWrongSequenceSizeTests(unittest.TestCase):
    """Casos em que a sequência não tem exatamente três dígitos."""

    def test_too_short(self) -> None:
        """Sequência com menos de 3 dígitos é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20261111-1")
        self.assertIn("Sequência inválida", str(ctx.exception))

    def test_too_long(self) -> None:
        """Sequência com mais de 3 dígitos é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20261111-1234")
        self.assertIn("Sequência inválida", str(ctx.exception))

    def test_non_numeric(self) -> None:
        """Sequência não-numérica é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20261111-ABC")
        self.assertIn("Sequência inválida", str(ctx.exception))


class ParseTaskIdStructuralTests(unittest.TestCase):
    """Casos com problemas estruturais (hífen, vazio, tamanho da data)."""

    def test_missing_hyphen(self) -> None:
        """Falta do hífen entre data e sequência é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-20261111921")
        self.assertIn("Formato inválido", str(ctx.exception))

    def test_empty_string(self) -> None:
        """String vazia é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("")
        self.assertIn("não-vazia", str(ctx.exception))

    def test_non_string(self) -> None:
        """Tipo diferente de string é rejeitado."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id(None)  # type: ignore[arg-type]
        self.assertIn("não-vazia", str(ctx.exception))

    def test_date_too_short(self) -> None:
        """Parte de data com menos de 8 dígitos é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-2026111-001")
        self.assertIn("Parte de data inválida", str(ctx.exception))

    def test_date_non_numeric(self) -> None:
        """Parte de data com caracteres não-numéricos é rejeitada."""
        with self.assertRaises(TaskIdError) as ctx:
            parse_task_id("LADE-ABCDEFGH-001")
        self.assertIn("Parte de data inválida", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()