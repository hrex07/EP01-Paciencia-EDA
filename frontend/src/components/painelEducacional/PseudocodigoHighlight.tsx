import React, { useEffect, useState } from 'react';
import type { OperacaoRealizada } from '../../tipos/tipos';
import { Play, Pause, SkipBack, SkipForward, FastForward } from 'lucide-react';

interface PseudocodigoHighlightProps {
  operacao: OperacaoRealizada | null;
  onPassoChange: (passoAtual: number) => void;
}

export const PseudocodigoHighlight: React.FC<PseudocodigoHighlightProps> = ({ 
  operacao, 
  onPassoChange 
}) => {
  const [passoAtivoIndex, setPassoAtivoIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [velocidade, setVelocidade] = useState(1000); // ms por passo

  useEffect(() => {
    // Reset ao mudar de operação
    setPassoAtivoIndex(0);
    setIsPlaying(false);
    if (operacao && (operacao.passos_executados || []).length > 0) {
      onPassoChange(1); // 1-based no componente pai
    }
  }, [operacao]);

  useEffect(() => {
    let interval: number;
    if (isPlaying && operacao && passoAtivoIndex < (operacao.passos_executados || []).length - 1) {
      interval = setInterval(() => {
        setPassoAtivoIndex(prev => {
          const next = prev + 1;
          onPassoChange(next + 1);
          if (next >= (operacao.passos_executados || []).length - 1) {
            setIsPlaying(false);
          }
          return next;
        });
      }, velocidade);
    } else if (isPlaying && operacao && passoAtivoIndex >= (operacao.passos_executados || []).length - 1) {
      setIsPlaying(false);
    }
    return () => clearInterval(interval);
  }, [isPlaying, passoAtivoIndex, operacao, velocidade, onPassoChange]);

  const handlePrev = () => {
    if (passoAtivoIndex > 0) {
      setPassoAtivoIndex(prev => {
        onPassoChange(prev); // prev é 1-based, prev-1+1
        return prev - 1;
      });
    }
  };

  const handleNext = () => {
    if (operacao && passoAtivoIndex < (operacao.passos_executados || []).length - 1) {
      setPassoAtivoIndex(prev => {
        onPassoChange(prev + 2);
        return prev + 1;
      });
    }
  };

  if (!operacao) {
    return (
      <div className="flex items-center justify-center h-full bg-neutral-900 border border-white/10 rounded-lg text-gray-500 text-sm">
        Selecione uma operação no log para inspecionar.
      </div>
    );
  }

  const passos = operacao.passos_executados || [];
  const passoAtivo = passos[passoAtivoIndex] || null;

  return (
    <div className="flex flex-col h-full bg-neutral-900 border border-white/10 rounded-lg overflow-hidden flex-1 min-h-0">
      <div className="flex items-center justify-between p-3 bg-neutral-800 border-b border-white/10 shrink-0">
        <h3 className="font-semibold text-sm text-gray-300">
          Pseudocódigo: <span className="text-indigo-400 font-mono">{operacao.operacao_nome}</span>
        </h3>
        <div className="flex items-center space-x-1">
          <button onClick={handlePrev} disabled={passoAtivoIndex === 0} className="p-1 hover:bg-white/10 rounded text-gray-400 disabled:opacity-30">
            <SkipBack size={16} />
          </button>
          <button onClick={() => setIsPlaying(!isPlaying)} className="p-1 hover:bg-white/10 rounded text-indigo-400">
            {isPlaying ? <Pause size={16} /> : <Play size={16} />}
          </button>
          <button onClick={handleNext} disabled={passoAtivoIndex === passos.length - 1} className="p-1 hover:bg-white/10 rounded text-gray-400 disabled:opacity-30">
            <SkipForward size={16} />
          </button>
          
          <div className="w-px h-4 bg-white/20 mx-1" />
          
          <button 
            onClick={() => setVelocidade(v => v === 1000 ? 400 : v === 400 ? 100 : 1000)}
            className="flex items-center px-2 py-1 bg-black/30 rounded text-xs text-gray-400 hover:text-white"
            title="Velocidade"
          >
            <FastForward size={14} className="mr-1" />
            {velocidade === 1000 ? '1x' : velocidade === 400 ? '2x' : '5x'}
          </button>
        </div>
      </div>

      {/* Código Fonte */}
      <div className="flex-1 overflow-auto p-4 bg-black/40 font-mono text-sm relative custom-scrollbar">
        <div className="absolute top-4 left-4 bottom-4 w-6 border-r border-white/10 text-right pr-2 text-gray-600 select-none">
          {passos.map((_, i) => (
            <div key={i}>{i + 1}</div>
          ))}
        </div>
        <div className="pl-8">
          {passos.map((passo, i) => {
            const isAtivo = i === passoAtivoIndex;
            const isPassado = i < passoAtivoIndex;
            
            return (
              <div 
                key={i} 
                className={`
                  py-0.5 px-2 -mx-2 rounded whitespace-pre transition-colors duration-200
                  ${isAtivo ? 'bg-indigo-900/50 text-indigo-200 border-l-2 border-indigo-400' : 
                    isPassado ? 'text-gray-400' : 'text-gray-500'}
                `}
              >
                {passo.pseudo_codigo}
              </div>
            );
          })}
        </div>
      </div>

      {/* Variáveis / Descrição do Passo Atual */}
      {passoAtivo && (
        <div className="p-4 bg-neutral-800 border-t border-white/10 shrink-0">
          <div className="text-sm text-gray-300 font-medium mb-1">Passo {passoAtivo.passo_numero} de {passos.length}</div>
          <div className="text-indigo-300 text-sm">{passoAtivo.descricao_acao}</div>
          
          {passoAtivo.variaveis_estado && (
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs font-mono bg-black/30 p-2 rounded border border-white/5">
              {Object.entries(passoAtivo.variaveis_estado).map(([k, v]) => (
                <div key={k} className="flex flex-col">
                  <span className="text-gray-500">{k}</span>
                  <span className="text-green-300">{JSON.stringify(v)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
