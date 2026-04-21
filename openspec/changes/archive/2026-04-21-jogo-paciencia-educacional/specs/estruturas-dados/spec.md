## ADDED Requirements

### Requirement: Classe Carta representa uma carta do baralho

O sistema DEVE possuir uma classe `CartaBaralho` com os atributos: `numero_carta` (int, 1 a 13), `naipe_carta` (str, um de "c", "o", "p", "e" representando copas, ouros, paus, espadas), e `status_carta` (bool, indicando se está virada para cima). A classe DEVE possuir um método para representação textual legível (ex: "K♠", "A♥").

#### Scenario: Criar carta válida
- **WHEN** uma carta é criada com `numero_carta=13` e `naipe_carta="e"`
- **THEN** a carta DEVE ter `numero_carta=13`, `naipe_carta="e"`, `status_carta=False` por padrão, e representação textual "K♠"

#### Scenario: Identificar cor da carta
- **WHEN** a carta possui `naipe_carta="c"` ou `naipe_carta="o"`
- **THEN** o método `cor_carta` DEVE retornar `"vermelha"`

#### Scenario: Identificar cor preta
- **WHEN** a carta possui `naipe_carta="p"` ou `naipe_carta="e"`
- **THEN** o método `cor_carta` DEVE retornar `"preta"`

### Requirement: Classe Nó encapsula um elemento encadeado

O sistema DEVE possuir uma classe `NoEncadeado` com os atributos: `dados_carta` (instância de CartaBaralho), `proximo_no` (referência ao próximo nó ou None) e `anterior_no` (referência ao nó anterior ou None, para lista duplamente ligada).

#### Scenario: Criar nó com carta
- **WHEN** um nó é criado com uma carta `CartaBaralho(1, "e")`
- **THEN** o nó DEVE ter `dados_carta` apontando para a carta, `proximo_no=None` e `anterior_no=None`

### Requirement: Classe Pilha implementa estrutura LIFO com log narrado

O sistema DEVE possuir uma classe `PilhaCartas` implementada from scratch (sem uso de bibliotecas de estruturas prontas) usando nós encadeados. DEVE suportar as operações: `empilhar` (push), `desempilhar` (pop), `espiar_topo` (peek), `esta_vazia` (isEmpty) e `obter_tamanho` (size). Cada operação DEVE retornar um dicionário contendo o resultado da operação e uma lista de `passos_executados`, onde cada passo possui `passo_numero`, `pseudo_codigo` em português e `descricao_acao` contextualizada.

#### Scenario: Empilhar carta em pilha vazia
- **WHEN** `empilhar` é chamado com uma carta em uma pilha vazia
- **THEN** DEVE retornar `operacao_sucesso=True`, a pilha DEVE ter tamanho 1, e `passos_executados` DEVE conter pelo menos 3 passos com pseudocódigo em português

#### Scenario: Empilhar carta em pilha com elementos
- **WHEN** `empilhar` é chamado com uma carta em uma pilha que já contém elementos
- **THEN** a carta DEVE se tornar o novo topo, o tamanho DEVE incrementar, e o log DEVE descrever a ligação do novo nó ao topo anterior

#### Scenario: Desempilhar carta
- **WHEN** `desempilhar` é chamado em uma pilha com elementos
- **THEN** DEVE retornar a carta do topo, o tamanho DEVE decrementar, e o log DEVE descrever a remoção e atualização do topo

#### Scenario: Desempilhar pilha vazia
- **WHEN** `desempilhar` é chamado em uma pilha vazia
- **THEN** DEVE retornar `operacao_sucesso=False` com mensagem de erro no log

#### Scenario: Espiar topo sem remover
- **WHEN** `espiar_topo` é chamado em uma pilha com elementos
- **THEN** DEVE retornar a carta do topo sem alterá-la, e o tamanho DEVE permanecer inalterado

### Requirement: Classe Fila implementa estrutura FIFO com log narrado

