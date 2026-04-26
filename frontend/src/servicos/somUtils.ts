import { Howler } from 'howler';

// Sistema de áudio sintetizado para evitar dependência de arquivos MP3 externos
const playTone = (freq: number, type: OscillatorType, duration: number, volume: number) => {
  try {
    const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    
    gain.gain.setValueAtTime(volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + duration);
  } catch (e) {
    console.warn("Áudio não suportado ou bloqueado pelo navegador", e);
  }
};

let somAtivo = true;

export const somUtils = {
  setAtivo(ativo: boolean) {
    somAtivo = ativo;
    if (typeof Howler !== 'undefined') {
      Howler.mute(!ativo);
    }
  },
  
  playClick() {
    if (!somAtivo) return;
    // Som de clique curto e agudo
    playTone(800, 'sine', 0.1, 0.1);
  },
  
  playErro() {
    if (!somAtivo) return;
    // Som de erro grave e curto
    playTone(150, 'sawtooth', 0.2, 0.05);
  },
  
  playStreak(nivel: string) {
    if (!somAtivo) return;
    
    switch (nivel) {
      case 'bom':
        playTone(500, 'sine', 0.3, 0.1);
        setTimeout(() => playTone(600, 'sine', 0.3, 0.1), 100);
        break;
      case 'otimo':
      case 'confetti':
        playTone(600, 'sine', 0.4, 0.1);
        setTimeout(() => playTone(800, 'sine', 0.4, 0.1), 100);
        break;
      case 'incrivel':
      case 'mestre':
        playTone(400, 'triangle', 0.5, 0.1);
        setTimeout(() => playTone(600, 'triangle', 0.5, 0.1), 150);
        setTimeout(() => playTone(800, 'triangle', 0.5, 0.1), 300);
        break;
      case 'vitoria':
        // Arpejo de vitória
        [440, 554, 659, 880].forEach((f, i) => {
          setTimeout(() => playTone(f, 'sine', 0.6, 0.1), i * 150);
        });
        break;
    }
  }
};
