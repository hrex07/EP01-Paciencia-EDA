"""Rotas para demonstração isolada de cada Estrutura de Dados (Pilha, Fila, Lista Ligada)."""

from fastapi import APIRouter, Body
from typing import Any

from modelo.carta_baralho import CartaBaralho
from modelo.pilha_cartas import PilhaCartas
from modelo.fila_cartas import FilaCartas
from modelo.lista_ligada_cartas import ListaLigadaCartas
from api.schemas import CartaEntrada
from api.serializacao_resposta import sanitizar_motor_para_json

rotas_estruturas = APIRouter()

# --- Como é uma demonstração isolada ("playground"), vamos manter instâncias em memória globais ---
# (Num ambiente de produção real precisaríamos de chaves de sessão para o playground,
# mas para MVP acadêmico uma instância fixa para cada tipo atende ao caso de teste simples).
PLAYGROUND_PILHA = PilhaCartas(nome_pilha="pilha_playground")
PLAYGROUND_FILA = FilaCartas(nome_fila="fila_playground")
PLAYGROUND_LISTA = ListaLigadaCartas(nome_lista="lista_playground")


def _carta_from_schema(c: CartaEntrada) -> CartaBaralho:
    return CartaBaralho(c.numero_carta, c.naipe_carta, status_carta=c.status_carta)


# == PILHA ==
@rotas_estruturas.post("/pilha/empilhar", summary="Demonstração: Push (Pilha)")
def demo_pilha_empilhar(carta: CartaEntrada = Body(...)) -> dict[str, Any]:
    return sanitizar_motor_para_json(
        PLAYGROUND_PILHA.empilhar(_carta_from_schema(carta), registrar_passos=True)
    )


@rotas_estruturas.post("/pilha/desempilhar", summary="Demonstração: Pop (Pilha)")
def demo_pilha_desempilhar() -> dict[str, Any]:
    resultado = PLAYGROUND_PILHA.desempilhar(registrar_passos=True)
    if resultado["operacao_sucesso"]:
        resultado["valor_retornado"] = resultado["valor_retornado"].texto_carta()
    return resultado


# == FILA ==
@rotas_estruturas.post("/fila/enfileirar", summary="Demonstração: Enqueue (Fila)")
def demo_fila_enfileirar(carta: CartaEntrada = Body(...)) -> dict[str, Any]:
    return sanitizar_motor_para_json(
        PLAYGROUND_FILA.enfileirar(_carta_from_schema(carta), registrar_passos=True)
    )


@rotas_estruturas.post("/fila/desenfileirar", summary="Demonstração: Dequeue (Fila)")
def demo_fila_desenfileirar() -> dict[str, Any]:
    resultado = PLAYGROUND_FILA.desenfileirar(registrar_passos=True)
    if resultado["operacao_sucesso"]:
        resultado["valor_retornado"] = resultado["valor_retornado"].texto_carta()
    return resultado


# == LISTA LIGADA ==
@rotas_estruturas.post("/lista/inserir_final", summary="Demonstração: Append (Lista)")
def demo_lista_inserir(carta: CartaEntrada = Body(...)) -> dict[str, Any]:
    return sanitizar_motor_para_json(
        PLAYGROUND_LISTA.inserir_final(_carta_from_schema(carta), registrar_passos=True)
    )


@rotas_estruturas.post("/lista/remover_final", summary="Demonstração: Remove Last (Lista)")
def demo_lista_remover() -> dict[str, Any]:
    resultado = PLAYGROUND_LISTA.remover_final(registrar_passos=True)
    if resultado["operacao_sucesso"]:
        resultado["valor_retornado"] = resultado["valor_retornado"].texto_carta()
    return resultado
