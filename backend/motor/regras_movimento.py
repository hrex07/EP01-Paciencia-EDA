"""Regras de validação de movimentos do Paciência (Klondike / EP01).

Funções puras que consultam fila, pilhas e listas ligadas sem alterar estado,
retornando ``(True, mensagem_ok)`` ou ``(False, motivo_da_rejeição)``.
"""

from modelo.carta_baralho import CartaBaralho
from modelo.fila_cartas import FilaCartas
from modelo.lista_ligada_cartas import ListaLigadaCartas
from modelo.pilha_cartas import PilhaCartas


def _leitura_topo_pilha_ou_motivo(pilha: PilhaCartas) -> tuple[CartaBaralho | None, str | None]:
    """Lê o topo da pilha sem pop; devolve motivo textual se leitura falhar.

    Args:
        pilha: Pilha de fundação ou auxiliar.

    Returns:
        Tupla ``(carta, None)`` em sucesso, ou ``(None, mensagem_erro)``.
    """
    r = pilha.espiar_topo(registrar_passos=False)
    if not r.get("operacao_sucesso"):
        return None, "A pilha de destino está vazia (leitura inconsistente)."
    c = r.get("valor_retornado")
    if not isinstance(c, CartaBaralho):
        return None, "Não foi possível ler o topo da pilha (estado inconsistente)."
    return c, None


def _leitura_ultima_lista_ou_motivo(lista: ListaLigadaCartas) -> tuple[CartaBaralho | None, str | None]:
    """Lê a carta da cauda da lista sem remover.

    Args:
        lista: Coluna do tableau.

    Returns:
        Tupla ``(carta, None)`` ou ``(None, mensagem_erro)``.
    """
    r = lista.obter_ultima_carta(registrar_passos=False)
    if not r.get("operacao_sucesso"):
        return None, "A lista de origem está vazia (leitura inconsistente com a validação anterior)."
    c = r.get("valor_retornado")
    if not isinstance(c, CartaBaralho):
        return None, "Não foi possível ler a última carta (estado inconsistente na coluna)."
    return c, None


def _validar_pode_empilhar(
    carta_mover: CartaBaralho, pilha_destino: PilhaCartas
) -> tuple[bool, str]:
    """Verifica se ``carta_mover`` pode ser empilhada em ``pilha_destino``.

    Regras: Ás inicia pilha vazia; demais cartas mesmo naipe e sequência crescente.

    Args:
        carta_mover: Carta candidata ao topo da pilha.
        pilha_destino: Pilha de fundação de destino.

    Returns:
        ``(True, mensagem)`` ou ``(False, motivo)``.
    """
    if pilha_destino.esta_vazia():
        if carta_mover.numero_carta == 1:
            return True, "Ás colocado em pilha vazia."
        return False, "Apenas um Ás pode iniciar uma pilha."

    topo, err = _leitura_topo_pilha_ou_motivo(pilha_destino)
    if err or topo is None:
        return False, err or "Não foi possível validar a pilha de destino."

    if carta_mover.naipe_carta != topo.naipe_carta:
        return False, "A carta deve ter o mesmo naipe da pilha."

    if carta_mover.numero_carta != topo.numero_carta + 1:
        return False, "A carta deve ser exatamente 1 número maior que o topo."

    return True, "Movimento válido para pilha."


