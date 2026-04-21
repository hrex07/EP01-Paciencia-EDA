## ADDED Requirements

### Requirement: Embaralhamento iterativo do vetor de cartas

O sistema DEVE implementar uma função `embaralhar_iterativo` que recebe um vetor de cartas e o embaralha trocando cartas em posições aleatórias 1000 vezes (conforme EP01). DEVE retornar o vetor embaralhado + log narrado com pseudocódigo de cada troca, incluindo as posições e cartas envolvidas. DEVE registrar o total de trocas e o tempo de execução.

#### Scenario: Embaralhar baralho ordenado
- **WHEN** `embaralhar_iterativo` é chamado com um vetor de 52 cartas ordenadas
- **THEN** DEVE retornar o vetor com cartas em ordem diferente da original, o log DEVE conter exatamente 1000 passos de troca, e DEVE incluir `tempo_execucao_ms`

#### Scenario: Log descreve cada troca
- **WHEN** o embaralhamento é executado com log habilitado
- **THEN** cada passo DEVE conter `pseudo_codigo` (ex: "trocar vetor[i] ↔ vetor[j]"), `descricao_acao` (ex: "Troca posição 15 (8♦) com posição 41 (J♠)"), e os `indices_trocados`

### Requirement: Embaralhamento recursivo do vetor de cartas

O sistema DEVE implementar uma função `embaralhar_recursivo` que recebe um vetor de cartas e um contador de iterações, realiza uma troca aleatória e chama a si mesma recursivamente decrementando o contador até atingir o caso base (contador = 0). DEVE retornar o vetor embaralhado + log narrado mostrando cada nível da recursão com pseudocódigo.

#### Scenario: Embaralhar recursivamente
- **WHEN** `embaralhar_recursivo` é chamado com vetor de 52 cartas e `contador_iteracoes=1000`
- **THEN** DEVE retornar o vetor embaralhado, o log DEVE mostrar a profundidade da recursão em cada passo e o caso base

#### Scenario: Caso base da recursão
- **WHEN** `contador_iteracoes` chega a 0
- **THEN** o log DEVE registrar "Caso base atingido: contador = 0, retornando vetor" e a recursão DEVE encerrar

#### Scenario: Log mostra profundidade recursiva
- **WHEN** a recursão está no nível 500 (de 1000)
- **THEN** o passo DEVE incluir `profundidade_recursao: 500` e `pseudo_codigo` mostrando a chamada recursiva com o contador decrementado

### Requirement: Ordenação Bubble Sort com métricas e log

O sistema DEVE implementar `ordenacao_bubble` que recebe um vetor de cartas e o ordena usando o algoritmo Bubble Sort. DEVE retornar o vetor ordenado + métricas (`total_comparacoes`, `total_trocas`, `tempo_execucao_ms`) + log narrado passo a passo com pseudocódigo.

#### Scenario: Ordenar vetor embaralhado com Bubble Sort
- **WHEN** `ordenacao_bubble` é chamado com vetor de 52 cartas embaralhadas
- **THEN** DEVE retornar o vetor ordenado por naipe e número, com métricas de comparações e trocas, e `tempo_execucao_ms`

#### Scenario: Log detalha comparações e trocas
- **WHEN** a ordenação é executada com log habilitado
- **THEN** cada passo DEVE conter: `pseudo_codigo` (ex: "SE vetor[i] > vetor[i+1] ENTÃO trocar"), `descricao_acao` (ex: "Compara 8♣ com 3♥: 8 > 3, troca!"), `indices_comparados` e `houve_troca` (bool)

#### Scenario: Vetor já ordenado
- **WHEN** `ordenacao_bubble` é chamado com vetor já ordenado
- **THEN** DEVE retornar o vetor inalterado, `total_trocas` DEVE ser 0, e o log DEVE indicar que nenhuma troca foi necessária

### Requirement: Ordenação Merge Sort com métricas e log

O sistema DEVE implementar `ordenacao_merge` que recebe um vetor de cartas e o ordena usando o algoritmo Merge Sort (divisão e conquista recursiva). DEVE retornar o vetor ordenado + métricas + log narrado mostrando as divisões, as conquistas e os merges com pseudocódigo.

#### Scenario: Ordenar vetor embaralhado com Merge Sort
- **WHEN** `ordenacao_merge` é chamado com vetor de 52 cartas embaralhadas
- **THEN** DEVE retornar o vetor ordenado com métricas de comparações e `tempo_execucao_ms`

#### Scenario: Log mostra divisão e conquista
- **WHEN** a ordenação é executada com log habilitado
- **THEN** o log DEVE mostrar cada etapa de divisão ("Dividir vetor[0..25] e vetor[26..51]"), cada merge ("Mesclar vetor[0..12] com vetor[13..25]") e as comparações durante o merge

### Requirement: Ordenação Quick Sort com métricas e log

O sistema DEVE implementar `ordenacao_quick` que recebe um vetor de cartas e o ordena usando o algoritmo Quick Sort (particionamento recursivo com pivô). DEVE retornar o vetor ordenado + métricas + log narrado mostrando a escolha do pivô, o particionamento e as chamadas recursivas.

#### Scenario: Ordenar vetor embaralhado com Quick Sort
- **WHEN** `ordenacao_quick` é chamado com vetor de 52 cartas embaralhadas
- **THEN** DEVE retornar o vetor ordenado com métricas de comparações, trocas e `tempo_execucao_ms`

#### Scenario: Log mostra pivô e partições
- **WHEN** a ordenação é executada com log habilitado
- **THEN** o log DEVE mostrar a escolha do pivô ("Pivô: 7♣ na posição 15"), o resultado do particionamento ("Menores à esquerda: 12 cartas, Maiores à direita: 8 cartas") e cada chamada recursiva

### Requirement: Comparação entre algoritmos de ordenação

O sistema DEVE oferecer uma função `comparar_algoritmos` que executa os três algoritmos de ordenação sobre o mesmo vetor e retorna uma tabela comparativa com `total_comparacoes`, `total_trocas` e `tempo_execucao_ms` de cada um.

#### Scenario: Comparar os três algoritmos
- **WHEN** `comparar_algoritmos` é chamado com um vetor de 52 cartas embaralhadas
- **THEN** DEVE retornar uma lista com 3 resultados (um por algoritmo), todos tendo ordenado o mesmo vetor de entrada, com métricas comparáveis

#### Scenario: Vetor de entrada é o mesmo para todos
- **WHEN** a comparação é executada
- **THEN** os três algoritmos DEVEM receber cópias idênticas do vetor original, garantindo comparação justa
