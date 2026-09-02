'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api';
import { useTheme } from '@/lib/theme';

export default function LoginPage() {
  const [email, setEmail] = useState('admin@imobpro.ai');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const router = useRouter();
  const { theme, toggleTheme } = useTheme();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await authApi.login(email, password);
      localStorage.setItem('token', result.access_token);
      localStorage.setItem('refresh_token', result.refresh_token);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Erro ao fazer login');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setError('');
    setSeeding(true);

    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/seed`, {
        method: 'POST',
      });

      const result = await authApi.login('admin@imobpro.ai', 'admin123');
      localStorage.setItem('token', result.access_token);
      localStorage.setItem('refresh_token', result.refresh_token);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Erro ao iniciar demo');
    } finally {
      setSeeding(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 dark:from-slate-900 dark:to-slate-800">
      <div className="w-full max-w-md">
        {/* Theme toggle */}
        <div className="flex justify-end mb-4">
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-gray-500 dark:text-slate-400 hover:bg-white/50 dark:hover:bg-slate-700/50 transition-colors"
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </div>

        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-primary-900 dark:text-primary-100">ImobPro.ai</h1>
          <p className="text-gray-600 dark:text-slate-400 mt-2">Agente Comercial de IA para Imobiliárias</p>
        </div>

        {/* Demo banner */}
        <div className="bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800 rounded-xl p-4 mb-6">
          <div className="flex items-start gap-3">
            <span className="text-2xl">🚀</span>
            <div>
              <h3 className="text-sm font-semibold text-primary-900 dark:text-primary-100">Conta de Demonstração</h3>
              <p className="text-xs text-primary-700 dark:text-primary-300 mt-1">
                Acesse com os dados pré-preenchidos para explorar todas as funcionalidades com dados reais de uma imobiliária.
              </p>
            </div>
          </div>
        </div>

        {/* Login form */}
        <form
          onSubmit={handleSubmit}
          className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-gray-200 dark:border-slate-700 p-8 space-y-6"
        >
          {error && (
            <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-sm text-red-700 dark:text-red-300">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">E-mail</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="seu@email.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Senha</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="••••••••"
            />
          </div>

          <div className="space-y-3">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </button>

            <button
              type="button"
              onClick={handleDemoLogin}
              disabled={seeding}
              className="w-full py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-lg font-medium hover:from-primary-600 hover:to-primary-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {seeding ? (
                'Preparando demo...'
              ) : (
                <>
                  <span>🚀</span>
                  <span>Entrar como Demo</span>
                </>
              )}
            </button>
          </div>

          <div className="text-center pt-2">
            <p className="text-xs text-gray-500 dark:text-slate-500">
              Credenciais demo: <span className="font-mono">admin@imobpro.ai</span> / <span className="font-mono">admin123</span>
            </p>
          </div>
        </form>

        {/* Footer info */}
        <p className="text-center text-xs text-gray-400 dark:text-slate-500 mt-6">
          Dados demo incluem: 8 leads, 6 imóveis, 2 agentes IA e 3 conversas ativas
        </p>
      </div>
    </div>
  );
}
