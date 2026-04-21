## 1. Fase 1 — Fundação: Estruturas de Dados (Backend Python)

- [x] 1.1 Criar estrutura do projeto backend: `pyproject.toml` com dependências (FastAPI, uvicorn, pydantic, pytest), diretórios `modelo/`, `algoritmos/`, `motor/`, `api/`, `testes/` e arquivos `__init__.py`
- [x] 1.2 Implementar classe `CartaBaralho` em `modelo/carta_baralho.py` com atributos `numero_carta`, `naipe_carta`, `status_carta`, métodos `cor_carta`, representação textual (ex: "K♠") e docstring Google style
- [x] 1.3 Implementar classe `NoEncadeado` em `modelo/no_encadeado.py` com atributos `dados_carta`, `proximo_no`, `anterior_no` e docstring Google style
- [x] 1.4 Implementar classe `PilhaCartas` em `modelo/pilha_cartas.py` com operações `empilhar`, `desempilhar`, `espiar_topo`, `esta_vazia`, `obter_tamanho` — cada operação retornando resultado + `passos_executados` com pseudocódigo narrado em português
- [x] 1.5 Escrever testes unitários para `PilhaCartas` em `testes/teste_pilha.py`: pilha vazia, empilhar, desempilhar, espiar topo, desempilhar vazia, verificar log narrado
- [x] 1.6 Implementar classe `FilaCartas` em `modelo/fila_cartas.py` com operações `enfileirar`, `desenfileirar`, `espiar_frente`, `reposicionar_frente`, `esta_vazia`, `obter_tamanho` — cada operação retornando resultado + `passos_executados` com pseudocódigo narrado
- [x] 1.7 Escrever testes unitários para `FilaCartas` em `testes/teste_fila.py`: fila vazia, enfileirar, desenfileirar, reposicionar, desenfileirar vazia, verificar log narrado
- [x] 1.8 Implementar classe `ListaLigadaCartas` em `modelo/lista_ligada_cartas.py` como lista duplamente ligada com operações `inserir_final`, `inserir_posicao`, `remover_final`, `remover_a_partir_de`, `obter_carta_posicao`, `obter_ultima_carta`, `buscar_carta`, `esta_vazia`, `obter_tamanho` — cada operação retornando resultado + `passos_executados` com pseudocódigo narrado
- [x] 1.9 Escrever testes unitários para `ListaLigadaCartas` em `testes/teste_lista_ligada.py`: lista vazia, inserir final, inserir posição, remover final, remover sublista, buscar, verificar log narrado
- [x] 1.10 Implementar função de criação do baralho completo (vetor de 52 cartas) com log da criação

## 2. Fase 1 — Fundação: Algoritmos (Backend Python)

- [x] 2.1 Implementar `embaralhamento_iterativo` em `algoritmos/embaralhamento_iterativo.py`: 1000 trocas aleatórias com log narrado (pseudocódigo + posições + cartas trocadas) e métricas de tempo
- [x] 2.2 Implementar `embaralhamento_recursivo` em `algoritmos/embaralhamento_recursivo.py`: troca + chamada recursiva com contador decremental, log mostrando profundidade da recursão e caso base
- [x] 2.3 Escrever testes para embaralhamento em `testes/teste_embaralhamento.py`: vetor muda de ordem, tamanho preservado, todas as cartas presentes, caso base da recursão, log gerado corretamente
- [x] 2.4 Implementar `ordenacao_bubble` em `algoritmos/ordenacao_bubble.py` com métricas (`total_comparacoes`, `total_trocas`, `tempo_execucao_ms`) e log passo a passo
- [x] 2.5 Implementar `ordenacao_merge` em `algoritmos/ordenacao_merge.py` com métricas e log mostrando divisão, conquista e merge
- [x] 2.6 Implementar `ordenacao_quick` em `algoritmos/ordenacao_quick.py` com métricas e log mostrando pivô, particionamento e chamadas recursivas
- [x] 2.7 Implementar função `comparar_algoritmos` que executa os 3 sobre cópias do mesmo vetor e retorna tabela comparativa
- [x] 2.8 Escrever testes para ordenação em `testes/teste_ordenacao.py`: resultado correto para cada algoritmo, métricas presentes, vetor já ordenado, comparação retorna 3 resultados

