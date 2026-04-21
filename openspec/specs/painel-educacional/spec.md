## ADDED Requirements

### Requirement: Visualizador da estrutura de dados ativa

O painel educacional DEVE exibir um diagrama visual da estrutura de dados que está sendo manipulada na jogada atual. Para Pilha: representação vertical com topo destacado. Para Fila: representação horizontal com frente e final. Para Lista Ligada: representação com nós e setas de ligação. O diagrama DEVE animar as transições (inserção, remoção, busca) em sincronização com os passos do log.

#### Scenario: Visualizar Pilha durante push
- **WHEN** uma jogada envolve `empilhar` em uma pilha
- **THEN** o visualizador DEVE mostrar a pilha vertical com o novo elemento aparecendo no topo com animação de entrada

#### Scenario: Visualizar Fila durante dequeue
- **WHEN** uma jogada envolve `desenfileirar` da fila
- **THEN** o visualizador DEVE mostrar a fila horizontal com o elemento da frente saindo com animação e os demais deslocando-se

#### Scenario: Visualizar Lista Ligada durante inserção
- **WHEN** uma jogada envolve `inserir_final` em uma lista ligada
- **THEN** o visualizador DEVE mostrar os nós com setas, com o novo nó aparecendo no final e as setas de ligação sendo animadas

#### Scenario: Múltiplas operações na mesma jogada
- **WHEN** uma jogada envolve desenfileirar da fila E inserir na lista (2 operações)
- **THEN** o visualizador DEVE mostrar as operações em sequência, atualizando o diagrama para cada estrutura envolvida

### Requirement: Pseudocódigo com highlight da linha executada

O painel educacional DEVE exibir o pseudocódigo em português da operação sendo executada, com destaque visual (highlight) na linha correspondente ao passo atual. O estudante DEVE poder avançar manualmente passo a passo ou deixar avançar automaticamente.

#### Scenario: Highlight sincronizado com passo
- **WHEN** o passo 3 de uma operação de empilhar está ativo
- **THEN** a linha 3 do pseudocódigo DEVE estar destacada (fundo colorido) e as linhas anteriores DEVEM ter indicação visual de "já executadas"

#### Scenario: Controles de passo a passo
- **WHEN** o estudante está visualizando os passos
- **THEN** DEVE haver botões de "Anterior", "Próximo", "Play/Pause" e um slider de velocidade

#### Scenario: Descrição do passo
- **WHEN** um passo está ativo no pseudocódigo
- **THEN** abaixo do pseudocódigo DEVE aparecer a `descricao_acao` daquele passo com valores concretos (ex: "K♠ agora aponta para Q♠")

### Requirement: Log de operações com histórico

O painel educacional DEVE exibir um log cronológico de todas as operações realizadas durante a partida. Cada entrada DEVE mostrar timestamp, nome da operação, estrutura envolvida e resultado. O log DEVE ser filtrável por tipo de estrutura e scrollável.

#### Scenario: Registrar operação no log
- **WHEN** uma jogada é executada
- **THEN** todas as operações envolvidas DEVEM aparecer no log com formato legível (ex: "[14:30:05] empilhar(pilha_espadas, K♠) → sucesso")

#### Scenario: Filtrar log por estrutura
- **WHEN** o estudante seleciona filtro "Pilha"
- **THEN** o log DEVE mostrar apenas operações relacionadas às pilhas

#### Scenario: Expandir detalhes de uma operação
- **WHEN** o estudante clica em uma entrada do log
- **THEN** DEVE expandir mostrando os passos detalhados daquela operação com pseudocódigo

### Requirement: Modo demonstração de algoritmos de ordenação

O painel educacional DEVE oferecer um modo separado onde o estudante pode selecionar algoritmos de ordenação (bubble, merge, quick), executá-los sobre um baralho embaralhado, visualizar a execução passo a passo e comparar métricas de performance entre eles.

#### Scenario: Executar demonstração de Bubble Sort
- **WHEN** o estudante seleciona "Bubble Sort" e clica "Executar"
- **THEN** DEVE chamar o endpoint de ordenação e exibir a animação do vetor sendo ordenado, com destaque nos elementos sendo comparados e trocados

#### Scenario: Comparar algoritmos lado a lado
- **WHEN** o estudante seleciona múltiplos algoritmos e clica "Comparar"
- **THEN** DEVE exibir uma tabela com `total_comparacoes`, `total_trocas` e `tempo_execucao_ms` de cada algoritmo

#### Scenario: Links para recursos educacionais
- **WHEN** o estudante está no modo demonstração de um algoritmo
- **THEN** DEVE haver links para recursos externos de visualização (ex: VisuAlgo, GeeksforGeeks) quando disponíveis

### Requirement: Indicador de estrutura de dados em uso

O painel educacional DEVE exibir um indicador permanente mostrando quais estruturas de dados estão ativas no jogo com suas quantidades: "Fila: 1 (24 cartas)", "Pilhas: 4 (K♠, 5♥, ...)", "Listas: 7". Ao clicar em qualquer estrutura, o visualizador DEVE focar nela.

#### Scenario: Exibir resumo das estruturas
- **WHEN** o painel educacional está visível
- **THEN** DEVE mostrar um resumo com ícones para cada tipo de ED, a quantidade de instâncias e o número total de cartas em cada tipo

#### Scenario: Clicar para inspecionar estrutura
- **WHEN** o estudante clica no indicador "Pilha Espadas (5 cartas)"
- **THEN** o visualizador DEVE mostrar o diagrama detalhado daquela pilha com todas as suas cartas
