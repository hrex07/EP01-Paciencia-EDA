import axios from 'axios';
import type {
  ResponseNovoJogo,
  EstadoJogo,
  ResponseMovimento,
  ResponseAlgoritmo,
  RequestMoverCarta,
  CartaEntrada,
} from '../tipos/tipos';

// Em dev, base relativa + proxy do Vite (vite.config) evita CORS (localhost vs 127.0.0.1).
// Em produção, defina VITE_API_URL com a URL pública do backend, ex.: https://api.exemplo.com/api
const API_URL = import.meta.env.VITE_API_URL || '/api';

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

  /**
   * POST /jogo/{id}/mover — `tipo_movimento` (1–6) é sempre obrigatório no JSON.
   * Campos opcionais omitidos se `undefined` (nunca omitir `tipo_movimento`).
   */
  async moverCarta(idSessao: string, corpo: RequestMoverCarta): Promise<ResponseMovimento> {
    if (
      typeof corpo.tipo_movimento !== 'number' ||
      !Number.isInteger(corpo.tipo_movimento) ||
      corpo.tipo_movimento < 1 ||
      corpo.tipo_movimento > 6
    ) {
      throw new Error('RequestMoverCarta: tipo_movimento deve ser inteiro de 1 a 6.');
    }
    const { tipo_movimento, naipe_destino, naipe_origem, indice_lista_origem, indice_lista_destino, posicao_corte } =
      corpo;
    const cleanPayload: Record<string, string | number> = { tipo_movimento };
    if (naipe_destino !== undefined) cleanPayload.naipe_destino = naipe_destino;
    if (naipe_origem !== undefined) cleanPayload.naipe_origem = naipe_origem;
    if (indice_lista_origem !== undefined) cleanPayload.indice_lista_origem = indice_lista_origem;
    if (indice_lista_destino !== undefined) cleanPayload.indice_lista_destino = indice_lista_destino;
    if (posicao_corte !== undefined) cleanPayload.posicao_corte = posicao_corte;

    const response = await api.post(`/jogo/${idSessao}/mover`, cleanPayload);
    return response.data as ResponseMovimento;
  },
};

export const algoritmoService = {
  async embaralhar(metodo: 'iterativo' | 'recursivo', cartas?: CartaEntrada[] | null): Promise<ResponseAlgoritmo> {
    const response = await api.post(`/algoritmos/embaralhar?metodo=${metodo}`, cartas ?? null);
    return response.data;
  },

  async ordenar(metodo: 'bubble' | 'merge' | 'quick', cartas?: CartaEntrada[] | null): Promise<ResponseAlgoritmo> {
    const response = await api.post(`/algoritmos/ordenar?metodo=${metodo}`, cartas ?? null);
    return response.data;
  },

  async comparar(cartas?: CartaEntrada[] | null): Promise<ResponseAlgoritmo[]> {
    const response = await api.post(`/algoritmos/comparar`, cartas ?? null);
    return response.data;
  }
};
