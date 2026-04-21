"""Regras de validação de movimentos do Paciência."""

from typing import Any

from modelo.carta_baralho import CartaBaralho
from modelo.fila_cartas import FilaCartas
from modelo.lista_ligada_cartas import ListaLigadaCartas
from modelo.pilha_cartas import PilhaCartas


def _validar_pode_empilhar(
    carta_mover: CartaBaralho, pilha_destino: PilhaCartas
) -> tuple[bool, str]:
    """Verifica se carta_mover pode entrar em pilha_destino (M1 adaptado / inverso de M2)."""
    if pilha_destino.esta_vazia():
        if carta_mover.numero_carta == 1:
            return True, "Ás colocado em pilha vazia."
        return False, "Apenas um Ás pode iniciar uma pilha."
    
    topo = pilha_destino.espiar_topo(registrar_passos=False)["valor_retornado"]
    if carta_mover.naipe_carta != topo.naipe_carta:
        return False, "A carta deve ter o mesmo naipe da pilha."
    
    if carta_mover.numero_carta != topo.numero_carta + 1:
        return False, "A carta deve ser exatamente 1 número maior que o topo."
        
    return True, "Movimento válido para pilha."


def _validar_pode_listar(
    carta_mover: CartaBaralho, lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    """Verifica se carta_mover pode entrar no final de lista_destino (M1/M2/M3)."""
    if lista_destino.esta_vazia():
        if carta_mover.numero_carta == 13:
            return True, "Rei colocado em lista vazia."
        return False, "Apenas um Rei pode ser movido para uma lista vazia."
    
    ultima_carta = lista_destino.obter_ultima_carta(registrar_passos=False)["valor_retornado"]
    
    if carta_mover.cor_carta() == ultima_carta.cor_carta():
        return False, "As cores devem ser alternadas (preto/vermelho)."
    
    if carta_mover.numero_carta != ultima_carta.numero_carta - 1:
        return False, "A carta deve ser exatamente 1 número menor que a última."
        
    return True, "Movimento válido para lista ligada."


def validar_fila_para_pilha(
    fila_origem: FilaCartas, pilha_destino: PilhaCartas
) -> tuple[bool, str]:
    if fila_origem.esta_vazia():
        return False, "A fila de compra está vazia."
        
    carta_frente = fila_origem.espiar_frente(registrar_passos=False)["valor_retornado"]
    return _validar_pode_empilhar(carta_frente, pilha_destino)


def validar_fila_para_lista(
    fila_origem: FilaCartas, lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    if fila_origem.esta_vazia():
        return False, "A fila de compra está vazia."
        
    carta_frente = fila_origem.espiar_frente(registrar_passos=False)["valor_retornado"]
    return _validar_pode_listar(carta_frente, lista_destino)


def validar_pilha_para_lista(
    pilha_origem: PilhaCartas, lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    if pilha_origem.esta_vazia():
        return False, "A pilha de origem está vazia."
        
    carta_topo = pilha_origem.espiar_topo(registrar_passos=False)["valor_retornado"]
    return _validar_pode_listar(carta_topo, lista_destino)


def validar_lista_para_pilha(
    lista_origem: ListaLigadaCartas, pilha_destino: PilhaCartas
) -> tuple[bool, str]:
    if lista_origem.esta_vazia():
        return False, "A lista de origem está vazia."
        
    ultima_carta = lista_origem.obter_ultima_carta(registrar_passos=False)["valor_retornado"]
    return _validar_pode_empilhar(ultima_carta, pilha_destino)


def validar_lista_para_lista(
    lista_origem: ListaLigadaCartas,
    indice_corte: int,
    lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    if lista_origem.esta_vazia():
        return False, "A lista de origem está vazia."
        
    carta_corte = lista_origem.obter_carta_posicao(indice_corte, registrar_passos=False)["valor_retornado"]
    if carta_corte is None:
        return False, "Índice de corte inválido."
        
    if not carta_corte.status_carta:
        return False, "Não é possível mover cartas que estão viradas para baixo."
        
    return _validar_pode_listar(carta_corte, lista_destino)
