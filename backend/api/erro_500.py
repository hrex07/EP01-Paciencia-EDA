"""Registro e corpo JSON opcional para respostas HTTP 500 (diagnóstico em dev)."""

from __future__ import annotations

import logging
import os
import sys
import traceback
from typing import Any

from fastapi import Request

# Logger próprio com handler em stderr: não depender da config do `uvicorn.error`
# (em alguns modos o nível/handlers não mostram `ERROR` no terminal).
def _obter_log_500() -> logging.Logger:
    name = "ep01.http500"
    log = logging.getLogger(name)
    if not log.handlers:
        log.setLevel(logging.ERROR)
        h = logging.StreamHandler(sys.stderr)
        h.setLevel(logging.ERROR)
        h.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        log.addHandler(h)
        log.propagate = False
    return log


def log_mensagem_500(mensagem: str) -> None:
    """Uma linha de log para 500 sem exceção (ex.: resposta 500 em texto plano)."""
    _obter_log_500().error("%s", mensagem)


def _expor_trace_no_json() -> bool:
    """Inclui o texto do stack no JSON; desligar em produção pública (API_500_INCLUIR_TRACO_NO_JSON=0)."""
    v = os.getenv("API_500_INCLUIR_TRACO_NO_JSON", "1")
    return v not in ("0", "false", "False")


def _expor_mensagem_excecao_no_json() -> bool:
    v = os.getenv("API_ERRO_500_CONTEUDO", "1")
    return v not in ("0", "false", "False")


def formatted_traceback(exc: BaseException) -> str:
    """String completa (multilinha) do stack, incluindo cause/chaining."""
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


def logar_500(
    exc: BaseException,
    *,
    request: Request | None = None,
    contexto: str = "",
) -> None:
    """Grava o traceback no stderr (sempre visível) — chamar para todo 500 com exceção associada."""
    m = f"500 {contexto or type(exc).__name__}" if not contexto else f"500 {contexto}"
    if request is not None:
        m = f"{m} | {request.method} {request.url.path}"
    # Tupla: funciona fora de `except`; com objeto BaseException sem tb às vezes o logging só
    # mostra a linha do erro — preferir a tupla explícita.
    _obter_log_500().error(
        m,
        exc_info=(type(exc), exc, exc.__traceback__),
    )


def corpo_comum_500(
    exc: BaseException,
    *,
    detalhe: str,
    request: Request | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Base JSON; inclui `stacktrace` se API_500_INCLUIR_TRACO_NO_JSON permitir."""
    logar_500(exc, request=request, contexto=type(exc).__name__)
    corpo: dict[str, Any] = {"detail": detalhe, "erro_tipo": type(exc).__name__}
    if _expor_mensagem_excecao_no_json():
        corpo["mensagem"] = f"{exc!s}"
    if _expor_trace_no_json():
        corpo["stacktrace"] = formatted_traceback(exc)
    if extra:
        corpo.update(extra)
    return corpo