def _validar_pode_listar(
    carta_mover: CartaBaralho, lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    """Verifica se ``carta_mover`` pode ir ao final de ``lista_destino`` (tableau).

    Args:
        carta_mover: Carta a posicionar na coluna.
        lista_destino: Lista duplamente encadeada da coluna.

    Returns:
        ``(True, mensagem)`` ou ``(False, motivo)``.
    """
    if lista_destino.esta_vazia():
        if carta_mover.numero_carta == 13:
            return True, "Rei colocado em lista vazia."
        return False, "Apenas um Rei pode ser movido para uma lista vazia."

    ultima_carta, err = _leitura_ultima_lista_ou_motivo(lista_destino)
    if err or ultima_carta is None:
        return False, err or "Não foi possível validar a coluna de destino."

    if carta_mover.cor_carta() == ultima_carta.cor_carta():
        return False, "As cores devem ser alternadas (preto/vermelho)."

    if carta_mover.numero_carta != ultima_carta.numero_carta - 1:
        return False, "A carta deve ser exatamente 1 número menor que a última."

    return True, "Movimento válido para lista ligada."


def validar_fila_para_pilha(
    fila_origem: FilaCartas, pilha_destino: PilhaCartas
) -> tuple[bool, str]:
    """Valida movimento da frente da fila de compra para uma pilha de fundação.

    Args:
        fila_origem: Fila de compra.
        pilha_destino: Pilha de destino.

    Returns:
        Resultado da validação de empilhamento sobre a carta da frente.
    """
    if fila_origem.esta_vazia():
        return False, "A fila de compra está vazia."

    r = fila_origem.espiar_frente(registrar_passos=False)
    if not r.get("operacao_sucesso"):
        return False, "Não foi possível ler a frente da fila."
    carta_frente = r.get("valor_retornado")
    if not isinstance(carta_frente, CartaBaralho):
        return False, "Estado inconsistente: carta inválida na fila de compra."
    return _validar_pode_empilhar(carta_frente, pilha_destino)


def validar_fila_para_lista(
    fila_origem: FilaCartas, lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    """Valida movimento da frente da fila para o final de uma coluna do tableau.

    Args:
        fila_origem: Fila de compra.
        lista_destino: Coluna de destino.

    Returns:
        Resultado da validação de encaixe na lista.
    """
    if fila_origem.esta_vazia():
        return False, "A fila de compra está vazia."

    r = fila_origem.espiar_frente(registrar_passos=False)
    if not r.get("operacao_sucesso"):
        return False, "Não foi possível ler a frente da fila."
    carta_frente = r.get("valor_retornado")
    if not isinstance(carta_frente, CartaBaralho):
        return False, "Estado inconsistente: carta inválida na fila de compra."
    return _validar_pode_listar(carta_frente, lista_destino)


def validar_pilha_para_lista(
    pilha_origem: PilhaCartas, lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    """Valida movimento do topo da pilha de origem para o final da coluna.

    Args:
        pilha_origem: Pilha de onde sai a carta.
        lista_destino: Coluna do tableau.

    Returns:
        Resultado da validação de encaixe na lista.
    """
    if pilha_origem.esta_vazia():
        return False, "A pilha de origem está vazia."

    r = pilha_origem.espiar_topo(registrar_passos=False)
    if not r.get("operacao_sucesso"):
        return False, "Não foi possível ler a pilha de origem."
    carta_topo = r.get("valor_retornado")
    if not isinstance(carta_topo, CartaBaralho):
        return False, "Estado inconsistente: carta inválida na pilha de origem."
    return _validar_pode_listar(carta_topo, lista_destino)


def validar_lista_para_pilha(
    lista_origem: ListaLigadaCartas, pilha_destino: PilhaCartas
) -> tuple[bool, str]:
    """Valida movimento da última carta visível da coluna para a pilha.

    Args:
        lista_origem: Coluna do tableau.
        pilha_destino: Pilha de fundação.

    Returns:
        Resultado da validação de empilhamento sobre a última carta da lista.
    """
    if lista_origem.esta_vazia():
        return False, "A lista de origem está vazia."

    ultima_carta, err = _leitura_ultima_lista_ou_motivo(lista_origem)
    if err or ultima_carta is None:
        return False, err or "Não foi possível validar a coluna de origem."

    return _validar_pode_empilhar(ultima_carta, pilha_destino)


def validar_lista_para_lista(
    lista_origem: ListaLigadaCartas,
    indice_corte: int,
    lista_destino: ListaLigadaCartas
) -> tuple[bool, str]:
    """Valida movimento de sublista (a partir de ``indice_corte``) entre colunas.

    Args:
        lista_origem: Coluna de onde parte o sufixo.
        indice_corte: Índice base zero do primeiro nó movido (face da carta deve estar para cima).
        lista_destino: Coluna de destino.

    Returns:
        ``(True, mensagem)`` ou ``(False, motivo)`` (índice, cor, ordem numérica).
    """
    if lista_origem.esta_vazia():
        return False, "A lista de origem está vazia."

    n = lista_origem.obter_tamanho()
    if indice_corte < 0 or indice_corte >= n:
        return (
            False,
            f"Índice de corte {indice_corte} fora do intervalo: a coluna tem {n} carta(s) "
            f"(use índices 0 a {n - 1} desde a cabeça da lista; o primeiro nó é 0).",
        )

    rpos = lista_origem.obter_carta_posicao(indice_corte, registrar_passos=False)
    if not rpos.get("operacao_sucesso"):
        return False, "Não foi possível ler a carta no índice de corte (estado inconsistente)."
    carta_corte = rpos.get("valor_retornado")
    if not isinstance(carta_corte, CartaBaralho):
        return False, "Não foi possível ler a carta no índice de corte (estado inconsistente)."

    if not carta_corte.status_carta:
        return False, "Não é possível mover cartas que estão viradas para baixo."
        
    return _validar_pode_listar(carta_corte, lista_destino)
