"""Brute force: movimento 5 (lista → pilha) com payload alinhado ao Network tab; sem 500."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from api import gerenciador_sessoes
from main import app
from modelo.carta_baralho import CartaBaralho
from motor.estado_jogo import EstadoJogo

HDR = {"Origin": "http://127.0.0.1:5173"}
PAYLOAD = {"tipo_movimento": 5, "naipe_destino": "p", "indice_lista_origem": 6}


def _montar_estado_as_lista6() -> str:
    e = EstadoJogo()
    as_paus = CartaBaralho(1, "p", status_carta=True)
    e.listas_tableau[6].inserir_final(as_paus, registrar_passos=False)
    gerenciador_sessoes.salvar_estado(e)
    return e.id_sessao


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def teste_mover_5p6_payload_paralelo_50_iteracoes_nunca_500() -> None:
    """Em cada iteração: 2 `TestClient` disparam o mesmo /mover em paralelo — nunca 500."""
    for i in range(50):
        sid = _montar_estado_as_lista6()

        def post() -> int:
            c = TestClient(app)
            r = c.post(f"/api/jogo/{sid}/mover", json=PAYLOAD, headers=HDR)
            return r.status_code

        with ThreadPoolExecutor(max_workers=2) as ex:
            f1 = ex.submit(post)
            f2 = ex.submit(post)
            a, b = f1.result(), f2.result()
        assert a == 200, f"iter {i} a={a}"
        assert b == 200, f"iter {i} b={b}"


def teste_mover_5p6_mesma_sessao_sequencial_100x_nunca_500() -> None:
    """1.ª jogada pode ser válida; as seguintes, inválidas — todas 200, nunca 5xx."""
    sid = _montar_estado_as_lista6()
    c = TestClient(app)
    for j in range(100):
        r = c.post(f"/api/jogo/{sid}/mover", json=PAYLOAD, headers=HDR)
        assert r.status_code == 200, f"iter {j} {r.status_code} {r.text[:300]}"
