"""Ponto de entrada da aplicação FastAPI."""

import os
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from api.erro_500 import corpo_comum_500, log_mensagem_500
from api.rotas_jogo import rotas_jogo
from api.rotas_algoritmos import rotas_algoritmos
from api.rotas_estruturas import rotas_estruturas

app = FastAPI(
    title="Paciência Educacional",
    description="API para o jogo Paciência com Estruturas de Dados didáticas. Projeto acadêmico de Mestrado em Computação Aplicada (IPT).",
    version="0.1.0",
)

# localhost e 127.0.0.1 são origens diferentes no navegador; inclua as duas (ou defina
# ALLOWED_ORIGINS no deploy). A regex abaixo cobre qualquer porta em dev.
_padrao_origens = (
    "http://localhost:5173,http://127.0.0.1:5173,"
    "http://localhost:3000,http://127.0.0.1:3000"
)
origens_permitidas = [
    s.strip() for s in os.getenv("ALLOWED_ORIGINS", _padrao_origens).split(",") if s.strip()
]
if "*" in origens_permitidas:
    origens_permitidas = ["*"]


# Rate limit em memória (módulo). 0 = desligado. Em dev o jogo + painel geram muitas chamadas
# (200/60s era fácil de estourar e parecia "erro" no front).
rate_limit_records: dict[str, list[float]] = {}
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "2000"))
RATE_LIMIT_WINDOW_SEC = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))


class LimiteRequisicoesHttp(BaseHTTPMiddleware):
    """Limita requisições por IP. Deve ficar *dentro* do CORS (add_middleware abaixo)."""

    async def dispatch(self, request: Request, call_next):
        if RATE_LIMIT_MAX_REQUESTS <= 0:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        agora = time.time()

        if client_ip not in rate_limit_records:
            rate_limit_records[client_ip] = []

        rate_limit_records[client_ip] = [
            t for t in rate_limit_records[client_ip] if agora - t < RATE_LIMIT_WINDOW_SEC
        ]

        if len(rate_limit_records[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"detail": "Muitas requisições (Rate Limit). Tente novamente em um minuto."},
            )

        rate_limit_records[client_ip].append(agora)
        return await call_next(request)


class Resposta500Logger(BaseHTTPMiddleware):
    """Garante log quando a aplicação devolve 500 sem passar nossos exception_handlers (raro: Starlette/ASGI)."""

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            resposta: Response = await call_next(request)
        except Exception:
            raise
        if resposta.status_code == 500 and resposta.headers.get("content-type", "").startswith(
            "text/plain"
        ):
            log_mensagem_500(
                "Resposta 500 (texto plano) — provável 500 padrão do ASGI, sem exceção "
                f"no handler FastAPI. Ver reloader ou caminhos fora de api/: {request.method} {request.url.path}"
            )
        return resposta


# Ordem do Starlette: o último add_middleware é a camada mais externa.
# CORS precisa ser o mais externo para anexar cabeçalhos a 200, 4xx, 5xx e 429.
# Resposta500Logger: dentro do CORS, para ainda ver cabeçalhos; por último antes do CORS
# fica a camada "mais interna" — ordem: LimiteRequisições -> 500log -> (app); depois CORS (externo)
app.add_middleware(Resposta500Logger)
app.add_middleware(LimiteRequisicoesHttp)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|::1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rotas_jogo, prefix="/api/jogo", tags=["Jogo"])
app.include_router(rotas_algoritmos, prefix="/api/algoritmos", tags=["Algoritmos"])
app.include_router(rotas_estruturas, prefix="/api/estruturas", tags=["Estruturas de Dados"])


@app.exception_handler(ResponseValidationError)
async def tratar_resposta_pydantic_invalida(
    request: Request, exc: ResponseValidationError
) -> JSONResponse:
    """Falha ao validar/serializar a *resposta* (OpenAPI) — muito comum com response_model e JSON profundo."""
    return JSONResponse(
        status_code=500,
        content=corpo_comum_500(
            exc,
            detalhe="Falha na validação da resposta (ResponseValidationError).",
            request=request,
            extra={"errors": exc.errors()},  # type: ignore[union-attr]
        ),
    )


@app.exception_handler(Exception)
async def tratar_excecao_generica(request: Request, exc: Exception) -> JSONResponse:  # noqa: BLE001
    """Garante traceback no log (uvicorn) e, por defeito, `stacktrace` no JSON; delega 4xx/422 ao padrão."""
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    if isinstance(exc, RequestValidationError):
        return await request_validation_exception_handler(request, exc)
    return JSONResponse(
        status_code=500,
        content=corpo_comum_500(
            exc,
            detalhe="Erro interno inesperado.",
            request=request,
        ),
    )
