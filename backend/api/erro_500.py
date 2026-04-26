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
    """Retorna logger dedicado a erros HTTP 500 com handler em stderr."""
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
    """Registra uma linha de erro sem objeto ``Exception`` (casos raros ASGI).

    Args:
        mensagem: Texto descritivo (ex.: 500 em texto plano sem traceback).
    """
    _obter_log_500().error("%s", mensagem)


def _expor_trace_no_json() -> bool:
    """Indica se o JSON de erro deve incluir ``stacktrace`` (variável de ambiente).

    Returns:
        ``False`` quando ``API_500_INCLUIR_TRACO_NO_JSON`` for ``0``/``false``.
    """
    v = os.getenv("API_500_INCLUIR_TRACO_NO_JSON", "1")
    return v not in ("0", "false", "False")


def _expor_mensagem_excecao_no_json() -> bool:
    """Indica se a mensagem textual da exceção entra no JSON (``API_ERRO_500_CONTEUDO``).

    Returns:
        ``False`` quando a variável de ambiente for ``0``/``false`` (omitir
        campo ``mensagem`` no JSON).
    """
    v = os.getenv("API_ERRO_500_CONTEUDO", "1")
    return v not in ("0", "false", "False")


def formatted_traceback(exc: BaseException) -> str:
    """Monta o traceback completo da exceção, incluindo encadeamento de causas.

    Args:
        exc: Qualquer ``BaseException`` com traceback associado.

    Returns:
        Texto multilinha compatível com logs e campo ``stacktrace`` no JSON.
    """
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


def logar_500(
    exc: BaseException,
    *,
    request: Request | None = None,
    contexto: str = "",
) -> None:
    """Grava o traceback no stderr; usar em todo 500 com exceção associada.

    Args:
        exc: Exceção capturada.
        request: Requisição FastAPI opcional (método e path no log).
        contexto: Rótulo curto para identificar o ponto do código (ex. prefixo
            ``mover:``).
    """
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
    """Monta o dicionário JSON padrão para respostas HTTP 500.

    Args:
        exc: Exceção original (para tipo, mensagem e stack opcional).
        detalhe: Campo ``detail`` amigável ao cliente.
        request: Opcional; usado apenas para logging via :func:`logar_500`.
        extra: Chaves adicionais fundidas no corpo (ex. ``errors`` de Pydantic).

    Returns:
        Dict com ``detail``, ``erro_tipo`` e, conforme flags de ambiente,
        ``mensagem`` e ``stacktrace``.
    """
    logar_500(exc, request=request, contexto=type(exc).__name__)
    corpo: dict[str, Any] = {"detail": detalhe, "erro_tipo": type(exc).__name__}
    if _expor_mensagem_excecao_no_json():
        corpo["mensagem"] = f"{exc!s}"
    if _expor_trace_no_json():
        corpo["stacktrace"] = formatted_traceback(exc)
    if extra:
        corpo.update(extra)
    return corpo
