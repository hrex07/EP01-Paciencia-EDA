#!/usr/bin/env python3
"""Testa CORS: front em http://127.0.0.1:5173 e chamadas à API (localhost:8000).

Reproduz o aviso: bloqueio por CORS quando a origem é 127.0.0.1 e a API
não devolve `Access-Control-Allow-Origin` para essa origem.

Requisito:
  - Vite: `http://127.0.0.1:5173` (ex.: `npm run dev -- --host 0.0.0.0` e abra o URL com 127.0.0.1).
  - Uvicorn **reiniciado** após alterar `main.py` (CORS precisa ser a camada mais externa
    e envolver o rate limit; processo antigo = mesmo erro de CORS no /mover).

Validação no CI sem browser: `pytest backend/testes/teste_cors_headers.py`

Uso: python e2e/teste_cors_127_0_0_1.py
"""

from __future__ import annotations

import sys
import time
from typing import Any

URL_FRONT = "http://127.0.0.1:5173/"
ORIGIN_ESPERADA = "http://127.0.0.1:5173"


def _cabe_ao_origin(valor: str | None) -> bool:
    if not valor:
        return False
    v = valor.strip()
    if v == "*":
        return True
    return v.rstrip("/") == ORIGIN_ESPERADA.rstrip("/")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Instale: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    respostas: list[dict[str, Any]] = []
    erros_cors: list[str] = []

    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True)
        ctx = nav.new_context(viewport={"width": 1280, "height": 900})
        pag = ctx.new_page()

        def rastrear(res) -> None:
            try:
                u = res.url
            except Exception:
                return
            if "/api/jogo" not in u:
                return
            try:
                h = res.headers
            except Exception:
                h = {}
            # Playwright costuma entregar chaves em minúsculo
            aca = None
            for chave, val in (h or {}).items():
                if chave.lower() == "access-control-allow-origin":
                    aca = val
                    break
            respostas.append(
                {
                    "url": u,
                    "status": res.status,
                    "access_control_allow_origin": aca,
                }
            )

        def consola(msg) -> None:
            t = str(msg.text)
            if "cors" in t.lower() or "blocked" in t.lower() or "access-control" in t.lower():
                erros_cors.append(f"[{msg.type}] {t}")

        pag.on("response", rastrear)
        pag.on("console", consola)

        try:
            pag.goto(URL_FRONT, wait_until="domcontentloaded", timeout=30_000)
        except Exception as exc:
            print("Falha ao abrir", URL_FRONT, ":", exc, file=sys.stderr)
            print("Suba o Vite com acesso a 127.0.0.1 (ex. --host 0.0.0.0).", file=sys.stderr)
            ctx.close()
            nav.close()
            return 1

        time.sleep(0.4)
        pag.get_by_role("button", name="Iniciar Partida").click(timeout=20_000)
        time.sleep(1.0)

        # Fila: primeiro clique seleciona, segundo executa Fila->Fila (POST /mover)
        alvo = pag.locator("div.bg-green-800 .mr-4").first.locator("div.cursor-pointer")
        alvo.first.click(timeout=8_000)
        time.sleep(0.4)
        alvo.first.click(timeout=8_000)
        time.sleep(1.0)

        ctx.close()
        nav.close()

    for r in respostas:
        print(r["status"], r.get("access_control_allow_origin"), r["url"][:100])

    if erros_cors:
        print("--- Console (CORS / bloqueio): ---", file=sys.stderr)
        for e in erros_cors:
            print(e, file=sys.stderr)

    jogo = [r for r in respostas if "jogo/novo" in r["url"]]
    mover = [r for r in respostas if "/mover" in r["url"]]

    if not jogo:
        print("Não houve POST /jogo/novo (jogo não iniciou?).", file=sys.stderr)
        return 1

    if not mover:
        print(
            "Aviso: não rastreou resposta a /mover (axios pode ser bloqueado antes; confira o console).",
            file=sys.stderr,
        )

    # /jogo/novo e /mover (se houver) devem refletir a origem ou regex (CORS na camada externa)
    ok_novo = any(_cabe_ao_origin(r.get("access_control_allow_origin")) for r in jogo)
    ok_mover = not mover or any(
        _cabe_ao_origin(r.get("access_control_allow_origin")) for r in mover
    )
    ok = ok_novo and ok_mover

    if not ok:
        for r in jogo + mover:
            o = r.get("access_control_allow_origin")
            if o:
                print("Origem no header:", o, "— esperava", ORIGIN_ESPERADA, "ou * (aceitável se sem credenciais).")
    # Bloqueio CORS: mensagem clássica do Chrome
    fez_bloq = any(
        "blocked by cors" in e.lower() or "no 'access-control-allow-origin'" in e.lower()
        for e in erros_cors
    )

    if not ok or fez_bloq:
        print(
            "FALHA: veja CORS/ALLOWED_ORIGINS, VITE_API_URL, ou processo Uvicorn antigo.",
            file=sys.stderr,
        )
        print(
            "  Pare o Uvicorn e suba de novo: cd backend && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000",
            file=sys.stderr,
        )
        print(
            "  Teste rápido (sem browser): cd backend && pytest testes/teste_cors_headers.py -q",
            file=sys.stderr,
        )
        return 1

    print("OK: CORS com origem", ORIGIN_ESPERADA, "em /jogo/novo" + (" e /mover" if mover else " (e movimento se disparado)."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
