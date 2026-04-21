"""Algoritmo iterativo para embaralhar um vetor de cartas."""

import random
import time
from typing import Any

from modelo.carta_baralho import CartaBaralho


def embaralhar_iterativo(
    vetor_cartas: list[CartaBaralho],
    *,
    quantidade_trocas: int = 1000,
    registrar_passos: bool = True,
) -> dict[str, Any]:
    """Embaralha iterativamente um vetor através de trocas aleatórias.

    Args:
        vetor_cartas: Lista de cartas a ser embaralhada.
        quantidade_trocas: Número de vezes que duas cartas serão trocadas.
        registrar_passos: Se True, registra cada troca no log.

    Returns:
        Dicionário com o vetor embaralhado, tempo gasto e log passo a passo.
    """
    inicio_tempo = time.perf_counter()
    lista_passos: list[dict[str, Any]] = []

    quantidade_cartas = len(vetor_cartas)
    if quantidade_cartas < 2:
        return {
            "algoritmo_nome": "Embaralhamento Iterativo",
            "vetor_cartas": vetor_cartas,
            "total_trocas": 0,
            "tempo_execucao_ms": 0.0,
            "passos_executados": lista_passos,
        }

    for indice_troca in range(quantidade_trocas):
        posicao_a = random.randint(0, quantidade_cartas - 1)
        posicao_b = random.randint(0, quantidade_cartas - 1)

        carta_a = vetor_cartas[posicao_a]
        carta_b = vetor_cartas[posicao_b]

        vetor_cartas[posicao_a], vetor_cartas[posicao_b] = (
            vetor_cartas[posicao_b],
            vetor_cartas[posicao_a],
        )

        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": indice_troca + 1,
                    "pseudo_codigo": "trocar vetor[i] ↔ vetor[j]",
                    "descricao_acao": (
                        f"Troca posição {posicao_a} ({carta_a.texto_carta()}) com "
                        f"posição {posicao_b} ({carta_b.texto_carta()})."
                    ),
                    "indices_trocados": [posicao_a, posicao_b],
                }
            )

    fim_tempo = time.perf_counter()
    tempo_execucao_ms = (fim_tempo - inicio_tempo) * 1000.0

    return {
        "algoritmo_nome": "Embaralhamento Iterativo",
        "vetor_cartas": vetor_cartas,
        "total_trocas": quantidade_trocas,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
        "passos_executados": lista_passos,
    }
