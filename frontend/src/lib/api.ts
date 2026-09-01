const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface RequestInit {
  method?: string;
  body?: any;
  headers?: Record<string, string>;
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Erro desconhecido' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export const api = {
  get: <T>(endpoint: string) => request<T>(endpoint),
  post: <T>(endpoint: string, body: any) => request<T>(endpoint, { method: 'POST', body }),
  patch: <T>(endpoint: string, body: any) => request<T>(endpoint, { method: 'PATCH', body }),
  delete: <T>(endpoint: string) => request<T>(endpoint, { method: 'DELETE' }),
};

// Auth
export const authApi = {
  login: (email: string, password: string) =>
    api.post<{ access_token: string; refresh_token: string }>('/api/auth/login', { email, password }),
  register: (data: { email: string; password: string; full_name: string }) =>
    api.post<any>('/api/auth/register', data),
  me: () => api.get<any>('/api/auth/me'),
};

// Dashboard
export const dashboardApi = {
  metrics: () => api.get<any>('/api/v1/dashboard/metrics'),
};

// Contacts
export const contactsApi = {
  list: (params?: { status?: string; skip?: number; limit?: number }) => {
    const query = new URLSearchParams(params as any).toString();
    return api.get<any[]>(`/api/v1/contacts${query ? `?${query}` : ''}`);
  },
  get: (id: string) => api.get<any>(`/api/v1/contacts/${id}`),
  create: (data: any) => api.post<any>('/api/v1/contacts', data),
  update: (id: string, data: any) => api.patch<any>(`/api/v1/contacts/${id}`, data),
};

// Properties
export const propertiesApi = {
  list: (params?: any) => {
    const query = new URLSearchParams(params).toString();
    return api.get<any[]>(`/api/v1/properties${query ? `?${query}` : ''}`);
  },
  get: (id: string) => api.get<any>(`/api/v1/properties/${id}`),
  create: (data: any) => api.post<any>('/api/v1/properties', data),
  update: (id: string, data: any) => api.patch<any>(`/api/v1/properties/${id}`, data),
};

// Agents
export const agentsApi = {
  list: () => api.get<any[]>('/api/v1/agents'),
  get: (id: string) => api.get<any>(`/api/v1/agents/${id}`),
  create: (data: any) => api.post<any>('/api/v1/agents', data),
  update: (id: string, data: any) => api.patch<any>(`/api/v1/agents/${id}`, data),
};

// Conversations
export const conversationsApi = {
  list: (params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams(params as any).toString();
    return api.get<any[]>(`/api/v1/conversations${query ? `?${query}` : ''}`);
  },
  get: (id: string) => api.get<any>(`/api/v1/conversations/${id}`),
};

// Users
export const usersApi = {
  list: () => api.get<any[]>('/api/v1/users'),
};
