"""Respostas da API: não podem conter instâncias de CartaBaralho (Uvicorn / JSON)."""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from api.serializacao_resposta import sanitizar_motor_para_json
from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _sem_instancia_carta(objeto: object) -> None:
    """Garante que o texto serializado não contém a repr de instância de domínio."""
    texto = json.dumps(objeto, ensure_ascii=False)
    assert "CartaBaralho(" not in texto


def teste_novo_jogo_e_mover_fila_geram_json_puro(client: TestClient) -> None:
    r = client.post(
        "/api/jogo/novo?log_detalhado=true",
        headers={"Origin": "http://127.0.0.1:5173"},
    )
    assert r.status_code == 201
    corpo = r.json()
    _sem_instancia_carta(corpo)
    if corpo.get("log_preparacao"):
        for item in corpo["log_preparacao"]:
            _sem_instancia_carta(item)

    sid = corpo["id_sessao"]
    r2 = client.post(
        f"/api/jogo/{sid}/mover",
        json={"tipo_movimento": 1},
        headers={"Origin": "http://127.0.0.1:5173"},
    )
    assert r2.status_code == 200
    c2 = r2.json()
    _sem_instancia_carta(c2)
    for op in c2.get("operacoes_realizadas", []):
        _sem_instancia_carta(op)


def teste_sanitizador_nao_recursao_infinita_ciclo() -> None:
    d: dict[object, object] = {}
    d["self"] = d
    out = sanitizar_motor_para_json(d)
    assert out["self"] == "<ciclo: dict ou list>"
    json.dumps(sanitizar_motor_para_json(d))
