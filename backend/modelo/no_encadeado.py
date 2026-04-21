"""Nó da lista duplamente encadeada que armazena uma carta."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from modelo.carta_baralho import CartaBaralho


class NoEncadeado:
    """Nó com ponteiro para antecessor e sucessor na lista dupla.

    Attributes:
        dados_carta: Carta armazenada neste nó.
        proximo_no: Próximo nó na sequência ou None.
        anterior_no: Nó anterior na sequência ou None.
    """

    def __init__(
        self,
        dados_carta: CartaBaralho,
        *,
        proximo_no: Optional["NoEncadeado"] = None,
        anterior_no: Optional["NoEncadeado"] = None,
    ) -> None:
        """Cria um nó contendo a carta informada.

        Args:
            dados_carta: Carta associada ao nó.
            proximo_no: Ligação para o próximo nó (opcional).
            anterior_no: Ligação para o nó anterior (opcional).
        """
        self.dados_carta = dados_carta
        self.proximo_no = proximo_no
        self.anterior_no = anterior_no
