import React, { useState, useRef } from 'react';
import { flushSync } from 'react-dom';
import type { EstadoJogo, OperacaoRealizada, StreakJogo } from '../../tipos/tipos';
import { jogoService } from '../../servicos/apiJogo';
import { FilaCompra } from './FilaCompra';
import { FundacaoPilha } from './FundacaoPilha';
import { ColunaTablau } from './ColunaTablau';

interface MesaJogoProps {
  idSessao: string;
  /** Única fonte de verdade: atualizada pelo Pai a partir do `estado_jogo` de cada resposta. */
  estadoJogo: EstadoJogo;
  onSincronizarEstado: (estado: EstadoJogo) => void;
  onOperacoesRealizadas: (ops: OperacaoRealizada[], streak?: StreakJogo) => void;
}

type Origem = 
  | { tipo: 'fila' }
  | { tipo: 'pilha'; naipe: string }
  | { tipo: 'lista'; indice: number; posicaoCorte: number };

export const MesaJogo: React.FC<MesaJogoProps> = ({
  idSessao,
  estadoJogo,
  onSincronizarEstado,
  onOperacoesRealizadas,
}) => {
  const [origemSelecionada, setOrigemSelecionada] = useState<Origem | null>(null);
  const [loading, setLoading] = useState(false);
  const emJogadaRef = useRef(false);
  /**
   * Uma fila de Promises por instância: múltiplas chamadas a `executarMovimento` (ex.: reentrada
   * de evento antes de `setLoading` pintar) executam o POST em série — evita dois POSTs com o
   * mesmo payload e 500/200 alternado no servidor.
   */
  const cadeiaMovimentoRef = useRef<Promise<unknown>>(Promise.resolve());

  const naipes = ['e', 'c', 'p', 'o']; // Espadas, Copas, Paus, Ouros

  const executarMovimento = (
    tipoMovimento: number,
    naipeDestino?: string,
    naipeOrigem?: string,
    indiceListaOrigem?: number,
    indiceListaDestino?: number,
    posicaoCorte?: number
  ) => {
    const p = cadeiaMovimentoRef.current.then(async () => {
      emJogadaRef.current = true;
      flushSync(() => {
        setLoading(true);
      });
      try {
        const result = await jogoService.moverCarta(idSessao, {
          tipo_movimento: tipoMovimento,
          naipe_destino: naipeDestino,
          naipe_origem: naipeOrigem,
          indice_lista_origem: indiceListaOrigem,
          indice_lista_destino: indiceListaDestino,
          posicao_corte: posicaoCorte,
        });

        if (result.estado_jogo) {
          onSincronizarEstado(result.estado_jogo);
        } else {
          console.warn("Resposta /mover sem estado_jogo — UI pode ficar dessincronizada.");
        }

        if (!result.jogada_valida) {
          console.warn("Jogada inválida:", result.motivo_rejeicao);
        }

        onOperacoesRealizadas(result.operacoes_realizadas, result.streak);
      } catch (e) {
        console.error(e);
      } finally {
        emJogadaRef.current = false;
        setLoading(false);
        setOrigemSelecionada(null);
      }
    });
    cadeiaMovimentoRef.current = p.then(
      () => undefined,
      () => undefined,
    );
    return p;
  };

  const handleFilaClick = () => {
    if (loading || emJogadaRef.current) return;
    if (origemSelecionada && origemSelecionada.tipo === 'fila') {
      // Reposicionar
      executarMovimento(1);
    } else {
      // Selecionar topo da fila
      setOrigemSelecionada({ tipo: 'fila' });
    }
  };

  const handlePilhaClick = (naipe: string) => {
    if (loading || emJogadaRef.current) return;
    if (!origemSelecionada) {
      // Se clica em uma pilha sem origem, selecionamos o topo da pilha
      if (estadoJogo.estruturas.pilhas_fundacao[naipe].length > 0) {
        setOrigemSelecionada({ tipo: 'pilha', naipe });
      }
    } else {
      // Já tem origem, tenta mover para esta pilha
      if (origemSelecionada.tipo === 'fila') {
        executarMovimento(2, naipe); // Fila -> Pilha
      } else if (origemSelecionada.tipo === 'lista') {
        executarMovimento(5, naipe, undefined, origemSelecionada.indice); // Lista -> Pilha
      } else if (origemSelecionada.tipo === 'pilha') {
        setOrigemSelecionada(null); // Pilha -> Pilha não existe nas regras
      }
    }
  };

  const handleListaClick = (indiceDestino: number, posicaoCorte?: number) => {
    if (loading || emJogadaRef.current) return;
    if (!origemSelecionada) {
      // Se não tem origem, selecionamos da lista (requer posicaoCorte)
      if (posicaoCorte !== undefined) {
        setOrigemSelecionada({ tipo: 'lista', indice: indiceDestino, posicaoCorte });
      }
    } else {
      // Tentar mover origem selecionada para esta lista
      if (origemSelecionada.tipo === 'fila') {
        executarMovimento(3, undefined, undefined, undefined, indiceDestino); // Fila -> Lista
      } else if (origemSelecionada.tipo === 'pilha') {
        executarMovimento(4, undefined, origemSelecionada.naipe, undefined, indiceDestino); // Pilha -> Lista
      } else if (origemSelecionada.tipo === 'lista') {
        if (origemSelecionada.indice === indiceDestino) {
          // Clique na mesma lista, cancela
          setOrigemSelecionada(null);
        } else {
          executarMovimento(6, undefined, undefined, origemSelecionada.indice, indiceDestino, origemSelecionada.posicaoCorte); // Lista -> Lista
        }
      }
    }
  };

  const bgStyle = "bg-green-800 min-h-[600px] w-full p-6 rounded-xl shadow-inner relative";

  return (
    <div
      className={bgStyle}
      style={{ pointerEvents: loading ? 'none' : 'auto' }}
      aria-busy={loading}
    >
      {estadoJogo.jogo_vencido && (
        <div className="absolute inset-0 bg-black/60 z-50 flex items-center justify-center rounded-xl backdrop-blur-sm">
          <div className="text-center text-white">
            <h1 className="text-6xl font-bold mb-4 text-yellow-400 drop-shadow-lg">Você Venceu!</h1>
            <p className="text-2xl">Parabéns por completar a partida.</p>
          </div>
        </div>
      )}

      {/* Topo: Fila e Pilhas */}
      <div className="flex justify-between mb-12 h-32">
        <div className="flex items-start">
          <FilaCompra
            fila={estadoJogo.estruturas.fila_compra}
            onCartaClick={handleFilaClick}
            selecionada={origemSelecionada?.tipo === 'fila'}
            destacada={false}
          />
        </div>
        
        <div className="flex space-x-4">
          {naipes.map((naipe) => (
            <FundacaoPilha
              key={naipe}
              naipe={naipe}
              cartas={estadoJogo.estruturas.pilhas_fundacao[naipe]}
              onPilhaClick={() => handlePilhaClick(naipe)}
              destacada={false}
            />
          ))}
        </div>
      </div>

      {/* Base: Tableau (Listas Ligadas) */}
      <div className="flex justify-between space-x-2">
        {estadoJogo.estruturas.listas_tableau.map((coluna, index) => (
          <ColunaTablau
            key={index}
            indice={index}
            cartas={coluna}
            onCartaClick={(posicaoCorte) => handleListaClick(index, posicaoCorte)}
            onColunaVaziaClick={() => handleListaClick(index)}
            indiceSelecionada={
              origemSelecionada?.tipo === 'lista' && origemSelecionada.indice === index
                ? origemSelecionada.posicaoCorte
                : null
            }
            destacada={false}
          />
        ))}
      </div>
    </div>
  );
};
