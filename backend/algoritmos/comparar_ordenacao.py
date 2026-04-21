"""Módulo para comparar desempenho dos algoritmos de ordenação."""

from typing import Any

from algoritmos.ordenacao_bubble import ordenacao_bubble
from algoritmos.ordenacao_merge import ordenacao_merge
from algoritmos.ordenacao_quick import ordenacao_quick
from modelo.carta_baralho import CartaBaralho


def comparar_algoritmos(vetor_cartas: list[CartaBaralho]) -> list[dict[str, Any]]:
    """Compara os três algoritmos de ordenação sobre cópias do mesmo vetor de entrada.

    Args:
        vetor_cartas: Vetor original (geralmente embaralhado).

    Returns:
        Lista com os três resultados, cada um contendo as métricas
        (tempo, comparações, trocas). O log narrado passo a passo não
        é gerado nesta função para economizar memória e focar na performance.
    """
    copia_para_bubble = list(vetor_cartas)
    copia_para_merge = list(vetor_cartas)
    copia_para_quick = list(vetor_cartas)

    resultado_bubble = ordenacao_bubble(copia_para_bubble, registrar_passos=False)
    resultado_merge = ordenacao_merge(copia_para_merge, registrar_passos=False)
    resultado_quick = ordenacao_quick(copia_para_quick, registrar_passos=False)

    return [resultado_bubble, resultado_merge, resultado_quick]
