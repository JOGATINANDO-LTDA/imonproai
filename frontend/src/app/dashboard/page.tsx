'use client';

import { useEffect, useState } from 'react';
import { dashboardApi } from '@/lib/api';
import { formatCurrency } from '@/lib/utils';

interface Metrics {
  total_contacts: number;
  active_conversations: number;
  total_properties: number;
  contacts_won: number;
  contacts_lost: number;
  conversion_rate: number;
  messages_today: number;
  avg_response_time_seconds: number;
}

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardApi.metrics().then(setMetrics).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="animate-pulse text-gray-500">Carregando métricas...</div>;
  }

  if (!metrics) {
    return <div className="text-red-500">Erro ao carregar métricas</div>;
  }

  return (
    <div className="space-y-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total de Leads"
          value={metrics.total_contacts.toString()}
          icon="👥"
          color="blue"
        />
        <MetricCard
          title="Conversas Ativas"
          value={metrics.active_conversations.toString()}
          icon="💬"
          color="green"
        />
        <MetricCard
          title="Imóveis Cadastrados"
          value={metrics.total_properties.toString()}
          icon="🏠"
          color="purple"
        />
        <MetricCard
          title="Taxa de Conversão"
          value={`${metrics.conversion_rate}%`}
          icon="📈"
          color="amber"
        />
      </div>

      {/* Second row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Leads Ganhos"
          value={metrics.contacts_won.toString()}
          icon="✅"
          color="green"
        />
        <MetricCard
          title="Leads Perdidos"
          value={metrics.contacts_lost.toString()}
          icon="❌"
          color="red"
        />
        <MetricCard
          title="Mensagens Hoje"
          value={metrics.messages_today.toString()}
          icon="📨"
          color="blue"
        />
        <MetricCard
          title="Tempo Resposta Médio"
          value={`${Math.round(metrics.avg_response_time_seconds)}s`}
          icon="⚡"
          color="amber"
        />
      </div>

      {/* Charts placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Conversas por Canal</h3>
          <div className="space-y-3">
            <ChannelBar channel="WhatsApp" count={45} total={100} />
            <ChannelBar channel="Telefone" count={25} total={100} />
            <ChannelBar channel="E-mail" count={20} total={100} />
            <ChannelBar channel="Web Chat" count={10} total={100} />
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Pipeline de Vendas</h3>
          <div className="space-y-3">
            <PipelineStage stage="Novo Lead" count={120} color="bg-blue-500" />
            <PipelineStage stage="Qualificado" count={80} color="bg-yellow-500" />
            <PipelineStage stage="Proposta" count={45} color="bg-orange-500" />
            <PipelineStage stage="Fechado" count={20} color="bg-green-500" />
          </div>
        </div>
      </div>

      {/* Recent activity */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Atividade Recente</h3>
        <div className="space-y-4">
          <ActivityItem
            time="2 min atrás"
            message="Novo lead qualificado via WhatsApp"
            type="lead"
          />
          <ActivityItem
            time="15 min atrás"
            message="Visita agendada para amanhã às 14h"
            type="visit"
          />
          <ActivityItem
            time="1h atrás"
            message="Follow-up enviado para Maria Silva"
            type="followup"
          />
          <ActivityItem
            time="2h atrás"
            message="Chamada de voz concluída - João Santos"
            type="call"
          />
        </div>
      </div>
    </div>
  );
}

function MetricCard({
  title,
  value,
  icon,
  color,
}: {
  title: string;
  value: string;
  icon: string;
  color: string;
}) {
  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-50 text-blue-700',
    green: 'bg-green-50 text-green-700',
    purple: 'bg-purple-50 text-purple-700',
    amber: 'bg-amber-50 text-amber-700',
    red: 'bg-red-50 text-red-700',
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center text-xl ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function ChannelBar({ channel, count, total }: { channel: string; count: number; total: number }) {
  const percentage = (count / total) * 100;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm">
        <span className="text-gray-600">{channel}</span>
        <span className="font-medium text-gray-900">{count}</span>
      </div>
      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
        <div className="h-full bg-primary-500 rounded-full" style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}

function PipelineStage({ stage, count, color }: { stage: string; count: number; color: string }) {
  return (
    <div className="flex items-center gap-3">
      <div className={`w-3 h-3 rounded-full ${color}`} />
      <span className="flex-1 text-sm text-gray-600">{stage}</span>
      <span className="text-sm font-medium text-gray-900">{count}</span>
    </div>
  );
}

function ActivityItem({ time, message, type }: { time: string; message: string; type: string }) {
  const icons: Record<string, string> = {
    lead: '👤',
    visit: '📅',
    followup: '📨',
    call: '📞',
  };

  return (
    <div className="flex items-start gap-3">
      <span className="text-lg">{icons[type]}</span>
      <div className="flex-1">
        <p className="text-sm text-gray-900">{message}</p>
        <p className="text-xs text-gray-500">{time}</p>
      </div>
    </div>
  );
}