## 3. Fase 2 — Motor do Jogo (Backend Python)

- [x] 3.1 Implementar classe `EstadoJogo` em `motor/estado_jogo.py` contendo 1 `FilaCartas`, 4 `PilhaCartas`, 7 `ListaLigadaCartas`, contadores de streak e serialização para JSON
- [x] 3.2 Implementar distribuição inicial das cartas em `motor/controlador_jogo.py`: criar baralho, embaralhar recursivamente, distribuir nas 7 listas (padrão clássico) e enfileirar as 24 restantes, gerando log completo de todas as operações
- [x] 3.3 Implementar validações de movimento em `motor/regras_movimento.py`: Fila→Pilha (ás em vazia ou mesmo naipe +1), Fila→Lista (rei em vazia ou cor alternada -1), Pilha→Lista, Lista→Pilha, Lista→Lista (M1, M2, M3) — cada validação retornando bool + log explicativo
- [x] 3.4 Implementar os 6 tipos de movimentação no controlador: (1) Fila→Fila, (2) Fila→Pilha, (3) Fila→Lista, (4) Pilha→Lista, (5) Lista→Pilha, (6) Lista→Lista — cada um validando, executando operações nas EDs e gerando log completo
- [x] 3.5 Implementar lógica de virar carta (quando última carta visível é removida de uma lista, a carta abaixo vira para cima)
- [x] 3.6 Implementar sistema de streaks: incrementar em jogada válida, zerar em inválida, mapear para `nivel_efeito`, gerar `mensagem_educacional` mencionando EDs usadas
- [x] 3.7 Implementar detecção de vitória (4 pilhas com 13 cartas cada)
- [x] 3.8 Implementar cálculo de movimentos possíveis (analisa estado e lista todas as jogadas válidas)
- [x] 3.9 Escrever testes para o motor do jogo em `testes/teste_jogo.py`: distribuição inicial correta (28 em listas + 24 na fila), validações M1/M2/M3, movimentações, virar carta, streak, vitória

## 4. Fase 2 — API REST (Backend Python)

- [x] 4.1 Criar `main.py` com aplicação FastAPI, configuração CORS e gerenciador de sessões em memória (dict com TTL)
- [x] 4.2 Implementar `POST /api/jogo/novo` em `api/rotas_jogo.py`: cria partida, retorna `id_sessao`, `estado_jogo` e `log_preparacao` opcional
- [x] 4.3 Implementar `GET /api/jogo/{id_sessao}/estado` com tratamento de sessão inexistente (404)
- [x] 4.4 Implementar `POST /api/jogo/{id_sessao}/mover` com corpo `{ tipo_movimento, indice_destino?, posicao_origem? }`, retornando estado atualizado, operações e streak
- [x] 4.5 Implementar `GET /api/jogo/{id_sessao}/movimentos` que retorna lista de jogadas válidas
- [x] 4.6 Implementar `GET /api/jogo/{id_sessao}/estatisticas` com métricas da partida
- [x] 4.7 Implementar endpoints de algoritmos em `api/rotas_algoritmos.py`: `POST /api/algoritmos/embaralhar`, `POST /api/algoritmos/ordenar`, `POST /api/algoritmos/comparar`
- [x] 4.8 Implementar endpoints de demonstração de EDs em `api/rotas_estruturas.py`: operações isoladas de pilha, fila e lista
- [x] 4.9 Definir schemas Pydantic para request/response com descrições em português e exemplos
- [x] 4.10 Verificar documentação Swagger gerada em `/docs` com descrições legíveis e exemplos interativos

