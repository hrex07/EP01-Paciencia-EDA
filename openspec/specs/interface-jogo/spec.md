## ADDED Requirements

### Requirement: Layout dividido em dois painéis

O frontend DEVE apresentar a tela dividida em dois painéis: painel esquerdo com o jogo Paciência e painel direito com a visualização educacional. O layout DEVE ser otimizado para desktop (largura mínima 1280px).

#### Scenario: Exibir layout dividido
- **WHEN** o usuário acessa a aplicação
- **THEN** DEVE visualizar dois painéis lado a lado: jogo à esquerda (~55% da tela) e visualização à direita (~45%)

#### Scenario: Painel direito colapsável
- **WHEN** o usuário clica em um botão de toggle no painel direito
- **THEN** o painel educacional DEVE colapsar/expandir, permitindo que o jogo ocupe a tela inteira quando desejado

### Requirement: Visualização das cartas no painel do jogo

O frontend DEVE renderizar cartas com representação visual reconhecível: número, naipe (com símbolo e cor), e estado (virada para cima com face visível, ou virada para baixo com dorso). As cartas DEVEM ser organizadas conforme o layout clássico do Solitaire: fila de compra no topo esquerdo, 4 fundações no topo direito, 7 colunas do tableau abaixo.

#### Scenario: Renderizar carta virada para cima
- **WHEN** uma carta tem `status_carta=true`
- **THEN** DEVE exibir o número e símbolo do naipe com a cor correta (vermelho para copas/ouros, preto para paus/espadas)

#### Scenario: Renderizar carta virada para baixo
- **WHEN** uma carta tem `status_carta=false`
- **THEN** DEVE exibir o dorso da carta (design padronizado) sem revelar número ou naipe

#### Scenario: Cartas empilhadas no tableau
- **WHEN** uma coluna do tableau tem múltiplas cartas
- **THEN** as cartas DEVEM ser exibidas sobrepostas verticalmente, com a parte superior de cada carta visível

### Requirement: Interação por clique para movimentação

O frontend DEVE permitir que o usuário selecione uma carta (clique) e depois clique no destino para movê-la. O sistema DEVE destacar visualmente a carta selecionada e os destinos válidos.

#### Scenario: Selecionar carta
- **WHEN** o usuário clica em uma carta virada para cima (na fila, no topo de pilha ou em lista)
- **THEN** a carta DEVE receber destaque visual (borda, brilho ou elevação) e os destinos válidos DEVEM ser indicados

#### Scenario: Mover carta para destino
- **WHEN** o usuário clica em um destino válido após selecionar uma carta
- **THEN** o sistema DEVE enviar a jogada ao backend e animar a carta movendo-se suavemente até o destino

#### Scenario: Cancelar seleção
- **WHEN** o usuário clica na mesma carta selecionada ou em área vazia
- **THEN** a seleção DEVE ser cancelada e os destaques removidos

#### Scenario: Tentativa de movimento inválido
- **WHEN** o usuário clica em um destino inválido
- **THEN** DEVE exibir feedback visual de erro (shake, flash vermelho) e som de erro

### Requirement: Animação de setup inicial do jogo

O frontend DEVE animar a preparação do jogo ao iniciar uma nova partida, mostrando visualmente: criação do baralho, embaralhamento (cartas se movendo), distribuição nas 7 colunas e enfileiramento das restantes. O usuário DEVE poder controlar a velocidade (lento, normal, rápido, instantâneo).

#### Scenario: Animação em velocidade normal
- **WHEN** o usuário inicia um novo jogo com velocidade "normal"
- **THEN** DEVE ver as cartas sendo distribuídas uma a uma nas colunas, com tempo total aproximado de 10-15 segundos

#### Scenario: Pular animação
- **WHEN** o usuário seleciona velocidade "instantâneo" ou clica em "Pular"
- **THEN** a animação DEVE ser interrompida e o estado final do jogo DEVE ser exibido imediatamente

### Requirement: Sistema de efeitos visuais de streak

O frontend DEVE interpretar o `nivel_efeito` retornado pelo backend e disparar efeitos visuais proporcionais: "basico" (transição suave), "bom" (brilho na carta), "otimo" (partículas douradas), "confetti" (explosão de confetti), "incrivel" (tela pulsa), "mestre" (arco-íris e shake). O efeito de "vitoria" DEVE ser o mais elaborado.

#### Scenario: Efeito de confetti no streak 5
- **WHEN** o backend retorna `nivel_efeito="confetti"`
- **THEN** o frontend DEVE disparar uma animação de confetti na tela com duração de 2-3 segundos

#### Scenario: Efeito de vitória
- **WHEN** o backend retorna `nivel_efeito="vitoria"`
- **THEN** o frontend DEVE disparar a animação mais elaborada (confetti + fogos + mensagem de parabéns) com as estatísticas finais

### Requirement: Sistema de efeitos sonoros

O frontend DEVE reproduzir sons de feedback: click suave ao mover carta, som de erro ao tentar movimento inválido, sons progressivos para cada nível de streak e fanfarra de vitória. O usuário DEVE poder silenciar/ajustar o volume dos sons.

#### Scenario: Som de jogada válida
- **WHEN** uma jogada válida é executada com streak nível "basico"
- **THEN** DEVE reproduzir um som de click suave

#### Scenario: Silenciar sons
- **WHEN** o usuário clica no botão de mute
- **THEN** todos os efeitos sonoros DEVEM ser desabilitados até reativação

### Requirement: Menu do jogo com opções de controle

O frontend DEVE possuir um menu com: "Novo Jogo", "Movimentos Possíveis" (solicita ao backend), "Estatísticas", "Modo Demonstração" (navega para a área de algoritmos), controle de volume e toggle do painel educacional.

#### Scenario: Iniciar novo jogo
- **WHEN** o usuário clica em "Novo Jogo"
- **THEN** DEVE confirmar se deseja abandonar a partida atual (se existir) e iniciar nova partida com animação de setup

#### Scenario: Ver movimentos possíveis
- **WHEN** o usuário clica em "Movimentos Possíveis"
- **THEN** DEVE destacar todas as cartas que podem ser movidas e seus destinos válidos
