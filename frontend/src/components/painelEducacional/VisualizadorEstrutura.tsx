import React from 'react';
import type { OperacaoRealizada } from '../../tipos/tipos';
import { motion, AnimatePresence } from 'framer-motion';
import { Layers, AlignJustify, List, ArrowRight } from 'lucide-react';

interface VisualizadorEstruturaProps {
  operacao: OperacaoRealizada | null;
  passoAtual: number; // 1-based index from PseudocodigoHighlight
}

export const VisualizadorEstrutura: React.FC<VisualizadorEstruturaProps> = ({ 
  operacao, 
  passoAtual 
}) => {
  if (!operacao) {
    return (
      <div className="flex flex-col items-center justify-center h-48 bg-neutral-900 border border-white/10 rounded-lg text-gray-500 text-sm p-4">
        <div className="w-16 h-16 bg-black/20 border border-white/5 rounded-xl mb-4 flex items-center justify-center opacity-50">
          <Layers size={24} />
        </div>
        Nenhuma operação selecionada.
      </div>
    );
  }

  // Get the state vector from the current step if available
  const passos = operacao.passos_executados;
  const passoInfo = passos[Math.min(passoAtual - 1, passos.length - 1)] || passos[passos.length - 1];
  
  // Se a operação for Bubble Sort, etc, teremos estado_vetor
  const arrayVis = passoInfo?.estado_vetor;

  // Renderiza a Pilha (vertical)
  const renderPilha = () => (
    <div className="flex flex-col items-center p-4">
      <h4 className="text-blue-400 font-semibold mb-4 text-sm flex items-center">
        <Layers className="mr-2" size={16} /> {operacao.nome_estrutura} (LIFO)
      </h4>
      <div className="relative w-32 border-x-2 border-b-2 border-blue-500/50 rounded-b-lg p-2 min-h-[160px] flex flex-col-reverse justify-start">
        {/* Placeholder: na prática teríamos o estado_depois com a lista de elementos */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-blue-900/10 pointer-events-none" />
        
        {/* Se houvesse dados reais do estado */}
        <div className="w-full text-center text-xs text-gray-400 mb-2 italic">
          {operacao.quantidade_elementos !== undefined ? `${operacao.quantidade_elementos} elementos` : 'Simulação'}
        </div>
        
        {/* Mock visual para dar ideia de como seria com elementos */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full bg-blue-600 border border-blue-400 text-white rounded p-2 text-center text-sm font-bold shadow-lg relative z-10 mb-1"
        >
          {operacao.operacao_nome === 'empilhar' ? 'NOVO NÓ' : 'TOPO'}
        </motion.div>
        
        {(operacao.quantidade_elementos || 1) > 1 && (
          <div className="w-full bg-blue-800/50 border border-blue-700/50 text-gray-300 rounded p-2 text-center text-sm mb-1 opacity-80">
            Nó Anterior
          </div>
        )}
      </div>
    </div>
  );

  // Renderiza a Fila (horizontal)
  const renderFila = () => (
    <div className="flex flex-col items-start p-4 w-full">
      <h4 className="text-green-400 font-semibold mb-4 text-sm flex items-center">
        <AlignJustify className="mr-2" size={16} /> {operacao.nome_estrutura} (FIFO)
      </h4>
      
      <div className="flex items-center w-full bg-black/20 p-4 rounded-xl border border-green-500/30 overflow-x-auto">
        <div className="flex flex-col items-center mr-4 text-green-500/70 text-xs font-bold uppercase tracking-widest">
          <ArrowRight size={16} className="mb-1" /> FRENTE
        </div>
        
        <div className="flex space-x-2">
          {operacao.operacao_nome === 'desenfileirar' ? (
            <motion.div 
              initial={{ x: 0, opacity: 1 }}
              animate={{ x: -20, opacity: 0 }}
              className="w-16 h-20 bg-green-600/50 border-2 border-green-400 rounded-md shadow-lg flex items-center justify-center text-white"
            >
              SAINDO
            </motion.div>
          ) : (
            <div className="w-16 h-20 bg-green-800/50 border border-green-700/50 rounded-md flex items-center justify-center text-gray-400">
              NÓ
            </div>
          )}
          
          <div className="w-16 h-20 bg-green-800/30 border border-green-700/30 rounded-md flex items-center justify-center text-gray-500">
            NÓ
          </div>
          
          {operacao.operacao_nome === 'enfileirar' && (
            <motion.div 
              initial={{ x: 20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              className="w-16 h-20 bg-green-600 border border-green-400 rounded-md shadow-lg flex items-center justify-center text-white"
            >
              NOVO
            </motion.div>
          )}
        </div>
        
        <div className="flex flex-col items-center ml-4 text-green-500/70 text-xs font-bold uppercase tracking-widest">
          FINAL <ArrowRight size={16} className="mt-1" />
        </div>
      </div>
    </div>
  );

  // Renderiza a Lista Ligada (nós e setas)
  const renderLista = () => (
    <div className="flex flex-col items-start p-4 w-full">
      <h4 className="text-purple-400 font-semibold mb-4 text-sm flex items-center">
        <List className="mr-2" size={16} /> {operacao.nome_estrutura} (Duplamente Enc.)
      </h4>
      
      <div className="flex items-center w-full p-4 overflow-x-auto min-h-[120px]">
        <div className="text-purple-500/50 text-xs font-bold mr-2">CABEÇA</div>
        
        <div className="flex items-center space-x-1">
          {/* Nó 1 */}
          <div className="flex flex-col">
            <div className="w-16 h-12 bg-purple-900/40 border border-purple-500/40 rounded flex flex-col items-center justify-center text-xs">
              <span className="text-white">Nó</span>
            </div>
            <div className="flex justify-between mt-1 text-[10px] text-gray-500 px-1">
              <span>prev</span><span>next</span>
            </div>
          </div>
          
          {/* Setas */}
          <div className="flex flex-col items-center justify-center px-1 text-purple-500/50">
            <span className="text-xs">⇄</span>
          </div>
          
          {/* Nó 2 (Novo ou Alvo) */}
          <div className="flex flex-col relative">
            <motion.div 
              animate={{ 
                scale: ['inserir', 'remover'].some(s => operacao.operacao_nome.includes(s)) ? [1, 1.05, 1] : 1,
                borderColor: ['inserir'].some(s => operacao.operacao_nome.includes(s)) ? 'rgba(168, 85, 247, 1)' : 'rgba(168, 85, 247, 0.4)'
              }}
              transition={{ duration: 0.5 }}
              className="w-16 h-12 bg-purple-800 border-2 border-purple-500 rounded flex flex-col items-center justify-center shadow-[0_0_15px_rgba(168,85,247,0.3)] z-10"
            >
              <span className="text-white font-bold text-xs text-center leading-tight">
                {operacao.operacao_nome.includes('inserir') ? '+ NOVO' : 'ALVO'}
              </span>
            </motion.div>
            <div className="flex justify-between mt-1 text-[10px] text-gray-500 px-1">
              <span>prev</span><span>next</span>
            </div>
            
            {/* Animação de ponteiros */}
            {passoInfo?.pseudo_codigo?.includes('próximo') && (
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: 30 }}
                className="absolute top-1/2 left-full h-0.5 bg-purple-400 origin-left"
              />
            )}
          </div>
        </div>
        
        <div className="text-purple-500/50 text-xs font-bold ml-6">CAUDA</div>
      </div>
    </div>
  );

  // Renderiza Vetor (para algoritmos de ordenação)
  const renderVetor = () => {
    if (!arrayVis) return null;
    const indicesTrocados = passoInfo.indices_trocados || [];
    const indicesComparados = passoInfo.indices_comparados || [];
    
    return (
      <div className="flex flex-col p-4 w-full">
        <h4 className="text-orange-400 font-semibold mb-4 text-sm flex items-center">
          Vetor: {operacao.algoritmo_nome}
        </h4>
        <div className="flex flex-wrap gap-2">
          {arrayVis.slice(0, 15).map((val, idx) => {
            const isTrocado = indicesTrocados.includes(idx);
            const isComparado = indicesComparados.includes(idx);
            
            return (
              <motion.div
                key={idx}
                layout
                initial={{ opacity: 0.8 }}
                animate={{ 
                  y: isTrocado ? [0, -10, 0] : 0,
                  backgroundColor: isTrocado ? 'rgba(249, 115, 22, 0.8)' : isComparado ? 'rgba(234, 179, 8, 0.5)' : 'rgba(38, 38, 38, 1)',
                  borderColor: isTrocado ? 'rgba(251, 146, 60, 1)' : isComparado ? 'rgba(250, 204, 21, 1)' : 'rgba(64, 64, 64, 1)'
                }}
                className="w-10 h-14 border rounded flex items-center justify-center text-xs font-bold text-white shadow-sm"
              >
                {val}
              </motion.div>
            );
          })}
          {arrayVis.length > 15 && (
            <div className="w-10 h-14 flex items-center justify-center text-gray-500">...</div>
          )}
        </div>
        <div className="mt-4 flex space-x-4 text-xs text-gray-400">
          <div className="flex items-center"><div className="w-3 h-3 bg-yellow-500/50 mr-1 rounded-sm"/> Comparando</div>
          <div className="flex items-center"><div className="w-3 h-3 bg-orange-500/80 mr-1 rounded-sm"/> Trocando</div>
        </div>
      </div>
    );
  };

  const tipo = operacao.estrutura_tipo.toLowerCase();
  
  return (
    <div className="bg-neutral-900 border border-white/10 rounded-lg overflow-hidden flex items-center justify-center min-h-[220px]">
      {arrayVis ? renderVetor() :
       tipo.includes('pilha') ? renderPilha() : 
       tipo.includes('fila') ? renderFila() : 
       tipo.includes('lista') ? renderLista() : 
       <div className="text-gray-500 text-sm">Visualização não disponível para {operacao.estrutura_tipo}</div>}
    </div>
  );
};
