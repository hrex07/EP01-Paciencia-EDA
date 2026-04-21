## Why

A disciplina de Estruturas de Dados e Análise de Algoritmos do mestrado em Computação Aplicada (IPT) exige a implementação do jogo Paciência (Solitaire) como exercício prático (EP01). O objetivo é demonstrar, de forma concreta e lúdica, o uso de estruturas de dados — Pilha, Fila e Lista Ligada — e algoritmos — recursão, ordenação (bubble, merge, quick) e busca — conforme descrito no enunciado do EP01 e fundamentado no artigo TISE 2014.

O diferencial deste projeto em relação a uma implementação convencional é a **visualização educacional em tempo real**: enquanto o estudante joga do lado esquerdo da tela, o lado direito exibe a estrutura de dados sendo manipulada, o pseudocódigo com destaque na linha executada e um log narrado de cada operação. Isso transforma o jogo de um simples exercício em um **objeto de aprendizagem interativo e público na internet**.

## What Changes

- **Novo backend em Python (FastAPI)** com implementação from scratch das estruturas de dados (Pilha, Fila, Lista Ligada), cada uma retornando logs narrados passo a passo com pseudocódigo e descrição.
- **Novo frontend em React (TypeScript)** com layout dividido: painel do jogo (esquerda) e painel educacional de visualização (direita).
- **Motor do jogo Paciência** com estado gerenciado no backend, seguindo as regras clássicas: 7 listas ligadas (tableau), 4 pilhas (fundações por naipe), 1 fila (monte de compra), 6 tipos de movimentação conforme EP01.
- **Modo demonstração de algoritmos** separado do jogo, permitindo ao usuário visualizar e comparar embaralhamento (iterativo e recursivo) e ordenação (bubble, merge, quick) com métricas de performance.
- **Sistema de gamificação (streaks)** com efeitos visuais e sonoros para sequências de jogadas válidas consecutivas, incentivando o engajamento do estudante.
- **API REST documentada (Swagger)** expondo endpoints para jogo, estruturas de dados e algoritmos de demonstração.

## Capabilities

### New Capabilities

- `estruturas-dados`: Classes Pilha, Fila e Lista Ligada implementadas from scratch com logs narrados (pseudocódigo + descrição) em cada operação. Inclui classe Carta e Nó.
- `algoritmos-ordenacao-embaralhamento`: Algoritmos de embaralhamento (iterativo e recursivo) e ordenação (bubble sort, merge sort, quick sort) com métricas de comparações, trocas e tempo, além de log passo a passo.
- `motor-jogo-paciencia`: Lógica completa do jogo — estado da partida, regras de validação de movimentos (M1, M2, M3 do EP01), distribuição inicial das cartas, detecção de vitória e sistema de streaks.
- `api-rest-jogo`: Endpoints FastAPI para criação de jogo, movimentação, estado, algoritmos de demonstração e operações isoladas de estruturas de dados. Sessão em memória.
- `interface-jogo`: Painel esquerdo do frontend com visualização das cartas, interação por clique, animação de setup inicial e efeitos de streak (visuais e sonoros).
- `painel-educacional`: Painel direito do frontend com visualizador da estrutura de dados ativa, pseudocódigo com highlight, log de operações e modo demonstração/comparação de algoritmos.

### Modified Capabilities

_(Nenhuma — projeto novo, sem capacidades pré-existentes.)_

## Impact

- **Novo repositório/projeto**: Backend Python + Frontend React, ambos a serem criados do zero.
- **Dependências backend**: Python 3.11+, FastAPI, uvicorn, pydantic.
- **Dependências frontend**: React 18+, TypeScript, bibliotecas de animação (framer-motion ou similar), biblioteca de sons (howler.js ou similar).
- **Infraestrutura de deploy**: Backend em Railway/Render, frontend em Vercel/Netlify.
- **APIs expostas**: REST JSON, documentação automática via Swagger/OpenAPI.
- **Dados**: Sem banco de dados — estado de sessão em memória (dict Python). Sem persistência de partidas no MVP.
