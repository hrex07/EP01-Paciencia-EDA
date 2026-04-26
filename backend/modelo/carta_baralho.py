"""Representação de uma carta de baralho tradicional (52 cartas)."""

from __future__ import annotations

from typing import Any, Final

from modelo.excecao_carta import CartaInvalidaError

_NAIPE_PARA_SIMBOLO: Final[dict[str, str]] = {
    "c": "\u2665",
    "o": "\u2666",
    "p": "\u2663",
    "e": "\u2660",
}


class CartaBaralho:
    """Carta com valor numérico, naipe e estado de visibilidade (virada ou não).

    Attributes:
        numero_carta: Valor de 1 (Ás) a 13 (Rei).
        naipe_carta: Letra do naipe em minúsculas: 'c' copas, 'o' ouros,
            'p' paus, 'e' espadas.
        status_carta: True se a face está visível (virada para cima).
    """

    def __init__(
        self,
        numero_carta: int,
        naipe_carta: str,
        *,
        status_carta: bool = False,
    ) -> None:
        """Instancia uma carta validando domínio de número e naipe.

        Args:
            numero_carta: Inteiro de 1 a 13.
            naipe_carta: Um dentre 'c', 'o', 'p', 'e'.
            status_carta: Se True, carta virada para cima.

        Raises:
            CartaInvalidaError: Se número ou naipe estiverem fora do permitido.
        """
        if numero_carta < 1 or numero_carta > 13:
            raise CartaInvalidaError(
                f"numero_carta deve estar entre 1 e 13, recebido: {numero_carta}"
            )
        naipe_normalizado = naipe_carta.lower().strip()
        if naipe_normalizado not in _NAIPE_PARA_SIMBOLO:
            raise CartaInvalidaError(
                f"naipe_carta deve ser um de 'c','o','p','e', recebido: {naipe_carta!r}"
            )
        self.numero_carta = numero_carta
        self.naipe_carta = naipe_normalizado
        self.status_carta = status_carta

    def cor_carta(self) -> str:
        """Retorna a cor da carta para regras de alternância no tableau.

        Returns:
            'vermelha' para copas e ouros; 'preta' para paus e espadas.
        """
        if self.naipe_carta in ("c", "o"):
            return "vermelha"
        return "preta"

    def para_dicionario_json(self) -> dict[str, Any]:
        """Mapeia a carta para dicionário JSON (API e ``operacoes_realizadas``).

        Carta virada para baixo não expõe número ou naipe; alinha com
        :meth:`motor.estado_jogo.EstadoJogo.serializar` para o tabuleiro.

        Returns:
            Dict com ``status_carta`` e, se virada para cima, campos ``numero_carta``,
            ``naipe_carta``, ``texto`` e ``cor``.
        """
        if not self.status_carta:
            return {"status_carta": False, "texto": "verso"}
        return {
            "numero_carta": self.numero_carta,
            "naipe_carta": self.naipe_carta,
            "status_carta": True,
            "texto": self.texto_carta(),
            "cor": self.cor_carta(),
        }

    def serializar_completo(self) -> dict[str, Any]:
        """Mapeia a carta para JSON completo (persistência / Firestore).

        Returns:
            Dict sempre com ``numero_carta``, ``naipe_carta`` e ``status_carta``.
        """
        return {
            "numero_carta": self.numero_carta,
            "naipe_carta": self.naipe_carta,
            "status_carta": self.status_carta,
        }

    @staticmethod
    def desserializar(dados: dict[str, Any]) -> CartaBaralho:
        """Recria uma instância a partir de um dicionário (persistência completa).

        Args:
            dados: Saída de :meth:`serializar_completo` com chaves obrigatórias.

        Returns:
            Nova instância de ``CartaBaralho``.

        Note:
            O JSON público da API para carta virada não inclui número/naipe;
            esse método destina-se ao payload completo salvo no Firestore.
        """
        return CartaBaralho(
            numero_carta=dados["numero_carta"],
            naipe_carta=dados["naipe_carta"],
            status_carta=dados.get("status_carta", False),
        )

    def texto_carta(self) -> str:
        """Representação curta legível: número + símbolo do naipe Unicode.

        Returns:
            Texto como 'A♠', '10♥', 'K♦'.
        """
        simbolo_naipe = _NAIPE_PARA_SIMBOLO[self.naipe_carta]
        if self.numero_carta == 1:
            rotulo_valor = "A"
        elif self.numero_carta == 11:
            rotulo_valor = "J"
        elif self.numero_carta == 12:
            rotulo_valor = "Q"
        elif self.numero_carta == 13:
            rotulo_valor = "K"
        else:
            rotulo_valor = str(self.numero_carta)
        return f"{rotulo_valor}{simbolo_naipe}"

    def __repr__(self) -> str:
        return (
            f"CartaBaralho(numero_carta={self.numero_carta!r}, "
            f"naipe_carta={self.naipe_carta!r}, status_carta={self.status_carta!r})"
        )

    def __eq__(self, outro_objeto: object) -> bool:
        """Igualdade por número, naipe e status de visibilidade."""
        if not isinstance(outro_objeto, CartaBaralho):
            return NotImplemented
        return (
            self.numero_carta == outro_objeto.numero_carta
            and self.naipe_carta == outro_objeto.naipe_carta
            and self.status_carta == outro_objeto.status_carta
        )
