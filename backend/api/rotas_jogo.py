"""Rotas para o motor do jogo Paciência."""

from fastapi import APIRouter, HTTPException, Path, Query, Request
from fastapi.encoders import jsonable_encoder
from typing import Any

from api.gerenciador_sessoes import obter_estado, salvar_estado
from api.locks_jogo import lock_motor_sessao
from api.erro_500 import logar_500
from api.serializacao_resposta import sanitizar_motor_para_json
from motor.estado_jogo import EstadoJogo
from motor import controlador_jogo
from api.schemas import RequestMoverCarta, ResponseNovoJogo

rotas_jogo = APIRouter()


@rotas_jogo.post(
    "/novo",
    response_model=ResponseNovoJogo,
    status_code=201,
    summary="Criar novo jogo",
    description="Cria uma nova partida, distribui as cartas nas estruturas e retorna o estado inicial."
)
def criar_novo_jogo(
    log_detalhado: bool = Query(True, description="Se True, retorna os passos narrados da criação e distribuição.")
) -> dict[str, Any]:
    estado_novo = EstadoJogo()
    log_preparacao = controlador_jogo.distribuir_cartas_novo_jogo(estado_novo)
    
    salvar_estado(estado_novo)
    
    resposta: dict[str, Any] = {
        "id_sessao": estado_novo.id_sessao,
        "estado_jogo": estado_novo.serializar(),
    }
    if log_detalhado:
        resposta["log_preparacao"] = sanitizar_motor_para_json(log_preparacao)

    return resposta


@rotas_jogo.get(
    "/{id_sessao}/estado",
    summary="Consultar estado do jogo",
    description="Retorna o estado atual completo da partida."
)
def consultar_estado_jogo(
    id_sessao: str = Path(..., description="UUID da sessão do jogo")
) -> dict[str, Any]:
    estado = obter_estado(id_sessao)
    if not estado:
        raise HTTPException(status_code=404, detail="Sessão não encontrada ou expirada.")
        
    return estado.serializar()


@rotas_jogo.post(
    "/{id_sessao}/mover",
    summary="Realizar jogada",
    description=(
        "Recebe o tipo do movimento e seus parâmetros, valida e executa nas estruturas. "
        "Sem `response_model`: a validação de resposta do Pydantic v2 gerava 500 em alguns "
        "movimentos (árvore aninhada) e o terminal do Uvicorn nem sempre mostrava o traceback."
    ),
)
def mover_carta(
    requisicao: RequestMoverCarta,
    request: Request,
    id_sessao: str = Path(..., description="UUID da sessão do jogo")
) -> dict[str, Any]:
    with lock_motor_sessao(id_sessao):
        estado = obter_estado(id_sessao)
        if not estado:
            raise HTTPException(status_code=404, detail="Sessão não encontrada ou expirada.")

        resultado_movimento: dict[str, Any] = {}

        if requisicao.tipo_movimento == 1:
            # Fila -> Fila
            resultado_movimento = controlador_jogo.executar_fila_para_fila(estado)

        elif requisicao.tipo_movimento == 2:
            # Fila -> Pilha
            if requisicao.naipe_destino is None:
                raise HTTPException(
                    status_code=400, detail="naipe_destino é obrigatório para este movimento."
                )
            resultado_movimento = controlador_jogo.executar_fila_para_pilha(
                estado, requisicao.naipe_destino
            )

        elif requisicao.tipo_movimento == 3:
            # Fila -> Lista
            if requisicao.indice_lista_destino is None:
                raise HTTPException(
                    status_code=400,
                    detail="indice_lista_destino é obrigatório para este movimento.",
                )
            resultado_movimento = controlador_jogo.executar_fila_para_lista(
                estado, requisicao.indice_lista_destino
            )

        elif requisicao.tipo_movimento == 4:
            # Pilha -> Lista
            if requisicao.naipe_origem is None or requisicao.indice_lista_destino is None:
                raise HTTPException(
                    status_code=400, detail="naipe_origem e indice_lista_destino são obrigatórios."
                )
            resultado_movimento = controlador_jogo.executar_pilha_para_lista(
                estado, requisicao.naipe_origem, requisicao.indice_lista_destino
            )

        elif requisicao.tipo_movimento == 5:
            # Lista -> Pilha
            if requisicao.indice_lista_origem is None or requisicao.naipe_destino is None:
                raise HTTPException(
                    status_code=400,
                    detail="indice_lista_origem e naipe_destino são obrigatórios.",
                )
            resultado_movimento = controlador_jogo.executar_lista_para_pilha(
                estado, requisicao.indice_lista_origem, requisicao.naipe_destino
            )

        elif requisicao.tipo_movimento == 6:
            # Lista -> Lista
            if (
                requisicao.indice_lista_origem is None
                or requisicao.indice_lista_destino is None
                or requisicao.posicao_corte is None
            ):
                raise HTTPException(
                    status_code=400,
                    detail="índices de listas origem/destino e posicao_corte são obrigatórios.",
                )
            resultado_movimento = controlador_jogo.executar_lista_para_lista(
                estado,
                requisicao.indice_lista_origem,
                requisicao.posicao_corte,
                requisicao.indice_lista_destino,
            )

        else:
            raise HTTPException(status_code=400, detail="tipo_movimento inválido.")

        salvar_estado(estado)

        # Estado tabuleiro (JSON seguro); se `sanitizar` falhar nos logs, ainda devolvemos 200 + estado.
        try:
            estado_serial = estado.serializar()
        except Exception as exc:
            logar_500(exc, request=request, contexto="mover:estado.serializar")
            raise HTTPException(status_code=500, detail="Falha ao serializar o estado do jogo.") from exc

        resultado_movimento["estado_jogo"] = estado_serial
        try:
            return sanitizar_motor_para_json(resultado_movimento)
        except Exception as exc:
            logar_500(exc, request=request, contexto="mover:sanitizar_motor_para_json")
            return jsonable_encoder(
                {
                    "jogada_valida": bool(resultado_movimento.get("jogada_valida")),
                    "motivo_rejeicao": resultado_movimento.get("motivo_rejeicao"),
                    "operacoes_realizadas": [],
                    "streak": resultado_movimento.get("streak"),
                    "estado_jogo": estado_serial,
                    "aviso": "Jogada aplicada; log de operações omitido por falha na serialização.",
                }
            )


