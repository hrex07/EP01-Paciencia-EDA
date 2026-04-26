"""Exclusão mútua por `id_sessao` nas rotas que alteram o :class:`EstadoJogo` em memória.

Evita condição de corrida entre requisições concorrentes (ex.: fila lida na validação
e esvaziada por outro pedido antes do `desenfileirar` neste), que levava a
`inserir_final(None)` / 500.
"""

import threading

_registry = threading.Lock()
_por_sessao: dict[str, threading.RLock] = {}


def lock_motor_sessao(id_sessao: str) -> threading.RLock:
    with _registry:
        if id_sessao not in _por_sessao:
            _por_sessao[id_sessao] = threading.RLock()
        return _por_sessao[id_sessao]
