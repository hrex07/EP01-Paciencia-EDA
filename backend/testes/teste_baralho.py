"""Testes da criação do baralho completo."""

from collections import Counter

from modelo.carta_baralho import CartaBaralho
from modelo.criacao_baralho import criar_baralho_completo


def test_baralho_completo_52_cartas_quatro_naipes() -> None:
    resultado = criar_baralho_completo()
    vetor_cartas = resultado["vetor_cartas"]
    assert len(vetor_cartas) == 52

    contador_naipes = Counter(c.naipe_carta for c in vetor_cartas)
    assert set(contador_naipes.values()) == {13}
    contador_valores = Counter(c.numero_carta for c in vetor_cartas)
    assert all(contador_valores[n] == 4 for n in range(1, 14))


def test_log_baralho_tem_52_passos() -> None:
    resultado = criar_baralho_completo(registrar_passos=True)
    assert len(resultado["passos_executados"]) == 52


def test_sem_log_nao_gera_passos() -> None:
    resultado = criar_baralho_completo(registrar_passos=False)
    assert resultado["passos_executados"] == []
