"""Ordenação via Merge Sort com logs de demonstração."""

import time
from typing import Any

from modelo.carta_baralho import CartaBaralho


def _valor_ordem(carta: CartaBaralho) -> tuple[int, int]:
    naipe_peso = {"c": 0, "o": 1, "p": 2, "e": 3}
    return (naipe_peso.get(carta.naipe_carta, 0), carta.numero_carta)


class _MergSortInterno:
    def __init__(self, registrar_passos: bool) -> None:
        self.registrar_passos = registrar_passos
        self.total_comparacoes = 0
        self.total_trocas = 0  # Em merge sort usamos cópias, mas contamos inserções
        self.lista_passos: list[dict[str, Any]] = []

    def merge_sort(
        self, vetor_original: list[CartaBaralho], inicio: int, fim: int
    ) -> None:
        if inicio < fim:
            meio = (inicio + fim) // 2

            if self.registrar_passos:
                self.lista_passos.append(
                    {
                        "passo_numero": len(self.lista_passos) + 1,
                        "pseudo_codigo": "Dividir vetor em duas metades",
                        "descricao_acao": f"Dividir vetor[{inicio}..{fim}] no índice {meio}.",
                    }
                )

            self.merge_sort(vetor_original, inicio, meio)
            self.merge_sort(vetor_original, meio + 1, fim)

            self.merge(vetor_original, inicio, meio, fim)

    def merge(
        self, vetor_original: list[CartaBaralho], inicio: int, meio: int, fim: int
    ) -> None:
        if self.registrar_passos:
            self.lista_passos.append(
                {
                    "passo_numero": len(self.lista_passos) + 1,
                    "pseudo_codigo": "Mesclar duas metades ordenadas",
                    "descricao_acao": f"Mesclar vetor[{inicio}..{meio}] com vetor[{meio + 1}..{fim}].",
                }
            )

        n_esquerda = meio - inicio + 1
        n_direita = fim - meio

        esquerda = vetor_original[inicio : meio + 1]
        direita = vetor_original[meio + 1 : fim + 1]

        i_esq = 0
        i_dir = 0
        k = inicio

        while i_esq < n_esquerda and i_dir < n_direita:
            self.total_comparacoes += 1
            carta_esq = esquerda[i_esq]
            carta_dir = direita[i_dir]

            if _valor_ordem(carta_esq) <= _valor_ordem(carta_dir):
                if self.registrar_passos:
                    self.lista_passos.append(
                        {
                            "passo_numero": len(self.lista_passos) + 1,
                            "pseudo_codigo": "SE esq ≤ dir ENTÃO vetor[k] ← esq",
                            "descricao_acao": (
                                f"{carta_esq.texto_carta()} ≤ {carta_dir.texto_carta()}, "
                                f"mantém da esquerda no índice {k}."
                            ),
                        }
                    )
                vetor_original[k] = esquerda[i_esq]
                i_esq += 1
            else:
                self.total_trocas += 1
                if self.registrar_passos:
                    self.lista_passos.append(
                        {
                            "passo_numero": len(self.lista_passos) + 1,
                            "pseudo_codigo": "SENÃO vetor[k] ← dir",
                            "descricao_acao": (
                                f"{carta_esq.texto_carta()} > {carta_dir.texto_carta()}, "
                                f"traz {carta_dir.texto_carta()} para índice {k}."
                            ),
                        }
                    )
                vetor_original[k] = direita[i_dir]
                i_dir += 1
            k += 1

        while i_esq < n_esquerda:
            vetor_original[k] = esquerda[i_esq]
            i_esq += 1
            k += 1
            self.total_trocas += 1

        while i_dir < n_direita:
            vetor_original[k] = direita[i_dir]
            i_dir += 1
            k += 1
            self.total_trocas += 1


def ordenacao_merge(
    vetor_cartas: list[CartaBaralho],
    *,
    registrar_passos: bool = True,
) -> dict[str, Any]:
    """Ordena in-place um vetor de cartas usando Merge Sort.

    Args:
        vetor_cartas: Lista de cartas.
        registrar_passos: Se True, registra o passo a passo.

    Returns:
        Dicionário com o resultado, métricas e log narrado.
    """
    inicio_tempo = time.perf_counter()

    algoritmo_interno = _MergSortInterno(registrar_passos=registrar_passos)

    tamanho = len(vetor_cartas)
    if tamanho > 1:
        algoritmo_interno.merge_sort(vetor_cartas, 0, tamanho - 1)

    fim_tempo = time.perf_counter()
    tempo_execucao_ms = (fim_tempo - inicio_tempo) * 1000.0

    return {
        "algoritmo_nome": "Merge Sort",
        "vetor_cartas": vetor_cartas,
        "total_comparacoes": algoritmo_interno.total_comparacoes,
        "total_trocas": algoritmo_interno.total_trocas,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
        "passos_executados": algoritmo_interno.lista_passos,
    }
