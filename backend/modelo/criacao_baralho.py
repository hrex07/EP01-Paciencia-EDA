"""Funções para criar um baralho completo de 52 cartas ordenado por naipe."""

from __future__ import annotations

from typing import Any

from modelo.carta_baralho import CartaBaralho

_ORDEM_NAIPE_BARALHO: tuple[str, ...] = ("c", "o", "p", "e")


def criar_baralho_completo(
    *,
    registrar_passos: bool = True,
) -> dict[str, Any]:
    """Monta um vetor (lista Python) com as 52 cartas únicas do baralho.

    Percorre naipes na ordem copas, ouros, paus, espadas e valores 1..13 para cada.

    Args:
        registrar_passos: Se True, inclui um passo por carta adicionada ao vetor.

    Returns:
        Dicionário com:
            ``vetor_cartas``: lista de ``CartaBaralho`` (tamanho 52),
            ``total_cartas``: 52,
            ``passos_executados``: lista de passos didáticos (vazia se
            ``registrar_passos`` for False).
    """
    vetor_cartas: list[CartaBaralho] = []
    lista_passos: list[dict[str, Any]] = []

    for naipe_atual in _ORDEM_NAIPE_BARALHO:
        for numero_atual in range(1, 14):
            carta_nova = CartaBaralho(numero_atual, naipe_atual)
            indice_posicao = len(vetor_cartas)
            vetor_cartas.append(carta_nova)
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": len(lista_passos) + 1,
                        "pseudo_codigo": (
                            f"vetor_cartas[{indice_posicao}] ← carta({numero_atual}, "
                            f"'{naipe_atual}')"
                        ),
                        "descricao_acao": (
                            f"Inserir na posição {indice_posicao} a carta "
                            f"{carta_nova.texto_carta()}."
                        ),
                    }
                )

    return {
        "operacao_nome": "criar_baralho_completo",
        "vetor_cartas": vetor_cartas,
        "total_cartas": len(vetor_cartas),
        "passos_executados": lista_passos,
    }
