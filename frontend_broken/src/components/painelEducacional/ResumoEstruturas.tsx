import React from 'react';
import { EstadoJogo } from '../../tipos/tipos';
import { Layers, AlignJustify, List } from 'lucide-react';

interface ResumoEstruturasProps {
  estado: EstadoJogo;
}

export const ResumoEstruturas: React.FC<ResumoEstruturasProps> = ({ estado }) => {
  if (!estado || !estado.estruturas) return null;

  const totalPilhas = Object.keys(estado.estruturas.pilhas_fundacao).length;
  const cartasPilhas = Object.values(estado.estruturas.pilhas_fundacao).reduce((acc, p) => acc + p.length, 0);

  const totalListas = estado.estruturas.listas_tableau.length;
  const cartasListas = estado.estruturas.listas_tableau.reduce((acc, l) => acc + l.length, 0);

  const cartasFila = estado.estruturas.fila_compra.length;

  return (
    <div className="grid grid-cols-3 gap-2">
      <div className="bg-neutral-800 border border-white/5 rounded-md p-3 flex flex-col items-center justify-center text-center">
        <AlignJustify className="text-green-400 mb-1" size={20} />
        <span className="text-xs text-gray-400 font-medium">Fila (1)</span>
        <span className="text-sm font-bold text-gray-200">{cartasFila} cartas</span>
      </div>

      <div className="bg-neutral-800 border border-white/5 rounded-md p-3 flex flex-col items-center justify-center text-center">
        <Layers className="text-blue-400 mb-1" size={20} />
        <span className="text-xs text-gray-400 font-medium">Pilhas ({totalPilhas})</span>
        <span className="text-sm font-bold text-gray-200">{cartasPilhas} cartas</span>
      </div>

      <div className="bg-neutral-800 border border-white/5 rounded-md p-3 flex flex-col items-center justify-center text-center">
        <List className="text-purple-400 mb-1" size={20} />
        <span className="text-xs text-gray-400 font-medium">Listas ({totalListas})</span>
        <span className="text-sm font-bold text-gray-200">{cartasListas} cartas</span>
      </div>
    </div>
  );
};
