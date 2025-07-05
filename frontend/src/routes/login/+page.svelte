<script>
  import { goto } from '$app/navigation';

  let email = '';
  let password = '';
  let error = '';

  async function handleLogin() {
    error = '';
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const res = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
      });

      if (!res.ok) {
        const { detail } = await res.json();
        throw new Error(detail || 'Login failed');
      }

      const { access_token } = await res.json();
      localStorage.setItem('token', access_token);
      goto('/dashboard');
    } catch (err) {
      error = err?.message || JSON.stringify(err);
    }
  }
</script>

<style>
  .form-container {
    max-width: 400px;
    margin: 5rem auto;
    padding: 2rem;
    background: var(--card-bg);
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  h1 {
    text-align: center;
    margin-bottom: 1.5rem;
    color: var(--text-color);
  }

  label {
    display: block;
    margin-top: 1rem;
    font-weight: bold;
    color: var(--text-color);
  }

  input {
    width: 100%;
    padding: 0.6rem;
    margin-top: 0.3rem;
    border-radius: 6px;
    border: 1px solid #ccc;
    background-color: transparent;
    color: var(--text-color);
  }

  input::placeholder {
    color: #aaa;
  }

  button {
    margin-top: 1.5rem;
    width: 100%;
    padding: 0.75rem;
    background-color: var(--btn-bg);
    color: var(--btn-text);
    font-weight: bold;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }

  button:hover {
    opacity: 0.9;
  }

  .error {
    color: red;
    margin-top: 1rem;
    text-align: center;
  }
</style>

<div class="form-container">
  <h1>Login</h1>

  <form on:submit|preventDefault={handleLogin}>
    <label for="email">Email</label>
    <input
      id="email"
      type="email"
      bind:value={email}
      required
      placeholder="Enter your email" />

    <label for="password">Password</label>
    <input
      id="password"
      type="password"
      bind:value={password}
      required
      placeholder="Enter your password" />

    <button type="submit">Login</button>
  </form>

  {#if error}
    <p class="error">{error}</p>
  {/if}
</div>

