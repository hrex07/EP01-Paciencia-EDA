"""Testes da estrutura PilhaCartas."""

from modelo.carta_baralho import CartaBaralho
from modelo.pilha_cartas import PilhaCartas


def test_pilha_vazia_e_tamanho_zero() -> None:
    pilha_teste = PilhaCartas(nome_pilha="pilha_teste")
    assert pilha_teste.esta_vazia()
    assert pilha_teste.obter_tamanho() == 0


def test_empilhar_espiar_desempilhar_com_logs() -> None:
    pilha_teste = PilhaCartas(nome_pilha="pilha_teste")
    carta_um = CartaBaralho(5, "c")
    resultado_push = pilha_teste.empilhar(carta_um)
    assert resultado_push["operacao_sucesso"]
    assert resultado_push["quantidade_elementos"] == 1
    assert len(resultado_push["passos_executados"]) >= 3

    resultado_peek = pilha_teste.espiar_topo()
    assert resultado_peek["operacao_sucesso"]
    assert resultado_peek["valor_retornado"] == carta_um
    assert pilha_teste.obter_tamanho() == 1

    resultado_pop = pilha_teste.desempilhar()
    assert resultado_pop["operacao_sucesso"]
    assert resultado_pop["valor_retornado"] == carta_um
    assert pilha_teste.esta_vazia()


def test_desempilhar_pilha_vazia_retorna_erro() -> None:
    pilha_teste = PilhaCartas(nome_pilha="pilha_teste")
    resultado = pilha_teste.desempilhar()
    assert not resultado["operacao_sucesso"]
    assert resultado["valor_retornado"] is None
    assert any(
        "vazia" in passo["descricao_acao"].lower()
        for passo in resultado["passos_executados"]
    )


def test_empilhar_duas_cartas_ordem_lifo() -> None:
    pilha_teste = PilhaCartas(nome_pilha="pilha_teste")
    pilha_teste.empilhar(CartaBaralho(3, "e"))
    resultado = pilha_teste.empilhar(CartaBaralho(7, "p"))
    assert resultado["quantidade_elementos"] == 2
    texto_passos = " ".join(
        p["descricao_acao"] for p in resultado["passos_executados"]
    )
    assert "não vazia" in texto_passos.lower() or "topo atual" in texto_passos.lower()

    topo = pilha_teste.espiar_topo()["valor_retornado"]
    assert topo is not None and topo.numero_carta == 7
