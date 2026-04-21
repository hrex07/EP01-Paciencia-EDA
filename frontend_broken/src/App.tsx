import React, { useState } from 'react';
import { MesaJogo } from './components/painelJogo';
import { 
  LogOperacoes, 
  ResumoEstruturas, 
  PseudocodigoHighlight, 
  VisualizadorEstrutura, 
  ComparadorAlgoritmos 
} from './components/painelEducacional';
import { EstadoJogo, OperacaoRealizada, StreakJogo } from './tipos/tipos';
import { jogoService } from './servicos/apiJogo';
import { Play, RotateCcw, BarChart2, Volume2, VolumeX, Menu } from 'lucide-react';

function App() {
  const [estado, setEstado] = useState<EstadoJogo | null>(null);
  const [loading, setLoading] = useState(false);
  const [painelAberto, setPainelAberto] = useState(true);
  const [somAtivo, setSomAtivo] = useState(true);

  // Estados do Painel Educacional
  const [operacoes, setOperacoes] = useState<OperacaoRealizada[]>([]);
  const [operacaoAtiva, setOperacaoAtiva] = useState<OperacaoRealizada | null>(null);
  const [passoAtual, setPassoAtual] = useState(1);
  const [filtroLog, setFiltroLog] = useState('todas');
  const [abaAtiva, setAbaAtiva] = useState<'estruturas' | 'algoritmos'>('estruturas');

  const iniciarJogo = async () => {
    setLoading(true);
    try {
      const resp = await jogoService.criarNovoJogo(true);
      setEstado(resp.estado_jogo);
      setOperacoes(resp.log_preparacao || []);
      if (resp.log_preparacao && resp.log_preparacao.length > 0) {
        setOperacaoAtiva(resp.log_preparacao[0]);
        setPassoAtual(1);
      }
    } catch (e) {
      console.error('Erro ao iniciar jogo:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleOperacoes = (ops: OperacaoRealizada[], streak?: StreakJogo) => {
    // Adiciona as novas operações no topo (ou no final, dependendo da UX preferida, vamos adicionar no topo)
    setOperacoes(prev => [...ops, ...prev]);
    if (ops.length > 0) {
      setOperacaoAtiva(ops[0]);
      setPassoAtual(1);
      setAbaAtiva('estruturas');
    }
    
    // Atualiza estado do jogo chamando a API novamente ou usando o retornado?
    // O ideal seria pegar o novo estado de jogo, mas a MesaJogo já lida com o estado visual.
    // Vamos apenas atualizar os componentes.
    if (streak) {
      console.log("Streak:", streak.nivel_efeito, streak.mensagem_educacional);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-900 text-slate-100 flex flex-col font-sans overflow-hidden">
      {/* Header */}
      <header className="h-16 bg-neutral-950 border-b border-white/10 flex items-center justify-between px-6 shrink-0 z-10">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center font-bold">P</div>
          <h1 className="text-xl font-semibold tracking-wide">Paciência Educacional</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <button 
            onClick={iniciarJogo}
            disabled={loading}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-md font-medium transition-colors"
          >
            <Play size={18} />
            <span>Novo Jogo</span>
          </button>
          
          <div className="h-6 w-px bg-white/20 mx-2" />
          
          <button className="p-2 hover:bg-white/10 rounded-md text-gray-400 hover:text-white transition-colors" title="Estatísticas">
            <BarChart2 size={20} />
          </button>
          
          <button 
            onClick={() => setSomAtivo(!somAtivo)}
            className="p-2 hover:bg-white/10 rounded-md text-gray-400 hover:text-white transition-colors"
            title={somAtivo ? "Mudo" : "Ativar Som"}
          >
            {somAtivo ? <Volume2 size={20} /> : <VolumeX size={20} />}
          </button>

          <button 
            onClick={() => setPainelAberto(!painelAberto)}
            className={`p-2 rounded-md transition-colors ${painelAberto ? 'bg-indigo-600 text-white' : 'hover:bg-white/10 text-gray-400'}`}
            title="Painel Educacional"
          >
            <Menu size={20} />
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 flex overflow-hidden">
        {/* Lado Esquerdo: Jogo (Flexível) */}
        <section className={`h-full overflow-auto p-6 transition-all duration-300 flex items-start justify-center
          ${painelAberto ? 'w-full lg:w-7/12 xl:w-3/5' : 'w-full'}
        `}>
          {!estado ? (
            <div className="flex flex-col items-center justify-center h-full text-center max-w-md">
              <div className="w-24 h-32 bg-blue-800/50 rounded-xl border-2 border-dashed border-blue-400/50 mb-6 flex items-center justify-center">
                <span className="text-blue-400 font-bold text-4xl">♠</span>
              </div>
              <h2 className="text-2xl font-bold mb-3">Bem-vindo ao Paciência Educacional</h2>
              <p className="text-gray-400 mb-8">
                Aprenda Estruturas de Dados e Análise de Algoritmos na prática. 
                Jogue Solitaire e visualize Pilhas, Filas e Listas Ligadas em tempo real.
              </p>
              <button 
                onClick={iniciarJogo}
                disabled={loading}
                className="px-8 py-3 bg-blue-600 hover:bg-blue-500 rounded-lg font-bold text-lg shadow-lg hover:shadow-blue-500/25 transition-all"
              >
                {loading ? 'Preparando Baralho...' : 'Iniciar Partida'}
              </button>
            </div>
          ) : (
            <div className="w-full max-w-5xl">
              {/* Efeitos de Streak (Placeholder) */}
              <div className="h-8 mb-4 flex justify-between items-center px-4 bg-black/20 rounded-md">
                <div className="text-sm font-medium text-emerald-400">
                  {estado.estatisticas.sequencia_atual > 0 ? `Sequência: ${estado.estatisticas.sequencia_atual}x🔥` : 'Faça uma jogada...'}
                </div>
                <div className="text-xs text-gray-500">
                  Jogadas: {estado.estatisticas.total_jogadas}
                </div>
              </div>
              
              <MesaJogo 
                idSessao={estado.id_sessao} 
                estadoInicial={estado} 
                onOperacoesRealizadas={handleOperacoes}
              />
            </div>
          )}
        </section>

        {/* Lado Direito: Painel Educacional (Fixo na direita) */}
        {painelAberto && (
          <aside className="w-full lg:w-5/12 xl:w-2/5 h-full bg-neutral-950 border-l border-white/10 flex flex-col shadow-2xl z-20">
            {/* Abas */}
            <div className="flex border-b border-white/10 bg-neutral-900 shrink-0">
              <button 
                onClick={() => setAbaAtiva('estruturas')}
                className={`flex-1 py-3 text-sm font-medium transition-colors ${abaAtiva === 'estruturas' ? 'bg-neutral-800 text-indigo-400 border-b-2 border-indigo-400' : 'text-gray-400 hover:text-gray-300 hover:bg-white/5'}`}
              >
                Estruturas de Dados
              </button>
              <button 
                onClick={() => setAbaAtiva('algoritmos')}
                className={`flex-1 py-3 text-sm font-medium transition-colors ${abaAtiva === 'algoritmos' ? 'bg-neutral-800 text-orange-400 border-b-2 border-orange-400' : 'text-gray-400 hover:text-gray-300 hover:bg-white/5'}`}
              >
                Algoritmos
              </button>
            </div>

            {abaAtiva === 'estruturas' ? (
              <div className="flex-1 flex flex-col p-4 space-y-4 overflow-hidden">
                {/* Indicador Permanente de Estado */}
                <div className="shrink-0">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Visão Geral</h3>
                  {estado && <ResumoEstruturas estado={estado} />}
                </div>

                {/* Visualizador Visual */}
                <div className="shrink-0">
                  <VisualizadorEstrutura operacao={operacaoAtiva} passoAtual={passoAtual} />
                </div>

                {/* Split: Pseudocódigo (Esquerda/Cima) e Log (Direita/Baixo) */}
                <div className="flex-1 flex flex-col min-h-0 gap-4">
                  <div className="h-1/2 flex flex-col">
                    <PseudocodigoHighlight 
                      operacao={operacaoAtiva} 
                      onPassoChange={setPassoAtual} 
                    />
                  </div>
                  <div className="h-1/2 flex flex-col">
                    <LogOperacoes 
                      operacoes={operacoes}
                      filtro={filtroLog}
                      setFiltro={setFiltroLog}
                      onSelecionarOperacao={(op) => {
                        setOperacaoAtiva(op);
                        setPassoAtual(1);
                      }}
                      operacaoAtiva={operacaoAtiva}
                    />
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex-1 p-4 overflow-hidden">
                <ComparadorAlgoritmos />
              </div>
            )}
          </aside>
        )}
      </main>
    </div>
  );
}

export default App;
