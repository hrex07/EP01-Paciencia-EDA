"""Exceções relacionadas a cartas inválidas ou tipos incorretos nas estruturas."""


class CartaInvalidaError(ValueError):
    """Lançada quando número, naipe ou tipo de objeto não satisfaz o domínio esperado.

    Herda de :class:`ValueError` para compatibilidade com validações comuns.
    """
