"""Script manual de depuração para cores e validação lista (não é suíte pytest)."""

from motor.estado_jogo import EstadoJogo
from modelo.carta_baralho import CartaBaralho
from motor.regras_movimento import _validar_pode_listar

c1 = CartaBaralho(12, "c", status_carta=True) # Q♥
c2 = CartaBaralho(13, "p", status_carta=True) # K♣

print(f"c1: {c1.cor_carta()}, c2: {c2.cor_carta()}")
print(_validar_pode_listar(c1, EstadoJogo().listas_tableau[0])) # empty list

lista = EstadoJogo().listas_tableau[0]
lista.inserir_final(c2)
print(_validar_pode_listar(c1, lista))
