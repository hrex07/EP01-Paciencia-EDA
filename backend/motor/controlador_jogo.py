"""Orquestrador do jogo: distribuição, movimentação e streaks."""

from typing import Any, Optional

from algoritmos.embaralhamento_recursivo import embaralhar_recursivo
from modelo.carta_baralho import CartaBaralho
from modelo.criacao_baralho import criar_baralho_completo
from modelo.fila_cartas import FilaCartas
from modelo.lista_ligada_cartas import ListaLigadaCartas
from modelo.pilha_cartas import PilhaCartas
from motor.estado_jogo import EstadoJogo
from motor import regras_movimento


def _rejeitar_por_estrutura_inconsistente(estado: EstadoJogo, motivo: str) -> dict[str, Any]:
    """Monta resposta de jogada inválida quando a estrutura falha após validação.

    Cobre casos raros de corrida ou estado inconsistente (ex.: fila lida como
    não vazia e esvaziada por outro pedido antes do ``desenfileirar``).

    Args:
        estado: Partida atual (para atualizar streak).
        motivo: Mensagem explicativa para o cliente.

    Returns:
        Dict com ``jogada_valida`` falso, ``motivo_rejeicao``, ``streak`` e
        ``operacoes_realizadas`` vazia.
    """
    streak = atualizar_streak(estado, False, [])
    return {
        "jogada_valida": False,
        "motivo_rejeicao": motivo,
        "streak": streak,
        "operacoes_realizadas": [],
    }


def distribuir_cartas_novo_jogo(estado: EstadoJogo) -> list[dict[str, Any]]:
    """Cria baralho, embaralha e distribui as cartas nas sete colunas e na fila.

    Args:
        estado: Partida mutada in-place (listas e fila preenchidas).

    Returns:
        Lista plana de passos didáticos (``passo_numero``, ``pseudo_codigo``,
        ``descricao_acao``) acumulados de todas as operações de preparação.
    """
    log_preparacao: list[dict[str, Any]] = []

    resultado_baralho = criar_baralho_completo(registrar_passos=True)
    vetor_cartas = resultado_baralho["vetor_cartas"]
    log_preparacao.extend(resultado_baralho["passos_executados"])

    resultado_embaralhar = embaralhar_recursivo(
        vetor_cartas, quantidade_trocas=100, registrar_passos=True
    )
    vetor_embaralhado = resultado_embaralhar["vetor_cartas"]
    log_preparacao.extend(resultado_embaralhar["passos_executados"])

    indice_carta = 0

    # Distribui nas 7 listas: L1=1, L2=2... L7=7
    for i in range(7):
        lista = estado.listas_tableau[i]
        qtde_cartas = i + 1
        for j in range(qtde_cartas):
            carta = vetor_embaralhado[indice_carta]
            indice_carta += 1

            # Apenas a última carta de cada lista fica virada para cima
            carta.status_carta = (j == qtde_cartas - 1)

            resultado_inserir = lista.inserir_final(carta, registrar_passos=True)
            log_preparacao.extend(resultado_inserir["passos_executados"])

    # Restante na fila
    while indice_carta < len(vetor_embaralhado):
        carta = vetor_embaralhado[indice_carta]
        indice_carta += 1
        
        # Na fila ficam viradas para baixo ou cima? Solitaire clássico elas ficam viradas
        # para baixo até o usuário comprar. No EP01 o usuário só vê o topo, mas podemos
        # deixar true para facilitar ou falso. O EP01 sugere "virar" mas vamos deixar
        # True por simplicidade didática da "frente" da fila.
        carta.status_carta = True
        
        resultado_fila = estado.fila_compra.enfileirar(carta, registrar_passos=True)
        log_preparacao.extend(resultado_fila["passos_executados"])

    return log_preparacao


def _virar_carta_lista(lista: ListaLigadaCartas) -> list[dict[str, Any]]:
    """Revela a última carta da coluna (Klondike) se estiver com face para baixo.

    Args:
        lista: Coluna do tableau.

    Returns:
        Lista de passos narrados (pode ser vazia se lista vazia ou carta já virada).
    """
    passos: list[dict[str, Any]] = []
    if lista.esta_vazia():
        return passos

    resultado_ultima = lista.obter_ultima_carta(registrar_passos=False)
    if not resultado_ultima.get("operacao_sucesso"):
        return passos
    ultima = resultado_ultima.get("valor_retornado")
    if not isinstance(ultima, CartaBaralho):
        return passos

    if not ultima.status_carta:
        ultima.status_carta = True
        passos.append(
            {
                "passo_numero": 1,
                "pseudo_codigo": "última_carta.status ← True",
                "descricao_acao": f"Revelou carta na {lista.nome_lista}: {ultima.texto_carta()}",
            }
        )
    return passos


