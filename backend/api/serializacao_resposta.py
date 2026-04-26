"""Conversão de estruturas do motor para JSON (respostas da API)."""

from __future__ import annotations

from typing import Any

from modelo.carta_baralho import CartaBaralho

# Evita `RecursionError` em passos muito aninhados (e o ASGI a devolver 21 B text/plain
# "Internal Server Error" quando a pilha C está esgotada e o exception handler nem corre).
_SANIT_PROF_MAX = 200


def _sanit_motor(
    objeto_qualquer: Any,
    *,
    _prof: int = 0,
    _caminho_ids: list[int] | None = None,
) -> Any:
    """Serializa recursivamente objetos do domínio para tipos JSON-safe.

    Args:
        objeto_qualquer: Valor arbitrário (dict, list, ``CartaBaralho``, etc.).
        _prof: Profundidade atual na travessia (uso interno).
        _caminho_ids: Rastreamento de ``id()`` para detetar ciclos (interno).

    Returns:
        Estrutura equivalente só com tipos serializáveis em JSON; ciclos e
        profundidade excessiva são substituídos por mensagens curtas em string.
    """
    if _prof > _SANIT_PROF_MAX:
        return f"<aninhamento máximo ({_SANIT_PROF_MAX}) excedido>"

    if isinstance(objeto_qualquer, CartaBaralho):
        return objeto_qualquer.para_dicionario_json()

    if _caminho_ids is None:
        _caminho_ids = []

    if isinstance(objeto_qualquer, (dict, list)):
        oid = id(objeto_qualquer)
        if oid in _caminho_ids:
            return "<ciclo: dict ou list>"
        _caminho_ids.append(oid)
        try:
            if isinstance(objeto_qualquer, list):
                return [
                    _sanit_motor(item, _prof=_prof + 1, _caminho_ids=_caminho_ids)
                    for item in objeto_qualquer
                ]
            return {
                chave: _sanit_motor(valor, _prof=_prof + 1, _caminho_ids=_caminho_ids)
                for chave, valor in objeto_qualquer.items()
            }
        finally:
            _caminho_ids.pop()

    if isinstance(objeto_qualquer, tuple):
        return _sanit_motor(list(objeto_qualquer), _prof=_prof, _caminho_ids=_caminho_ids)
    if isinstance(objeto_qualquer, set):
        return _sanit_motor(list(objeto_qualquer), _prof=_prof, _caminho_ids=_caminho_ids)
    if isinstance(objeto_qualquer, bool) or isinstance(objeto_qualquer, (str, int)) or objeto_qualquer is None:
        return objeto_qualquer
    if isinstance(objeto_qualquer, float):
        if objeto_qualquer != objeto_qualquer:  # NaN
            return None
        return objeto_qualquer
    return str(objeto_qualquer)


def sanitizar_motor_para_json(objeto_qualquer: Any) -> Any:
    """Converte aninhadamente :class:`CartaBaralho` em dicionários dentro de dicts/listas.

    Usado em ``log_preparacao`` e ``operacoes_realizadas``: o ASGI não serializa
    instâncias de modelos de domínio. Inclui limite de profundidade e deteção
    básica de ciclos para evitar ``RecursionError`` (500 em ``text/plain``).

    Args:
        objeto_qualquer: Resposta parcial ou completa do motor (dict/list).

    Returns:
        Mesma forma aninhada com cartas como dicts e sem referências cíclicas.
    """
    return _sanit_motor(objeto_qualquer, _prof=0, _caminho_ids=None)