O sistema DEVE possuir uma classe `FilaCartas` implementada from scratch usando nós encadeados. DEVE suportar as operações: `enfileirar` (enqueue), `desenfileirar` (dequeue), `espiar_frente` (peek), `esta_vazia` (isEmpty), `obter_tamanho` (size) e `reposicionar_frente` (mover a carta da frente para o final — operação "da Fila para a Fila" do EP01). Cada operação DEVE retornar resultado + `passos_executados` com pseudocódigo narrado.

#### Scenario: Enfileirar carta em fila vazia
- **WHEN** `enfileirar` é chamado com uma carta em uma fila vazia
- **THEN** a carta DEVE se tornar tanto a frente quanto o final da fila, tamanho DEVE ser 1, e o log DEVE descrever a criação do primeiro nó

#### Scenario: Desenfileirar carta
- **WHEN** `desenfileirar` é chamado em uma fila com elementos
- **THEN** DEVE retornar a carta da frente (FIFO), o tamanho DEVE decrementar, e o log DEVE descrever a remoção e atualização da frente

#### Scenario: Reposicionar frente para o final
- **WHEN** `reposicionar_frente` é chamado (operação "Fila para Fila")
- **THEN** a carta da frente DEVE ser movida para o final da fila, o tamanho DEVE permanecer inalterado, e o log DEVE descrever o desenfileirar seguido do enfileirar

#### Scenario: Desenfileirar fila vazia
- **WHEN** `desenfileirar` é chamado em uma fila vazia
- **THEN** DEVE retornar `operacao_sucesso=False` com mensagem de erro no log

### Requirement: Classe Lista Ligada implementa estrutura encadeada com log narrado

O sistema DEVE possuir uma classe `ListaLigadaCartas` implementada from scratch como lista duplamente ligada com nós encadeados. DEVE suportar as operações: `inserir_final` (append), `inserir_posicao` (insert at position), `remover_final` (remove last), `remover_a_partir_de` (remove sublist from position), `obter_carta_posicao` (get at index), `obter_ultima_carta` (get last), `esta_vazia`, `obter_tamanho` e `buscar_carta`. Cada operação DEVE retornar resultado + `passos_executados` com pseudocódigo narrado. A lista DEVE ter um atributo `nome_lista` para identificação (ex: "lista_ligada_1").

#### Scenario: Inserir carta no final de lista vazia
- **WHEN** `inserir_final` é chamado com uma carta em uma lista vazia
- **THEN** a carta DEVE se tornar o primeiro e único nó, tamanho DEVE ser 1, e o log DEVE descrever a criação do nó cabeça

#### Scenario: Inserir carta no final de lista com elementos
- **WHEN** `inserir_final` é chamado com uma carta em uma lista com elementos
- **THEN** a carta DEVE ser adicionada após o último nó, as referências `proximo_no` e `anterior_no` DEVEM ser atualizadas, e o log DEVE descrever a travessia e ligação

#### Scenario: Remover sublista a partir de posição
- **WHEN** `remover_a_partir_de` é chamado com posição 3 em uma lista de 6 elementos
- **THEN** DEVE retornar uma lista com os elementos das posições 3 a 5 (3 cartas), a lista original DEVE ter tamanho 3, e o log DEVE descrever o corte e religação dos nós

#### Scenario: Buscar carta na lista
- **WHEN** `buscar_carta` é chamado com critérios de busca
- **THEN** DEVE retornar a posição da carta se encontrada ou -1 se não encontrada, e o log DEVE descrever cada nó visitado durante a travessia

### Requirement: Vetor de 52 cartas como estrutura base

O sistema DEVE criar um vetor (lista Python) de 52 objetos `CartaBaralho`, representando um baralho completo com 4 naipes e 13 valores cada. A criação do vetor DEVE gerar um log descrevendo a inserção de cada carta.

#### Scenario: Criar baralho completo
- **WHEN** a função de criação do baralho é chamada
- **THEN** DEVE retornar uma lista com 52 cartas, contendo exatamente 13 cartas de cada naipe, com números de 1 a 13

#### Scenario: Log da criação do baralho
- **WHEN** o baralho é criado com log habilitado
- **THEN** o log DEVE conter 52 passos, cada um descrevendo a carta inserida e sua posição no vetor