def atualizar_streak(estado: EstadoJogo, jogada_valida: bool, estruturas_usadas: list[str]) -> dict[str, Any]:
    """Atualiza contadores de sequência e devolve feedback educacional.

    Args:
        estado: Partida (campos ``sequencia_atual``, ``total_jogadas``, etc.).
        jogada_valida: Se a jogada aplicada foi aceita pelo motor.
        estruturas_usadas: Nomes didáticos das estruturas envolvidas (para a mensagem).

    Returns:
        Dict com ``sequencia_atual``, ``maior_sequencia``, ``nivel_efeito`` e
        ``mensagem_educacional`` para o frontend.
    """
    if jogada_valida:
        estado.sequencia_atual += 1
        estado.total_jogadas += 1
        if estado.sequencia_atual > estado.maior_sequencia:
            estado.maior_sequencia = estado.sequencia_atual
            
        nivel = "basico"
        if estado.sequencia_atual >= 10:
            nivel = "mestre"
        elif estado.sequencia_atual >= 7:
            nivel = "incrivel"
        elif estado.sequencia_atual >= 5:
            nivel = "confetti"
        elif estado.sequencia_atual >= 3:
            nivel = "otimo"
        elif estado.sequencia_atual >= 2:
            nivel = "bom"
            
        estruturas_nomes = ", ".join(set(estruturas_usadas))
        msg = f"{estado.sequencia_atual} movimentos em sequência usando: {estruturas_nomes}!"
    else:
        estado.sequencia_atual = 0
        nivel = "erro"
        msg = "Sequência quebrada. Tente novamente."
        
    return {
        "sequencia_atual": estado.sequencia_atual,
        "maior_sequencia": estado.maior_sequencia,
        "nivel_efeito": nivel,
        "mensagem_educacional": msg
    }


def verificar_vitoria(estado: EstadoJogo) -> bool:
    """Define ``jogo_vencido`` se as quatro pilhas de fundação tiverem 13 cartas cada.

    Args:
        estado: Partida a inspecionar (mutado quando há vitória).

    Returns:
        ``True`` se e somente se todas as pilhas estão completas.
    """
    for pilha in estado.pilhas_fundacao.values():
        if pilha.obter_tamanho() != 13:
            return False
    estado.jogo_vencido = True
    return True


def executar_fila_para_fila(estado: EstadoJogo) -> dict[str, Any]:
    """Executa movimento tipo 1: rotação da frente da fila de compra para o final.

    Args:
        estado: Partida cujo ``fila_compra`` será alterado.

    Returns:
        Resultado padrão com ``jogada_valida``, ``operacoes_realizadas`` e ``streak``.
    """
    resultado = estado.fila_compra.reposicionar_frente(registrar_passos=True)
    if not resultado["operacao_sucesso"]:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": "Fila vazia", "streak": streak, "operacoes_realizadas": []}
        
    streak = atualizar_streak(estado, True, ["Fila (FIFO)"])
    return {
        "jogada_valida": True,
        "operacoes_realizadas": [resultado],
        "streak": streak
    }


def executar_fila_para_pilha(estado: EstadoJogo, naipe_destino: str) -> dict[str, Any]:
    """Executa movimento tipo 2: frente da fila para pilha de fundação do naipe dado.

    Args:
        estado: Partida atual.
        naipe_destino: Chave da pilha: ``c``, ``o``, ``p`` ou ``e``.

    Returns:
        Resultado padrão; em vitória, ``streak['nivel_efeito']`` pode ser ``vitoria``.
    """
    pilha = estado.pilhas_fundacao.get(naipe_destino)
    if not pilha:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": "Pilha inválida", "streak": streak, "operacoes_realizadas": []}
        
    valido, motivo = regras_movimento.validar_fila_para_pilha(estado.fila_compra, pilha)
    if not valido:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": motivo, "streak": streak, "operacoes_realizadas": []}
        
    res_fila = estado.fila_compra.desenfileirar(registrar_passos=True)
    if not res_fila.get("operacao_sucesso") or not isinstance(
        res_fila.get("valor_retornado"), CartaBaralho
    ):
        return _rejeitar_por_estrutura_inconsistente(
            estado, "Fila vazia ao retirar a carta; atualize o estado e tente de novo."
        )
    carta = res_fila["valor_retornado"]
    res_pilha = pilha.empilhar(carta, registrar_passos=True)
    
    venceu = verificar_vitoria(estado)
    streak = atualizar_streak(estado, True, ["Fila (FIFO)", "Pilha (LIFO)"])
    if venceu:
        streak["nivel_efeito"] = "vitoria"
        
    return {
        "jogada_valida": True,
        "operacoes_realizadas": [res_fila, res_pilha],
        "streak": streak
    }


