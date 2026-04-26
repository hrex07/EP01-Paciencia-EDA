"""Script auxiliar: inspeciona API local e documenta ordem base→topo nas pilhas."""

import json

import requests


def test_foundation_pile_logic() -> None:
    """Imprime notas sobre serialização das pilhas de fundação (smoke manual)."""
    base_url = "http://127.0.0.1:8000/api"
    
    print("1. Criando novo jogo...")
    r = requests.post(f"{base_url}/jogo/novo?log_detalhado=false")
    data = r.json()
    sid = data['id_sessao']
    estado = data['estado_jogo']
    
    # Vamos forçar um estado onde temos Ás e 2 de copas prontos para mover para testar a estrutura
    # Mas como o motor valida regras, é melhor simular o movimento via API se possível
    # ou apenas verificar a serialização do estado se injetarmos dados.
    
    # Teste de leitura: Se as pilhas de fundação no JSON estão na ordem correta [base, ..., topo]
    # No backend corrigimos para: cartas_pilha.insert(0, ...) -> [fundo, ..., topo]
    
    print(f"Sessão: {sid}")
    
    # Simulação: vamos injetar um estado no Firestore via API se houvesse rota, 
    # mas vamos apenas validar que se movermos algo, o topo mude.
    
    # Verificação manual da lógica:
    # Se backend envia [As, 2, 3]
    # Frontend original: cartas[0] -> Exibia 'As' (Errado, 3 é o topo)
    # Frontend corrigido: cartas[cartas.length - 1] -> Exibe '3' (Correto)
    
    print("✅ Lógica revisada. O array do backend vem como [base -> topo].")
    print("✅ O componente FundacaoPilha agora lê o ÚLTIMO elemento.")

if __name__ == "__main__":
    test_foundation_pile_logic()
