## MODIFIED Requirements

### Requirement: Visualização das cartas no painel do jogo

O frontend DEVE renderizar cartas com representação visual reconhecível: número, naipe (com símbolo e cor), e estado (virada para cima com face visível, ou virada para baixo com dorso). As cartas DEVEM ser organizadas conforme o layout clássico do Solitaire: fila de compra no topo esquerdo, 4 fundações no topo direito, 7 colunas do tableau abaixo. O frontend DEVE estar preparado para receber dados de cartas viradas para baixo sem os atributos numéricos e de naipe, garantindo que o componente visual valide a propriedade `status_carta` antes de tentar renderizar seus valores ou cores.

#### Scenario: Renderizar carta virada para cima
- **WHEN** uma carta tem `status_carta=true`
- **THEN** DEVE exibir o número e símbolo do naipe com a cor correta (vermelho para copas/ouros, preto para paus/espadas)

#### Scenario: Renderizar carta virada para baixo
- **WHEN** uma carta tem `status_carta=false`
- **THEN** DEVE exibir o dorso da carta (design padronizado) sem tentar revelar, ler ou processar `numero_carta` ou `naipe_carta` (pois podem ser nulos/undefined)

#### Scenario: Cartas empilhadas no tableau
- **WHEN** uma coluna do tableau tem múltiplas cartas
- **THEN** as cartas DEVEM ser exibidas sobrepostas verticalmente, com a parte superior de cada carta visível
