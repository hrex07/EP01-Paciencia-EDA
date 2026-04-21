## Why

O sistema atualmente rejeita erroneamente movimentos de cartas entre colunas do tableau (Listas Ligadas) quando o jogador tenta colocar cartas de cores alternadas, mesmo que o movimento seja legítimo de acordo com as regras clássicas de Paciência (por exemplo, mover uma Dama vermelha sobre um Rei preto resulta no erro "Jogada inválida: As cores devem ser alternadas (preto/vermelho)"). A correção é necessária para garantir a progressão correta e a jogabilidade funcional da aplicação conforme exigido pelos requisitos de demonstração dos algoritmos de pilhas, listas e filas.

## What Changes

- Modificação da lógica de validação de movimento no backend (motor do jogo) para que cartas de cores diferentes sejam aceitas corretamente em movimentações entre listas.
- Ajuste na comparação condicional em `motor/regras_movimento.py` na validação de lista para lista.

## Capabilities

### New Capabilities
Não há novas capacidades sistêmicas, trata-se de uma correção de bug em componentes já existentes.

### Modified Capabilities
- `motor-jogo-paciencia`: Modificação no comportamento e validação das regras de negócio que ditam as transferências de cartas entre as listas (Tableau), assegurando a correta validação de alternância de cores.

## Impact

- `backend/motor/regras_movimento.py`: Alteração no código de verificação booleana que controla o retorno do movimento (Lista → Lista e possivelmente outros que envolvem o Tableau).
- Testes unitários em `backend/testes/teste_jogo.py` precisarão ser executados e possivelmente ajustados/acrescidos para testar explicitamente o bloqueio apenas para mesmas cores e permitir cores diferentes.