'use client';

import { useEffect, useState } from 'react';

interface Agent {
  id: string;
  name: string;
  llm_model: string;
}

interface ModelOption {
  name: string;
  provider: string;
}

export default function SettingsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [models, setModels] = useState<ModelOption[]>([]);
  const [saving, setSaving] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8888';

    fetch(`${base}/api/agents`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then((data) => setAgents(Array.isArray(data) ? data : []))
      .catch(() => {});

    fetch(`${base}/api/models`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then((data) => setModels(data.models?.map((m: any) => ({ name: m.name, provider: m.provider })) || []))
      .catch(() => {});
  }, []);

  const handleModelChange = async (agentId: string, newModel: string) => {
    setSaving(agentId);
    try {
      const token = localStorage.getItem('token');
      const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8888';
      await fetch(`${base}/api/agents/${agentId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ llm_model: newModel }),
      });
      setAgents((prev) => prev.map((a) => (a.id === agentId ? { ...a, llm_model: newModel } : a)));
    } catch (e) {
      console.error(e);
    } finally {
      setSaving(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-4">Configurações da Imobiliária</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Nome da Imobiliária</label>
            <input
              type="text"
              defaultValue="Imobiliária Modelo"
              className="w-full px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">CNPJ</label>
            <input
              type="text"
              defaultValue="00.000.000/0001-00"
              className="w-full px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Regras Comerciais (para o agente IA)</label>
            <textarea
              rows={4}
              defaultValue="Não oferecer descontos superiores a 5%. Sempre agendar visitas para período da manhã ou tarde. Priorizar imóveis com vista e aceitar negociação em até 3x parcelas."
              className="w-full px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>
        <button className="mt-4 px-6 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          Salvar Alterações
        </button>
      </div>

      <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-2">Modelo por Agente</h3>
        <p className="text-sm text-gray-500 dark:text-slate-400 mb-4">
          Selecione qual modelo de IA cada agente irá utilizar. O modelo será carregado sob demanda.
        </p>
        <div className="space-y-3">
          {agents.map((agent) => (
            <div key={agent.id} className="flex items-center justify-between py-3 border-b border-gray-100 dark:border-slate-700 last:border-0">
              <div>
                <span className="text-sm font-medium text-gray-900 dark:text-slate-100">{agent.name}</span>
                <span className="ml-2 text-xs text-gray-500 dark:text-slate-400">({agent.llm_model})</span>
              </div>
              <select
                value={agent.llm_model}
                onChange={(e) => handleModelChange(agent.id, e.target.value)}
                disabled={saving === agent.id}
                className="px-3 py-1.5 text-sm border border-gray-200 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {models.map((m) => (
                  <option key={`${m.provider}:${m.name}`} value={m.name}>
                    {m.name} ({m.provider})
                  </option>
                ))}
                {models.length === 0 && <option value="qwen3.5-9b-deepseek-v4-flash">qwen3.5-9b-deepseek-v4-flash (lmstudio)</option>}
              </select>
            </div>
          ))}
          {agents.length === 0 && (
            <p className="text-sm text-gray-500 dark:text-slate-400">Nenhum agente encontrado.</p>
          )}
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-4">Integrações</h3>
        <div className="space-y-4">
          <IntegrationRow name="WhatsApp (Evolution API)" status="connected" />
          <IntegrationRow name="Telefone (Twilio)" status="connected" />
          <IntegrationRow name="E-mail (SMTP)" status="disconnected" />
          <IntegrationRow name="LMStudio (Local)" status="connected" />
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-slate-100 mb-4">Equipe</h3>
        <p className="text-sm text-gray-600 dark:text-slate-400 mb-4">Gerencie os acessos da sua equipe ao sistema</p>
        <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          + Adicionar Membro
        </button>
      </div>
    </div>
  );
}

function IntegrationRow({ name, status }: { name: string; status: string }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-gray-100 dark:border-slate-700 last:border-0">
      <span className="text-sm text-gray-900 dark:text-slate-100">{name}</span>
      <span
        className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
          status === 'connected' ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-400'
        }`}
      >
        {status === 'connected' ? 'Conectado' : 'Desconectado'}
      </span>
    </div>
  );
}
