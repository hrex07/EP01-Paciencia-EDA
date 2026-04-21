import React from 'react';
import { OperacaoRealizada } from '../../tipos/tipos';
import { Layers, AlignJustify, List } from 'lucide-react';

interface LogOperacoesProps {
  operacoes: OperacaoRealizada[];
  filtro: string;
  setFiltro: (filtro: string) => void;
  onSelecionarOperacao: (op: OperacaoRealizada) => void;
  operacaoAtiva: OperacaoRealizada | null;
}

export const LogOperacoes: React.FC<LogOperacoesProps> = ({
  operacoes,
  filtro,
  setFiltro,
  onSelecionarOperacao,
  operacaoAtiva
}) => {
  const operacoesFiltradas = filtro === 'todas' 
    ? operacoes 
    : operacoes.filter(op => op.estrutura_tipo.toLowerCase().includes(filtro.toLowerCase()));

  const getIconeEstrutura = (tipo: string) => {
    const t = tipo.toLowerCase();
    if (t.includes('pilha')) return <Layers size={16} className="text-blue-400" />;
    if (t.includes('fila')) return <AlignJustify size={16} className="text-green-400" />;
    if (t.includes('lista')) return <List size={16} className="text-purple-400" />;
    return <span className="w-4 h-4" />;
  };

  return (
    <div className="flex flex-col h-full bg-neutral-900 border border-white/10 rounded-lg overflow-hidden">
      <div className="flex items-center justify-between p-3 bg-neutral-800 border-b border-white/10 shrink-0">
        <h3 className="font-semibold text-sm text-gray-300">Log de Operações</h3>
        <select 
          className="bg-black/40 text-xs text-gray-300 border border-white/20 rounded p-1"
          value={filtro}
          onChange={(e) => setFiltro(e.target.value)}
        >
          <option value="todas">Todas</option>
          <option value="pilha">Pilhas</option>
          <option value="fila">Fila</option>
          <option value="lista">Listas Ligadas</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto p-2 space-y-2 custom-scrollbar">
        {operacoesFiltradas.length === 0 ? (
          <div className="text-center text-gray-500 text-xs mt-4">
            Nenhuma operação registrada ainda.
          </div>
        ) : (
          operacoesFiltradas.map((op, index) => (
            <div 
              key={index}
              onClick={() => onSelecionarOperacao(op)}
              className={`
                p-2 rounded cursor-pointer border text-sm transition-colors flex items-start space-x-3
                ${operacaoAtiva === op 
                  ? 'bg-indigo-900/40 border-indigo-500/50' 
                  : 'bg-black/20 border-white/5 hover:bg-white/5'}
              `}
            >
              <div className="mt-0.5">
                {getIconeEstrutura(op.estrutura_tipo)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex justify-between">
                  <span className="font-mono font-medium text-gray-200">
                    {op.operacao_nome}()
                  </span>
                  <span className={op.operacao_sucesso ? 'text-green-400' : 'text-red-400'}>
                    {op.operacao_sucesso ? 'OK' : 'ERRO'}
                  </span>
                </div>
                <div className="text-xs text-gray-500 truncate mt-0.5">
                  {op.nome_estrutura} ({op.passos_executados.length} passos)
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
