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
    available: 'bg-green-100 text-green-800',
    sold: 'bg-red-100 text-red-800',
    rented: 'bg-blue-100 text-blue-800',
    reserved: 'bg-yellow-100 text-yellow-800',
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
            className="px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 w-64"
          />
          <select className="px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500">
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
            <div key={i} className="bg-white rounded-xl border border-gray-200 p-4 animate-pulse">
              <div className="h-40 bg-gray-100 rounded-lg mb-4" />
              <div className="h-4 bg-gray-100 rounded w-3/4 mb-2" />
              <div className="h-4 bg-gray-100 rounded w-1/2" />
            </div>
          ))
        ) : properties.length === 0 ? (
          <div className="col-span-full p-8 text-center text-gray-500 bg-white rounded-xl border border-gray-200">
            Nenhum imóvel cadastrado
          </div>
        ) : (
          properties.map((property) => (
            <div key={property.id} className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
              <div className="h-40 bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
                <span className="text-4xl">🏠</span>
              </div>
              <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-gray-900">{property.title}</h3>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[property.status]}`}>
                    {statusLabels[property.status]}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{property.address}</p>
                <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                  <span>🛏 {property.bedrooms}</span>
                  <span>🚿 {property.bathrooms}</span>
                  <span>📐 {property.area_m2}m²</span>
                </div>
                <p className="text-lg font-bold text-primary-700">{formatCurrency(property.price)}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
