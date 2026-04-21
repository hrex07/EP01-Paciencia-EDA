"""Ponto de entrada da aplicação FastAPI."""

import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.rotas_jogo import rotas_jogo
from api.rotas_algoritmos import rotas_algoritmos
from api.rotas_estruturas import rotas_estruturas

app = FastAPI(
    title="Paciência Educacional",
    description="API para o jogo Paciência com Estruturas de Dados didáticas. Projeto acadêmico de Mestrado em Computação Aplicada (IPT).",
    version="0.1.0",
)

origens_permitidas = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
# Se a lista estiver vazia ou for um asterisco solto na variável, permite tudo
if "*" in origens_permitidas:
    origens_permitidas = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Básico (Token Bucket simples por IP em memória)
# Adequado para um projeto acadêmico de pequeno porte
rate_limit_records = {}
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "200"))
RATE_LIMIT_WINDOW_SEC = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))

@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    agora = time.time()
    
    if client_ip not in rate_limit_records:
        rate_limit_records[client_ip] = []
        
    rate_limit_records[client_ip] = [t for t in rate_limit_records[client_ip] if agora - t < RATE_LIMIT_WINDOW_SEC]
    
    if len(rate_limit_records[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        return JSONResponse(status_code=429, content={"detail": "Muitas requisições (Rate Limit). Tente novamente em um minuto."})
        
    rate_limit_records[client_ip].append(agora)
    response = await call_next(request)
    return response

app.include_router(rotas_jogo, prefix="/api/jogo", tags=["Jogo"])
app.include_router(rotas_algoritmos, prefix="/api/algoritmos", tags=["Algoritmos"])
app.include_router(rotas_estruturas, prefix="/api/estruturas", tags=["Estruturas de Dados"])
