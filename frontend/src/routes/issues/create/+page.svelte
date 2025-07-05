<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { apiFetch } from '$lib/api.js';

  let token = '';
  let title = '';
  let description = '';
  let severity = 'LOW';
  let file_path = '';
  let error = '';

  onMount(() => {
    token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
    }
  });

  async function createIssue() {
    try {
      await apiFetch('/api/issues/', 'POST', token, {
        title,
        description,
        severity,
        file_path
      });

      goto('/dashboard');
    } catch (err) {
      error = err.message;
    }
  }
</script>

<style>
  .container {
    max-width: 500px;
    margin: 3rem auto;
    padding: 2rem;
    background: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 0 10px #eee;
  }

  h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 2rem;
  }

  label {
    font-weight: 600;
    margin-top: 1rem;
    display: block;
  }

  input, select, textarea {
    width: 100%;
    padding: 0.6rem;
    margin-top: 0.3rem;
    margin-bottom: 1rem;
    border-radius: 4px;
    border: 1px solid #ccc;
  }

  button {
    width: 100%;
    padding: 0.75rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    cursor: pointer;
  }

  button:hover {
    background-color: #2980b9;
  }

  .error {
    color: red;
    text-align: center;
    margin-bottom: 1rem;
  }
</style>

<div class="container">
  <h1>Create New Issue</h1>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <form on:submit|preventDefault={createIssue}>
    <label>Title:</label>
    <input bind:value={title} required />

    <label>Description:</label>
    <textarea bind:value={description} required></textarea>

    <label>Severity:</label>
    <select bind:value={severity}>
      <option value="LOW">LOW</option>
      <option value="MEDIUM">MEDIUM</option>
      <option value="HIGH">HIGH</option>
      <option value="CRITICAL">CRITICAL</option>
    </select>

    <label>File Path:</label>
    <input bind:value={file_path} required />

    <button type="submit">Create Issue</button>
  </form>
</div>
