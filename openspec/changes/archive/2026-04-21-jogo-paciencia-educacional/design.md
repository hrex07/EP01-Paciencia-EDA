## Context

Projeto acadêmico do mestrado em Computação Aplicada (IPT), disciplina Estruturas de Dados e Análise de Algoritmos. O exercício EP01 solicita a implementação do jogo Paciência (Solitaire) utilizando obrigatoriamente: Pilha, Fila, Lista Ligada, recursão e algoritmos de ordenação (bubble, merge, quick).

O diferencial proposto é um **painel educacional em tempo real** que exibe, ao lado do jogo, a estrutura de dados sendo manipulada, o pseudocódigo com highlight e um log narrado de cada operação. O sistema será público na internet para uso por outros estudantes.

Estado atual: projeto do zero, apenas documentação de referência existente.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       ARQUITETURA GERAL                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─── PYTHON (FastAPI) ─────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  modelo/              motor/               api/                  │  │
│  │  ├ carta_baralho.py   ├ estado_jogo.py     ├ rotas_jogo.py      │  │
│  │  ├ no_encadeado.py    ├ regras_movimento.py├ rotas_algoritmos.py │  │
│  │  ├ pilha_cartas.py    └ controlador_jogo.py└ rotas_estruturas.py│  │
│  │  ├ fila_cartas.py                                                │  │
│  │  └ lista_ligada.py    algoritmos/                                │  │
│  │                       ├ embaralhamento_iterativo.py              │  │
│  │                       ├ embaralhamento_recursivo.py              │  │
│  │                       ├ ordenacao_bubble.py                      │  │
│  │                       ├ ordenacao_merge.py                       │  │
│  │                       └ ordenacao_quick.py                       │  │
│  │                                                                   │  │
│  │  testes/                                                          │  │
│  │  ├ teste_pilha.py    ├ teste_fila.py     ├ teste_lista.py       │  │
│  │  ├ teste_ordenacao.py└ teste_jogo.py                             │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              │ REST JSON                                │
│  ┌─── REACT (TypeScript) ───▼───────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  components/                                                      │  │
│  │  ├ painelJogo/           ├ painelEducacional/    ├ comum/        │  │
│  │  │ MesaJogo.tsx          │ VisualizadorED.tsx    │ BotaoAcao.tsx │  │
│  │  │ CartaVisual.tsx       │ PseudocodigoHL.tsx    │ IconeNaipe.tsx│  │
│  │  │ FilaCompra.tsx        │ LogOperacoes.tsx      └───────────────│  │
│  │  │ FundacaoPilha.tsx     │ ComparadorAlgo.tsx                    │  │
│  │  │ ColunaTablau.tsx      │ EfeitosStreak.tsx                     │  │
│  │                                                                   │  │
│  │  servicos/               tipos/                                   │  │
│  │  └ apiJogo.ts            └ tipos.ts                              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Goals / Non-Goals

**Goals:**
- Implementar todas as estruturas de dados (Pilha, Fila, Lista Ligada) from scratch em Python, atendendo 100% dos requisitos do EP01.
- Cada operação das EDs DEVE retornar resultado + log narrado com pseudocódigo e descrição em português.
- Jogo Paciência completamente funcional com os 6 tipos de movimentação do EP01.
- Painel educacional em tempo real mostrando ED ativa, pseudocódigo com highlight e log de operações.
- Modo demonstração de algoritmos de ordenação com comparação de métricas.
- Sistema de streaks com feedback visual e sonoro para engajamento.
- Deploy público acessível pela internet.
- Código documentado como referência acadêmica para outros estudantes.

**Non-Goals:**
- Não é um jogo comercial — não há monetização, ranking global ou login de usuários.
- Não haverá persistência de partidas em banco de dados (estado em memória é suficiente).
- Não haverá drag-and-drop sofisticado — interação por clique é suficiente para o MVP.
- Não serão criadas animações/vídeos dos algoritmos (links externos quando disponíveis).
- Não haverá multiplayer ou modo competitivo.
- Não haverá suporte a dispositivos móveis no MVP (desktop first).

## Decisions

### D1: Python (FastAPI) + React (TypeScript) como stack

**Decisão:** Backend em Python com FastAPI; frontend em React com TypeScript.

**Alternativas consideradas:**
- **Java puro (Swing/JavaFX):** Atenderia o requisito literal do EP01, mas dificulta deploy web e animações. A GUI por `System.out.println` limitaria a visualização das EDs.
- **React full-stack (Node.js):** Simplificaria o deploy, mas Python é a linguagem-alvo do aluno e as EDs devem ser implementadas em Python para fins acadêmicos.

