"""Ordenação via Bubble Sort com logs de demonstração."""

import time
from typing import Any

from modelo.carta_baralho import CartaBaralho


def _valor_ordem(carta: CartaBaralho) -> tuple[int, int]:
    """Retorna tupla para ordenação: naipe (c=0, o=1, p=2, e=3), número (1 a 13)."""
    naipe_peso = {"c": 0, "o": 1, "p": 2, "e": 3}
    return (naipe_peso.get(carta.naipe_carta, 0), carta.numero_carta)


def ordenacao_bubble(
    vetor_cartas: list[CartaBaralho],
    *,
    registrar_passos: bool = True,
) -> dict[str, Any]:
    """Ordena in-place um vetor de cartas usando Bubble Sort.

    Args:
        vetor_cartas: Lista de cartas.
        registrar_passos: Se True, registra o passo a passo das comparações/trocas.

    Returns:
        Dicionário com o resultado, métricas e log narrado.
    """
    inicio_tempo = time.perf_counter()
    lista_passos: list[dict[str, Any]] = []
    total_comparacoes = 0
    total_trocas = 0

    tamanho = len(vetor_cartas)

    for iteracao_i in range(tamanho):
        houve_troca_iteracao = False
        for indice_j in range(0, tamanho - iteracao_i - 1):
            carta_esquerda = vetor_cartas[indice_j]
            carta_direita = vetor_cartas[indice_j + 1]

            total_comparacoes += 1
            precisa_trocar = _valor_ordem(carta_esquerda) > _valor_ordem(carta_direita)

            if registrar_passos:
                acao = (
                    f"Compara {carta_esquerda.texto_carta()} com {carta_direita.texto_carta()}: "
                    f"{carta_esquerda.texto_carta()} > {carta_direita.texto_carta()}"
                )
                if precisa_trocar:
                    acao += " → Troca!"
                else:
                    acao += " → Mantém ordem."

                lista_passos.append(
                    {
                        "passo_numero": len(lista_passos) + 1,
                        "pseudo_codigo": "SE vetor[j] > vetor[j+1] ENTÃO trocar",
                        "descricao_acao": acao,
                        "indices_comparados": [indice_j, indice_j + 1],
                        "houve_troca": precisa_trocar,
                        "estado_vetor": [c.texto_carta() for c in vetor_cartas],
                    }
                )

            if precisa_trocar:
                total_trocas += 1
                houve_troca_iteracao = True
                vetor_cartas[indice_j], vetor_cartas[indice_j + 1] = (
                    vetor_cartas[indice_j + 1],
                    vetor_cartas[indice_j],
                )

        if not houve_troca_iteracao:
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": len(lista_passos) + 1,
                        "pseudo_codigo": "SE não houve trocas ENTÃO BREAK",
                        "descricao_acao": "Nenhuma troca nesta passagem. Vetor ordenado.",
                    }
                )
            break

    fim_tempo = time.perf_counter()
    tempo_execucao_ms = (fim_tempo - inicio_tempo) * 1000.0

    return {
        "algoritmo_nome": "Bubble Sort",
        "vetor_cartas": vetor_cartas,
        "total_comparacoes": total_comparacoes,
        "total_trocas": total_trocas,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
        "passos_executados": lista_passos,
    }
