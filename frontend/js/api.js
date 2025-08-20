const API_BASE = 'http://127.0.0.1:8000';

const ENDPOINTS = {
  create: '/contractors',                      
  list: '/contractors',
  prequalify: (id) => `/contractors/${id}/prequalify`,
  summary: '/bff/contractors/summary'
};

async function api(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });

  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }

  if (!res.ok) {
    console.error('API error', res.status, data);
    const msg = (data && (data.detail || data.message)) || res.statusText;
    throw new Error(typeof msg === 'string' ? msg : 'Request failed');
  }
  return data;
}
