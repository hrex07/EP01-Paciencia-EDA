from motor.estado_jogo import EstadoJogo
from modelo.carta_baralho import CartaBaralho

def test_persistencia_pilhas_fundacao_multiplas_cartas() -> None:
    # 1. Cria estado e adiciona cartas na pilha de copas ('c')
    estado = EstadoJogo()
    pilha_c = estado.pilhas_fundacao['c']
    
    # Adiciona Ás, 2 e 3 de Copas
    pilha_c.empilhar(CartaBaralho(1, 'c', status_carta=True), registrar_passos=False)
    pilha_c.empilhar(CartaBaralho(2, 'c', status_carta=True), registrar_passos=False)
    pilha_c.empilhar(CartaBaralho(3, 'c', status_carta=True), registrar_passos=False)
    
    assert pilha_c.obter_tamanho() == 3
    assert pilha_c.elemento_topo.dados_carta.numero_carta == 3
    
    # 2. Serializa para DB
    dados_db = estado.serializar_completo()
    
    # 3. Desserializa
    recuperado = EstadoJogo.desserializar(dados_db)
    pilha_recup = recuperado.pilhas_fundacao['c']
    
    # 4. Verifica integridade
    assert pilha_recup.obter_tamanho() == 3, f"Esperado 3 cartas, obteve {pilha_recup.obter_tamanho()}"
    assert pilha_recup.elemento_topo.dados_carta.numero_carta == 3, "O topo deveria ser o 3 de Copas"
    
    # Verifica a ordem desempilhando
    assert pilha_recup.desempilhar(registrar_passos=False)['valor_retornado'].numero_carta == 3
    assert pilha_recup.desempilhar(registrar_passos=False)['valor_retornado'].numero_carta == 2
    assert pilha_recup.desempilhar(registrar_passos=False)['valor_retornado'].numero_carta == 1
    assert pilha_recup.esta_vazia()
