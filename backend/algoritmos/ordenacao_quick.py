"""Ordenação via Quick Sort com logs de demonstração."""

import time
from typing import Any

from modelo.carta_baralho import CartaBaralho


def _valor_ordem(carta: CartaBaralho) -> tuple[int, int]:
    """Retorna tupla (peso do naipe, número) para ordenação lexicográfica."""
    naipe_peso = {"c": 0, "o": 1, "p": 2, "e": 3}
    return (naipe_peso.get(carta.naipe_carta, 0), carta.numero_carta)


class _QuickSortInterno:
    """Estado mutável e logging do quicksort Lomuto (ou equivalente) do módulo."""

    def __init__(self, registrar_passos: bool) -> None:
        """Inicializa contadores e buffer de passos.

        Args:
            registrar_passos: Se acumula narrativa em ``lista_passos``.
        """
        self.registrar_passos = registrar_passos
        self.total_comparacoes = 0
        self.total_trocas = 0
        self.lista_passos: list[dict[str, Any]] = []

    def quick_sort(
        self, vetor_original: list[CartaBaralho], baixo: int, alto: int
    ) -> None:
        if baixo < alto:
            indice_pivo = self.partition(vetor_original, baixo, alto)

            if self.registrar_passos:
                self.lista_passos.append(
                    {
                        "passo_numero": len(self.lista_passos) + 1,
                        "pseudo_codigo": "quick_sort(vetor, baixo, pivo - 1)",
                        "descricao_acao": f"Chamada recursiva para subvetor à esquerda [{baixo}..{indice_pivo - 1}].",
                    }
                )
            self.quick_sort(vetor_original, baixo, indice_pivo - 1)

            if self.registrar_passos:
                self.lista_passos.append(
                    {
                        "passo_numero": len(self.lista_passos) + 1,
                        "pseudo_codigo": "quick_sort(vetor, pivo + 1, alto)",
                        "descricao_acao": f"Chamada recursiva para subvetor à direita [{indice_pivo + 1}..{alto}].",
                    }
                )
            self.quick_sort(vetor_original, indice_pivo + 1, alto)

    def partition(
        self, vetor_original: list[CartaBaralho], baixo: int, alto: int
    ) -> int:
        carta_pivo = vetor_original[alto]
        i = baixo - 1

        if self.registrar_passos:
            self.lista_passos.append(
                {
                    "passo_numero": len(self.lista_passos) + 1,
                    "pseudo_codigo": "pivô ← vetor[alto]",
                    "descricao_acao": f"Pivô escolhido: {carta_pivo.texto_carta()} na posição {alto}.",
                }
            )

        for j in range(baixo, alto):
            self.total_comparacoes += 1
            if _valor_ordem(vetor_original[j]) <= _valor_ordem(carta_pivo):
                i += 1
                self.total_trocas += 1
                vetor_original[i], vetor_original[j] = (
                    vetor_original[j],
                    vetor_original[i],
                )

        self.total_trocas += 1
        vetor_original[i + 1], vetor_original[alto] = (
            vetor_original[alto],
            vetor_original[i + 1],
        )

        qtde_esq = (i + 1) - baixo
        qtde_dir = alto - (i + 1)

        if self.registrar_passos:
            self.lista_passos.append(
                {
                    "passo_numero": len(self.lista_passos) + 1,
                    "pseudo_codigo": "posicionar pivô entre menores e maiores",
                    "descricao_acao": (
                        f"Particionamento concluído. Pivô {carta_pivo.texto_carta()} "
                        f"no índice {i + 1}. "
                        f"Menores à esquerda: {qtde_esq} cartas, Maiores à direita: {qtde_dir} cartas."
                    ),
                }
            )

        return i + 1


def ordenacao_quick(
    vetor_cartas: list[CartaBaralho],
    *,
    registrar_passos: bool = True,
) -> dict[str, Any]:
    """Ordena in-place um vetor de cartas usando Quick Sort.

    Args:
        vetor_cartas: Lista de cartas.
        registrar_passos: Se True, registra o passo a passo.

    Returns:
        Dicionário com o resultado, métricas e log narrado.
    """
    inicio_tempo = time.perf_counter()

    algoritmo_interno = _QuickSortInterno(registrar_passos=registrar_passos)

    tamanho = len(vetor_cartas)
    if tamanho > 1:
        algoritmo_interno.quick_sort(vetor_cartas, 0, tamanho - 1)

    fim_tempo = time.perf_counter()
    tempo_execucao_ms = (fim_tempo - inicio_tempo) * 1000.0

    return {
        "algoritmo_nome": "Quick Sort",
        "vetor_cartas": vetor_cartas,
        "total_comparacoes": algoritmo_interno.total_comparacoes,
        "total_trocas": algoritmo_interno.total_trocas,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
        "passos_executados": algoritmo_interno.lista_passos,
    }
