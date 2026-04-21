## 1. Atualização de Tipagem (Frontend)

- [ ] 1.1 Em `frontend/src/tipos/tipos.ts`, alterar a interface `CartaBaralho` tornando `numero_carta` e `naipe_carta` opcionais (`?`).

## 2. Correção de Componente Visual (Frontend)

- [ ] 2.1 Em `frontend/src/components/painelJogo/CartaVisual.tsx`, adicionar condicional ou default values para evitar acesso ao `.toString()` quando a carta estiver virada para baixo (ou seja, quando `status_carta` for `false` ou `numero_carta` for `undefined`).
