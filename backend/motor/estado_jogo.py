"""Estado encapsulado de uma partida de Paciência."""

from __future__ import annotations

import uuid
from typing import Any

from modelo.carta_baralho import CartaBaralho
from modelo.fila_cartas import FilaCartas
from modelo.lista_ligada_cartas import ListaLigadaCartas
from modelo.pilha_cartas import PilhaCartas


class EstadoJogo:
    """Encapsula as estruturas de dados e o estado de uma partida.

    Attributes:
        id_sessao: Identificador único da partida.
        fila_compra: O monte de onde se puxam novas cartas.
        pilhas_fundacao: Dicionário com 4 pilhas (chaves: 'c', 'o', 'p', 'e').
        listas_tableau: Lista de 7 listas duplamente encadeadas.
        sequencia_atual: Contador do streak ativo.
        maior_sequencia: Maior streak atingido na partida.
        total_jogadas: Total de movimentos válidos realizados.
        jogo_vencido: Flag indicando se as 4 pilhas estão completas.
    """

    def __init__(self) -> None:
        self.id_sessao = str(uuid.uuid4())
        self.fila_compra = FilaCartas(nome_fila="fila_compra")

        self.pilhas_fundacao: dict[str, PilhaCartas] = {
            "c": PilhaCartas(nome_pilha="pilha_copas"),
            "o": PilhaCartas(nome_pilha="pilha_ouros"),
            "p": PilhaCartas(nome_pilha="pilha_paus"),
            "e": PilhaCartas(nome_pilha="pilha_espadas"),
        }

        self.listas_tableau: list[ListaLigadaCartas] = [
            ListaLigadaCartas(nome_lista=f"lista_ligada_{i+1}")
            for i in range(7)
        ]

        self.sequencia_atual = 0
        self.maior_sequencia = 0
        self.total_jogadas = 0
        self.jogo_vencido = False

    def serializar(self) -> dict[str, Any]:
        """Serializa o estado atual para JSON.
        
        Cartas viradas para baixo não expõem seu número ou naipe.
        """
        def _serializar_carta(carta) -> dict[str, Any]:
            if carta is None or not isinstance(carta, CartaBaralho):
                return {"status_carta": False, "texto": "carta indisponível", "erro_dominio": True}
            return carta.para_dicionario_json()

        # Serializando a fila
        fila_cartas = []
        atual_fila = self.fila_compra.no_frente
        while atual_fila is not None:
            fila_cartas.append(_serializar_carta(atual_fila.dados_carta))
            atual_fila = atual_fila.proximo_no

        # Serializando as pilhas
        pilhas_dict = {}
        for naipe, pilha in self.pilhas_fundacao.items():
            cartas_pilha = []
            atual_pilha = pilha.elemento_topo
            while atual_pilha is not None:
                # Return in base-to-top order for the UI as well
                cartas_pilha.insert(0, _serializar_carta(atual_pilha.dados_carta))
                atual_pilha = atual_pilha.proximo_no
            pilhas_dict[naipe] = cartas_pilha

        # Serializando o tableau
        tableau_listas = []
        for lista in self.listas_tableau:
            cartas_lista = []
            atual_lista = lista.cabeca_no
            while atual_lista is not None:
                cartas_lista.append(_serializar_carta(atual_lista.dados_carta))
                atual_lista = atual_lista.proximo_no
            tableau_listas.append(cartas_lista)

        return {
            "id_sessao": self.id_sessao,
            "jogo_vencido": self.jogo_vencido,
            "estatisticas": {
                "total_jogadas": self.total_jogadas,
                "sequencia_atual": self.sequencia_atual,
                "maior_sequencia": self.maior_sequencia,
            },
            "estruturas": {
                "fila_compra": fila_cartas,
                "pilhas_fundacao": pilhas_dict,
                "listas_tableau": tableau_listas,
            },
        }

    def serializar_completo(self) -> dict[str, Any]:
        """Serializa o estado COMPLETO para o Banco de Dados.
        Usa dicionários para envolver listas e evitar erros de 'invalid nested entity' no Firestore.
        """
        # Fila
        fila_cartas = []
        atual_fila = self.fila_compra.no_frente
        while atual_fila is not None:
            fila_cartas.append(atual_fila.dados_carta.serializar_completo())
            atual_fila = atual_fila.proximo_no

        # Pilhas
        pilhas_dict = {}
        for naipe, pilha in self.pilhas_fundacao.items():
            cartas_pilha = []
            atual_pilha = pilha.elemento_topo
            while atual_pilha is not None:
                # Top-to-bottom order: the first in list is the top of the stack.
                # When deserializing, we will reverse the list to push from bottom up,
                # or just change how we serialize. 
                # Let's keep it simple: list = [bottom, ..., top]
                # So we use insert(0) to get bottom-to-top.
                cartas_pilha.insert(0, atual_pilha.dados_carta.serializar_completo())
                atual_pilha = atual_pilha.proximo_no
            pilhas_dict[naipe] = {"cartas": cartas_pilha}

        # Tableau
        tableau_listas = []
        for lista in self.listas_tableau:
            cartas_lista = []
            atual_lista = lista.cabeca_no
            while atual_lista is not None:
                cartas_lista.append(atual_lista.dados_carta.serializar_completo())
                atual_lista = atual_lista.proximo_no
            tableau_listas.append({"cartas": cartas_lista})

        return {
            "id_sessao": self.id_sessao,
            "jogo_vencido": self.jogo_vencido,
            "sequencia_atual": self.sequencia_atual,
            "maior_sequencia": self.maior_sequencia,
            "total_jogadas": self.total_jogadas,
            "estruturas": {
                "fila_compra": {"cartas": fila_cartas},
                "pilhas_fundacao": pilhas_dict,
                "listas_tableau": tableau_listas,
            },
        }

    @staticmethod
    def desserializar(dados: dict[str, Any]) -> EstadoJogo:
        """Recria o EstadoJogo completo a partir do dicionário do Banco de Dados."""
        estado = EstadoJogo()
        estado.id_sessao = dados["id_sessao"]
        estado.jogo_vencido = dados.get("jogo_vencido", False)
        estado.sequencia_atual = dados.get("sequencia_atual", 0)
        estado.maior_sequencia = dados.get("maior_sequencia", 0)
        estado.total_jogadas = dados.get("total_jogadas", 0)

        estruturas = dados["estruturas"]

        # Fila
        estado.fila_compra = FilaCartas.desserializar(
            estruturas["fila_compra"]["cartas"], nome_fila="fila_compra"
        )

        # Pilhas
        for naipe in ["c", "o", "p", "e"]:
            mapa_nomes = {"c": "copas", "o": "ouros", "p": "paus", "e": "espadas"}
            nome_real = f"pilha_{mapa_nomes[naipe]}"
            estado.pilhas_fundacao[naipe] = PilhaCartas.desserializar(
                estruturas["pilhas_fundacao"][naipe]["cartas"], nome_pilha=nome_real
            )

        # Tableau
        estado.listas_tableau = []
        for i, lista_wrapper in enumerate(estruturas["listas_tableau"]):
            estado.listas_tableau.append(
                ListaLigadaCartas.desserializar(
                    lista_wrapper["cartas"], nome_lista=f"lista_ligada_{i+1}"
                )
            )

        return estado