def executar_fila_para_lista(estado: EstadoJogo, indice_lista: int) -> dict[str, Any]:
    """Executa movimento tipo 3: frente da fila para o final da coluna ``indice_lista``.

    Args:
        estado: Partida atual.
        indice_lista: Índice 0..6 da coluna do tableau.

    Returns:
        Resultado padrão do motor.
    """
    if indice_lista < 0 or indice_lista > 6:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": "Lista inválida", "streak": streak, "operacoes_realizadas": []}
        
    lista = estado.listas_tableau[indice_lista]
    valido, motivo = regras_movimento.validar_fila_para_lista(estado.fila_compra, lista)
    if not valido:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": motivo, "streak": streak, "operacoes_realizadas": []}
        
    res_fila = estado.fila_compra.desenfileirar(registrar_passos=True)
    if not res_fila.get("operacao_sucesso") or not isinstance(
        res_fila.get("valor_retornado"), CartaBaralho
    ):
        return _rejeitar_por_estrutura_inconsistente(
            estado, "Fila vazia ao retirar a carta; atualize o estado e tente de novo."
        )
    carta = res_fila["valor_retornado"]
    res_lista = lista.inserir_final(carta, registrar_passos=True)
    
    streak = atualizar_streak(estado, True, ["Fila (FIFO)", "Lista Ligada"])
    return {
        "jogada_valida": True,
        "operacoes_realizadas": [res_fila, res_lista],
        "streak": streak
    }


def executar_pilha_para_lista(estado: EstadoJogo, naipe_origem: str, indice_lista: int) -> dict[str, Any]:
    """Executa movimento tipo 4: topo da pilha de ``naipe_origem`` para a coluna.

    Args:
        estado: Partida atual.
        naipe_origem: ``c``, ``o``, ``p`` ou ``e``.
        indice_lista: Coluna de destino (0..6).

    Returns:
        Resultado padrão do motor.
    """
    pilha = estado.pilhas_fundacao.get(naipe_origem)
    if not pilha or indice_lista < 0 or indice_lista > 6:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": "Pilha ou lista inválida", "streak": streak, "operacoes_realizadas": []}
        
    lista = estado.listas_tableau[indice_lista]
    valido, motivo = regras_movimento.validar_pilha_para_lista(pilha, lista)
    if not valido:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": motivo, "streak": streak, "operacoes_realizadas": []}
        
    res_pilha = pilha.desempilhar(registrar_passos=True)
    if not res_pilha.get("operacao_sucesso") or not isinstance(
        res_pilha.get("valor_retornado"), CartaBaralho
    ):
        return _rejeitar_por_estrutura_inconsistente(
            estado, "Pilha vazia ao retirar a carta; atualize o estado e tente de novo."
        )
    carta = res_pilha["valor_retornado"]
    res_lista = lista.inserir_final(carta, registrar_passos=True)
    
    streak = atualizar_streak(estado, True, ["Pilha (LIFO)", "Lista Ligada"])
    return {
        "jogada_valida": True,
        "operacoes_realizadas": [res_pilha, res_lista],
        "streak": streak
    }


