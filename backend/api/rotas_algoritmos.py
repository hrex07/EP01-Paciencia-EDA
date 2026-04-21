"""Rotas para demonstração dos algoritmos de embaralhamento e ordenação."""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import Any, Optional

from modelo.carta_baralho import CartaBaralho
from api.schemas import CartaEntrada
from modelo.criacao_baralho import criar_baralho_completo
from algoritmos.embaralhamento_iterativo import embaralhar_iterativo
from algoritmos.embaralhamento_recursivo import embaralhar_recursivo
from algoritmos.ordenacao_bubble import ordenacao_bubble
from algoritmos.ordenacao_merge import ordenacao_merge
from algoritmos.ordenacao_quick import ordenacao_quick
from algoritmos.comparar_ordenacao import comparar_algoritmos

rotas_algoritmos = APIRouter()


def _converter_entrada_para_cartas(lista_entrada: Optional[list[CartaEntrada]]) -> list[CartaBaralho]:
    if not lista_entrada:
        return criar_baralho_completo(registrar_passos=False)["vetor_cartas"]
    
    return [CartaBaralho(c.numero_carta, c.naipe_carta, status_carta=c.status_carta) for c in lista_entrada]


def _formatar_cartas_saida(resultado: dict[str, Any]) -> dict[str, Any]:
    """Converte instâncias de CartaBaralho no vetor de saída para ditos seriais."""
    resposta = dict(resultado)
    if "vetor_cartas" in resposta:
        resposta["vetor_cartas"] = [
            {
                "numero_carta": c.numero_carta, 
                "naipe_carta": c.naipe_carta, 
                "texto": c.texto_carta()
            } for c in resposta["vetor_cartas"]
        ]
    return resposta


@rotas_algoritmos.post(
    "/embaralhar",
    summary="Embaralhar vetor de cartas",
    description="Recebe um vetor opcional (ou cria baralho padrão) e aplica o embaralhamento iterativo ou recursivo."
)
def embaralhar_vetor(
    metodo: str = Query("iterativo", description="Método de embaralhamento ('iterativo' ou 'recursivo')"),
    cartas: Optional[list[CartaEntrada]] = Body(None, description="Vetor opcional de cartas. Se omitido, usará 52 cartas.")
) -> dict[str, Any]:
    vetor_cartas = _converter_entrada_para_cartas(cartas)
    
    if metodo.lower() == "iterativo":
        resultado = embaralhar_iterativo(vetor_cartas, quantidade_trocas=200, registrar_passos=True)
    elif metodo.lower() == "recursivo":
        resultado = embaralhar_recursivo(vetor_cartas, quantidade_trocas=200, registrar_passos=True)
    else:
        raise HTTPException(status_code=400, detail="Método deve ser 'iterativo' ou 'recursivo'.")
        
    return _formatar_cartas_saida(resultado)


@rotas_algoritmos.post(
    "/ordenar",
    summary="Ordenar vetor de cartas",
    description="Aplica algoritmo de ordenação escolhido e retorna vetor com log de passos e métricas."
)
def ordenar_vetor(
    metodo: str = Query(..., description="Algoritmo de ordenação ('bubble', 'merge', 'quick')"),
    cartas: Optional[list[CartaEntrada]] = Body(None, description="Vetor opcional. Se omitido, usará 52 cartas.")
) -> dict[str, Any]:
    vetor_cartas = _converter_entrada_para_cartas(cartas)
    # Sempre interessante testar em baralho embaralhado se omitido
    if not cartas:
        vetor_cartas = embaralhar_iterativo(vetor_cartas, quantidade_trocas=200, registrar_passos=False)["vetor_cartas"]
        
    if metodo.lower() == "bubble":
        resultado = ordenacao_bubble(vetor_cartas, registrar_passos=True)
    elif metodo.lower() == "merge":
        resultado = ordenacao_merge(vetor_cartas, registrar_passos=True)
    elif metodo.lower() == "quick":
        resultado = ordenacao_quick(vetor_cartas, registrar_passos=True)
    else:
        raise HTTPException(status_code=400, detail="Método deve ser 'bubble', 'merge' ou 'quick'.")
        
    return _formatar_cartas_saida(resultado)


@rotas_algoritmos.post(
    "/comparar",
    summary="Comparar algoritmos de ordenação",
    description="Compara os três algoritmos (Bubble, Merge, Quick) sobre cópias idênticas do mesmo vetor de entrada e retorna tabela de métricas."
)
def comparar_ordenacao(
    cartas: Optional[list[CartaEntrada]] = Body(None, description="Vetor opcional. Se omitido, usará 52 cartas embaralhadas aleatoriamente.")
) -> list[dict[str, Any]]:
    vetor_cartas = _converter_entrada_para_cartas(cartas)
    if not cartas:
        vetor_cartas = embaralhar_iterativo(vetor_cartas, quantidade_trocas=200, registrar_passos=False)["vetor_cartas"]
        
    resultados = comparar_algoritmos(vetor_cartas)
    return [_formatar_cartas_saida(res) for res in resultados]
