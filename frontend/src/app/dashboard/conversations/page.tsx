'use client';

import { useEffect, useState } from 'react';
import { conversationsApi } from '@/lib/api';
import { formatDate } from '@/lib/utils';

interface Conversation {
  id: string;
  contact_name: string;
  channel: string;
  status: string;
  summary: string;
  last_message: string;
  last_message_at: string;
  created_at: string;
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    conversationsApi.list().then(setConversations).finally(() => setLoading(false));
  }, []);

  const channelIcons: Record<string, string> = {
    whatsapp: '💬',
    voice: '📞',
    email: '📧',
    sms: '📱',
    webchat: '🌐',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder="Buscar conversas..."
          className="px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 w-64"
        />
        <select className="px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
          <option value="">Todos os canais</option>
          <option value="whatsapp">WhatsApp</option>
          <option value="voice">Telefone</option>
          <option value="email">E-mail</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Conversation list */}
        <div className="lg:col-span-1 bg-white rounded-xl border border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200">
            <h3 className="font-semibold text-gray-900">Conversas ({conversations.length})</h3>
          </div>
          <div className="divide-y divide-gray-200 max-h-[600px] overflow-y-auto">
            {loading ? (
              <div className="p-4 text-center text-gray-500 animate-pulse">Carregando...</div>
            ) : conversations.length === 0 ? (
              <div className="p-4 text-center text-gray-500">Nenhuma conversa</div>
            ) : (
              conversations.map((conv) => (
                <div
                  key={conv.id}
                  onClick={() => setSelected(conv.id)}
                  className={`p-4 cursor-pointer hover:bg-gray-50 transition-colors ${
                    selected === conv.id ? 'bg-primary-50 border-l-4 border-primary-500' : ''
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-gray-900 text-sm">{conv.contact_name}</span>
                    <span className="text-xs text-gray-500">
                      {channelIcons[conv.channel]} {conv.channel}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 truncate">{conv.last_message || conv.summary}</p>
                  <p className="text-xs text-gray-400 mt-1">{formatDate(conv.last_message_at || conv.created_at)}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Chat area */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200">
          {selected ? (
            <div className="flex flex-col h-[600px]">
              <div className="p-4 border-b border-gray-200">
                <h3 className="font-semibold text-gray-900">Detalhes da Conversa</h3>
              </div>
              <div className="flex-1 p-4 overflow-y-auto space-y-4">
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg px-4 py-2 max-w-[70%]">
                    <p className="text-sm text-gray-900">Olá! Vi um apartamento no site e tenho interesse.</p>
                    <p className="text-xs text-gray-500 mt-1">10:30</p>
                  </div>
                </div>
                <div className="flex justify-end">
                  <div className="bg-primary-500 text-white rounded-lg px-4 py-2 max-w-[70%]">
                    <p className="text-sm">Olá! Ficamos felizes com seu interesse! Posso te ajudar a encontrar o imóvel perfeito. Qual sua faixa de preço e região preferida?</p>
                    <p className="text-xs text-primary-200 mt-1">10:30</p>
                  </div>
                </div>
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg px-4 py-2 max-w-[70%]">
                    <p className="text-sm text-gray-900">Até R$ 500.000, perto do metrô.</p>
                    <p className="text-xs text-gray-500 mt-1">10:32</p>
                  </div>
                </div>
              </div>
              <div className="p-4 border-t border-gray-200">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Digite sua mensagem..."
                    className="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                  <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700">
                    Enviar
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-[600px] text-gray-500">
              Selecione uma conversa para visualizar
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
