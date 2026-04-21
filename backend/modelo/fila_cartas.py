"""Fila (FIFO) de cartas com ponteiros para frente e final da lista encadeada."""

from __future__ import annotations

from typing import Any, Optional

from modelo.carta_baralho import CartaBaralho
from modelo.excecao_carta import CartaInvalidaError
from modelo.no_encadeado import NoEncadeado


class FilaCartas:
    """Fila dinâmica: primeiro a entrar é o primeiro a sair (FIFO).

    Attributes:
        nome_fila: Identificador para logs didáticos.
        no_frente: Primeiro nó da fila (saída) ou None.
        no_final: Último nó da fila (entrada) ou None.
        quantidade_elementos: Contador de cartas na fila.
    """

    def __init__(self, nome_fila: str = "fila_sem_nome") -> None:
        """Inicializa fila vazia.

        Args:
            nome_fila: Nome usado nos relatórios e logs narrados.
        """
        self.nome_fila = nome_fila
        self.no_frente: Optional[NoEncadeado] = None
        self.no_final: Optional[NoEncadeado] = None
        self.quantidade_elementos = 0

    def esta_vazia(self) -> bool:
        """Verifica se a fila não possui elementos."""
        return self.no_frente is None

    def obter_tamanho(self) -> int:
        """Retorna quantidade de cartas enfileiradas."""
        return self.quantidade_elementos

    def enfileirar(
        self,
        carta_nova: CartaBaralho,
        *,
        registrar_passos: bool = True,
    ) -> dict[str, Any]:
        """Insere carta no final da fila (enqueue).

        Args:
            carta_nova: Carta a enfileirar.
            registrar_passos: Controla geração do log detalhado.

        Returns:
            Resultado padronizado com `passos_executados`.

        Raises:
            CartaInvalidaError: Se `carta_nova` não for `CartaBaralho`.
        """
        if not isinstance(carta_nova, CartaBaralho):
            raise CartaInvalidaError("enfileirar espera instância de CartaBaralho.")
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
                        f"Criar nó para enfileirar {carta_nova.texto_carta()}."
                    ),
                }
            )

        if self.no_final is None:
            numero_passo += 1
            self.no_frente = no_novo
            self.no_final = no_novo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": "SE fila vazia ENTÃO frente ← final ← nó_novo",
                        "descricao_acao": (
                            f"Primeira carta da fila `{self.nome_fila}`: "
                            f"{carta_nova.texto_carta()}."
                        ),
                    }
                )
        else:
            numero_passo += 1
            no_novo.anterior_no = self.no_final
            self.no_final.proximo_no = no_novo
            self.no_final = no_novo
            if registrar_passos:
                lista_passos.append(
                    {
                        "passo_numero": numero_passo,
                        "pseudo_codigo": (
                            "final.próximo ← nó_novo ; final ← nó_novo"
                        ),
                        "descricao_acao": (
                            f"Encadear {carta_nova.texto_carta()} após o antigo final."
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
                        f"Tamanho da fila `{self.nome_fila}` = "
                        f"{self.quantidade_elementos}."
                    ),
                }
            )

        return {
            "operacao_nome": "enfileirar",
            "estrutura_tipo": "FilaCartas",
            "nome_estrutura": self.nome_fila,
            "operacao_sucesso": True,
            "valor_retornado": None,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def desenfileirar(self, *, registrar_passos: bool = True) -> dict[str, Any]:
        """Remove carta da frente da fila (dequeue)."""
        lista_passos: list[dict[str, Any]] = []
        numero_passo = 0

        if self.no_frente is None:
            numero_passo += 1
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "SE frente = NULO ENTÃO ERRO",
                    "descricao_acao": (
                        f"Fila `{self.nome_fila}` vazia: não há elemento para remover."
                    ),
                }
            )
            return {
                "operacao_nome": "desenfileirar",
                "estrutura_tipo": "FilaCartas",
                "nome_estrutura": self.nome_fila,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": self.quantidade_elementos,
                "mensagem_erro": "fila vazia",
                "passos_executados": lista_passos,
            }

        numero_passo += 1
        carta_removida = self.no_frente.dados_carta
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "carta ← frente.dados_carta",
                    "descricao_acao": (
                        f"Carta da frente será {carta_removida.texto_carta()}."
                    ),
                }
            )

        numero_passo += 1
        novo_frente = self.no_frente.proximo_no
        if novo_frente is not None:
            novo_frente.anterior_no = None
        else:
            self.no_final = None
        self.no_frente = novo_frente
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": numero_passo,
                    "pseudo_codigo": "frente ← frente.próximo ; ajustar encadeamento",
                    "descricao_acao": "Remover nó da frente e religar sucessor.",
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
                        f"Tamanho da fila `{self.nome_fila}` = "
                        f"{self.quantidade_elementos}."
                    ),
                }
            )

        return {
            "operacao_nome": "desenfileirar",
            "estrutura_tipo": "FilaCartas",
            "nome_estrutura": self.nome_fila,
            "operacao_sucesso": True,
            "valor_retornado": carta_removida,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def espiar_frente(self, *, registrar_passos: bool = True) -> dict[str, Any]:
        """Consulta a carta da frente sem remover (peek)."""
        lista_passos: list[dict[str, Any]] = []
        if self.no_frente is None:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "SE frente = NULO ENTÃO",
                    "descricao_acao": "Fila vazia: não há frente.",
                }
            )
            return {
                "operacao_nome": "espiar_frente",
                "estrutura_tipo": "FilaCartas",
                "nome_estrutura": self.nome_fila,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": 0,
                "mensagem_erro": "fila vazia",
                "passos_executados": lista_passos,
            }

        carta_frente = self.no_frente.dados_carta
        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 1,
                    "pseudo_codigo": "RETORNAR frente.dados_carta",
                    "descricao_acao": (
                        f"Frente da fila `{self.nome_fila}`: {carta_frente.texto_carta()}."
                    ),
                }
            )

        return {
            "operacao_nome": "espiar_frente",
            "estrutura_tipo": "FilaCartas",
            "nome_estrutura": self.nome_fila,
            "operacao_sucesso": True,
            "valor_retornado": carta_frente,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": lista_passos,
        }

    def reposicionar_frente(self, *, registrar_passos: bool = True) -> dict[str, Any]:
        """Move a carta da frente para o final (rotação da fila).

        Equivalente conceitual a desenfileirar seguido de enfileirar a mesma carta,
        único para o EP01 opção «da Fila para a Fila».

        Args:
            registrar_passos: Se inclui narrativa passo a passo.

        Returns:
            Resultado acumulado com `passos_executados` de toda a rotação.
        """
        lista_passos: list[dict[str, Any]] = []

        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 0,
                    "pseudo_codigo": "PROCEDIMENTO ReposicionarFrente",
                    "descricao_acao": (
                        "Início: mover frente para o final mantendo FIFO relativo "
                        "aos demais elementos."
                    ),
                }
            )

        resultado_saida = self.desenfileirar(registrar_passos=registrar_passos)
        lista_passos.extend(resultado_saida["passos_executados"])

        if not resultado_saida["operacao_sucesso"]:
            lista_renumerada = _renumerar_passos(lista_passos)
            return {
                "operacao_nome": "reposicionar_frente",
                "estrutura_tipo": "FilaCartas",
                "nome_estrutura": self.nome_fila,
                "operacao_sucesso": False,
                "valor_retornado": None,
                "quantidade_elementos": self.quantidade_elementos,
                "mensagem_erro": resultado_saida.get("mensagem_erro"),
                "passos_executados": lista_renumerada,
            }

        carta_rotacao = resultado_saida["valor_retornado"]
        assert carta_rotacao is not None

        resultado_entrada = self.enfileirar(
            carta_rotacao, registrar_passos=registrar_passos
        )
        lista_passos.extend(resultado_entrada["passos_executados"])

        if registrar_passos:
            lista_passos.append(
                {
                    "passo_numero": 0,
                    "pseudo_codigo": "FIM ReposicionarFrente",
                    "descricao_acao": (
                        f"Carta {carta_rotacao.texto_carta()} passou da frente para "
                        "o final da fila."
                    ),
                }
            )

        return {
            "operacao_nome": "reposicionar_frente",
            "estrutura_tipo": "FilaCartas",
            "nome_estrutura": self.nome_fila,
            "operacao_sucesso": True,
            "valor_retornado": carta_rotacao,
            "quantidade_elementos": self.quantidade_elementos,
            "passos_executados": _renumerar_passos(lista_passos),
        }


def _renumerar_passos(lista_passos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Atribui passo_numero sequencial a partir de 1."""
    resultado: list[dict[str, Any]] = []
    for indice, passo in enumerate(lista_passos, start=1):
        copia = dict(passo)
        copia["passo_numero"] = indice
        resultado.append(copia)
    return resultado