@rotas_jogo.get(
    "/{id_sessao}/movimentos",
    summary="Listar movimentos possíveis",
    description="Analisa o estado atual e retorna a lista de todas as jogadas válidas disponíveis (a implementar cálculo exato futuramente)."
)
def listar_movimentos(
    id_sessao: str = Path(..., description="UUID da sessão")
) -> dict[str, Any]:
    estado = obter_estado(id_sessao)
    if not estado:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")
    
    # A implementação exata de calcular todos os movimentos possíveis requer
    # varrer todas as cartas do topo/frente e tentar contra todos os destinos.
    # Por enquanto, retornamos os 6 tipos com descrições genéricas,
    # que atende o requisito acadêmico básico e servirá de base.
    # O frontend pode usar os validadores (motor) para indicar ou
    # simplesmente esperar a validação ao tentar.
    
    return {
        "tipos_movimentos": [
            {"id": 1, "nome": "Fila -> Fila", "descricao": "Reposiciona a frente da fila para o final."},
            {"id": 2, "nome": "Fila -> Pilha", "descricao": "Move a carta da frente da fila para a pilha do naipe correspondente."},
            {"id": 3, "nome": "Fila -> Lista Ligada", "descricao": "Move a carta da frente da fila para o tableau."},
            {"id": 4, "nome": "Pilha -> Lista Ligada", "descricao": "Move o topo da pilha para uma coluna do tableau."},
            {"id": 5, "nome": "Lista Ligada -> Pilha", "descricao": "Move a carta da base do tableau para uma pilha de fundação."},
            {"id": 6, "nome": "Lista Ligada -> Lista Ligada", "descricao": "Move uma sublista (ou carta única) entre colunas do tableau."}
        ]
    }


@rotas_jogo.get(
    "/{id_sessao}/estatisticas",
    summary="Consultar estatísticas da partida",
    description="Retorna métricas e contadores da partida atual."
)
def consultar_estatisticas(
    id_sessao: str = Path(..., description="UUID da sessão")
) -> dict[str, Any]:
    estado = obter_estado(id_sessao)
    if not estado:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")
        
    return {
        "id_sessao": estado.id_sessao,
        "jogo_vencido": estado.jogo_vencido,
        "estatisticas": {
            "total_jogadas": estado.total_jogadas,
            "sequencia_atual": estado.sequencia_atual,
            "maior_sequencia": estado.maior_sequencia,
            "estruturas_resumo": "Listas (7), Pilhas (4), Fila (1)",
        }
    }
