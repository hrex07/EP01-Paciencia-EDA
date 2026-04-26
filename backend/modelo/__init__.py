"""Modelos de domínio: cartas e estruturas de dados implementadas manualmente.

Exporta tipos centrais usados pelo motor e pela API (cartas, nós encadeados,
exceções de validação).
"""

from modelo.carta_baralho import CartaBaralho
from modelo.excecao_carta import CartaInvalidaError
from modelo.no_encadeado import NoEncadeado

__all__ = ["CartaBaralho", "CartaInvalidaError", "NoEncadeado"]
