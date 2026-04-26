"""Pilha (LIFO) de cartas implementada com lista encadeada — topo aponta para o primeiro nó."""

from __future__ import annotations

from typing import Any, Optional

from modelo.carta_baralho import CartaBaralho
from modelo.excecao_carta import CartaInvalidaError
from modelo.no_encadeado import NoEncadeado


class PilhaCartas:
    """Pilha dinâmica: último a entrar é o primeiro a sair (LIFO).

    O ponteiro `elemento_topo` referencia o nó do topo; cada `proximo_no`
    aponta para o elemento abaixo na pilha.

    Attributes:
        nome_pilha: Identificador para logs didáticos.
        elemento_topo: Topo atual da pilha ou None se vazia.
        quantidade_elementos: Contador de cartas na pilha.
    """

    def __init__(self, nome_pilha: str = "pilha_sem_nome") -> None:
        """Inicializa pilha vazia.

        Args:
            nome_pilha: Nome mostrado nos relatórios e logs narrados.
        """
        self.nome_pilha = nome_pilha
        self.elemento_topo: Optional[NoEncadeado] = None
        self.quantidade_elementos = 0

    def esta_vazia(self) -> bool:
        """Verifica se não há elementos na pilha."""
        return self.elemento_topo is None

    def obter_tamanho(self) -> int:
        """Retorna número de cartas atualmente empilhadas."""
        return self.quantidade_elementos

    @staticmethod
    def desserializar(dados_lista: list[dict[str, Any]], nome_pilha: str) -> PilhaCartas:
        """Recria uma instância de PilhaCartas a partir de uma lista de dicionários de cartas."""
        pilha = PilhaCartas(nome_pilha=nome_pilha)
        for d_carta in dados_lista:
            carta = CartaBaralho.desserializar(d_carta)
            pilha.empilhar(carta, registrar_passos=False)
        return pilha

    def empilhar(
        self,
        carta_nova: CartaBaralho,
        *,
        registrar_passos: bool = True,
    ) -> dict[str, Any]:
        """Empilha uma carta no topo (push).

        Pseudocódigo de referência (cada linha vira um passo no log):
        PROCEDIMENTO Empilhar(carta_nova)
        | INÍCIO
        |   nó_novo ← CriarNó(carta_nova)
        |   SE pilha.topo = NULO ENTÃO
        |       pilha.topo ← nó_novo
        |   SENÃO
        |       nó_novo.próximo ← pilha.topo
        |       pilha.topo ← nó_novo
        |   FIM SE
        |   pilha.tamanho ← pilha.tamanho + 1
        | FIM

        Args:
            carta_nova: Carta a ser colocada no topo.
            registrar_passos: Se False, não monta lista detalhada de passos.

        Returns:
            Dicionário com `operacao_sucesso`, `passos_executados`,
            `quantidade_elementos` e serialização opcional da pilha.

        Raises:
            CartaInvalidaError: Se `carta_nova` não for instância válida.
        """
        if not isinstance(carta_nova, CartaBaralho):
            raise CartaInvalidaError("empilhar espera instância de CartaBaralho.")
        lista_passos: list[dict[str, Any]] = []
        numero_passo = 0

        # nó_novo ← CriarNó(carta_nova)
        numero_passo += 1
        no_novo = NoEncadeado(dados_carta=carta_nova)
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "nó_novo ← CriarNó(carta_nova)",
                    "descricao_acao": (
                        f"Alocar nó com a carta {carta_nova.texto_carta()}."
                    ),
                }
            )

        if self.elemento_topo is None:
            numero_passo += 1
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "SE elemento_topo = NULO ENTÃO",
                        "descricao_acao": "Pilha vazia: novo nó será o único elemento.",
                    }
                )
            numero_passo += 1
            self.elemento_topo = no_novo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "elemento_topo ← nó_novo",
                        "descricao_acao": (
                            f"Topo `{self.nome_pilha}` aponta para {carta_nova.texto_carta()}."
                        ),
                    }
                )
        else:
            numero_passo += 1
            topo_anterior = self.elemento_topo.dados_carta.texto_carta()
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "SE elemento_topo = NULO ENTÃO ... SENÃO",
                        "descricao_acao": (
                            f"Pilha não vazia; topo atual é {topo_anterior}."
                        ),
                    }
                )
            numero_passo += 1
            no_novo.proximo_no = self.elemento_topo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "nó_novo.próximo ← elemento_topo",
                        "descricao_acao": (
                            f"Encadear {carta_nova.texto_carta()} acima de {topo_anterior}."
                        ),
                    }
                )
            numero_passo += 1
            self.elemento_topo = no_novo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "elemento_topo ← nó_novo",
                        "descricao_acao": (
                            f"Atualizar topo `{self.nome_pilha}` para {carta_nova.texto_carta()}."
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
                        f"Tamanho da pilha `{self.nome_pilha}` agora é "
                        f"{self.quantidade_elementos}."
                    ),
                }
            )

        return {
            "operacao_nome": "empilhar",
            "estrutura_tipo": "PilhaCartas",
            "nome_estrutura": self.nome_pilha,
            "operacao_sucesso": True,
            "valor_retornado": None,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def desempilhar(self, *, registrar_passos: bool = True) -> dict[str, Any]:
        """Remove e retorna a carta do topo (pop)."""
        lista_passos: list[dict[str, Any]] = []
        numero_passo = 0

        if self.elemento_topo is None:
            numero_passo += 1
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "SE elemento_topo = NULO ENTÃO ERRO",
                    "descricao_acao": (
                        f"Não é possível desempilhar: pilha `{self.nome_pilha}` está vazia."
                    ),
                }
            )
            return {
                "operacao_nome": "desempilhar",
                "estrutura_tipo": "PilhaCartas",
                "nome_estrutura": self.nome_pilha,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": self.quantidade_elementos,
                "mensagem_erro": "pilha vazia",
                "passos_executados": lista_passos,
            }

        numero_passo += 1
        carta_topo = self.elemento_topo.dados_carta
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "carta_topo ← elemento_topo.dados_carta",
                    "descricao_acao": (
                        f"Ler carta do topo: {carta_topo.texto_carta()}."
                    ),
                }
            )

        numero_passo += 1
        no_removido = self.elemento_topo
        self.elemento_topo = no_removido.proximo_no
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "elemento_topo ← elemento_topo.próximo",
                    "descricao_acao": (
                        "Avançar topo para o próximo nó encadeado (desempilhar)."
                    ),
                }
            )

        numero_passo += 1
        self.quantidade_elementos -= 1
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "quantidade_elementos ← quantidade_elementos − 1",
                    "descricao_acao": (
                        f"Tamanho da pilha `{self.nome_pilha}` agora é "
                        f"{self.quantidade_elementos}."
                    ),
                }
            )

        return {
            "operacao_nome": "desempilhar",
            "estrutura_tipo": "PilhaCartas",
            "nome_estrutura": self.nome_pilha,
            "operacao_sucesso": True,
            "valor_retornado": carta_topo,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def espiar_topo(self, *, registrar_passos: bool = True) -> dict[str, Any]:
        """Retorna o topo sem remover (peek)."""
        lista_passos: list[dict[str, Any]] = []
        numero_passo = 0

        if self.elemento_topo is None:
            numero_passo += 1
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "SE elemento_topo = NULO ENTÃO",
                    "descricao_acao": "Não há topo em pilha vazia.",
                }
            )
            return {
                "operacao_nome": "espiar_topo",
                "estrutura_tipo": "PilhaCartas",
                "nome_estrutura": self.nome_pilha,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": 0,
                "mensagem_erro": "pilha vazia",
                "passos_executados": lista_passos,
            }

        numero_passo += 1
        carta_topo = self.elemento_topo.dados_carta
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "RETORNAR elemento_topo.dados_carta SEM ALTERAR PILHA",
                    "descricao_acao": (
                        f"Topo atual é {carta_topo.texto_carta()} (somente leitura)."
                    ),
                }
            )

        return {
            "operacao_nome": "espiar_topo",
            "estrutura_tipo": "PilhaCartas",
            "nome_estrutura": self.nome_pilha,
            "operacao_sucesso": True,
            "valor_retornado": carta_topo,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }
