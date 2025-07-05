// src/lib/api/client.js
export const API_BASE = 'http://localhost:8000';

export async function api(endpoint, method = 'GET', data, authToken) {
    const config = {
        method,
        headers: {
            'Content-Type': 'application/json',
            ...(authToken && { Authorization: `Bearer ${authToken}` })
        }
    };

    if (data) config.body = JSON.stringify(data);

    const res = await fetch(`${API_BASE}${endpoint}`, config);
    if (!res.ok) {
        const error = await res.text();
        throw new Error(error || 'API error');
    }

    return await res.json();
}