<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { apiFetch } from '$lib/api.js';

  let token = '';
  let issues = [];
  let error = '';
  let issuesVisible = false;

  async function fetchIssues() {
    error = '';
    try {
      const res = await apiFetch('/api/issues/', 'GET', token);
      issues = await res.json();
      issuesVisible = true;
    } catch (err) {
      error = err.message || JSON.stringify(err);
    }
  }

  function connectSSE() {
    const eventSource = new EventSource('http://localhost:8000/api/stream/');

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.event === 'issue_created') {
        issues = [data, ...issues];
      }

      if (data.event === 'issue_updated') {
        issues = issues.map(issue =>
          issue.id === data.issue_id
            ? { ...issue, status: data.status, title: data.title }
            : issue
        );
      }
    };

    eventSource.onerror = (err) => {
      console.error('SSE error:', err);
      eventSource.close();
    };
  }

  function editIssue(id) {
    goto(`/issues/${id}/edit`);
  }

  function createNewIssue() {
    goto('/issues/create');
  }

  function logout() {
    localStorage.removeItem('token');
    goto('/login');
  }

  function deleteIssue(id) {
    if (!confirm('Are you sure you want to delete this issue?')) return;

    apiFetch(`/api/issues/${id}`, 'DELETE', token)
      .then(() => {
        issues = issues.filter(issue => issue.id !== id);
      })
      .catch(err => {
        error = err.message || JSON.stringify(err);
      });
  }

  onMount(() => {
    token = localStorage.getItem('token');
    if (!token) {
      goto('/login');
      return;
    }

    connectSSE(); // SSE still active to get updates
  });
</script>

<style>
  h1 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #2c3e50;
  }

  .actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .actions button {
    padding: 0.5rem 1rem;
    font-weight: bold;
    border: none;
    background-color: #3498db;
    color: white;
    cursor: pointer;
    border-radius: 4px;
  }

  .actions button:hover {
    background-color: #2980b9;
  }

  .issue-card {
    margin: 1rem auto;
    padding: 1rem;
    border-radius: 6px;
    border: 1px solid #ddd;
    width: 80%;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
  }

  .issue-card h3 {
    margin-bottom: 0.5rem;
    color: #333;
  }

  .issue-card p {
    margin: 0.2rem 0;
  }

  .issue-card button {
    margin-top: 0.5rem;
    padding: 0.4rem 0.8rem;
    margin-right: 0.5rem;
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .issue-card button:last-child {
    background-color: #e74c3c;
  }

  .issue-card button:hover {
    opacity: 0.9;
  }

  .error {
    color: red;
    text-align: center;
    margin-top: 1rem;
  }

  .info {
    text-align: center;
    margin-top: 1rem;
    color: #666;
  }
</style>

<h1>📊 Dashboard</h1>

<div class="actions">
  <button on:click={createNewIssue}>➕ Create Issue</button>
  <button on:click={fetchIssues}>📋 Show All Issues</button>
  <button on:click={logout}>🚪 Logout</button>
</div>

{#if error}
  <p class="error">{error}</p>
{/if}

{#if issuesVisible}
  {#each issues as issue}
    <div class="issue-card">
      <h3>{issue.title}</h3>
      <p><strong>Description:</strong> {issue.description}</p>
      <p><strong>Status:</strong> {issue.status}</p>
      <p><strong>Severity:</strong> {issue.severity}</p>
      <p><strong>File Path:</strong> {issue.file_path}</p>

      <button on:click={() => editIssue(issue.id)}>✏️ Edit</button>
      <button on:click={() => deleteIssue(issue.id)}>🗑️ Delete</button>
    </div>
  {/each}
{:else}
  <p class="info">Click "📋 Show All Issues" to load your issues.</p>
{/if}