def executar_lista_para_pilha(estado: EstadoJogo, indice_lista: int, naipe_destino: str) -> dict[str, Any]:
    """Executa movimento tipo 5: última carta da coluna para a pilha de fundação.

    Args:
        estado: Partida atual.
        indice_lista: Coluna de origem (0..6).
        naipe_destino: Pilha de destino.

    Returns:
        Resultado padrão; pode incluir operação sintética ``virar_carta`` na origem.
    """
    pilha = estado.pilhas_fundacao.get(naipe_destino)
    if not pilha or indice_lista < 0 or indice_lista > 6:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": "Pilha ou lista inválida", "streak": streak, "operacoes_realizadas": []}
        
    lista = estado.listas_tableau[indice_lista]
    valido, motivo = regras_movimento.validar_lista_para_pilha(lista, pilha)
    if not valido:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": motivo, "streak": streak, "operacoes_realizadas": []}
        
    res_lista = lista.remover_final(registrar_passos=True)
    if not res_lista.get("operacao_sucesso") or not isinstance(
        res_lista.get("valor_retornado"), CartaBaralho
    ):
        return _rejeitar_por_estrutura_inconsistente(
            estado, "Lista vazia ao retirar a carta; atualize o estado e tente de novo."
        )
    carta = res_lista["valor_retornado"]
    res_pilha = pilha.empilhar(carta, registrar_passos=True)
    
    res_virar = _virar_carta_lista(lista)
    
    venceu = verificar_vitoria(estado)
    streak = atualizar_streak(estado, True, ["Lista Ligada", "Pilha (LIFO)"])
    if venceu:
        streak["nivel_efeito"] = "vitoria"
        
    operacoes = [res_lista, res_pilha]
    if res_virar:
        operacoes.append({
            "operacao_nome": "virar_carta",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": lista.nome_lista,
            "operacao_sucesso": True,
            "passos_executados": res_virar
        })
        
    return {
        "jogada_valida": True,
        "operacoes_realizadas": operacoes,
        "streak": streak
    }


def executar_lista_para_lista(estado: EstadoJogo, indice_origem: int, posicao_corte: int, indice_destino: int) -> dict[str, Any]:
    """Executa movimento tipo 6: sublista a partir de ``posicao_corte`` entre colunas.

    Args:
        estado: Partida atual.
        indice_origem: Coluna de onde se remove o sufixo.
        posicao_corte: Índice base zero do primeiro nó movido (ordem do array da API).
        indice_destino: Coluna de destino.

    Returns:
        Resultado padrão; ``operacoes_realizadas`` inclui remoção e um ``inserir_final``
        por carta, mais ``virar_carta`` na origem quando aplicável.
    """
    if indice_origem < 0 or indice_origem > 6 or indice_destino < 0 or indice_destino > 6:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": "Listas inválidas", "streak": streak, "operacoes_realizadas": []}
        
    if indice_origem == indice_destino:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": "Origem e destino iguais", "streak": streak, "operacoes_realizadas": []}
        
    lista_orig = estado.listas_tableau[indice_origem]
    lista_dest = estado.listas_tableau[indice_destino]
    
    valido, motivo = regras_movimento.validar_lista_para_lista(lista_orig, posicao_corte, lista_dest)
    if not valido:
        streak = atualizar_streak(estado, False, [])
        return {"jogada_valida": False, "motivo_rejeicao": motivo, "streak": streak, "operacoes_realizadas": []}
        
    res_lista_orig = lista_orig.remover_a_partir_de(posicao_corte, registrar_passos=True)
    if not res_lista_orig.get("operacao_sucesso"):
        cartas_falha = res_lista_orig.get("valor_retornado")
        streak = atualizar_streak(estado, False, [])
        detalhe = "Falha ao remover sublista no tableau."
        if cartas_falha is None:
            detalhe = "Remoção no tableau não retornou cartas; índice de corte inconsistente."
        return {
            "jogada_valida": False,
            "motivo_rejeicao": detalhe,
            "streak": streak,
            "operacoes_realizadas": [],
        }
    cartas_removidas = res_lista_orig["valor_retornado"]
    operacoes = [res_lista_orig]
    
    # Insere as cartas na nova lista preservando a ordem
    for carta in cartas_removidas:
        res_dest = lista_dest.inserir_final(carta, registrar_passos=True)
        operacoes.append(res_dest)
        
    res_virar = _virar_carta_lista(lista_orig)
    if res_virar:
        operacoes.append({
            "operacao_nome": "virar_carta",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": lista_orig.nome_lista,
            "operacao_sucesso": True,
            "passos_executados": res_virar
        })
        
    streak = atualizar_streak(estado, True, ["Lista Ligada"])
    return {
        "jogada_valida": True,
        "operacoes_realizadas": operacoes,
        "streak": streak
    }
