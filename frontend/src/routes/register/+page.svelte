<script>
  import { goto } from '$app/navigation';

  let email = '';
  let password = '';
  let role = 'REPORTER'; // Default role
  let error = '';

  async function handleRegister() {
    error = '';

    try {
      const res = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email,
          password,
          role
        })
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Registration failed');
      }

      goto('/login');
    } catch (err) {
      error = err.message || JSON.stringify(err);
    }
  }
</script>

<style>
  .container {
    max-width: 400px;
    margin: 3rem auto;
    padding: 2rem;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
    background: #fafafa;
  }

  h1 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: #2c3e50;
  }

  label {
    font-weight: 600;
    margin-top: 1rem;
    display: block;
  }

  input, select {
    width: 100%;
    padding: 0.5rem;
    margin-top: 0.25rem;
    margin-bottom: 1rem;
    border-radius: 4px;
    border: 1px solid #ccc;
  }

  button {
    width: 100%;
    padding: 0.6rem;
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    cursor: pointer;
  }

  button:hover {
    background-color: #219150;
  }

  .error {
    color: red;
    text-align: center;
    margin-top: 1rem;
  }
</style>

<div class="container">
  <h1>Register</h1>

  <form on:submit|preventDefault={handleRegister}>
    <label for="email">Email</label>
    <input id="email" type="email" bind:value={email} required />

    <label for="password">Password</label>
    <input id="password" type="password" bind:value={password} required />

    <label for="role">Role</label>
    <select id="role" bind:value={role}>
      <option value="ADMIN">ADMIN</option>
      <option value="MAINTAINER">MAINTAINER</option>
      <option value="REPORTER">REPORTER</option>
    </select>

    <button type="submit">Register</button>
  </form>

  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>
