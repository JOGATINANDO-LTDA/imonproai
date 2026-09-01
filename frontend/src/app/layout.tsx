import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ImobPro.ai - Dashboard',
  description: 'Agente Comercial de IA para Imobiliárias',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
