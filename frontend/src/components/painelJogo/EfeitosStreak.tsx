import React, { useEffect, useState } from 'react';
import type { StreakJogo } from '../../tipos/tipos';
import { motion, AnimatePresence } from 'framer-motion';

interface EfeitosStreakProps {
  streak?: StreakJogo;
}

export const EfeitosStreak: React.FC<EfeitosStreakProps> = ({ streak }) => {
  const [showConfetti, setShowConfetti] = useState(false);

  useEffect(() => {
    if (!streak) return;
    
    if (['confetti', 'incrivel', 'mestre', 'vitoria'].includes(streak.nivel_efeito)) {
      setShowConfetti(true);
      const timer = setTimeout(() => setShowConfetti(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [streak]);

  if (!streak || streak.sequencia_atual < 3) return null;

  return (
    <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-50 pointer-events-none flex flex-col items-center">
      <AnimatePresence>
        <motion.div
          key={streak.sequencia_atual}
          initial={{ y: -50, opacity: 0, scale: 0.5 }}
          animate={{ y: 0, opacity: 1, scale: 1.2 }}
          exit={{ opacity: 0, scale: 0.8 }}
          className={`
            font-bold text-2xl px-6 py-2 rounded-full shadow-lg backdrop-blur-sm border
            ${streak.nivel_efeito === 'mestre' ? 'bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 text-white border-white/50' : 
              streak.nivel_efeito === 'incrivel' ? 'bg-orange-500 text-white border-orange-300' :
              'bg-blue-500 text-white border-blue-300'}
          `}
        >
          {streak.sequencia_atual}x Combo!
        </motion.div>
      </AnimatePresence>
      
      {streak.mensagem_educacional && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-2 text-sm bg-black/60 text-white px-4 py-1 rounded-md"
        >
          {streak.mensagem_educacional}
        </motion.div>
      )}

      {/* Confetti simulation (simple CSS version) */}
      {showConfetti && (
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `-5%`,
                backgroundColor: ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'][Math.floor(Math.random() * 5)],
                animation: `fall ${1 + Math.random() * 2}s linear forwards`,
                animationDelay: `${Math.random() * 2}s`
              }}
            />
          ))}
          <style>{`
            @keyframes fall {
              to { transform: translateY(100vh) rotate(360deg); opacity: 0; }
            }
          `}</style>
        </div>
      )}
    </div>
  );
};
