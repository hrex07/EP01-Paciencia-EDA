"""Testes do motor do jogo Paciência."""

from modelo.carta_baralho import CartaBaralho
from motor.estado_jogo import EstadoJogo
from motor.controlador_jogo import (
    distribuir_cartas_novo_jogo,
    executar_fila_para_fila,
    executar_fila_para_pilha,
    executar_fila_para_lista,
    executar_pilha_para_lista,
    executar_lista_para_pilha,
    executar_lista_para_lista,
)


def test_distribuicao_inicial() -> None:
    estado = EstadoJogo()
    log_preparacao = distribuir_cartas_novo_jogo(estado)
    
    assert len(log_preparacao) > 0
    # Verifica tamanho das 7 listas (1, 2, 3, 4, 5, 6, 7) => total 28
    for i in range(7):
        assert estado.listas_tableau[i].obter_tamanho() == i + 1
        
        # Última carta virada para cima
        ultima = estado.listas_tableau[i].obter_ultima_carta(registrar_passos=False)["valor_retornado"]
        assert ultima.status_carta is True
        
        # Se tamanho > 1, primeira carta para baixo
        if i > 0:
            primeira = estado.listas_tableau[i].obter_carta_posicao(0, registrar_passos=False)["valor_retornado"]
            assert primeira.status_carta is False

    # Fila com 24
    assert estado.fila_compra.obter_tamanho() == 24
    
    # Pilhas vazias
    for p in estado.pilhas_fundacao.values():
        assert p.esta_vazia()


def test_serializacao_estado() -> None:
    estado = EstadoJogo()
    distribuir_cartas_novo_jogo(estado)
    
    json_data = estado.serializar()
    assert "id_sessao" in json_data
    assert "estruturas" in json_data
    
    estruturas = json_data["estruturas"]
    assert len(estruturas["fila_compra"]) == 24
    assert len(estruturas["pilhas_fundacao"]["c"]) == 0
    assert len(estruturas["listas_tableau"]) == 7
    
    # A lista 0 tem 1 carta virada pra cima
    assert estruturas["listas_tableau"][0][0]["status_carta"] is True
    # A lista 1 tem 2 cartas, a primeira virada pra baixo (texto = verso)
    assert estruturas["listas_tableau"][1][0]["status_carta"] is False
    assert estruturas["listas_tableau"][1][0]["texto"] == "verso"


def test_movimentacao_invalida_zera_streak() -> None:
    estado = EstadoJogo()
    # Fila vazia, erro
    res = executar_fila_para_fila(estado)
    
    assert not res["jogada_valida"]
    assert res["streak"]["sequencia_atual"] == 0
    assert res["streak"]["nivel_efeito"] == "erro"


def test_virar_carta_apos_remover() -> None:
    estado = EstadoJogo()
    lista = estado.listas_tableau[0]
    
    carta_baixa = CartaBaralho(10, "c", status_carta=False)
    carta_alta = CartaBaralho(9, "e", status_carta=True)
    
    lista.inserir_final(carta_baixa, registrar_passos=False)
    lista.inserir_final(carta_alta, registrar_passos=False)
    
    pilha = estado.pilhas_fundacao["e"]
    pilha.empilhar(CartaBaralho(8, "e"), registrar_passos=False) # Para deixar M2 valido se fosse possivel
    
    # Simularemos direto usando a função para testar o virar carta
    res = executar_lista_para_pilha(estado, 0, "e")
    
    # A remoção deve virar a carta 10 de copas
    carta_agora_alta = lista.obter_ultima_carta(registrar_passos=False)["valor_retornado"]
    assert carta_agora_alta.status_carta is True
