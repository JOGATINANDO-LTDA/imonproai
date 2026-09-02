'use client';

import { useEffect, useState } from 'react';
import { agentsApi } from '@/lib/api';
import { formatDate } from '@/lib/utils';

interface Agent {
  id: string;
  name: string;
  voice_id: string;
  llm_model: string;
  is_active: boolean;
  phone_number: string;
  whatsapp_instance: string;
  created_at: string;
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    agentsApi.list().then(setAgents).finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600 dark:text-slate-400">Gerencie os agentes de IA da sua imobiliária</p>
        <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          + Novo Agente
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6 animate-pulse">
              <div className="h-12 bg-gray-100 dark:bg-slate-700 rounded-lg mb-4" />
              <div className="h-4 bg-gray-100 dark:bg-slate-700 rounded w-3/4 mb-2" />
              <div className="h-4 bg-gray-100 dark:bg-slate-700 rounded w-1/2" />
            </div>
          ))
        ) : agents.length === 0 ? (
          <div className="col-span-full p-8 text-center text-gray-500 dark:text-slate-400 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700">
            Nenhum agente configurado. Crie seu primeiro agente de IA!
          </div>
        ) : (
          agents.map((agent) => (
            <div key={agent.id} className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
                    <span className="text-2xl">🤖</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-slate-100">{agent.name}</h3>
                    <p className="text-xs text-gray-500 dark:text-slate-400">{agent.llm_model}</p>
                  </div>
                </div>
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    agent.is_active ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-slate-700 text-gray-800 dark:text-slate-300'
                  }`}
                >
                  {agent.is_active ? 'Ativo' : 'Inativo'}
                </span>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-gray-500 dark:text-slate-400">Voz:</span>
                  <span className="text-gray-900 dark:text-slate-100">{agent.voice_id}</span>
                </div>
                {agent.phone_number && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-500 dark:text-slate-400">Telefone:</span>
                    <span className="text-gray-900 dark:text-slate-100">{agent.phone_number}</span>
                  </div>
                )}
                {agent.whatsapp_instance && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-500 dark:text-slate-400">WhatsApp:</span>
                    <span className="text-gray-900 dark:text-slate-100">{agent.whatsapp_instance}</span>
                  </div>
                )}
                <div className="flex items-center justify-between">
                  <span className="text-gray-500 dark:text-slate-400">Criado em:</span>
                  <span className="text-gray-900 dark:text-slate-100">{formatDate(agent.created_at)}</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-slate-700 flex gap-2">
                <button className="flex-1 px-3 py-2 text-sm text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors">
                  Editar
                </button>
                <button className="flex-1 px-3 py-2 text-sm text-gray-600 dark:text-slate-400 hover:bg-gray-50 dark:hover:bg-slate-700 rounded-lg transition-colors">
                  Testar
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
