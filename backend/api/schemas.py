"""Schemas Pydantic para validação e documentação da API."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class CartaEntrada(BaseModel):
    """Representa a entrada de uma carta."""
    numero_carta: int = Field(..., ge=1, le=13, description="Número da carta (1 a 13)")
    naipe_carta: str = Field(..., description="Naipe da carta ('c', 'o', 'p', 'e')")
    status_carta: bool = Field(False, description="True se a carta está virada para cima")


class RequestMoverCarta(BaseModel):
    """Corpo da requisição para realizar um movimento."""
    tipo_movimento: int = Field(
        ...,
        ge=1,
        le=6,
        description="""Tipo de movimento: 
        1 = Fila -> Fila (reposicionar);
        2 = Fila -> Pilha;
        3 = Fila -> Lista;
        4 = Pilha -> Lista;
        5 = Lista -> Pilha;
        6 = Lista -> Lista"""
    )
    naipe_destino: Optional[str] = Field(None, description="Naipe da pilha de destino (c, o, p, e), usado para tipos 2 e 5")
    naipe_origem: Optional[str] = Field(None, description="Naipe da pilha de origem (c, o, p, e), usado para tipo 4")
    indice_lista_origem: Optional[int] = Field(None, ge=0, le=6, description="Índice da lista de origem (0 a 6), usado para tipos 5 e 6")
    indice_lista_destino: Optional[int] = Field(None, ge=0, le=6, description="Índice da lista de destino (0 a 6), usado para tipos 3, 4 e 6")
    posicao_corte: Optional[int] = Field(
        None,
        ge=0,
        description=(
            "Tipo 6: posição (base 0) do primeiro nó a mover, na **mesma ordem** do array "
            "`estado.estruturas.listas_tableau[coluna]`: o elemento [0] é a carta de **cima** da coluna, "
            "o último [n−1] é a de **baixo** (face-up, em Klondike). Ex.: 5 cartas (4 escondidas + 1 virada) "
            "→ índices 0 a 4, e a virada de baixo é 4. O valor de `n` é **sempre** o `len` desse array no "
            "estado corrente (muda com jogadas); não contar 1 a n “à mão”."
        ),
    )


class ResponsePadraoOperacao(BaseModel):
    """Resposta padrão para operações e movimentos.

    `operacoes_realizadas` usa `list[Any]` (não `list[dict[str, Any]]`):
    o motor aninha listas e dicts; a validação estrita de resposta do Pydantic v2
    podia falhar (500) em alguns passos, embora o JSON estivesse correto.
    """

    jogada_valida: bool = Field(..., description="Indica se a jogada foi válida ou rejeitada")
    motivo_rejeicao: Optional[str] = Field(None, description="Mensagem explicando por que foi rejeitado, se for o caso")
    operacoes_realizadas: list[Any] = Field(default_factory=list, description="Logs das operações com pseudocódigo narrado")
    estado_jogo: Optional[Any] = Field(None, description="Estado completo do jogo após a jogada (árvore aninhada)")
    streak: Optional[dict[str, Any]] = Field(None, description="Contadores e feedbacks do streak ativo")


class ResponseNovoJogo(BaseModel):
    """Resposta para a criação de um novo jogo."""
    id_sessao: str = Field(..., description="UUID identificador da sessão")
    estado_jogo: dict[str, Any] = Field(..., description="Estado serializado das estruturas do jogo")
    log_preparacao: Optional[list[dict[str, Any]]] = Field(None, description="Log narrado da preparação se log_detalhado=True")