**Rationale:** Python permite implementação didática das EDs com docstrings ricas. FastAPI gera documentação Swagger automática (valor acadêmico). React oferece a melhor experiência para animações e visualização em tempo real. O aluno domina ambas as linguagens.

### D2: Estado do jogo gerenciado no backend

**Decisão:** O estado completo do jogo (fila, pilhas, listas ligadas, contadores) é mantido em memória no Python, acessado via `id_sessao` (UUID).

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLUXO DE ESTADO                                   │
│                                                                     │
│  React                          FastAPI                             │
│  ─────                          ───────                             │
│  POST /api/jogo/novo ──────▶   Cria EstadoJogo                    │
│                                 sessoes[uuid] = estado              │
│  ◄── { id_sessao, estado }                                         │
│                                                                     │
│  POST /api/jogo/{id}/mover ──▶ Busca sessoes[id]                  │
│  { tipo, destino }              Valida + executa + loga            │
│  ◄── { estado, operacoes[] }    Atualiza sessoes[id]               │
│                                                                     │
│  Armazenamento: dict[str, EstadoJogo]                              │
│  Limpeza: TTL de 2h sem atividade                                  │
└─────────────────────────────────────────────────────────────────────┘
```

**Alternativas consideradas:**
- **Estado no frontend:** React gerenciaria tudo, Python seria stateless. Mais escalável, mas obrigaria a reimplementar as EDs em TypeScript, perdendo o propósito acadêmico.
- **Banco de dados (SQLite):** Persistência desnecessária para projeto acadêmico. Adicionaria complexidade sem valor educacional.

**Rationale:** Manter o estado no backend garante que todas as operações de ED aconteçam em Python (onde estão documentadas). O React fica leve, focado apenas em UX e visualização.

### D3: Formato do log narrado (RegistroOperacao)

**Decisão:** Cada operação de ED retorna um dicionário padronizado contendo o resultado e uma lista de passos, onde cada passo tem pseudocódigo e descrição em português.

```
┌─────────────────────────────────────────────────────────────────────┐
│                  FORMATO DO LOG NARRADO                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  {                                                                  │
│    "operacao_nome": "empilhar",                                    │
│    "estrutura_tipo": "Pilha",                                      │
│    "estrutura_nome": "pilha_espadas",                              │
│    "operacao_sucesso": true,                                       │
│    "valor_entrada": { "numero": 13, "naipe": "e" },               │
│    "valor_retornado": null,                                        │
│                                                                     │
│    "estado_antes": {                                                │
│      "tamanho": 2,                                                 │
│      "topo": { "numero": 12, "naipe": "e" },                      │
│      "elementos": [12e, 11e]                                       │
│    },                                                               │
│                                                                     │
│    "estado_depois": {                                               │
│      "tamanho": 3,                                                 │
│      "topo": { "numero": 13, "naipe": "e" },                      │
│      "elementos": [13e, 12e, 11e]                                  │
│    },                                                               │
│                                                                     │
│    "passos_executados": [                                           │
│      {                                                              │
│        "passo_numero": 1,                                          │
│        "pseudo_codigo": "nó_novo ← CriarNó(carta)",               │
│        "descricao_acao": "Cria um novo nó para armazenar K♠",     │
│        "variaveis_estado": { "nó_novo": "K♠", "topo": "Q♠" }     │
│      },                                                             │
│      {                                                              │
│        "passo_numero": 2,                                          │
│        "pseudo_codigo": "SE pilha.topo == NULO ENTÃO",             │
│        "descricao_acao": "Verifica se a pilha está vazia",         │
│        "variaveis_estado": { "pilha.topo": "Q♠", "avaliação": false}│
│      },                                                             │
│      {                                                              │
│        "passo_numero": 3,                                          │
│        "pseudo_codigo": "nó_novo.próximo ← pilha.topo",           │
│        "descricao_acao": "K♠ agora aponta para Q♠ (topo atual)",  │
│        "variaveis_estado": { "nó_novo.próximo": "Q♠" }            │
│      },                                                             │
│      {                                                              │
│        "passo_numero": 4,                                          │
│        "pseudo_codigo": "pilha.topo ← nó_novo",                   │
│        "descricao_acao": "O topo da pilha agora é K♠",            │
│        "variaveis_estado": { "pilha.topo": "K♠" }                 │
│      },                                                             │
│      {                                                              │
│        "passo_numero": 5,                                          │
│        "pseudo_codigo": "pilha.tamanho ← pilha.tamanho + 1",      │
│        "descricao_acao": "Incrementa o tamanho: 2 → 3",           │
│        "variaveis_estado": { "pilha.tamanho": 3 }                 │
│      }                                                              │
│    ]                                                                │
│  }                                                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Rationale:** O formato `estado_antes` / `estado_depois` permite ao frontend animar a transição. O campo `variaveis_estado` em cada passo permite highlight contextual no pseudocódigo. Tudo em português para consistência acadêmica.

