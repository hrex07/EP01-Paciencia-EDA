## 1. Correção Lógica no Backend

- [x] 1.1 Em `backend/motor/regras_movimento.py`, ajustar a lógica na função `_validar_pode_listar` para que a condição de cor aceite cores **diferentes** (`carta_origem.cor_carta() != carta_destino.cor_carta()`) ao invés de rejeitar a jogada quando as cores forem diferentes (ou seja, corrigir a relação de igualdade que estava causando o bug de cores alternadas).

## 2. Testes de Regressão

- [x] 2.1 Em `backend/testes/teste_jogo.py`, verificar e caso necessário adaptar testes existentes que testem as movimentações envolvendo listas (M1, M2, M3) para garantir que eles validem as movimentações com as regras de cores corretas.
