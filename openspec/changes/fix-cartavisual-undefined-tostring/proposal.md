## Why

Durante a renderização do jogo, ocorre um erro no console do frontend (`Uncaught TypeError: Cannot read properties of undefined (reading 'toString')`) no componente `CartaVisual.tsx`. Este erro acontece porque o backend (Python) serializa as cartas viradas para baixo (`status_carta = False`) omitindo os atributos `numero_carta` e `naipe_carta` por questões de segurança de estado, enviando apenas `{"status_carta": False, "texto": "verso"}`. No entanto, o frontend em React pressupõe que esses atributos sempre estarão presentes na interface `CartaBaralho`, tentando executar `.toString()` em `numero_carta`, o que resulta em `undefined`.

## What Changes

- Modificação da interface TypeScript `CartaBaralho` em `tipos.ts` para refletir que `numero_carta` e `naipe_carta` podem ser opcionais quando a carta está virada para baixo.
- Correção no componente `CartaVisual.tsx` para que a desestruturação e a tentativa de conversão de `numero_carta` e leitura de `naipe_carta` só ocorram quando `status_carta` for verdadeiro, ou utilizando *optional chaining* e valores padrão defensivos.

## Capabilities

### New Capabilities
Não há novas capacidades sistêmicas, apenas correção de bug em componentes existentes.

### Modified Capabilities
- `interface-jogo`: Modificação da especificação para lidar adequadamente com a tipagem de cartas com face virada para baixo no frontend.

## Impact

- `frontend/src/tipos/tipos.ts`: Atualização da tipagem da interface `CartaBaralho`.
- `frontend/src/components/painelJogo/CartaVisual.tsx`: Adição de checagem defensiva na renderização da carta.
