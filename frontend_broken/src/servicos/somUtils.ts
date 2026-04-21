import { Howl } from 'howler';

// Sons base (placeholders, na prática seriam arquivos .mp3 na pasta public)
const sounds = {
  click: new Howl({ src: ['/sounds/click.mp3'], volume: 0.5 }),
  erro: new Howl({ src: ['/sounds/error.mp3'], volume: 0.4 }),
  streakBasico: new Howl({ src: ['/sounds/streak1.mp3'], volume: 0.6 }),
  streakBom: new Howl({ src: ['/sounds/streak2.mp3'], volume: 0.6 }),
  streakOtimo: new Howl({ src: ['/sounds/streak3.mp3'], volume: 0.6 }),
  vitoria: new Howl({ src: ['/sounds/victory.mp3'], volume: 0.8 }),
};

let somAtivo = true;

export const somUtils = {
  setAtivo(ativo: boolean) {
    somAtivo = ativo;
    Howler.mute(!ativo);
  },
  
  playClick() {
    if (somAtivo) sounds.click.play();
  },
  
  playErro() {
    if (somAtivo) sounds.erro.play();
  },
  
  playStreak(nivel: string) {
    if (!somAtivo) return;
    
    switch (nivel) {
      case 'bom':
        sounds.streakBasico.play();
        break;
      case 'otimo':
      case 'confetti':
        sounds.streakBom.play();
        break;
      case 'incrivel':
      case 'mestre':
        sounds.streakOtimo.play();
        break;
      case 'vitoria':
        sounds.vitoria.play();
        break;
    }
  }
};
