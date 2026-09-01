'use client';

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Configurações da Imobiliária</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nome da Imobiliária</label>
            <input
              type="text"
              defaultValue="Imobiliária Modelo"
              className="w-full px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">CNPJ</label>
            <input
              type="text"
              defaultValue="00.000.000/0001-00"
              className="w-full px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Regras Comerciais (para o agente IA)</label>
            <textarea
              rows={4}
              defaultValue="Não oferecer descontos superiores a 5%. Sempre agendar visitas para período da manhã ou tarde. Priorizar imóveis com vista e aceitar negociação em até 3x parcelas."
              className="w-full px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>
        <button className="mt-4 px-6 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          Salvar Alterações
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Integrações</h3>
        <div className="space-y-4">
          <IntegrationRow name="WhatsApp (Evolution API)" status="connected" />
          <IntegrationRow name="Telefone (Twilio)" status="connected" />
          <IntegrationRow name="E-mail (SMTP)" status="disconnected" />
          <IntegrationRow name="OpenAI" status="connected" />
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Equipe</h3>
        <p className="text-sm text-gray-600 mb-4">Gerencie os acessos da sua equipe ao sistema</p>
        <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          + Adicionar Membro
        </button>
      </div>
    </div>
  );
}

function IntegrationRow({ name, status }: { name: string; status: string }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
      <span className="text-sm text-gray-900">{name}</span>
      <span
        className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
          status === 'connected' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
        }`}
      >
        {status === 'connected' ? 'Conectado' : 'Desconectado'}
      </span>
    </div>
  );
}
