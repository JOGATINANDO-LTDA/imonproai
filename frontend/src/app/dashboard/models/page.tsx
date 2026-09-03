'use client';

import { useCallback, useEffect, useState } from 'react';

interface ModelInfo {
  name: string;
  provider: string;
  loaded: boolean;
  instance_id: string | null;
  size_bytes: number | null;
  supports_load_unload: boolean;
  last_used: number;
  ttl_remaining: number | null;
}

interface ModelsResponse {
  models: ModelInfo[];
  providers: string[];
  active_model: ModelInfo | null;
}

export default function ModelsPage() {
  const [data, setData] = useState<ModelsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingModel, setLoadingModel] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchModels = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8888'}/api/models`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Erro ao buscar modelos');
      const json = await res.json();
      setData(json);
      setError(null);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchModels();
    const interval = setInterval(fetchModels, 10000);
    return () => clearInterval(interval);
  }, [fetchModels]);

  const handleLoad = async (model: string, provider: string) => {
    setLoadingModel(model);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8888'}/api/models/load`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ model, provider }),
      });
      const result = await res.json();
      if (result.status === 'error') {
        setError(result.error || 'Erro ao carregar modelo');
      }
      await fetchModels();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoadingModel(null);
    }
  };

  const handleUnload = async (model: string, provider: string) => {
    setLoadingModel(model);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8888'}/api/models/unload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ model, provider }),
      });
      await res.json();
      await fetchModels();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoadingModel(null);
    }
  };

  const formatSize = (bytes: number | null) => {
    if (!bytes) return '—';
    if (bytes < 1024 ** 2) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 ** 3) return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
    return `${(bytes / 1024 ** 3).toFixed(1)} GB`;
  };

  const formatTTL = (seconds: number | null) => {
    if (seconds === null) return '—';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500 dark:text-slate-400 animate-pulse">Carregando modelos...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-slate-100">Modelos de IA</h2>
          <p className="text-sm text-gray-500 dark:text-slate-400 mt-1">
            Gerencie modelos carregados. Modelos são descarregados automaticamente após 5min de inatividade.
          </p>
        </div>
        <button
          onClick={fetchModels}
          className="px-4 py-2 text-sm bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-slate-300 rounded-lg hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
        >
          Atualizar
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300 text-sm">
          {error}
        </div>
      )}

      {data?.active_model && (
        <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm font-medium text-green-800 dark:text-green-300">
              Modelo ativo: {data.active_model.name}
            </span>
            <span className="text-xs text-green-600 dark:text-green-400">
              ({data.active_model.provider}) — TTL: {formatTTL(data.active_model.ttl_remaining)}
            </span>
          </div>
        </div>
      )}

      <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-750">
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                Modelo
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                Provider
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                Status
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                Tamanho
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                TTL
              </th>
              <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 dark:text-slate-400 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
            {data?.models.map((model) => (
              <tr
                key={`${model.provider}:${model.name}`}
                className="hover:bg-gray-50 dark:hover:bg-slate-750 transition-colors"
              >
                <td className="px-6 py-4">
                  <div className="text-sm font-medium text-gray-900 dark:text-slate-100">{model.name}</div>
                </td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-slate-700 text-gray-800 dark:text-slate-300">
                    {model.provider}
                  </span>
                </td>
                <td className="px-6 py-4">
                  {model.loaded ? (
                    <span className="inline-flex items-center gap-1.5 text-sm text-green-700 dark:text-green-400">
                      <span className="w-2 h-2 bg-green-500 rounded-full" />
                      Carregado
                    </span>
                  ) : (
                    <span className="text-sm text-gray-500 dark:text-slate-400">Descarregado</span>
                  )}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 dark:text-slate-400">
                  {formatSize(model.size_bytes)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 dark:text-slate-400">
                  {model.loaded ? formatTTL(model.ttl_remaining) : '—'}
                </td>
                <td className="px-6 py-4 text-right">
                  {model.supports_load_unload && (
                    <div className="flex items-center justify-end gap-2">
                      {model.loaded ? (
                        <button
                          onClick={() => handleUnload(model.name, model.provider)}
                          disabled={loadingModel === model.name}
                          className="px-3 py-1.5 text-xs font-medium text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 disabled:opacity-50 transition-colors"
                        >
                          {loadingModel === model.name ? '...' : 'Descarregar'}
                        </button>
                      ) : (
                        <button
                          onClick={() => handleLoad(model.name, model.provider)}
                          disabled={loadingModel === model.name}
                          className="px-3 py-1.5 text-xs font-medium text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 disabled:opacity-50 transition-colors"
                        >
                          {loadingModel === model.name ? 'Carregando...' : 'Carregar'}
                        </button>
                      )}
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {data?.models.length === 0 && (
          <div className="px-6 py-12 text-center text-gray-500 dark:text-slate-400">
            Nenhum modelo encontrado. Verifique se o LMStudio está rodando.
          </div>
        )}
      </div>
    </div>
  );
}
