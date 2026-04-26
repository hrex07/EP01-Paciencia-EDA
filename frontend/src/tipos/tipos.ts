export interface CartaBaralho {
  numero_carta?: number;
  naipe_carta?: "c" | "o" | "p" | "e";
  status_carta: boolean;
  texto: string;
  cor?: "vermelha" | "preta";
}

export interface PassoExecucao {
  passo_numero: number;
  pseudo_codigo: string;
  descricao_acao: string;
  indices_trocados?: number[];
  indices_comparados?: number[];
  houve_troca?: boolean;
  estado_vetor?: string[];
  profundidade_recursao?: number;
  variaveis_estado?: Record<string, any>;
}

export interface StreakJogo {
  sequencia_atual: number;
  maior_sequencia: number;
  nivel_efeito: "basico" | "bom" | "otimo" | "confetti" | "incrivel" | "mestre" | "vitoria" | "erro";
  mensagem_educacional: string;
}

export interface EstatisticasJogo {
  total_jogadas: number;
  sequencia_atual: number;
  maior_sequencia: number;
  estruturas_resumo?: string;
}

export interface EstruturasJogo {
  fila_compra: CartaBaralho[];
  pilhas_fundacao: Record<string, CartaBaralho[]>;
  listas_tableau: CartaBaralho[][];
}

export interface EstadoJogo {
  id_sessao: string;
  jogo_vencido: boolean;
  estatisticas: EstatisticasJogo;
  estruturas: EstruturasJogo;
}

/** Corpo de POST /jogo/{id}/mover — espelha `api.schemas.RequestMoverCarta`. */
export interface RequestMoverCarta {
  tipo_movimento: number;
  naipe_destino?: string;
  naipe_origem?: string;
  indice_lista_origem?: number;
  indice_lista_destino?: number;
  posicao_corte?: number;
}

/** Carta na API de algoritmos/estruturas — espelha `api.schemas.CartaEntrada`. */
export interface CartaEntrada {
  numero_carta: number;
  naipe_carta: string;
  status_carta?: boolean;
}

export interface ResponseNovoJogo {
  id_sessao: string;
  estado_jogo: EstadoJogo;
  log_preparacao?: PassoExecucao[];
}

export interface OperacaoRealizada {
  operacao_nome: string;
  algoritmo_nome?: string; // Para algoritmos de ordenação
  estrutura_tipo: string;
  nome_estrutura: string;
  operacao_sucesso: boolean;
  valor_retornado?: any;
  quantidade_elementos?: number;
  passos_executados: PassoExecucao[];
  mensagem_erro?: string;
}

export interface ResponseMovimento {
  jogada_valida: boolean;
  motivo_rejeicao?: string;
  operacoes_realizadas: OperacaoRealizada[];
  estado_jogo?: EstadoJogo;
  streak?: StreakJogo;
}

export interface TipoMovimento {
  id: number;
  nome: string;
  descricao: string;
}

export interface ResponseAlgoritmo {
  algoritmo_nome: string;
  vetor_cartas: CartaBaralho[];
  total_comparacoes?: number;
  total_trocas?: number;
  tempo_execucao_ms: number;
  passos_executados: PassoExecucao[];
}
