"""CORS: com Origin, respostas devem incluir Access-Control-Allow-Origin (camada CORS por cima do rate limit)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from main import app

_HEADER = "access-control-allow-origin"
_ORIGEM_127 = "http://127.0.0.1:5173"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _origem_aceite(headers: dict[str, str], esperado: str) -> bool:
    h = {k.lower(): v for k, v in headers.items() if v is not None}
    o = h.get("access-control-allow-origin", "")
    return o == esperado or o == "*"


def teste_post_novo_com_origem_127_tem_cors(client: TestClient) -> None:
    r = client.post(
        "/api/jogo/novo?log_detalhado=false",
        headers={"Origin": _ORIGEM_127},
    )
    assert r.status_code == 201
    assert _origem_aceite(dict(r.headers), _ORIGEM_127), r.headers.get(_HEADER)


def teste_post_mover_sessao_inexistente_com_origem_tem_cors(client: TestClient) -> None:
    r = client.post(
        "/api/jogo/00000000-0000-0000-0000-000000000000/mover",
        json={"tipo_movimento": 1},
        headers={"Origin": _ORIGEM_127},
    )
    assert r.status_code == 404
    assert _origem_aceite(dict(r.headers), _ORIGEM_127), r.headers.get(_HEADER)


def teste_post_mover_tipo_invalido_tem_cors(client: TestClient) -> None:
    r0 = client.post(
        "/api/jogo/novo?log_detalhado=false",
        headers={"Origin": _ORIGEM_127},
    )
    assert r0.status_code == 201
    sid = r0.json()["id_sessao"]
    r = client.post(
        f"/api/jogo/{sid}/mover",
        json={"tipo_movimento": 99},
        headers={"Origin": _ORIGEM_127},
    )
    assert r.status_code == 422
    assert _origem_aceite(dict(r.headers), _ORIGEM_127), r.headers.get(_HEADER)
