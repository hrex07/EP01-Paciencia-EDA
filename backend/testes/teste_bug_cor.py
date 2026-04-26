"""Testes de regressão para alternância de cores no tableau (:func:`_validar_pode_listar`)."""

from modelo.carta_baralho import CartaBaralho


def test_validar_pode_listar_cores_alternadas() -> None:
    """Garante que vermelho sobre preto (e vice-versa) é aceito; mesma cor é rejeitada."""
    from motor.regras_movimento import _validar_pode_listar
    from modelo.lista_ligada_cartas import ListaLigadaCartas
    
    lista = ListaLigadaCartas("teste")
    carta_preta = CartaBaralho(6, "p", status_carta=True)
    lista.inserir_final(carta_preta, registrar_passos=False)
    
    carta_vermelha = CartaBaralho(5, "c", status_carta=True)
    valido, _ = _validar_pode_listar(carta_vermelha, lista)
    assert valido is True, "Deveria aceitar vermelha sobre preta"
    
    carta_outra_preta = CartaBaralho(5, "e", status_carta=True)
    valido_invalido, _ = _validar_pode_listar(carta_outra_preta, lista)
    assert valido_invalido is False, "Não deveria aceitar preta sobre preta"
