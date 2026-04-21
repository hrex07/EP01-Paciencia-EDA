import React from 'react';
import type { CartaBaralho } from '../../tipos/tipos';
import { CartaVisual } from './CartaVisual';

interface FilaCompraProps {
  fila: CartaBaralho[];
  onCartaClick: () => void;
  selecionada: boolean;
  destacada: boolean;
}

export const FilaCompra: React.FC<FilaCompraProps> = ({ fila, onCartaClick, selecionada, destacada }) => {
  const vazia = fila.length === 0;
  // A carta da frente (topo visível)
  const cartaFrente = fila.length > 0 ? fila[0] : null;

  return (
    <div className="relative w-20 h-28 mr-4">
      {vazia ? (
        <div className="w-full h-full border-2 border-dashed border-gray-400/50 rounded-md flex items-center justify-center bg-black/10">
          <span className="text-gray-400 text-xs">Fila (0)</span>
        </div>
      ) : (
        <div className="relative">
          {/* Representar pilha de cartas da fila */}
          {fila.length > 1 && (
            <div className="absolute top-1 -left-1 w-20 h-28 bg-blue-800 rounded-md shadow-sm border border-white/20" />
          )}
          {fila.length > 2 && (
            <div className="absolute top-2 -left-2 w-20 h-28 bg-blue-800 rounded-md shadow-sm border border-white/20" />
          )}
          
          <div className="absolute top-0 left-0 z-10">
            {cartaFrente && (
              <CartaVisual
                carta={cartaFrente}
                selecionada={selecionada}
                destacada={destacada}
                onClick={onCartaClick}
              />
            )}
          </div>
          <div className="absolute -bottom-6 left-0 w-full text-center text-xs text-white bg-black/40 rounded px-1">
            {fila.length} cartas
          </div>
        </div>
      )}
    </div>
  );
};
