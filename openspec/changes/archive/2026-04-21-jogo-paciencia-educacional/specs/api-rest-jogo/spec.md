## ADDED Requirements

### Requirement: Endpoint para criar novo jogo

O sistema DEVE expor `POST /api/jogo/novo` que cria uma nova partida, embaralha o baralho recursivamente, distribui as cartas nas 7 listas e 1 fila, e retorna o `id_sessao`, o `estado_jogo` completo e o `log_preparacao` contendo toda a narração da criação do baralho, embaralhamento e distribuição.

#### Scenario: Criar jogo com log de preparação
- **WHEN** `POST /api/jogo/novo` é chamado
- **THEN** DEVE retornar status 201, com `id_sessao` (UUID), `estado_jogo` serializado e `log_preparacao` contendo os passos de criação do vetor, embaralhamento recursivo e distribuição nas estruturas

#### Scenario: Parâmetro de velocidade do log
- **WHEN** `POST /api/jogo/novo` é chamado com `?log_detalhado=false`
- **THEN** DEVE retornar apenas o `estado_jogo` e `id_sessao`, sem o `log_preparacao`

### Requirement: Endpoint para consultar estado do jogo

O sistema DEVE expor `GET /api/jogo/{id_sessao}/estado` que retorna o estado atual completo da partida, incluindo todas as estruturas e contadores.

#### Scenario: Consultar estado existente
- **WHEN** `GET /api/jogo/{id_sessao}/estado` é chamado com sessão válida
- **THEN** DEVE retornar status 200 com o estado completo do jogo

#### Scenario: Sessão inexistente
- **WHEN** `GET /api/jogo/{id_sessao}/estado` é chamado com UUID inexistente
- **THEN** DEVE retornar status 404 com mensagem "Sessão não encontrada"

### Requirement: Endpoint para realizar jogada

O sistema DEVE expor `POST /api/jogo/{id_sessao}/mover` que recebe o `tipo_movimento` (1 a 6), parâmetros de origem/destino quando aplicável, valida e executa a jogada. DEVE retornar o novo `estado_jogo`, `operacoes_realizadas` com logs narrados e dados do `streak`.

#### Scenario: Jogada válida
- **WHEN** `POST /api/jogo/{id}/mover` é chamado com movimento válido
- **THEN** DEVE retornar status 200, `jogada_valida=true`, `estado_jogo` atualizado, `operacoes_realizadas[]` com passos e `streak` atualizado

#### Scenario: Jogada inválida
- **WHEN** `POST /api/jogo/{id}/mover` é chamado com movimento inválido
- **THEN** DEVE retornar status 200, `jogada_valida=false`, estado inalterado, `motivo_rejeicao` descritivo e `streak.sequencia_atual=0`

#### Scenario: Corpo da requisição
- **WHEN** o frontend envia uma jogada
- **THEN** o corpo DEVE conter `tipo_movimento` (int 1-6), e opcionalmente `indice_destino` (int, para escolher qual pilha ou lista) e `posicao_origem` (int, para M3 indicar a posição na lista origem)

### Requirement: Endpoint para listar movimentos possíveis

O sistema DEVE expor `GET /api/jogo/{id_sessao}/movimentos` que analisa o estado atual e retorna a lista de todos os movimentos válidos disponíveis.

#### Scenario: Listar movimentos disponíveis
- **WHEN** `GET /api/jogo/{id}/movimentos` é chamado
- **THEN** DEVE retornar status 200 com lista de movimentos possíveis, cada um contendo `tipo_movimento`, `descricao` legível e os parâmetros necessários para executá-lo

### Requirement: Endpoint para consultar estatísticas

O sistema DEVE expor `GET /api/jogo/{id_sessao}/estatisticas` que retorna métricas da partida: `total_jogadas`, `jogadas_validas`, `jogadas_invalidas`, `sequencia_atual`, `maior_sequencia`, `tempo_jogo_segundos` e um resumo das EDs utilizadas com contagem de operações.

#### Scenario: Estatísticas de partida em andamento
- **WHEN** `GET /api/jogo/{id}/estatisticas` é chamado durante uma partida
- **THEN** DEVE retornar as métricas atualizadas incluindo contagem de operações por tipo de ED (ex: "pilha: 12 push, 3 pop")

### Requirement: Endpoints de demonstração de algoritmos

O sistema DEVE expor: `POST /api/algoritmos/embaralhar` (aceita parâmetro `metodo`: "iterativo" ou "recursivo"), `POST /api/algoritmos/ordenar` (aceita parâmetro `metodo`: "bubble", "merge" ou "quick") e `POST /api/algoritmos/comparar`. Todos aceitam um vetor de cartas opcional (se omitido, criam um baralho padrão). Todos retornam resultado + métricas + log narrado passo a passo.

#### Scenario: Ordenar com algoritmo específico
- **WHEN** `POST /api/algoritmos/ordenar?metodo=bubble` é chamado
- **THEN** DEVE retornar o vetor ordenado, `total_comparacoes`, `total_trocas`, `tempo_execucao_ms` e `passos_executados[]`

#### Scenario: Comparar todos os algoritmos
- **WHEN** `POST /api/algoritmos/comparar` é chamado
- **THEN** DEVE retornar resultados dos 3 algoritmos sobre o mesmo vetor, permitindo comparação direta de métricas

### Requirement: Endpoints de demonstração de estruturas de dados

O sistema DEVE expor endpoints para demonstração isolada de cada operação de ED: `POST /api/estruturas/pilha/{operacao}`, `POST /api/estruturas/fila/{operacao}`, `POST /api/estruturas/lista/{operacao}`. Cada endpoint mantém uma instância temporária da estrutura em sessão e retorna o resultado + log narrado.

#### Scenario: Demonstrar push na pilha
- **WHEN** `POST /api/estruturas/pilha/empilhar` é chamado com uma carta
- **THEN** DEVE retornar o resultado da operação com `passos_executados[]` completo e o estado da pilha

### Requirement: Documentação automática via Swagger

O sistema DEVE gerar documentação OpenAPI/Swagger automaticamente via FastAPI. Todos os endpoints DEVEM ter descrições em português, exemplos de request/response e schemas Pydantic tipados.

#### Scenario: Acessar documentação
- **WHEN** o usuário acessa `/docs`
- **THEN** DEVE visualizar todos os endpoints documentados com descrições em português e exemplos interativos
