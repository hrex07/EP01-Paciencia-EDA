"""Testes dos algoritmos de embaralhamento."""

from typing import cast

from algoritmos.embaralhamento_iterativo import embaralhar_iterativo
from algoritmos.embaralhamento_recursivo import embaralhar_recursivo
from modelo.carta_baralho import CartaBaralho
from modelo.criacao_baralho import criar_baralho_completo


def test_embaralhar_iterativo() -> None:
    baralho = criar_baralho_completo(registrar_passos=False)
    vetor_original = list(cast(list[CartaBaralho], baralho["vetor_cartas"]))

    # Fazemos uma cópia para não alterar o original ainda
    vetor_para_embaralhar = list(vetor_original)

    resultado = embaralhar_iterativo(vetor_para_embaralhar, quantidade_trocas=50)

    vetor_embaralhado = resultado["vetor_cartas"]
    assert len(vetor_embaralhado) == len(vetor_original)
    # Garante que todos os elementos continuam lá
    assert sorted(str(c) for c in vetor_embaralhado) == sorted(
        str(c) for c in vetor_original
    )

    # Verifica se a ordem mudou (extremamente provável com 50 trocas)
    assert vetor_embaralhado != vetor_original
    assert len(resultado["passos_executados"]) == 50
    assert "tempo_execucao_ms" in resultado


def test_embaralhar_recursivo() -> None:
    baralho = criar_baralho_completo(registrar_passos=False)
    vetor_original = list(cast(list[CartaBaralho], baralho["vetor_cartas"]))

    vetor_para_embaralhar = list(vetor_original)
    resultado = embaralhar_recursivo(vetor_para_embaralhar, quantidade_trocas=50)

    vetor_embaralhado = resultado["vetor_cartas"]
    assert len(vetor_embaralhado) == len(vetor_original)
    assert sorted(str(c) for c in vetor_embaralhado) == sorted(
        str(c) for c in vetor_original
    )
    assert vetor_embaralhado != vetor_original
    assert "tempo_execucao_ms" in resultado

    passos = resultado["passos_executados"]
    # 50 trocas + 1 do caso base
    assert len(passos) == 51

    ultimo_passo = passos[-1]
    assert "Caso base atingido" in ultimo_passo["descricao_acao"]
    assert ultimo_passo["profundidade_recursao"] == 0