### D4: Sistema de streaks com feedback escalável

**Decisão:** O backend contabiliza jogadas válidas consecutivas e retorna nível de efeito. O frontend interpreta o nível e dispara efeitos visuais + sonoros.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE STREAKS                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Backend calcula:                                                   │
│  {                                                                  │
│    "sequencia_atual": 5,                                           │
│    "maior_sequencia": 8,                                           │
│    "nivel_efeito": "confetti",    ← frontend mapeia para efeito   │
│    "mensagem_educacional": "5 movimentos usando Pilha e Fila!"    │
│  }                                                                  │
│                                                                     │
│  Mapeamento de níveis:                                             │
│  ──────────────────────                                             │
│  Streak 1     → "basico"     → click suave                        │
│  Streak 2     → "bom"        → click + nota musical               │
│  Streak 3     → "otimo"      → partículas douradas + acorde       │
│  Streak 5     → "confetti"   → explosão de confetti + fanfarra    │
│  Streak 7     → "incrivel"   → tela pulsa + aplausos              │
│  Streak 10+   → "mestre"     → arco-íris + ovação                 │
│                                                                     │
│  Jogada inválida → sequencia_atual = 0, nivel = "erro"            │
│                                                                     │
│  A mensagem educacional menciona quais EDs foram usadas            │
│  na sequência, reforçando o aprendizado.                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Rationale:** Separar o cálculo (backend) da apresentação (frontend) mantém a responsabilidade clara. O backend sabe quais EDs foram usadas; o frontend sabe como animar.

### D5: Animação de setup inicial via endpoint dedicado

**Decisão:** O endpoint `POST /api/jogo/novo` retorna o estado final do jogo **e** o log completo de toda a preparação (criação do vetor, embaralhamento recursivo, distribuição nas listas, enfileiramento), permitindo ao frontend reproduzir a animação passo a passo.

**Rationale:** O setup inicial é uma oportunidade rica de mostrar vetor, recursão, lista ligada e fila operando em sequência. Ao retornar tudo de uma vez (em vez de streaming), o frontend pode controlar a velocidade da animação (lento, rápido, instantâneo).

### D6: Modo demonstração de algoritmos como endpoints separados

**Decisão:** Algoritmos de ordenação e embaralhamento possuem endpoints próprios (`/api/algoritmos/*`), independentes do jogo. Aceitam um vetor de cartas e retornam o resultado + métricas + log passo a passo.

**Alternativas consideradas:**
- **Integrar no jogo:** Desordenar/reordenar o baralho durante o jogo. Não faz sentido semanticamente — a ordenação é uma demonstração didática, não uma ação do jogo.

**Rationale:** Separar permite ao estudante experimentar cada algoritmo isoladamente, comparar métricas lado a lado, sem interferir numa partida em andamento.

## Risks / Trade-offs

**[Estado em memória é volátil]** → Se o servidor reiniciar, todas as partidas em andamento são perdidas. **Mitigação:** Aceitável para projeto acadêmico. Se necessário futuramente, serializar estado para SQLite é uma extensão simples.

**[Logs narrados aumentam o tamanho da resposta JSON]** → Uma jogada que aciona múltiplas operações (ex: mover sublista entre listas ligadas) pode gerar um JSON com dezenas de passos. **Mitigação:** Parâmetro opcional `incluir_passos=true` nos endpoints. O frontend solicita passos detalhados apenas quando o painel educacional está visível.

**[Latência de rede afeta a experiência]** → Cada jogada é uma chamada HTTP. **Mitigação:** Deploy em serviço com baixa latência (Railway/Render). As respostas são pequenas (< 10KB). Para o público acadêmico, latência de 100-200ms é aceitável.

**[Complexidade do frontend para animações]** → Animar passo a passo operações de ED com highlight de pseudocódigo exige gerenciamento de estado temporal no React. **Mitigação:** Usar uma state machine simples (passo atual, timer, play/pause). Framer-motion simplifica as transições visuais.

**[Manutenção de pseudocódigo em português]** → O pseudocódigo está embutido no código Python como strings. Se a lógica mudar, o pseudocódigo pode ficar desatualizado. **Mitigação:** Testes que validam a quantidade de passos retornados por cada operação.

## Open Questions

- **Desfazer jogada (undo):** Implementar com uma pilha de estados anteriores? Isso seria inclusive uma demonstração adicional do uso de Pilha. A decidir na Fase 2.
- **Dica automática:** Calcular e sugerir a melhor jogada possível? Pode usar busca. A decidir na Fase 3.
- **CORS e segurança:** Para deploy público, definir políticas de CORS e rate limiting na Fase 5.
