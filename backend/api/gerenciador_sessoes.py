"""Gerenciamento de sessões do jogo no Google Cloud Firestore."""

import os
import time
from typing import Optional

from google.cloud import firestore
from motor.estado_jogo import EstadoJogo

# Configurações do Firestore
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "ipt-master")
COLECAO_SESSOES = "sessoes"

# Tempo de expiração (TTL) em segundos. Ex: 2 horas = 7200s
TTL_SESSAO_SEGUNDOS = 7200

# Inicializa o cliente Firestore apontando para a base 'main'
db = firestore.Client(project=PROJECT_ID, database="main")


def obter_estado(id_sessao: str) -> Optional[EstadoJogo]:
    """Retorna o estado do jogo do Firestore ou None se não existir / expirou."""
    doc_ref = db.collection(COLECAO_SESSOES).document(id_sessao)
    doc = doc_ref.get()
    
    if not doc.exists:
        return None
        
    dados = doc.to_dict()
    
    # Verificação manual de expiração (além do TTL nativo do Firestore se configurado)
    agora = time.time()
    if dados.get("expira_em", 0) < agora:
        # Opcional: deletar se expirado
        doc_ref.delete()
        return None
        
    # Atualiza o tempo de expiração no Firestore (slide window)
    doc_ref.update({"expira_em": agora + TTL_SESSAO_SEGUNDOS})
    
    return EstadoJogo.desserializar(dados["estado_completo"])


def salvar_estado(estado: EstadoJogo) -> None:
    """Salva o estado serializado no Firestore."""
    agora = time.time()
    dados_sessao = {
        "id_sessao": estado.id_sessao,
        "ultimo_acesso": agora,
        "expira_em": agora + TTL_SESSAO_SEGUNDOS,
        "estado_completo": estado.serializar_completo()
    }
    
    doc_ref = db.collection(COLECAO_SESSOES).document(estado.id_sessao)
    doc_ref.set(dados_sessao)
