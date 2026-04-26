"""Lista duplamente ligada de cartas com operações didáticas e log narrado.

Cada método que altera ou consulta a estrutura pode devolver um dicionário
padrão com ``operacao_nome``, ``operacao_sucesso``, ``passos_executados``,
etc., para integração com o painel educacional e a API.
"""

from __future__ import annotations

from typing import Any, Optional

from modelo.carta_baralho import CartaBaralho
from modelo.excecao_carta import CartaInvalidaError
from modelo.no_encadeado import NoEncadeado


class ListaLigadaCartas:
    """Lista duplamente encadeada para colunas da mesa.

    Attributes:
        nome_lista: Identificador estável para logs (ex.: lista_ligada_3).
        cabeca_no: Primeiro nó ou None se vazia.
        cauda_no: Último nó ou None se vazia.
        quantidade_elementos: Contagem de nós.
    """

    def __init__(self, nome_lista: str = "lista_sem_nome") -> None:
        """Inicializa lista vazia.

        Args:
            nome_lista: Nome mostrado nos relatórios educacionais.
        """
        self.nome_lista = nome_lista
        self.cabeca_no: Optional[NoEncadeado] = None
        self.cauda_no: Optional[NoEncadeado] = None
        self.quantidade_elementos = 0

    def esta_vazia(self) -> bool:
        """Indica se a lista não contém nós.

        Returns:
            ``True`` se ``cabeca_no`` for ``None``.
        """
        return self.cabeca_no is None

    def obter_tamanho(self) -> int:
        """Retorna a quantidade atual de nós (cartas) na lista.

        Returns:
            Valor do contador ``quantidade_elementos``.
        """
        return self.quantidade_elementos

    @staticmethod
    def desserializar(dados_lista: list[dict[str, Any]], nome_lista: str) -> ListaLigadaCartas:
        """Reconstrói a lista a partir de cartas serializadas completas.

        Args:
            dados_lista: Sequência de dicts aceitos por ``CartaBaralho.desserializar``.
            nome_lista: Nome lógico da coluna (logs).

        Returns:
            Instância preenchida na ordem do array (cabeça → cauda).
        """
        lista = ListaLigadaCartas(nome_lista=nome_lista)
        for d_carta in dados_lista:
            carta = CartaBaralho.desserializar(d_carta)
            lista.inserir_final(carta, registrar_passos=False)
        return lista

    def _no_indice(self, indice_alvo: int) -> Optional[NoEncadeado]:
        """Percorre a partir da cabeça até o índice informado.

        Args:
            indice_alvo: Posição base zero (0 = cabeça).

        Returns:
            Referência ao nó ou ``None`` se índice inválido.
        """
        if indice_alvo < 0 or indice_alvo >= self.quantidade_elementos:
            return None
        no_atual = self.cabeca_no
        for _ in range(indice_alvo):
            if no_atual is None:
                return None
            no_atual = no_atual.proximo_no
        return no_atual

    def inserir_final(
        self,
        carta_nova: CartaBaralho,
        *, #Força o uso de argumentos nomeados
        registrar_passos: bool = True,
    ) -> dict[str, Any]:
        """Insere a carta após o último nó (append na lista dupla).

        Args:
            carta_nova: Carta a anexar na cauda.
            registrar_passos: Se inclui narrativa passo a passo.

        Returns:
            Dicionário-padrão de operação com ``operacao_nome`` ``inserir_final``.

        Raises:
            CartaInvalidaError: Se ``carta_nova`` não for ``CartaBaralho``.
        """
        if not isinstance(carta_nova, CartaBaralho):
            raise CartaInvalidaError("inserir_final espera CartaBaralho.")
        lista_passos: list[dict[str, Any]] = []
        numero_passo = 0

        no_novo = NoEncadeado(dados_carta=carta_nova)
        numero_passo += 1
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "nó_novo ← CriarNó(carta_nova)",
                    "descricao_acao": (
                        f"Criar nó contendo {carta_nova.texto_carta()} para inserção."
                    ),
                }
            )

        if self.cauda_no is None:
            numero_passo += 1
            self.cabeca_no = no_novo
            self.cauda_no = no_novo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "SE lista vazia ENTÃO cabeça ← cauda ← nó_novo",
                        "descricao_acao": (
                            f"Lista `{self.nome_lista}` recebe primeiro nó "
                            f"({carta_nova.texto_carta()})."
                        ),
                    }
                )
        else:
            numero_passo += 1
            no_novo.anterior_no = self.cauda_no
            self.cauda_no.proximo_no = no_novo
            self.cauda_no = no_novo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": (
                            "cauda.próximo ← nó_novo ; cauda ← nó_novo"
                        ),
                        "descricao_acao": (
                            f"Encadear {carta_nova.texto_carta()} após o antigo último nó."
                        ),
                    }
                )

        numero_passo += 1
        self.quantidade_elementos += 1
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "quantidade_elementos ← quantidade_elementos + 1",
                    "descricao_acao": (
                        f"Tamanho da lista `{self.nome_lista}` = "
                        f"{self.quantidade_elementos}."
                    ),
                }
            )

        return {
            "operacao_nome": "inserir_final",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": self.nome_lista,
            "operacao_sucesso": True,
            "valor_retornado": None,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def inserir_posicao(
        self,
        carta_nova: CartaBaralho,
        indice_posicao: int,
        *,
        registrar_passos: bool = True,
    ) -> dict[str, Any]:
        """Insere carta na posição ``indice_posicao`` (0 = novo primeiro nó).

        Args:
            carta_nova: Carta a inserir.
            indice_posicao: Índice base zero; pode ser ``tamanho`` para delegar a
                :meth:`inserir_final`.
            registrar_passos: Controla o log didático.

        Returns:
            Resultado-padrão; em índice inválido, ``operacao_sucesso`` é falso.

        Raises:
            CartaInvalidaError: Se ``carta_nova`` não for ``CartaBaralho``.
        """
        if not isinstance(carta_nova, CartaBaralho):
            raise CartaInvalidaError("inserir_posicao espera CartaBaralho.")
        lista_passos: list[dict[str, Any]] = []
        numero_passo = 0

        if indice_posicao < 0 or indice_posicao > self.quantidade_elementos:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "VALIDAR 0 ≤ indice ≤ tamanho",
                    "descricao_acao": (
                        f"Índice {indice_posicao} fora do intervalo permitido "
                        f"(0..{self.quantidade_elementos})."
                    ),
                }
            )
            return {
                "operacao_nome": "inserir_posicao",
                "estrutura_tipo": "ListaLigadaCartas",
                "nome_estrutura": self.nome_lista,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": self.quantidade_elementos,
                "mensagem_erro": "indice invalido",
                "passos_executados": lista_passos,
            }

        if indice_posicao == self.quantidade_elementos:
            return self.inserir_final(carta_nova, registrar_passos=registrar_passos)

        no_novo = NoEncadeado(dados_carta=carta_nova)
        numero_passo += 1
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "nó_novo ← CriarNó(carta_nova)",
                    "descricao_acao": f"Preparar inserção de {carta_nova.texto_carta()}.",
                }
            )

        if indice_posicao == 0:
            numero_passo += 1
            assert self.cabeca_no is not None
            no_novo.proximo_no = self.cabeca_no
            self.cabeca_no.anterior_no = no_novo
            self.cabeca_no = no_novo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "nó_novo.próximo ← cabeça ; cabeça ← nó_novo",
                        "descricao_acao": "Inserir novo nó antes do antigo primeiro.",
                    }
                )
        else:
            no_anterior = self._no_indice(indice_posicao - 1)
            assert no_anterior is not None
            no_posterior = no_anterior.proximo_no
            numero_passo += 1
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "localizar nó no índice indice_posicao − 1",
                        "descricao_acao": (
                            f"Percorrer até o nó anterior à posição {indice_posicao}."
                        ),
                    }
                )
            no_novo.proximo_no = no_posterior
            no_novo.anterior_no = no_anterior
            no_anterior.proximo_no = no_novo
            if no_posterior is not None:
                no_posterior.anterior_no = no_novo
            if registrar_passos:
                numero_passo += 1
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": (
                            "encaixar nó_novo entre anterior e posterior"
                        ),
                        "descricao_acao": "Religar ponteiros duplos na posição desejada.",
                    }
                )

        numero_passo += 1
        self.quantidade_elementos += 1
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "quantidade_elementos ← quantidade_elementos + 1",
                    "descricao_acao": (
                        f"Tamanho da lista `{self.nome_lista}` = "
                        f"{self.quantidade_elementos}."
                    ),
                }
            )

        return {
            "operacao_nome": "inserir_posicao",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": self.nome_lista,
            "operacao_sucesso": True,
            "valor_retornado": None,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def remover_final(self, *, registrar_passos: bool = True) -> dict[str, Any]:
        """Remove o último nó e devolve a carta da antiga cauda.

        Args:
            registrar_passos: Se inclui narrativa passo a passo.

        Returns:
            Resultado-padrão com ``valor_retornado`` = ``CartaBaralho`` em sucesso.
        """
        lista_passos: list[dict[str, Any]] = []
        if self.cauda_no is None:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "SE cauda = NULO ENTÃO ERRO",
                    "descricao_acao": f"Lista `{self.nome_lista}` vazia.",
                }
            )
            return {
                "operacao_nome": "remover_final",
                "estrutura_tipo": "ListaLigadaCartas",
                "nome_estrutura": self.nome_lista,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": 0,
                "mensagem_erro": "lista vazia",
                "passos_executados": lista_passos,
            }

        carta_removida = self.cauda_no.dados_carta
        penultimo = self.cauda_no.anterior_no
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "carta ← cauda.dados_carta",
                    "descricao_acao": (
                        f"Última carta é {carta_removida.texto_carta()}."
                    ),
                }
            )

        if penultimo is None:
            self.cabeca_no = None
            self.cauda_no = None
        else:
            penultimo.proximo_no = None
            self.cauda_no = penultimo

        self.quantidade_elementos -= 1
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 2,
                    "pseudo_codigo": "remover cauda e atualizar penúltimo",
                    "descricao_acao": "Desencadear último nó e atualizar ponteiro cauda.",
                }
            )

        return {
            "operacao_nome": "remover_final",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": self.nome_lista,
            "operacao_sucesso": True,
            "valor_retornado": carta_removida,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def remover_a_partir_de(
        self,
        indice_inicio: int,
        *,
        registrar_passos: bool = True,
    ) -> dict[str, Any]:
        """Remove o sufixo a partir do índice base zero (inclusive).

        Args:
            indice_inicio: Primeira posição removida (0 = desde o início).
            registrar_passos: Controla narrativa detalhada.

        Returns:
            Dicionário com `valor_retornado` = lista de `CartaBaralho` removidas,
            na ordem de cima da mesa (início do sufixo até o final).
        """
        lista_passos: list[dict[str, Any]] = []
        if (
            indice_inicio < 0
            or indice_inicio >= self.quantidade_elementos
            or self.cabeca_no is None
        ):
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "VALIDAR índice e lista não vazia",
                    "descricao_acao": (
                        f"Índice {indice_inicio} inválido ou lista `{self.nome_lista}` vazia."
                    ),
                }
            )
            return {
                "operacao_nome": "remover_a_partir_de",
                "estrutura_tipo": "ListaLigadaCartas",
                "nome_estrutura": self.nome_lista,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": self.quantidade_elementos,
                "mensagem_erro": "indice invalido ou lista vazia",
                "passos_executados": lista_passos,
            }

        no_inicio = self._no_indice(indice_inicio)
        assert no_inicio is not None

        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "no_inicio ← nó no índice indice_inicio",
                    "descricao_acao": (
                        f"Início do sufixo: {no_inicio.dados_carta.texto_carta()} "
                        f"(índice {indice_inicio})."
                    ),
                }
            )

        cartas_removidas: list[CartaBaralho] = []
        no_atual: Optional[NoEncadeado] = no_inicio
        while no_atual is not None:
            cartas_removidas.append(no_atual.dados_carta)
            no_atual = no_atual.proximo_no

        no_anterior = no_inicio.anterior_no
        if no_anterior is None:
            self.cabeca_no = None
            self.cauda_no = None
        else:
            no_anterior.proximo_no = None
            self.cauda_no = no_anterior

        self.quantidade_elementos -= len(cartas_removidas)

        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 2,
                    "pseudo_codigo": (
                        "encerrar encadeamento antes do sufixo ; descartar sufixo"
                    ),
                    "descricao_acao": (
                        f"Removidas {len(cartas_removidas)} cartas do final "
                        f"visual da coluna `{self.nome_lista}`."
                    ),
                }
            )

        return {
            "operacao_nome": "remover_a_partir_de",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": self.nome_lista,
            "operacao_sucesso": True,
            "valor_retornado": cartas_removidas,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def obter_carta_posicao(
        self,
        indice_posicao: int,
        *,
        registrar_passos: bool = True,
    ) -> dict[str, Any]:
        """Retorna a carta no índice informado sem alterar a lista (acesso indexado).

        Args:
            indice_posicao: Posição base zero a partir da cabeça.
            registrar_passos: Se inclui passos de “percorrer” a lista.

        Returns:
            Resultado-padrão com ``valor_retornado`` = carta em sucesso.
        """
        lista_passos: list[dict[str, Any]] = []
        if indice_posicao < 0 or indice_posicao >= self.quantidade_elementos:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "VALIDAR índice",
                    "descricao_acao": "Índice fora do intervalo.",
                }
            )
            return {
                "operacao_nome": "obter_carta_posicao",
                "estrutura_tipo": "ListaLigadaCartas",
                "nome_estrutura": self.nome_lista,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": self.quantidade_elementos,
                "mensagem_erro": "indice invalido",
                "passos_executados": lista_passos,
            }

        no_atual = self.cabeca_no
        for passo_indice in range(indice_posicao):
            assert no_atual is not None
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": len(lista_passos) + 1,
                        "pseudo_codigo": "no_atual ← no_atual.próximo",
                        "descricao_acao": (
                            f"Sair do índice {passo_indice} "
                            f"(carta {no_atual.dados_carta.texto_carta()}), "
                            f"avançando em direção ao índice {indice_posicao}."
                        ),
                    }
                )
            no_atual = no_atual.proximo_no

        assert no_atual is not None
        carta_encontrada = no_atual.dados_carta
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": len(lista_passos) + 1,
                    "pseudo_codigo": "RETORNAR no_atual.dados_carta",
                    "descricao_acao": (
                        f"Carta no índice {indice_posicao}: {carta_encontrada.texto_carta()}."
                    ),
                }
            )

        return {
            "operacao_nome": "obter_carta_posicao",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": self.nome_lista,
            "operacao_sucesso": True,
            "valor_retornado": carta_encontrada,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def obter_ultima_carta(self, *, registrar_passos: bool = True) -> dict[str, Any]:
        """Retorna a carta da cauda sem remover (peek do fim da coluna).

        Args:
            registrar_passos: Se inclui passo didático.

        Returns:
            Resultado-padrão com ``valor_retornado`` em sucesso.
        """
        lista_passos: list[dict[str, Any]] = []
        if self.cauda_no is None:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "SE cauda = NULO ENTÃO",
                    "descricao_acao": "Lista vazia.",
                }
            )
            return {
                "operacao_nome": "obter_ultima_carta",
                "estrutura_tipo": "ListaLigadaCartas",
                "nome_estrutura": self.nome_lista,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": 0,
                "mensagem_erro": "lista vazia",
                "passos_executados": lista_passos,
            }

        ultima_carta = self.cauda_no.dados_carta
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "RETORNAR cauda.dados_carta",
                    "descricao_acao": (
                        f"Última carta da lista `{self.nome_lista}`: "
                        f"{ultima_carta.texto_carta()}."
                    ),
                }
            )

        return {
            "operacao_nome": "obter_ultima_carta",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": self.nome_lista,
            "operacao_sucesso": True,
            "valor_retornado": ultima_carta,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def buscar_carta(
        self,
        *,
        numero_carta: Optional[int] = None,
        naipe_carta: Optional[str] = None,
        registrar_passos: bool = True,
    ) -> dict[str, Any]:
        """Percorre a lista e devolve o primeiro índice que satisfaz os critérios.

        Pelo menos um dentre ``numero_carta`` ou ``naipe_carta`` deve ser informado.
        Se ambos forem informados, exige coincidência nos dois campos.

        Args:
            numero_carta: Valor 1..13 opcional.
            naipe_carta: Letra do naipe opcional.
            registrar_passos: Se inclui narrativa da busca linear.

        Returns:
            Resultado-padrão com ``valor_retornado`` = índice (int) ou ``-1``.
        """
        lista_passos: list[dict[str, Any]] = []
        if numero_carta is None and naipe_carta is None:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "VALIDAR critérios de busca",
                    "descricao_acao": "Informe numero_carta e/ou naipe_carta.",
                }
            )
            return {
                "operacao_nome": "buscar_carta",
                "estrutura_tipo": "ListaLigadaCartas",
                "nome_estrutura": self.nome_lista,
                "operacao_sucesso": False,
                "valor_retornado": -1,
                "quantidade_elementos": self.quantidade_elementos,
                "mensagem_erro": "criterios ausentes",
                "passos_executados": lista_passos,
            }

        no_atual = self.cabeca_no
        indice_atual = 0
        while no_atual is not None:
            dados = no_atual.dados_carta
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": len(lista_passos) + 1,
                        "pseudo_codigo": "VISITAR no_atual ; COMPARAR critérios",
                        "descricao_acao": (
                            f"Índice {indice_atual}: {dados.texto_carta()}."
                        ),
                    }
                )

            corresponde_numero = (
                numero_carta is None or dados.numero_carta == numero_carta
            )
            naipe_cmp = naipe_carta.lower().strip() if naipe_carta else None
            corresponde_naipe = (
                naipe_cmp is None or dados.naipe_carta == naipe_cmp
            )
            if corresponde_numero and corresponde_naipe:
                return {
                    "operacao_nome": "buscar_carta",
                    "estrutura_tipo": "ListaLigadaCartas",
                    "nome_estrutura": self.nome_lista,
                    "operacao_sucesso": True,
                    "valor_retornado": indice_atual,
                    "quantidade_elementos": self.quantidade_elementos,
                    "passos_executados": lista_passos,
                }

            no_atual = no_atual.proximo_no
            indice_atual += 1

        lista_passos.append(
            {
                "passo_numero": len(lista_passos) + 1,
                "pseudo_codigo": "RETORNAR −1 ; não encontrado",
                "descricao_acao": "Percorreu toda a lista sem encontrar.",
            }
        )
        return {
            "operacao_nome": "buscar_carta",
            "estrutura_tipo": "ListaLigadaCartas",
            "nome_estrutura": self.nome_lista,
            "operacao_sucesso": True,
            "valor_retornado": -1,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }
