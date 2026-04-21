"""Testes para os algoritmos de ordenação e função de comparação."""

from algoritmos.comparar_ordenacao import comparar_algoritmos
from algoritmos.embaralhamento_iterativo import embaralhar_iterativo
from algoritmos.ordenacao_bubble import ordenacao_bubble
from algoritmos.ordenacao_merge import ordenacao_merge
from algoritmos.ordenacao_quick import ordenacao_quick
from modelo.criacao_baralho import criar_baralho_completo


def _obter_baralho_embaralhado() -> list:
    baralho = criar_baralho_completo(registrar_passos=False)
    vetor = list(baralho["vetor_cartas"])
    embaralhado = embaralhar_iterativo(vetor, quantidade_trocas=200, registrar_passos=False)
    return list(embaralhado["vetor_cartas"])


def _verificar_ordenacao(resultado: dict) -> None:
    vetor = resultado["vetor_cartas"]
    assert len(vetor) == 52
    assert "total_comparacoes" in resultado
    assert "total_trocas" in resultado
    assert "tempo_execucao_ms" in resultado

    # Verifica se realmente ordenou corretamente (pelo naipe_peso e número)
    naipe_peso = {"c": 0, "o": 1, "p": 2, "e": 3}
    for i in range(len(vetor) - 1):
        carta_atual = vetor[i]
        carta_proxima = vetor[i + 1]

        peso_atual = (naipe_peso.get(carta_atual.naipe_carta, 0), carta_atual.numero_carta)
        peso_proximo = (naipe_peso.get(carta_proxima.naipe_carta, 0), carta_proxima.numero_carta)

        assert peso_atual <= peso_proximo


def test_ordenacao_bubble_sort() -> None:
    vetor_embaralhado = _obter_baralho_embaralhado()
    resultado = ordenacao_bubble(vetor_embaralhado, registrar_passos=True)
    _verificar_ordenacao(resultado)
    assert len(resultado["passos_executados"]) > 0


def test_ordenacao_bubble_sort_ja_ordenado() -> None:
    vetor_ordenado = list(criar_baralho_completo(registrar_passos=False)["vetor_cartas"])
    resultado = ordenacao_bubble(vetor_ordenado, registrar_passos=True)
    assert resultado["total_trocas"] == 0
    
    # Menos passos pois vai breakar na primeira iteração (já ordenado)
    assert len(resultado["passos_executados"]) <= 53


def test_ordenacao_merge_sort() -> None:
    vetor_embaralhado = _obter_baralho_embaralhado()
    resultado = ordenacao_merge(vetor_embaralhado, registrar_passos=True)
    _verificar_ordenacao(resultado)
    
    passos = resultado["passos_executados"]
    assert any("Dividir" in p["pseudo_codigo"] for p in passos)
    assert any("Mesclar" in p["pseudo_codigo"] for p in passos)


def test_ordenacao_quick_sort() -> None:
    vetor_embaralhado = _obter_baralho_embaralhado()
    resultado = ordenacao_quick(vetor_embaralhado, registrar_passos=True)
    _verificar_ordenacao(resultado)

    passos = resultado["passos_executados"]
    assert any("pivô" in p["pseudo_codigo"] for p in passos)


def test_comparacao_retorna_tres_resultados() -> None:
    vetor_embaralhado = _obter_baralho_embaralhado()
    resultados = comparar_algoritmos(vetor_embaralhado)
    
    assert len(resultados) == 3
    for res in resultados:
        _verificar_ordenacao(res)
        assert res["passos_executados"] == []  # Comparação desliga logs
