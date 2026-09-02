'use client';

import { useEffect, useState } from 'react';
import { contactsApi } from '@/lib/api';
import { formatDate } from '@/lib/utils';

interface Contact {
  id: string;
  name: string;
  phone: string;
  email: string;
  whatsapp: string;
  status: string;
  score: number;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export default function ContactsPage() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('');

  useEffect(() => {
    contactsApi.list({ status: filter || undefined }).then(setContacts).finally(() => setLoading(false));
  }, [filter]);

  const statusColors: Record<string, string> = {
    new: 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300',
    qualified: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300',
    proposal: 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300',
    won: 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300',
    lost: 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300',
  };

  const statusLabels: Record<string, string> = {
    new: 'Novo',
    qualified: 'Qualificado',
    proposal: 'Proposta',
    won: 'Ganho',
    lost: 'Perdido',
  };

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="flex items-center gap-4">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">Todos os status</option>
          <option value="new">Novos</option>
          <option value="qualified">Qualificados</option>
          <option value="proposal">Proposta</option>
          <option value="won">Ganhos</option>
          <option value="lost">Perdidos</option>
        </select>
        <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          + Novo Contato
        </button>
      </div>

      {/* Table */}
      <div className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-500 dark:text-slate-400 animate-pulse">Carregando contatos...</div>
        ) : contacts.length === 0 ? (
          <div className="p-8 text-center text-gray-500 dark:text-slate-400">Nenhum contato encontrado</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-slate-700/50 border-b border-gray-200 dark:border-slate-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase">Nome</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase">WhatsApp</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase">E-mail</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-slate-400 uppercase">Criado em</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
              {contacts.map((contact) => (
                <tr key={contact.id} className="hover:bg-gray-50 dark:hover:bg-slate-700/50 cursor-pointer">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-900 dark:text-slate-100">{contact.name}</div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600 dark:text-slate-400">{contact.whatsapp || '-'}</td>
                  <td className="px-6 py-4 text-sm text-gray-600 dark:text-slate-400">{contact.email || '-'}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[contact.status] || 'bg-gray-100 dark:bg-slate-700 text-gray-800 dark:text-slate-300'}`}>
                      {statusLabels[contact.status] || contact.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600 dark:text-slate-400">{contact.score}</td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-slate-400">{formatDate(contact.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
