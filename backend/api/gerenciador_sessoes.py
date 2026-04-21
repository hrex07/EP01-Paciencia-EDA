"""Gerenciamento de sessões do jogo em memória."""

import time
from typing import Optional

from motor.estado_jogo import EstadoJogo

class SessaoJogo:
    """Uma sessão ativa com controle de tempo (TTL)."""
    def __init__(self, estado: EstadoJogo):
        self.estado = estado
        self.ultimo_acesso = time.time()

# Dicionário que guarda as sessões ativas (id_sessao -> SessaoJogo)
sessoes_ativas: dict[str, SessaoJogo] = {}

# Tempo de expiração (TTL) em segundos. Ex: 2 horas = 7200s
TTL_SESSAO_SEGUNDOS = 7200


def obter_estado(id_sessao: str) -> Optional[EstadoJogo]:
    """Retorna o estado do jogo ou None se não existir / expirou."""
    _limpar_sessoes_expiradas()
    
    sessao = sessoes_ativas.get(id_sessao)
    if not sessao:
        return None
        
    sessao.ultimo_acesso = time.time()
    return sessao.estado


def salvar_estado(estado: EstadoJogo) -> None:
    """Salva o estado no dicionário de sessões."""
    sessoes_ativas[estado.id_sessao] = SessaoJogo(estado)
    _limpar_sessoes_expiradas()


def _limpar_sessoes_expiradas() -> None:
    """Remove sessões que passaram do TTL."""
    agora = time.time()
    expiradas = [
        id_sessao for id_sessao, sessao in sessoes_ativas.items()
        if agora - sessao.ultimo_acesso > TTL_SESSAO_SEGUNDOS
    ]
    for id_sessao in expiradas:
        del sessoes_ativas[id_sessao]
