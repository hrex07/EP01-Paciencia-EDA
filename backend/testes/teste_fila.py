"""Testes da estrutura FilaCartas."""

from modelo.carta_baralho import CartaBaralho
from modelo.fila_cartas import FilaCartas


def test_fila_vazia_dequeue_falha() -> None:
    fila_teste = FilaCartas(nome_fila="fila_teste")
    resultado = fila_teste.desenfileirar()
    assert not resultado["operacao_sucesso"]
    assert resultado["mensagem_erro"] == "fila vazia"


def test_enqueue_dequeue_ordem_fifo() -> None:
    fila_teste = FilaCartas(nome_fila="fila_teste")
    primeira = CartaBaralho(4, "o")
    segunda = CartaBaralho(9, "p")
    fila_teste.enfileirar(primeira)
    resultado_enq = fila_teste.enfileirar(segunda)
    assert resultado_enq["quantidade_elementos"] == 2

    primeira_saida = fila_teste.desenfileirar()
    assert primeira_saida["valor_retornado"] == primeira
    segunda_saida = fila_teste.desenfileirar()
    assert segunda_saida["valor_retornado"] == segunda


def test_reposicionar_frente_preserva_tamanho() -> None:
    fila_teste = FilaCartas(nome_fila="fila_teste")
    fila_teste.enfileirar(CartaBaralho(1, "e"))
    fila_teste.enfileirar(CartaBaralho(2, "e"))
    fila_teste.enfileirar(CartaBaralho(3, "e"))
    tamanho_antes = fila_teste.obter_tamanho()
    resultado = fila_teste.reposicionar_frente()
    assert resultado["operacao_sucesso"]
    assert fila_teste.obter_tamanho() == tamanho_antes
    frente = fila_teste.espiar_frente()["valor_retornado"]
    assert frente is not None and frente.numero_carta == 2


def test_logs_contem_pseudo_codigo() -> None:
    fila_teste = FilaCartas(nome_fila="fila_teste")
    resultado = fila_teste.enfileirar(CartaBaralho(12, "c"))
    assert all("pseudo_codigo" in passo for passo in resultado["passos_executados"])
