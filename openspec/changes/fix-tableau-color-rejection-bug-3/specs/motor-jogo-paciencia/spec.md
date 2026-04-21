## MODIFIED Requirements

### Requirement: Validação de movimento da Fila para Lista Ligada (M1)

O sistema DEVE verificar se a carta da frente da fila pode ser inserida no final de uma lista ligada. A regra é: a lista está vazia e a carta é um Rei (numero_carta=13), OU a carta tem cor diferente da última carta da lista e número exatamente 1 a menos. A verificação de cor DEVE garantir que a jogada só prossiga se a cor da carta de origem for de fato diferente da carta de destino.

#### Scenario: Inserir Rei em lista vazia
- **WHEN** a carta da frente da fila é K♠ e a lista está vazia
- **THEN** a validação DEVE retornar `True`

#### Scenario: Inserir carta com cor alternada e ordem decrescente
- **WHEN** a carta da frente da fila é 5♥ (vermelha) e a última carta da lista é 6♠ (preta)
- **THEN** a validação DEVE retornar `True`

#### Scenario: Rejeitar mesma cor
- **WHEN** a carta da frente da fila é 5♥ (vermelha) e a última carta da lista é 6♦ (vermelha)
- **THEN** a validação DEVE retornar `False`

### Requirement: Validação de movimento de Lista Ligada para Lista Ligada (M3)

O sistema DEVE verificar se uma carta em uma posição específica de uma lista ligada (e todas as cartas após ela) podem ser movidas para o final de outra lista. A carta na posição especificada DEVE ter `status_carta=True`, ter cor diferente da última carta da lista destino, e número exatamente 1 a menos. A validação de cor DEVE garantir que cartas com cores distintas (vermelho sobre preto ou preto sobre vermelho) sejam aceitas, enquanto cores idênticas sejam rejeitadas.

#### Scenario: Mover sublista entre listas com cores iguais (Inválido)
- **WHEN** a lista origem tem [K♠, Q♥, J♠] e queremos mover Q♥ e J♠ para uma lista cuja última carta é K♦
- **THEN** a validação DEVE retornar `False` (Q♥ vermelha sobre K♦ vermelha é inválido)

#### Scenario: Mover sublista válida
- **WHEN** a lista origem tem [K♠, Q♥, J♠] e queremos mover Q♥ e J♠ para uma lista cuja última carta é K♣ (preta)
- **THEN** a validação DEVE retornar `True` (Q♥ vermelha sobre K♣ preta, 12 = 13-1)