## 5. Fase 3 — Interface do Jogo (Frontend React)

- [x] 5.1 Criar projeto React com TypeScript (Vite), instalar dependências: framer-motion, howler.js (ou similar para áudio), axios
- [x] 5.2 Definir tipos TypeScript em `tipos/tipos.ts` espelhando os schemas Pydantic do backend (CartaBaralho, EstadoJogo, ResultadoOperacao, etc.)
- [x] 5.3 Implementar serviço de API em `servicos/apiJogo.ts` com funções para todos os endpoints do backend
- [x] 5.4 Implementar componente `CartaVisual.tsx`: renderização de carta com número, naipe (símbolo + cor), dorso, estados (normal, selecionada, destaque)
- [x] 5.5 Implementar layout principal `App.tsx` com dois painéis (jogo ~55% | educacional ~45%) e toggle para colapsar painel direito
- [x] 5.6 Implementar componentes do painel do jogo: `FilaCompra.tsx`, `FundacaoPilha.tsx` (4x), `ColunaTablau.tsx` (7x) com cartas sobrepostas
- [x] 5.7 Implementar `MesaJogo.tsx` integrando todos os componentes em layout de Solitaire clássico
- [x] 5.8 Implementar interação por clique: selecionar carta → destacar destinos válidos → clicar destino → enviar jogada ao backend → animar resultado
- [x] 5.9 Implementar animação de setup inicial: cartas sendo distribuídas com controle de velocidade (lento, normal, rápido, instantâneo / pular)
- [x] 5.10 Implementar sistema de efeitos visuais de streak: mapeamento de `nivel_efeito` para animações (partículas, confetti, pulso, arco-íris, vitória)
- [x] 5.11 Implementar sistema de efeitos sonoros: sons de click, erro, streaks progressivos, vitória; botão de mute e controle de volume
- [x] 5.12 Implementar menu do jogo: "Novo Jogo", "Movimentos Possíveis", "Estatísticas", "Modo Demonstração", controles de áudio, toggle painel

## 6. Fase 4 — Painel Educacional (Frontend React)

- [x] 6.1 Implementar `VisualizadorEstrutura.tsx`: diagrama visual de Pilha (vertical), Fila (horizontal), Lista Ligada (nós + setas) com animações de transição sincronizadas com passos
- [x] 6.2 Implementar `PseudocodigoHighlight.tsx`: exibição do pseudocódigo com highlight na linha ativa, linhas já executadas marcadas, descrição contextualizada abaixo, controles de passo (anterior, próximo, play/pause, slider de velocidade)
- [x] 6.3 Implementar `LogOperacoes.tsx`: histórico cronológico scrollável com timestamp, operação, estrutura e resultado; filtro por tipo de ED; expansão de detalhes ao clicar
- [x] 6.4 Implementar `ComparadorAlgoritmos.tsx`: seleção de algoritmos, execução via API, tabela comparativa de métricas, visualização passo a passo opcional, links para recursos educacionais externos
- [x] 6.5 Implementar indicador permanente de EDs em uso (resumo com ícones, quantidades, clique para inspecionar)
- [x] 6.6 Integrar painel educacional com o fluxo do jogo: a cada jogada, atualizar visualizador, pseudocódigo e log automaticamente

## 7. Fase 5 — Polish e Deploy

- [x] 7.1 Configurar CORS adequadamente para domínio de produção e rate limiting básico
- [x] 7.2 Escrever README.md completo em português: descrição do projeto, motivação acadêmica, como executar localmente, como acessar online, stack tecnológica, estrutura do projeto, referências
- [x] 7.3 Deploy do backend em Railway ou Render com variáveis de ambiente configuradas
- [x] 7.4 Deploy do frontend em Vercel ou Netlify com variável de URL do backend
- [x] 7.5 Testes end-to-end manuais: fluxo completo de uma partida, modo demonstração, painel educacional
- [x] 7.6 Revisão final de código, docstrings e pseudocódigos narrados
