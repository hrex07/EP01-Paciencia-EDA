import React from 'react';
import { CartaBaralho } from '../../tipos/tipos';
import { CartaVisual } from './CartaVisual';

interface FundacaoPilhaProps {
  naipe: string;
  cartas: CartaBaralho[];
  onPilhaClick: () => void;
  destacada: boolean;
}

export const FundacaoPilha: React.FC<FundacaoPilhaProps> = ({ naipe, cartas, onPilhaClick, destacada }) => {
  const topo = cartas.length > 0 ? cartas[0] : null; // Topo está na frente (índice 0)

  const corFundo = naipe === 'c' || naipe === 'o' ? 'text-red-500/20' : 'text-gray-500/20';
  const simbolos: Record<string, string> = { c: '♥', o: '♦', p: '♣', e: '♠' };

  return (
    <div
      className={`relative w-20 h-28 rounded-md flex items-center justify-center cursor-pointer transition-all duration-200
        ${destacada ? 'ring-4 ring-green-400 bg-green-500/10' : 'border-2 border-white/30 bg-black/20 hover:bg-white/10'}
      `}
      onClick={onPilhaClick}
    >
      {!topo && (
        <span className={`text-4xl font-bold ${corFundo}`}>{simbolos[naipe]}</span>
      )}
      
      {topo && (
        <div className="absolute inset-0 pointer-events-none">
          <CartaVisual carta={topo} style={{ position: 'absolute', top: 0, left: 0 }} />
        </div>
      )}
    </div>
  );
};
