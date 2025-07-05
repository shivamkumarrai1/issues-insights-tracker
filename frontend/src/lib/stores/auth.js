// src/lib/stores/auth.js
import { writable } from 'svelte/store';

export const user = writable(null);
export const token = writable(localStorage.getItem('token') || '');

token.subscribe(value => {
    if (value) localStorage.setItem('token', value);
    else localStorage.removeItem('token');
});