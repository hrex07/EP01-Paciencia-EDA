"""Stress: /mover não pode alternar 500/200 por corrida; repete a mesma jogada muitas vezes."""

from __future__ import annotations

import threading

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _novo_id_sessao(c: TestClient) -> str:
    r = c.post("/api/jogo/novo?log_detalhado=false", headers={"Origin": "http://127.0.0.1:5173"})
    assert r.status_code == 201, r.text
    return r.json()["id_sessao"]


def teste_mover_mesma_sessao_sequencial_500x_sem_500(client: TestClient) -> None:
    """Simula o cenário "segundo clique depois dá 200" com centenas de POSTs em série."""
    sid = _novo_id_sessao(client)
    for i in range(500):
        r = client.post(
            f"/api/jogo/{sid}/mover",
            json={"tipo_movimento": 1},
            headers={"Origin": "http://127.0.0.1:5173"},
        )
        assert r.status_code == 200, f"iter {i} esperado 200, obteve {r.status_code}: {r.text[:500]}"


def teste_mover_8_threads_30cada_mesma_sessao_sem_500() -> None:
    """Cada `TestClient` numa thread, mesma `id_sessão`: força concorrência; RLock+lock de sessão evitam 500."""
    c0 = TestClient(app)
    sid = _novo_id_sessao(c0)
    err: list[str] = []
    err_lock = threading.Lock()

    def worker() -> None:
        c = TestClient(app)
        for j in range(30):
            r = c.post(
                f"/api/jogo/{sid}/mover",
                json={"tipo_movimento": 1},
                headers={"Origin": "http://127.0.0.1:5173"},
            )
            if r.status_code != 200:
                with err_lock:
                    err.append(
                        f"thread {threading.get_ident()} iter {j} -> {r.status_code} {r.text[:200]}"
                    )

    ths: list[threading.Thread] = []
    for _ in range(8):
        t = threading.Thread(target=worker)
        ths.append(t)
        t.start()
    for t in ths:
        t.join()

    assert not err, "\n".join(err)
