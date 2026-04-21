## ADDED Requirements

### Requirement: Estado do jogo encapsula toda a partida

O sistema DEVE possuir uma classe `EstadoJogo` que contém: 1 instância de `FilaCartas` (monte de compra), 4 instâncias de `PilhaCartas` (fundações, uma por naipe), 7 instâncias de `ListaLigadaCartas` (tableau), `sequencia_atual` (int, streak de jogadas válidas), `maior_sequencia` (int), `total_jogadas` (int), `id_sessao` (str, UUID) e `jogo_vencido` (bool).

#### Scenario: Criar novo estado de jogo
- **WHEN** um novo jogo é criado
- **THEN** DEVE conter 1 fila, 4 pilhas nomeadas por naipe, 7 listas ligadas nomeadas de 1 a 7, contadores zerados e `jogo_vencido=False`

#### Scenario: Serializar estado para JSON
- **WHEN** o estado é serializado
- **THEN** DEVE produzir um JSON contendo a representação de todas as estruturas, com cartas visíveis (status_carta=True) e cartas ocultas representadas como "virada para baixo"

### Requirement: Distribuição inicial segue padrão clássico do Solitaire

O sistema DEVE distribuir as cartas nas 7 listas ligadas seguindo o padrão: Lista 1 recebe 1 carta, Lista 2 recebe 2, Lista 3 recebe 3... Lista 7 recebe 7 (total 28 cartas). Em cada lista, apenas a última carta DEVE ter `status_carta=True` (virada para cima); as demais ficam com `status_carta=False`. As 24 cartas restantes DEVEM ser enfileiradas na fila. A distribuição completa DEVE gerar um log narrando cada operação de inserção.

#### Scenario: Distribuição nas listas ligadas
- **WHEN** um novo jogo é criado com baralho embaralhado
- **THEN** a Lista 1 DEVE ter 1 carta (virada para cima), a Lista 2 DEVE ter 2 cartas (1 virada para baixo, 1 para cima), e assim até a Lista 7 com 7 cartas (6 para baixo, 1 para cima)

#### Scenario: Cartas restantes na fila
- **WHEN** a distribuição nas listas é concluída
- **THEN** a fila DEVE conter exatamente 24 cartas

#### Scenario: Log da distribuição
- **WHEN** a distribuição é executada com log habilitado
- **THEN** DEVE gerar um log com todas as operações de `inserir_final` nas listas e `enfileirar` na fila, totalizando 52 operações narradas

### Requirement: Validação de movimento da Fila para Pilha (M1 adaptado)

O sistema DEVE verificar se a carta da frente da fila pode ser empilhada em uma das 4 pilhas. A regra é: a pilha está vazia e a carta é um Ás (numero_carta=1) do naipe correspondente, OU a carta é do mesmo naipe da pilha e seu número é exatamente 1 a mais que o topo da pilha.

#### Scenario: Empilhar Ás em pilha vazia
- **WHEN** a carta da frente da fila é A♠ e a pilha de espadas está vazia
- **THEN** a validação DEVE retornar `True`

#### Scenario: Empilhar carta em sequência
- **WHEN** a carta da frente da fila é 5♥ e o topo da pilha de copas é 4♥
- **THEN** a validação DEVE retornar `True`

#### Scenario: Rejeitar carta fora de sequência
- **WHEN** a carta da frente da fila é 7♦ e o topo da pilha de ouros é 5♦
- **THEN** a validação DEVE retornar `False` com mensagem explicativa no log

#### Scenario: Rejeitar naipe diferente
- **WHEN** a carta da frente da fila é 2♣ e a pilha é de espadas
- **THEN** a validação DEVE retornar `False`

### Requirement: Validação de movimento da Fila para Lista Ligada (M1)

O sistema DEVE verificar se a carta da frente da fila pode ser inserida no final de uma lista ligada. A regra é: a lista está vazia e a carta é um Rei (numero_carta=13), OU a carta tem cor diferente da última carta da lista e número exatamente 1 a menos.

#### Scenario: Inserir Rei em lista vazia
- **WHEN** a carta da frente da fila é K♠ e a lista está vazia
- **THEN** a validação DEVE retornar `True`

#### Scenario: Inserir carta com cor alternada e ordem decrescente
- **WHEN** a carta da frente da fila é 5♥ (vermelha) e a última carta da lista é 6♠ (preta)
- **THEN** a validação DEVE retornar `True`

#### Scenario: Rejeitar mesma cor
- **WHEN** a carta da frente da fila é 5♥ (vermelha) e a última carta da lista é 6♦ (vermelha)
- **THEN** a validação DEVE retornar `False`

### Requirement: Validação de movimento de Pilha para Lista Ligada (M2)

O sistema DEVE verificar se a carta do topo de uma pilha pode ser inserida no final de uma lista ligada, seguindo as mesmas regras de cor alternada e ordem decrescente.

