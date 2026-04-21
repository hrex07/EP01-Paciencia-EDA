"""Algoritmo recursivo para embaralhar um vetor de cartas."""

import random
import time
from typing import Any

from modelo.carta_baralho import CartaBaralho


def _embaralhar_recursivo_interno(
    vetor_cartas: list[CartaBaralho],
    contador_iteracoes: int,
    lista_passos: list[dict[str, Any]],
    quantidade_total: int,
    *,
    registrar_passos: bool = True,
) -> None:
    """Função auxiliar que executa a recursão e acumula os logs.

    Args:
        vetor_cartas: Lista de cartas sendo embaralhada.
        contador_iteracoes: Número restante de trocas.
        lista_passos: Acumulador de logs.
        quantidade_total: Número total de trocas solicitadas na chamada inicial.
        registrar_passos: Se True, registra logs na lista.
    """
    if contador_iteracoes <= 0:
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": len(lista_passos) + 1,
                    "pseudo_codigo": "SE contador_iteracoes = 0 ENTÃO RETORNAR",
                    "descricao_acao": "Caso base atingido: contador = 0, retornando vetor.",
                    "profundidade_recursao": 0,
                }
            )
        return

    profundidade_atual = quantidade_total - contador_iteracoes + 1
    quantidade_cartas = len(vetor_cartas)

    if quantidade_cartas >= 2:
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
                    "passo_numero": len(lista_passos) + 1,
                    "pseudo_codigo": "embaralhar_recursivo(vetor, contador - 1)",
                    "descricao_acao": (
                        f"Nível {profundidade_atual}: Troca {carta_a.texto_carta()} "
                        f"com {carta_b.texto_carta()} e chama recursivamente."
                    ),
                    "profundidade_recursao": profundidade_atual,
                    "indices_trocados": [posicao_a, posicao_b],
                }
            )

    _embaralhar_recursivo_interno(
        vetor_cartas,
        contador_iteracoes - 1,
        lista_passos,
        quantidade_total,
        registrar_passos=registrar_passos,
    )


def embaralhar_recursivo(
    vetor_cartas: list[CartaBaralho],
    *,
    quantidade_trocas: int = 1000,
    registrar_passos: bool = True,
) -> dict[str, Any]:
    """Embaralha recursivamente um vetor através de trocas aleatórias.

    A profundidade da recursão será igual a `quantidade_trocas` + 1.
    Atenção: Valores muito grandes de `quantidade_trocas` (ex: > 900 no Python padrão)
    podem causar RecursionError devido ao limite de pilha do Python. Em projetos reais,
    costuma-se alterar sys.setrecursionlimit() ou reduzir o limite.

    Args:
        vetor_cartas: Lista de cartas a ser embaralhada.
        quantidade_trocas: Profundidade da recursão / número de trocas.
        registrar_passos: Se True, gera logs narrados.

    Returns:
        Dicionário com vetor embaralhado, logs e tempo de execução.
    """
    inicio_tempo = time.perf_counter()
    lista_passos: list[dict[str, Any]] = []

    _embaralhar_recursivo_interno(
        vetor_cartas,
        quantidade_trocas,
        lista_passos,
        quantidade_trocas,
        registrar_passos=registrar_passos,
    )

    fim_tempo = time.perf_counter()
    tempo_execucao_ms = (fim_tempo - inicio_tempo) * 1000.0

    return {
        "algoritmo_nome": "Embaralhamento Recursivo",
        "vetor_cartas": vetor_cartas,
        "total_trocas": quantidade_trocas,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
        "passos_executados": lista_passos,
    }
