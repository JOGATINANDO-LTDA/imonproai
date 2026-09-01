'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="text-center space-y-8 p-8">
        <div className="space-y-4">
          <h1 className="text-5xl font-bold text-primary-900">ImobPro.ai</h1>
          <p className="text-xl text-primary-700">Agente Comercial de IA para Imobiliárias</p>
          <p className="text-gray-600 max-w-md mx-auto">
            Seu vendedor virtual que não dorme, não esquece e fecha negócios 24/7
          </p>
        </div>
        <div className="flex gap-4 justify-center">
          <Link
            href="/dashboard"
            className="px-8 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            Acessar Dashboard
          </Link>
          <Link
            href="/login"
            className="px-8 py-3 border border-primary-600 text-primary-600 rounded-lg font-medium hover:bg-primary-50 transition-colors"
          >
            Login
          </Link>
        </div>
        <div className="grid grid-cols-3 gap-6 max-w-2xl mx-auto mt-12">
          <FeatureCard
            title="WhatsApp & SMS"
            description="Atenda leads automaticamente por WhatsApp"
          />
          <FeatureCard
            title="Chamadas de Voz"
            description="Receba e faça ligações com IA"
          />
          <FeatureCard
            title="Follow-ups"
            description="Nunca mais esqueça de retomar um lead"
          />
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
      <h3 className="font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );
}
