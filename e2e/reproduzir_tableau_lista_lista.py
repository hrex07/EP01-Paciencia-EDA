#!/usr/bin/env python3
"""Simula, com Playwright, uma jogada lista->lista validada no mesmo estado da API.

- Recarrega a página, clica em Iniciar Partida.
- Lê o JSON de `POST .../jogo/novo` (mesmo estado do React).
- Encontra uma jogada: carta (virada) em uma coluna sobre a última de outra,
  com alternância de cores e número imediatamente menor.
- Clica no centro horizontal e na parte superior (faixa fora do overlap)
  de `data-columna-indice` / `data-carta-indice` e ouve o console.
- Repete a mesma jogada com `POST /jogo/{id}/mover` e imprime o resultado.

Uso (janela visível por padrão):

  pip install playwright && playwright install chromium
  # Terminal 1: API em :8000  |  Terminal 2: npm run dev em :5173
  python e2e/reproduzir_tableau_lista_lista.py
  python e2e/reproduzir_tableau_lista_lista.py --headless   # sem UI (CI)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Any, Optional

import urllib.error
import urllib.request

API_BASE = "http://127.0.0.1:8000/api"
FRONTEND_URL = "http://127.0.0.1:5173/"


@dataclass
class JogadaLista:
    coluna_origem: int
    indice_corte: int
    coluna_destino: int


def _cor_carta(naipe: str) -> str:
    n = naipe.lower().strip()
    if n in ("c", "o"):
        return "vermelha"
    return "preta"


def _pode_listar_sobre(
    carta_mover: dict[str, Any], coluna_destino: list[dict[str, Any]]
) -> bool:
    """Compatível com a validação de `_validar_pode_listar` no motor."""
    if not carta_mover.get("status_carta", False):
        return False
    if not coluna_destino:
        return carta_mover.get("numero_carta") == 13
    ultima = coluna_destino[-1]
    if not ultima.get("status_carta", False):
        return False
    naipe_m = carta_mover.get("naipe_carta")
    naipe_u = ultima.get("naipe_carta")
    if naipe_m is None or naipe_u is None:
        return False
    if _cor_carta(naipe_m) == _cor_carta(naipe_u):
        return False
    return int(carta_mover["numero_carta"]) == int(ultima["numero_carta"]) - 1


def _encontrar_jogada(
    tabel: list[list[dict[str, Any]]],
) -> Optional[JogadaLista]:
    for o in range(7):
        col_o = tabel[o]
        for c in range(len(col_o)):
            carta = col_o[c]
            if not carta.get("status_carta", False):
                continue
            for d in range(7):
                if d == o:
                    continue
                if _pode_listar_sobre(carta, tabel[d]):
                    return JogadaLista(o, c, d)
    return None


def _clicar_area_carta(
    pagina,
    coluna: int,
    indice: int,
    *,
    fracao_y: float = 0.5,
) -> bool:
    """Clica (mouse) em `(meio, fracao_y * altura)` da `motion` da carta.

    A cascata e o z-index fazem a carta imediatamente abaixo cobrir a face;
    `fracao_y` pequena na origem evita o hit na carta errada.

    Returns:
        True se o alvo existiu, senão False.
    """
    alvo = pagina.locator(
        f'[data-columna-indice="{coluna}"][data-carta-indice="{indice}"]'
    ).first
    # Coluna: w-20 (relative) > div.relative (mapa) > div[absolute] (cada carta) > div (motion)
    alvo_flex = (
        pagina.locator("div.bg-green-800 div.flex.justify-between.space-x-2 > div")
        .nth(coluna)
    )
    alvo_por_dados = alvo
    try:
        alvo_por_dados.wait_for(state="visible", timeout=3000)
    except Exception:
        alvo = (
            alvo_flex.locator("> div.relative > div").nth(indice).locator("> div").first
        )
    try:
        alvo.wait_for(state="visible", timeout=10_000)
    except Exception:
        return False
    try:
        alvo.scroll_into_view_if_needed()
    except Exception:
        pass
    box = alvo.bounding_box()
    if not box:
        return False
    pagina.mouse.click(
        box["x"] + box["width"] * 0.5,
        box["y"] + box["height"] * fracao_y,
    )
    return True


def _api_post_json(
    path: str,
    corpo: dict[str, Any],
    api_base: str | None = None,
) -> dict[str, Any]:
    base = api_base if api_base is not None else API_BASE
    dados = json.dumps(corpo).encode("utf-8")
    requisicao = urllib.request.Request(
        f"{base}{path}",
        data=dados,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(requisicao, timeout=30) as resposta:
        return json.load(resposta)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Playwright: testa movimento listas do tableau (lista -> lista).",
    )
    ap.add_argument(
        "--headless",
        action="store_true",
        help="Não abrir o Chromium (padrão: janela visível).",
    )
    ap.add_argument(
        "--url",
        default=FRONTEND_URL,
        help=f"URL do Vite (padrão: {FRONTEND_URL})",
    )
    ap.add_argument(
        "--api",
        default=API_BASE,
        help="Base da API para comparação (padrão: http://127.0.0.1:8000/api).",
    )
    ap.add_argument(
        "--slow-mo",
        type=int,
        default=0,
        metavar="MS",
        help="Atraso entre ações (ms) para acompanhar o clique, ex. 100.",
    )
    args = ap.parse_args()
    url_front = args.url
    api_base = args.api

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Instale: pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        return 1

    avisos_console: list[str] = []
    rejeicoes_ui: list[str] = []
    jogo_capturado: dict[str, Any] = {}

    with sync_playwright() as p:
        navegador = p.chromium.launch(
            headless=args.headless,
            slow_mo=args.slow_mo,
        )
        contexto = navegador.new_context(
            viewport={"width": 1600, "height": 900},
        )
        pagina = contexto.new_page()

        def _ao_resposta(resposta) -> None:
            try:
                u = resposta.url
            except Exception:
                return
            if "jogo/novo" in u and resposta.status == 201:
                try:
                    jogo_capturado["payload"] = resposta.json()
                except Exception:
                    pass

        def _on_console(mensagem) -> None:
            texto = str(mensagem.text)
            avisos_console.append(f"[{mensagem.type}] {texto}")
            if "Jogada inválida" in texto or "jogada inválida" in texto.lower():
                rejeicoes_ui.append(texto)

        pagina.on("response", _ao_resposta)
        pagina.on("console", _on_console)

        for tentativa in range(200):
            jogo_capturado.clear()
            rejeicoes_ui.clear()
            avisos_console.clear()
            pagina.goto(url_front, wait_until="networkidle", timeout=60_000)
            time.sleep(0.3)
            pagina.reload(wait_until="networkidle", timeout=60_000)
            time.sleep(0.3)
            pagina.get_by_role("button", name="Iniciar Partida").click(
                timeout=20_000
            )
            pagina.wait_for_timeout(2000)
            payload = jogo_capturado.get("payload")
            if not payload:
                print("Tentativa", tentativa, ": resposta de novo jogo não capturada.")
                continue
            id_sess: str = payload["id_sessao"]
            estado = payload.get("estado_jogo", payload)
            tabel = estado.get("estruturas", {}).get("listas_tableau", [])
            jog = _encontrar_jogada(tabel) if tabel and len(tabel) == 7 else None
            if jog is None:
                # Mesmo jogo: pedir outro ao servidor com embaralhado novo
                pagina.get_by_role("button", name="Novo Jogo").click(timeout=20_000)
                pagina.wait_for_timeout(2000)
                payload = jogo_capturado.get("payload")
                if not payload:
                    continue
                estado = payload.get("estado_jogo", payload)
                tabel = estado.get("estruturas", {}).get("listas_tableau", [])
                jog = _encontrar_jogada(tabel) if tabel and len(tabel) == 7 else None
            if jog is None:
                print(
                    "Tentativa", tentativa, ": nenhum movimento lista->lista nesta partida."
                )
                continue

            print("Partida (id):", id_sess)
            print(
                "Jogada prevista: origem coluna",
                jog.coluna_origem,
                "índice corte",
                jog.indice_corte,
                "-> destino coluna",
                jog.coluna_destino,
            )

            # Detalhe do estado (número/cor) — útil p.ex. D+Valete vs D+Rei.
            cm = tabel[jog.coluna_origem][jog.indice_corte]
            ult = tabel[jog.coluna_destino][-1]
            print(
                "Carta (origem) número/cor naipe:",
                cm.get("numero_carta"),
                cm.get("cor"),
                cm.get("naipe_carta"),
            )
            print(
                "Carta (destino, topo) número/cor naipe:",
                ult.get("numero_carta"),
                ult.get("cor"),
                ult.get("naipe_carta"),
            )

            col_deste = tabel[jog.coluna_destino]
            if not tabel[jog.coluna_origem] or not col_deste or len(col_deste) == 0:
                print("Coluna inválida no JSON.")
                contexto.close()
                navegador.close()
                return 1
            if not cm.get("texto") or not ult.get("texto"):
                print("Falta texto no JSON (carta fechada?).")
                contexto.close()
                navegador.close()
                return 1
            # Clique: faixa superior da origem; centro do destino (última da coluna).
            ind_ult = len(tabel[jog.coluna_destino]) - 1
            if not _clicar_area_carta(
                pagina, jog.coluna_origem, jog.indice_corte, fracao_y=0.14
            ):
                print("Não foi possível localizar a carta de origem no DOM.")
                contexto.close()
                navegador.close()
                return 1
            time.sleep(1.0)
            if not _clicar_area_carta(
                pagina, jog.coluna_destino, ind_ult, fracao_y=0.5
            ):
                print("Falha ao clicar no destino (verifique o layout / viewport).")
                contexto.close()
                navegador.close()
                return 1
            time.sleep(0.6)

            if rejeicoes_ui:
                print("--- A UI (console) registrou rejeição após a jogada: ---")
                for linha in rejeicoes_ui:
                    print(linha)
                print("--- Comparação: mesma requisição à API (estado ainda ocorre) ---")
                resposta_motor = _api_post_json(
                    f"/jogo/{id_sess}/mover",
                    {
                        "tipo_movimento": 6,
                        "indice_lista_origem": jog.coluna_origem,
                        "indice_lista_destino": jog.coluna_destino,
                        "posicao_corte": jog.indice_corte,
                    },
                    api_base=api_base,
                )
                print("jogada_valida (API):", resposta_motor.get("jogada_valida"))
                print("motivo_rejeicao (API):", resposta_motor.get("motivo_rejeicao"))
                if resposta_motor.get("jogada_valida"):
                    print(
                        "Diagnóstico: a API aceitou; a rejeição veio de parâmetros"
                        " diferentes ou o clique não correspondeu à jogada."
                    )
                print("--- Últimas 20 linhas de console: ---")
                for linha in avisos_console[-20:]:
                    print(linha)
            else:
                print("Nenhum aviso de 'Jogada inválida' no console após a sequência de cliques.")
                if avisos_console:
                    print("Amostra de console:", *avisos_console[-5:], sep="\n")

            contexto.close()
            navegador.close()
            return 0

        print("Esgotadas tentativas sem encontrar uma partida com jogada lista->lista.")
        contexto.close()
        navegador.close()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
