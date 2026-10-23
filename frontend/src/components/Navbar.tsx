import React from "react";
import { Activity, ShieldAlert, Cpu } from "lucide-react";

export const Navbar: React.FC = () => {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-400 to-sky-500 flex items-center justify-center shadow-lg shadow-emerald-500/10">
            <Activity className="w-5 h-5 text-slate-950 font-bold" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg tracking-tight text-white">ADAPTIVE LOOP</span>
            </div>
            <p className="text-[10px] text-slate-400 uppercase tracking-wider font-medium">
              Intervention Intelligence Engine
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300">
            <Cpu className="w-3.5 h-3.5 text-emerald-400" />
            <span>Active Model:</span>
            <span className="font-mono text-emerald-400 font-medium">openai/gpt-oss-120b</span>
          </div>

          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-xs text-amber-400">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Clinical Decision Support Prototype</span>
            <span className="sm:hidden">Prototype</span>
          </div>
        </div>
      </div>
    </header>
  );
};
