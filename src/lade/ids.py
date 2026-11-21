# ---------------------------------------------------------------------------
# task_id: LADE-20261111-921
# produced_by: software-engineer
# review_level: standard
# references: [.hermes/references/lattinus-code.md, .hermes/references/engineering/python.md]
# adr: none
# gates: {safety: pass, dependencies: pass, git: na, documentation: na}
# status: IN_PROGRESS
# assumptions:
#   - A sequência numérica (NNN) é sempre três dígitos com zeros à esquerda.
#   - A data YYYYMMDD é validada pelo calendário gregoriano (módulo datetime).
#   - O prefixo "LADE-" é fixo e sensível a maiúsculas/minúsculas.
# ---------------------------------------------------------------------------
"""Validação e parsing de identificadores de tarefa no formato LADE-YYYYMMDD-NNN.

Uso::

    from lade.ids import parse_task_id, ParsedTaskId

    parsed = parse_task_id("LADE-20261111-921")
    assert parsed.date == date(2026, 11, 11)
    assert parsed.sequence == 921
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

_PREFIX: str = "LADE-"
_SEQUENCE_LENGTH: int = 3


class TaskIdError(ValueError):
    """Identificador de tarefa inválido — não segue o formato LADE-YYYYMMDD-NNN."""


@dataclass(frozen=True)
class ParsedTaskId:
    """Resultado do parsing de um identificador de tarefa.

    Attributes:
        date: Data extraída da porção YYYYMMDD.
        sequence: Número sequencial de três dígitos (NNN).
    """

    date: date
    sequence: int


def parse_task_id(value: str) -> ParsedTaskId:
    """Valida e interpreta um identificador no formato ``LADE-YYYYMMDD-NNN``.

    Args:
        value: String candidata (ex.: ``"LADE-20261111-921"``).

    Returns:
        ``ParsedTaskId`` com a data e a sequência extraídas.

    Raises:
        TaskIdError: Se *value* não obedecer ao formato, o prefixo estiver
            errado, a data for impossível ou a sequência não tiver exatamente
            três dígitos.
    """
    if not isinstance(value, str) or not value:
        raise TaskIdError(f"Esperado string não-vazia; recebido {type(value).__name__}")

    if not value.startswith(_PREFIX):
        raise TaskIdError(
            f"Prefixo inválido: esperado '{_PREFIX}', "
            f"recebido '{value[:len(_PREFIX)]}' (id completo: '{value}')"
        )

    body: str = value[len(_PREFIX):]  # "YYYYMMDD-NNN"

    if "-" not in body:
        raise TaskIdError(
            f"Formato inválido: esperado 'YYYYMMDD-NNN' após o prefixo, "
            f"recebido '{body}' (id completo: '{value}')"
        )

    date_str, seq_str = body.split("-", 1)

    if len(date_str) != 8 or not date_str.isdigit():
        raise TaskIdError(
            f"Parte de data inválida: esperado 8 dígitos (YYYYMMDD), "
            f"recebido '{date_str}' (id completo: '{value}')"
        )

    try:
        parsed_date: date = datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        raise TaskIdError(
            f"Data impossível: '{date_str}' não é uma data válida "
            f"(id completo: '{value}')"
        ) from None

    if len(seq_str) != _SEQUENCE_LENGTH or not seq_str.isdigit():
        raise TaskIdError(
            f"Sequência inválida: esperado exatamente {_SEQUENCE_LENGTH} dígitos, "
            f"recebido '{seq_str}' (id completo: '{value}')"
        )

    sequence: int = int(seq_str)

    return ParsedTaskId(date=parsed_date, sequence=sequence)