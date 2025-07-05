<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { apiFetch } from '$lib/api.js';
  import { page } from '$app/stores';

  let issueId;
  let title = '';
  let description = '';
  let severity = 'LOW';
  let status = 'OPEN';
  let file_path = '';
  let error = '';

  $: issueId = $page.params.id;

  async function fetchIssue() {
    error = '';
    try {
      const token = localStorage.getItem('token');
      const res = await apiFetch(`/api/issues/${issueId}`, 'GET', token);
      const data = await res.json();

      title = data.title;
      description = data.description;
      severity = data.severity;
      status = data.status;
      file_path = data.file_path;
    } catch (err) {
      const msg = err.message || '';
      if (msg.includes('Forbidden')) {
        error = "❌ Only ADMINs can edit issues";
      } else if (msg.includes('Issue not found')) {
        error = "❌ Issue not found";
      } else {
        error = msg;
      }
    }
  }

  async function updateIssue() {
    error = '';
    try {
      const token = localStorage.getItem('token');
      const res = await apiFetch(`/api/issues/${issueId}`, 'PUT', token, {
        title,
        description,
        severity,
        status,
        file_path
      });
      await res.json();
      goto('/dashboard');
    } catch (err) {
      const msg = err.message || '';
      if (msg.includes('Forbidden')) {
        error = "❌ Only ADMINs can edit issues";
      } else {
        error = msg;
      }
    }
  }

  onMount(() => {
    fetchIssue();
  });
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
    background-color: #e67e22;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    cursor: pointer;
  }

  button:hover {
    background-color: #d35400;
  }

  .error {
    color: red;
    text-align: center;
    margin-bottom: 1rem;
  }
</style>

<div class="container">
  <h1>Edit Issue</h1>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <form on:submit|preventDefault={updateIssue}>
    <label>Title:</label>
    <input type="text" bind:value={title} required />

    <label>Description:</label>
    <textarea bind:value={description}></textarea>

    <label>Severity:</label>
    <select bind:value={severity}>
      <option value="LOW">LOW</option>
      <option value="MEDIUM">MEDIUM</option>
      <option value="HIGH">HIGH</option>
      <option value="CRITICAL">CRITICAL</option>
    </select>

    <label>Status:</label>
    <select bind:value={status}>
      <option value="OPEN">OPEN</option>
      <option value="TRIAGED">TRIAGED</option>
      <option value="IN_PROGRESS">IN_PROGRESS</option>
      <option value="DONE">DONE</option>
    </select>

    <label>File Path:</label>
    <input type="text" bind:value={file_path} />

    <button type="submit">Update Issue</button>
  </form>
</div>

