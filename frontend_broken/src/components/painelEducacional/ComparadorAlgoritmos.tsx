import React, { useState } from 'react';
import { algoritmoService } from '../../servicos/apiJogo';
import { ResponseAlgoritmo } from '../../tipos/tipos';
import { BarChart3, Play } from 'lucide-react';

export const ComparadorAlgoritmos: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [resultados, setResultados] = useState<ResponseAlgoritmo[]>([]);

  const executarComparacao = async () => {
    setLoading(true);
    try {
      // Chama o endpoint de comparação (executa bubble, merge e quick no mesmo vetor gerado)
      const res = await algoritmoService.comparar();
      setResultados(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-neutral-900 border border-white/10 rounded-lg overflow-hidden">
      <div className="flex items-center justify-between p-3 bg-neutral-800 border-b border-white/10 shrink-0">
        <h3 className="font-semibold text-sm text-gray-300 flex items-center">
          <BarChart3 size={16} className="mr-2 text-orange-400" /> Comparador de Algoritmos
        </h3>
        <button 
          onClick={executarComparacao}
          disabled={loading}
          className="flex items-center px-3 py-1 bg-orange-600 hover:bg-orange-500 disabled:opacity-50 text-white text-xs font-medium rounded transition-colors"
        >
          {loading ? 'Processando...' : <><Play size={12} className="mr-1" /> Executar Todos</>}
        </button>
      </div>

      <div className="p-4 overflow-y-auto custom-scrollbar">
        {!resultados || resultados.length === 0 ? (
          <div className="text-center text-gray-500 text-xs py-8">
            Clique em "Executar Todos" para rodar Bubble Sort, Merge Sort e Quick Sort sobre o mesmo vetor de 52 cartas embaralhadas.
          </div>
        ) : (
          <div className="space-y-4">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/10 text-xs text-gray-400 uppercase tracking-wider">
                  <th className="pb-2 font-medium">Algoritmo</th>
                  <th className="pb-2 font-medium text-right">Comparações</th>
                  <th className="pb-2 font-medium text-right">Trocas/Cópia</th>
                  <th className="pb-2 font-medium text-right">Tempo (ms)</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {resultados.map((res, idx) => (
                  <tr key={idx} className="border-b border-white/5 hover:bg-white/5">
                    <td className="py-3 font-medium text-orange-200">{res.algoritmo_nome}</td>
                    <td className="py-3 text-right text-gray-300">{res.total_comparacoes}</td>
                    <td className="py-3 text-right text-gray-300">{res.total_trocas}</td>
                    <td className="py-3 text-right font-mono text-green-400">{res.tempo_execucao_ms.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            <div className="mt-4 p-3 bg-black/30 rounded border border-white/5">
              <h4 className="text-xs font-semibold text-gray-400 mb-2">💡 Conclusões Didáticas</h4>
              <ul className="text-xs text-gray-300 space-y-1 list-disc pl-4">
                <li>O <strong>Bubble Sort</strong> (<span className="font-mono">O(n²)</span>) realiza muitas comparações e trocas, sendo ineficiente.</li>
                <li>O <strong>Merge Sort</strong> (<span className="font-mono">O(n log n)</span>) é consistente, mas usa memória extra.</li>
                <li>O <strong>Quick Sort</strong> (<span className="font-mono">O(n log n)</span>) geralmente tem o melhor tempo prático devido à localidade de cache.</li>
              </ul>
            </div>
            
            <div className="text-center pt-2">
              <a href="https://visualgo.net/en/sorting" target="_blank" rel="noopener noreferrer" className="text-xs text-indigo-400 hover:text-indigo-300 underline">
                Ver animações detalhadas no VisuAlgo.net
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
