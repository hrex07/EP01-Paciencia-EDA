## Context

O jogo de Paciência clássico (Solitaire) possui uma regra estrita de que no Tableau (neste projeto, implementado pelas 7 Listas Ligadas), uma carta só pode ser empilhada sobre outra se possuir um número imediatamente inferior e a cor do naipe for diferente (vermelha sobre preta, preta sobre vermelha). 
Atualmente, o usuário reportou que ao tentar colocar uma Dama Vermelha (Q♥) sobre um Rei Preto (K♣), o backend rejeita a ação enviando a mensagem `Jogada inválida: As cores devem ser alternadas (preto/vermelho).`. Isso evidencia que a função de validação das regras em `regras_movimento.py` está com sua lógica invertida ao realizar a comparação de cores, barrando cores diferentes em vez de barrar cores iguais.

## Goals / Non-Goals

**Goals:**
- Corrigir a lógica de comparação em `motor/regras_movimento.py` na validação de movimentos direcionados para as listas do tableau.
- Garantir que a comparação correta seja `carta_origem.cor_carta() != carta_destino.cor_carta()`.

**Non-Goals:**
- Modificar o fluxo de distribuição inicial das cartas ou demais movimentos válidos do jogo que não envolvem as colunas do tableau.
- Modificar os logs educacionais das Estruturas de Dados gerados durante os testes.

## Decisions

**1. Correção Condicional Simples**
O arquivo alvo é `motor/regras_movimento.py`. Iremos corrigir a condicional `_validar_pode_listar`.
*Rationale:* A função `_validar_pode_listar` é a função central que é reaproveitada nas movimentações `Fila → Lista`, `Pilha → Lista` e `Lista → Lista`. O erro foi apenas uma inversão relacional (`==` ao invés de `!=`).

```ascii
[Motor do Jogo]
      |
      v
[regras_movimento.py] -> def _validar_pode_listar(origem, destino)
                            |
                            v
[Lógica de Cor] --------> IF origem.cor_carta() == destino.cor_carta() -> INVALIIDO
                            (Impede que copas caia sobre ouros, ou paus sobre espadas)
```

## Risks / Trade-offs

- **[Risco]** A regressão na lógica principal do jogo pode quebrar testes automatizados que foram inadvertidamente desenhados para aceitar a lógica invertida anterior.
- **Mitigação:** Vamos analisar o `teste_jogo.py` durante a implementação para garantir que, caso houvessem testes validando a cor "igual", eles sejam reescritos corretamente.