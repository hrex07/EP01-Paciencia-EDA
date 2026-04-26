import React from 'react';
import { motion } from 'framer-motion';
import type { CartaBaralho } from '../../tipos/tipos';

interface CartaVisualProps {
  carta: CartaBaralho;
  selecionada?: boolean;
  destacada?: boolean;
  onClick?: () => void;
  style?: React.CSSProperties;
  /** Atributos de teste (Playwright) — índice da carta na coluna. */
  dataCartaIndice?: number;
  dataColunaIndice?: number;
}

const NaipeIcone = ({ naipe, cor }: { naipe: string; cor: string }) => {
  const simbolos: Record<string, string> = {
    c: '♥',
    o: '♦',
    p: '♣',
    e: '♠',
  };
  return <span className={cor === 'vermelha' ? 'text-red-600' : 'text-gray-900'}>{simbolos[naipe]}</span>;
};

export const CartaVisual: React.FC<CartaVisualProps> = ({
  carta,
  selecionada = false,
  destacada = false,
  onClick,
  style = {},
  dataCartaIndice,
  dataColunaIndice,
}) => {
  const { numero_carta, naipe_carta, status_carta, cor } = carta;
  
  // Rótulo do valor
  let rotulo = "";
  if (status_carta && numero_carta !== undefined) {
    rotulo = numero_carta.toString();
    if (numero_carta === 1) rotulo = 'A';
    if (numero_carta === 11) rotulo = 'J';
    if (numero_carta === 12) rotulo = 'Q';
    if (numero_carta === 13) rotulo = 'K';
  }

  const textColor = cor === 'vermelha' ? 'text-red-600' : 'text-gray-900';

  const onClickComum = (e: React.MouseEvent) => {
    e.stopPropagation();
    onClick?.();
  };

  return (
    <motion.div
      data-carta-indice={dataCartaIndice}
      data-columna-indice={dataColunaIndice}
      onClick={onClick ? onClickComum : undefined}
      style={style}
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      whileHover={status_carta && onClick ? { y: -5, boxShadow: "0px 10px 20px rgba(0,0,0,0.1)" } : {}}
      className={`
        relative w-20 h-28 rounded-md shadow-md cursor-pointer select-none transition-all
        ${selecionada ? 'ring-4 ring-blue-500 transform -translate-y-2' : ''}
        ${destacada ? 'ring-4 ring-green-400' : 'ring-1 ring-gray-200'}
        ${status_carta ? 'bg-white' : 'bg-blue-800 bg-[radial-gradient(#1e3a8a_1px,transparent_1px)] [background-size:8px_8px]'}
      `}
    >
      {status_carta && naipe_carta !== undefined ? (
        <div className="pointer-events-none absolute inset-0 flex flex-col p-1.5 justify-between">
          {/* Top Left */}
          <div className="flex flex-col items-center self-start leading-none">
            <span className={`text-lg font-bold ${textColor}`}>{rotulo}</span>
            <NaipeIcone naipe={naipe_carta} cor={cor || 'preta'} />
          </div>
          
          {/* Center */}
          <div className="absolute inset-0 flex items-center justify-center text-3xl opacity-80">
            <NaipeIcone naipe={naipe_carta} cor={cor || 'preta'} />
          </div>
          
          {/* Bottom Right */}
          <div className="flex flex-col items-center self-end leading-none transform rotate-180">
            <span className={`text-lg font-bold ${textColor}`}>{rotulo}</span>
            <NaipeIcone naipe={naipe_carta} cor={cor || 'preta'} />
          </div>
        </div>
      ) : (
        <div className="pointer-events-none absolute inset-1 border-2 border-white/20 rounded-sm"></div>
      )}
    </motion.div>
  );
};