#### Scenario: Mover topo da pilha para lista
- **WHEN** o topo da pilha de espadas é 10♠ (preta) e a última carta da lista é J♥ (vermelha)
- **THEN** a validação DEVE retornar `True`

### Requirement: Validação de movimento de Lista Ligada para Pilha (inverso de M2)

O sistema DEVE verificar se a última carta de uma lista ligada pode ser empilhada em uma pilha, seguindo as regras da pilha (mesmo naipe, sequência crescente).

#### Scenario: Mover última carta da lista para pilha
- **WHEN** a última carta da lista é 3♦ e o topo da pilha de ouros é 2♦
- **THEN** a validação DEVE retornar `True`

#### Scenario: Virar carta após remoção
- **WHEN** a última carta visível de uma lista é removida e a carta abaixo tem `status_carta=False`
- **THEN** a carta abaixo DEVE ter `status_carta` atualizado para `True` (virar para cima)

### Requirement: Validação de movimento de Lista Ligada para Lista Ligada (M3)

O sistema DEVE verificar se uma carta em uma posição específica de uma lista ligada (e todas as cartas após ela) podem ser movidas para o final de outra lista. A carta na posição especificada DEVE ter `status_carta=True`, ter cor diferente da última carta da lista destino, e número exatamente 1 a menos.

#### Scenario: Mover sublista entre listas
- **WHEN** a lista origem tem [K♠, Q♥, J♠] e queremos mover Q♥ e J♠ para uma lista cuja última carta é K♦
- **THEN** a validação DEVE retornar `True` (Q♥ vermelha sobre K♦ vermelha? Não! K♦ é vermelha e Q♥ é vermelha → `False`)

#### Scenario: Mover sublista válida
- **WHEN** a lista origem tem [K♠, Q♥, J♠] e queremos mover Q♥ e J♠ para uma lista cuja última carta é K♣ (preta)
- **THEN** a validação DEVE retornar `True` (Q♥ vermelha sobre K♣ preta, 12 = 13-1)

### Requirement: Executar os 6 tipos de movimentação do EP01

O sistema DEVE implementar 6 tipos de movimento conforme o EP01: (1) Fila para Fila (reposicionar), (2) Fila para Pilha, (3) Fila para Lista Ligada, (4) Pilha para Lista Ligada, (5) Lista Ligada para Pilha, (6) Lista Ligada para Lista Ligada. Cada movimento DEVE: validar a jogada, executar as operações nas EDs, gerar log narrado completo e atualizar o contador de streak.

#### Scenario: Movimento válido gera log completo
- **WHEN** qualquer movimento válido é executado
- **THEN** DEVE retornar o novo estado do jogo, a lista de todas as `operacoes_realizadas` (com passos de cada ED envolvida) e o status atualizado do streak

#### Scenario: Movimento inválido zera o streak
- **WHEN** um movimento inválido é tentado
- **THEN** DEVE retornar `jogada_valida=False`, `sequencia_atual=0`, e mensagem explicando por que o movimento não é permitido

### Requirement: Detecção de vitória

O sistema DEVE detectar que o jogo foi vencido quando todas as 4 pilhas contêm 13 cartas cada (total de 52 cartas nas fundações).

#### Scenario: Jogo vencido
- **WHEN** a última carta é empilhada completando as 4 pilhas
- **THEN** `jogo_vencido` DEVE ser `True`, e o retorno DEVE incluir `nivel_efeito="vitoria"` com estatísticas finais (total de jogadas, maior sequência, tempo de jogo)

### Requirement: Sistema de streaks rastreia sequências de jogadas válidas

O backend DEVE manter contadores `sequencia_atual` e `maior_sequencia`. A cada jogada válida, `sequencia_atual` incrementa; a cada jogada inválida, zera. O backend DEVE retornar `nivel_efeito` mapeado conforme: 1="basico", 2="bom", 3="otimo", 5="confetti", 7="incrivel", 10+="mestre". DEVE incluir `mensagem_educacional` mencionando as EDs usadas na sequência.

#### Scenario: Streak incrementa em jogada válida
- **WHEN** o jogador faz 3 jogadas válidas consecutivas
- **THEN** `sequencia_atual` DEVE ser 3, `nivel_efeito` DEVE ser "otimo"

#### Scenario: Streak zera em jogada inválida
- **WHEN** o jogador tenta uma jogada inválida após streak de 5
- **THEN** `sequencia_atual` DEVE ser 0, `nivel_efeito` DEVE ser "erro", `maior_sequencia` DEVE permanecer 5

#### Scenario: Mensagem educacional contextualizada
- **WHEN** a streak atinge nível "confetti" e as últimas jogadas usaram Fila e Pilha
- **THEN** `mensagem_educacional` DEVE mencionar ambas as estruturas (ex: "5 movimentos usando Fila (FIFO) e Pilha (LIFO)!")
