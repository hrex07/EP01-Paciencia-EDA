import React from 'react';
import type { CartaBaralho } from '../../tipos/tipos';
import { CartaVisual } from './CartaVisual';

interface ColunaTablauProps {
  indice: number;
  cartas: CartaBaralho[];
  onCartaClick: (posicaoCorte: number) => void;
  onColunaVaziaClick: () => void;
  indiceSelecionada: number | null;
  destacada: boolean;
}

export const ColunaTablau: React.FC<ColunaTablauProps> = ({
  indice,
  cartas,
  onCartaClick,
  onColunaVaziaClick,
  indiceSelecionada,
  destacada
}) => {
  const vazia = cartas.length === 0;

  return (
    <div className="relative w-20 flex-shrink-0" style={{ minHeight: '300px' }}>
      {vazia ? (
        <div
          className={`w-20 h-28 border-2 border-white/20 rounded-md cursor-pointer transition-all
            ${destacada ? 'ring-4 ring-green-400 bg-green-500/10' : 'bg-black/10 hover:bg-white/10'}
          `}
          onClick={onColunaVaziaClick}
        />
      ) : (
        <div className="relative">
          {cartas.map((carta, index) => {
            const isSelecionada = indiceSelecionada === index;
            // Se esta carta ou alguma abaixo dela está selecionada, ela sobe junto (visual de "bloco" ou sublista)
            const fazParteDaSelecao = indiceSelecionada !== null && index >= indiceSelecionada;
            
            // Distância vertical para cascata
            const topOffset = index * 24;

            return (
              <div
                key={`${carta.numero_carta}-${carta.naipe_carta}-${index}`}
                style={{
                  position: 'absolute',
                  top: topOffset,
                  left: 0,
                  zIndex: index,
                  transition: 'transform 0.2s',
                  transform: fazParteDaSelecao ? 'translateY(-10px)' : 'none'
                }}
                className={destacada && index === cartas.length - 1 ? 'ring-4 ring-green-400 rounded-md' : ''}
              >
                <CartaVisual
                  carta={carta}
                  selecionada={isSelecionada}
                  onClick={() => carta.status_carta ? onCartaClick(index) : undefined}
                />
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
