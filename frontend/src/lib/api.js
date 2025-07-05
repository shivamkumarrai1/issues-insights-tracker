// src/lib/api.js
const API_BASE = 'http://localhost:8000';

export async function apiFetch(endpoint, method = 'GET', token = '', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { Authorization: `Bearer ${token}` })
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const res = await fetch(`${API_BASE}${endpoint}`, options);

    if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'API Error');
    }

    return res
}