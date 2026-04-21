"""Testes da estrutura ListaLigadaCartas."""

from modelo.carta_baralho import CartaBaralho
from modelo.lista_ligada_cartas import ListaLigadaCartas


def test_inserir_final_e_obter_ultima() -> None:
    lista_teste = ListaLigadaCartas(nome_lista="lista_teste")
    carta_um = CartaBaralho(10, "c")
    resultado = lista_teste.inserir_final(carta_um)
    assert resultado["operacao_sucesso"]
    assert resultado["quantidade_elementos"] == 1

    ultima = lista_teste.obter_ultima_carta()
    assert ultima["valor_retornado"] == carta_um


def test_remover_suffixo_mantem_prefixo() -> None:
    lista_teste = ListaLigadaCartas(nome_lista="lista_teste")
    for numero in range(6):
        lista_teste.inserir_final(CartaBaralho(numero + 1, "p"))

    resultado = lista_teste.remover_a_partir_de(3)
    assert resultado["operacao_sucesso"]
    cartas_removidas = resultado["valor_retornado"]
    assert cartas_removidas is not None and len(cartas_removidas) == 3
    assert lista_teste.obter_tamanho() == 3

    primeira = lista_teste.obter_carta_posicao(0)
    assert primeira["valor_retornado"] == CartaBaralho(1, "p")


def test_buscar_carta_encontra_indice() -> None:
    lista_teste = ListaLigadaCartas(nome_lista="lista_teste")
    alvo = CartaBaralho(7, "e")
    lista_teste.inserir_final(CartaBaralho(2, "o"))
    lista_teste.inserir_final(alvo)

    resultado = lista_teste.buscar_carta(
        numero_carta=7, naipe_carta="e", registrar_passos=True
    )
    assert resultado["valor_retornado"] == 1


def test_inserir_posicao_meio() -> None:
    lista_teste = ListaLigadaCartas(nome_lista="lista_teste")
    lista_teste.inserir_final(CartaBaralho(1, "c"))
    lista_teste.inserir_final(CartaBaralho(3, "c"))
    lista_teste.inserir_posicao(CartaBaralho(2, "c"), 1)

    assert lista_teste.obter_carta_posicao(0)["valor_retornado"].numero_carta == 1
    assert lista_teste.obter_carta_posicao(1)["valor_retornado"].numero_carta == 2
    assert lista_teste.obter_carta_posicao(2)["valor_retornado"].numero_carta == 3


def test_remover_final() -> None:
    lista_teste = ListaLigadaCartas(nome_lista="lista_teste")
    lista_teste.inserir_final(CartaBaralho(4, "p"))
    lista_teste.inserir_final(CartaBaralho(9, "p"))

    resultado = lista_teste.remover_final()
    assert resultado["operacao_sucesso"]
    assert resultado["valor_retornado"] == CartaBaralho(9, "p")
    assert lista_teste.obter_tamanho() == 1


def test_passos_executados_presentes() -> None:
    lista_teste = ListaLigadaCartas(nome_lista="lista_teste")
    r = lista_teste.inserir_final(CartaBaralho(5, "o"))
    assert len(r["passos_executados"]) >= 2
