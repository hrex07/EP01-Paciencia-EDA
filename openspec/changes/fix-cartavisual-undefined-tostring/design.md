## Context

O frontend assume que todas as cartas recebidas do backend via JSON na resposta da API (`EstadoJogo`) possuam obrigatoriamente os campos `numero_carta` e `naipe_carta`, conforme definido na interface `CartaBaralho`. Porém, como medida de segurança para que o jogador não inspecione o tráfego da rede para ver as cartas viradas para baixo, a função `_serializar_carta` no backend (`motor/estado_jogo.py`) retorna apenas `{"status_carta": False, "texto": "verso"}` quando a carta não está visível. 

Isso causa uma falha na renderização de `CartaVisual.tsx` que tenta acessar o método `toString()` do campo `numero_carta` que encontra-se como `undefined`.

## Goals / Non-Goals

**Goals:**
- Prevenir a quebra (crash) da interface do jogo ao renderizar cartas viradas para baixo.
- Manter o alinhamento de segurança do backend: o backend não deve ser alterado para expor as cartas que estão de costas.
- Garantir a renderização visual correta do verso da carta em `CartaVisual.tsx`.

**Non-Goals:**
- Mudar a regra de negócio do jogo ou como o backend processa o estado interno das Estruturas de Dados.
- Alterar o sistema de logs narrados (não é o foco deste bug).

## Decisions

**1. Alteração da tipagem no Frontend**
A interface `CartaBaralho` em `tipos.ts` será modificada para que `numero_carta` e `naipe_carta` sejam opcionais.
*Rationale:* Reflete a realidade do contrato JSON enviado pelo backend.
*Alternative considered:* Modificar o backend para enviar valores "falsos" (ex: `numero_carta: 0`, `naipe_carta: '?'`). Isso foi descartado pois quebra a semântica de tipagem restrita estabelecida no backend e suja o payload do JSON.

**2. Checagem defensiva no componente visual**
Em `CartaVisual.tsx`, vamos alterar a linha que define o `rotulo` para só acessar e converter o `numero_carta` caso o `status_carta` seja `true`.
*Rationale:* Garante que não ocorra a invocação de métodos de `undefined`. Quando a carta estiver virada para baixo (status_carta = false), o componente já lida com o estado visual renderizando apenas um div simples para o verso. Não há necessidade da variável `rotulo` ter um valor correto nesse cenário.

```ascii
[Backend JSON] --> {status_carta: False, texto: "verso"} 
      |
      v
[Frontend API] --> Converte para CartaBaralho (numero_carta = undefined)
      |
      v
[CartaVisual.tsx] --> status_carta é False -> Ignora rotulo e renderiza div do verso
```

## Risks / Trade-offs

- **[Risco]** Modificar `CartaBaralho` com campos opcionais pode introduzir erros de tipagem do TypeScript em outras partes do código que não validam a presença de `numero_carta` antes de utilizá-lo.
- **Mitigação:** Como a grande maioria da lógica do jogo fica no backend, o frontend é majoritariamente burro (dumb) visual. Modificar para opcional apenas forçará o TypeScript a avisar sobre possíveis nulos nos demais componentes visuais (que devem lidar com isso, ou que só são invocados para cartas viradas para cima). Se houver erros estáticos de TypeScript nos outros componentes, adicionaremos checagem neles.