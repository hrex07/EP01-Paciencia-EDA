"""Gerenciamento de sessões do jogo no Google Cloud Firestore.

Lê e grava o :class:`motor.estado_jogo.EstadoJogo` serializado, com janela
deslizante de expiração (TTL) por documento de sessão.
"""

import os
import time
from typing import Optional

from google.cloud import firestore
from motor.estado_jogo import EstadoJogo

# Configurações do Firestore
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "ipt-master")
DATABASE_ID = os.getenv("FIRESTORE_DATABASE", "main")
COLECAO_SESSOES = "sessoes"

# Tempo de expiração (TTL) em segundos. Ex: 2 horas = 7200s
TTL_SESSAO_SEGUNDOS = 7200

# Inicializa o cliente Firestore apontando para a base configurada
db = firestore.Client(project=PROJECT_ID, database=DATABASE_ID)


def obter_estado(id_sessao: str) -> Optional[EstadoJogo]:
    """Carrega o estado da partida a partir do Firestore.

    Args:
        id_sessao: UUID do documento na coleção configurada.

    Returns:
        Instância de ``EstadoJogo`` desserializada, ou ``None`` se o documento
        não existir ou tiver expirado (e for removido).
    """
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
    """Persiste o estado completo da partida (upsert por ``id_sessao``).

    Args:
        estado: Partida atual; ``estado.serializar_completo()`` é gravado
            no campo ``estado_completo``, com carimbo de acesso e expiração.
    """
    agora = time.time()
    dados_sessao = {
        "id_sessao": estado.id_sessao,
        "ultimo_acesso": agora,
        "expira_em": agora + TTL_SESSAO_SEGUNDOS,
        "estado_completo": estado.serializar_completo()
    }
    
    doc_ref = db.collection(COLECAO_SESSOES).document(estado.id_sessao)
    doc_ref.set(dados_sessao)
