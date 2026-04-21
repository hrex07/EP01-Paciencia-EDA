"""Exceções relacionadas a cartas inválidas."""


class CartaInvalidaError(ValueError):
    """Carta com número ou naipe fora do domínio permitido."""
