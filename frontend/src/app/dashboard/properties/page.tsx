'use client';

import { useEffect, useState } from 'react';
import { propertiesApi } from '@/lib/api';
import { formatCurrency, formatDate } from '@/lib/utils';

interface Property {
  id: string;
  title: string;
  description: string;
  price: number;
  address: string;
  bedrooms: number;
  bathrooms: number;
  area_m2: number;
  property_type: string;
  status: string;
  features: string[];
  created_at: string;
}

export default function PropertiesPage() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    propertiesApi.list().then(setProperties).finally(() => setLoading(false));
  }, []);

  const statusColors: Record<string, string> = {
    available: 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300',
    sold: 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300',
    rented: 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300',
    reserved: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300',
  };

  const statusLabels: Record<string, string> = {
    available: 'Disponível',
    sold: 'Vendido',
    rented: 'Alugado',
    reserved: 'Reservado',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <input
            type="text"
            placeholder="Buscar imóveis..."
            className="px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500 w-64"
          />
          <select className="px-4 py-2 border border-gray-200 dark:border-slate-600 rounded-lg text-sm bg-white dark:bg-slate-700 text-gray-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
            <option value="">Todos os tipos</option>
            <option value="apartment">Apartamento</option>
            <option value="house">Casa</option>
            <option value="land">Terreno</option>
            <option value="commercial">Comercial</option>
          </select>
        </div>
        <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors">
          + Novo Imóvel
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-4 animate-pulse">
              <div className="h-40 bg-gray-100 dark:bg-slate-700 rounded-lg mb-4" />
              <div className="h-4 bg-gray-100 dark:bg-slate-700 rounded w-3/4 mb-2" />
              <div className="h-4 bg-gray-100 dark:bg-slate-700 rounded w-1/2" />
            </div>
          ))
        ) : properties.length === 0 ? (
          <div className="col-span-full p-8 text-center text-gray-500 dark:text-slate-400 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700">
            Nenhum imóvel cadastrado
          </div>
        ) : (
          properties.map((property) => (
            <div key={property.id} className="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden hover:shadow-lg transition-shadow">
              <div className="h-40 bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900/30 dark:to-primary-800/30 flex items-center justify-center">
                <span className="text-4xl">🏠</span>
              </div>
              <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 dark:text-slate-100">{property.title}</h3>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[property.status]}`}>
                    {statusLabels[property.status]}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-slate-400 mb-3">{property.address}</p>
                <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-slate-400 mb-3">
                  <span>🛏 {property.bedrooms}</span>
                  <span>🚿 {property.bathrooms}</span>
                  <span>📐 {property.area_m2}m²</span>
                </div>
                <p className="text-lg font-bold text-primary-700 dark:text-primary-300">{formatCurrency(property.price)}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
