#!/usr/bin/env python3
"""Abre o front com Playwright e imprime erros do console e respostas HTTP 4xx/5xx.

Modo padrão (recomendado em CI e para evitar CORS/500 de processo antigo):
  sobe Uvicorn **sem** --reload (porta 8040) e Vite (BACKEND_PORT=8040) e testa
  o fluxo: Iniciar Partida + duplo clique na fila (Fila->Fila).

Uso simples:  python e2e/capturar_console.py

Só o browser (Vite/ API já rodam, mesma config):  python e2e/capturar_console.py --externo --port 5173
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Any


def _aguardar_url_ok(url: str, timeout_s: float = 30) -> bool:
    import urllib.error
    import urllib.request

    t0 = time.time()
    while time.time() - t0 < timeout_s:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status < 500:
                    return True
        except (urllib.error.URLError, OSError, TimeoutError):
            time.sleep(0.2)
    return False


def _fluxo(
    base_url: str,
) -> tuple[list[str], list[str]]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Instale: pip install playwright && playwright install chromium", file=sys.stderr)
        return ([], ["playwright ausente"])

    linhas: list[str] = []
    requisicoes_falharam: list[str] = []

    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True)
        ctx = nav.new_context(viewport={"width": 1280, "height": 900})
        pag = ctx.new_page()

        def on_console(msg: Any) -> None:
            t = str(msg.type)
            if t in ("error", "warning"):
                try:
                    tx = str(msg.text)
                except Exception:
                    tx = repr(msg)
                linhas.append(f"[console {t}] {tx}")

        def on_page_error(err: str) -> None:
            linhas.append(f"[pageerror] {err}")

        def on_response(res: Any) -> None:
            try:
                s = int(res.status)
            except Exception:
                return
            if s >= 400:
                u = res.url
                requisicoes_falharam.append(f"HTTP {s} {u[:200]}")

        pag.on("console", on_console)
        pag.on("pageerror", on_page_error)
        pag.on("response", on_response)

        try:
            pag.goto(base_url, wait_until="domcontentloaded", timeout=30_000)
        except Exception as exc:
            print("Falha ao abrir", base_url, ":", exc, file=sys.stderr)
            ctx.close()
            nav.close()
            return requisicoes_falharam, [f"goto: {exc!s}"]

        time.sleep(0.5)
        try:
            pag.get_by_role("button", name="Iniciar Partida").click(timeout=20_000)
        except Exception as e:
            linhas.append(f"[falha UI] {e!s}")
        time.sleep(1.0)

        try:
            alvo = pag.locator("div.bg-green-800 .mr-4").first.locator("div.cursor-pointer")
            alvo.first.click(timeout=5_000)
            time.sleep(0.2)
            alvo.first.click(timeout=5_000)
        except Exception as e:
            linhas.append(f"[fila clique] {e!s}")
        time.sleep(0.8)

        ctx.close()
        nav.close()

    return requisicoes_falharam, linhas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--externo",
        action="store_true",
        help="Não sobe Vite/ API; use só o browser (Vite/ backend já de manual).",
    )
    ap.add_argument(
        "--port",
        type=int,
        default=5173,
        help="Só com --externo: porta do Vite (padrão 5173).",
    )
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    procs: list = []
    try:
        if not args.externo:
            import subprocess

            raiz = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
            back_cwd = os.path.join(raiz, "backend")
            front_cwd = os.path.join(raiz, "frontend")
            be_port = "8040"
            fe_port = 5180
            env_fe = {**os.environ, "BACKEND_PORT": be_port}
            p_be = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", be_port],
                cwd=back_cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
            procs.append(p_be)
            if not _aguardar_url_ok(f"http://127.0.0.1:{be_port}/openapi.json"):
                print("Timeout esperando o backend em", be_port, file=sys.stderr)
                return 1
            # `npm` no PATH em Windows muitas vezes só com shell=True (comando = cmd).
            p_fe = subprocess.Popen(
                f"npm run dev -- --host 127.0.0.1 --port {fe_port}",
                cwd=front_cwd,
                env=env_fe,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
            procs.append(p_fe)
            if not _aguardar_url_ok(f"http://127.0.0.1:{fe_port}/"):
                print("Timeout esperando o Vite em", fe_port, file=sys.stderr)
                return 1
            base = f"http://127.0.0.1:{fe_port}/"
        else:
            base = f"http://127.0.0.1:{args.port}/"

        requisicoes_falharam, linhas = _fluxo(base)

    finally:
        for p in procs:
            try:
                p.terminate()
                p.wait(timeout=5)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass

    for r in requisicoes_falharam:
        print(r)
    for line in linhas:
        print(line)
    if not requisicoes_falharam and not any(
        l for l in linhas if l.startswith("[console")
    ) and not any("pageerror" in l for l in linhas):
        print("(sem erros/avisos de console nem HTTP 4xx/5xx no fluxo básico)")

    has_err = bool(requisicoes_falharam) or any(
        "[console error]" in x or x.startswith("[pageerror]") for x in linhas
    )
    return 1 if has_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
