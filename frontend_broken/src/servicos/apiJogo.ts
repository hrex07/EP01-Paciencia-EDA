import axios from 'axios';
import { ResponseNovoJogo, EstadoJogo, ResponseMovimento, CartaBaralho, ResponseAlgoritmo } from '../tipos/tipos';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const jogoService = {
  async criarNovoJogo(logDetalhado: boolean = true): Promise<ResponseNovoJogo> {
    const response = await api.post(`/jogo/novo?log_detalhado=${logDetalhado}`);
    return response.data;
  },

  async consultarEstado(idSessao: string): Promise<EstadoJogo> {
    const response = await api.get(`/jogo/${idSessao}/estado`);
    return response.data;
  },

  async moverCarta(
    idSessao: string,
    tipoMovimento: number,
    naipeDestino?: string,
    naipeOrigem?: string,
    indiceListaOrigem?: number,
    indiceListaDestino?: number,
    posicaoCorte?: number
  ): Promise<ResponseMovimento> {
    const payload = {
      tipo_movimento: tipoMovimento,
      naipe_destino: naipeDestino,
      naipe_origem: naipeOrigem,
      indice_lista_origem: indiceListaOrigem,
      indice_lista_destino: indiceListaDestino,
      posicao_corte: posicaoCorte,
    };
    
    // Removendo undefined keys
    const cleanPayload = Object.fromEntries(Object.entries(payload).filter(([_, v]) => v !== undefined));
    
    const response = await api.post(`/jogo/${idSessao}/mover`, cleanPayload);
    return response.data;
  },
};

export const algoritmoService = {
  async embaralhar(metodo: 'iterativo' | 'recursivo', cartas?: CartaBaralho[]): Promise<ResponseAlgoritmo> {
    const response = await api.post(`/algoritmos/embaralhar?metodo=${metodo}`, cartas);
    return response.data;
  },

  async ordenar(metodo: 'bubble' | 'merge' | 'quick', cartas?: CartaBaralho[]): Promise<ResponseAlgoritmo> {
    const response = await api.post(`/algoritmos/ordenar?metodo=${metodo}`, cartas);
    return response.data;
  },

  async comparar(cartas?: CartaBaralho[]): Promise<ResponseAlgoritmo[]> {
    const response = await api.post(`/algoritmos/comparar`, cartas);
    return response.data;
  }
};
