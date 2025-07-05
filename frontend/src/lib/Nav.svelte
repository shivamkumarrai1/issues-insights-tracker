<script>
  import { goto } from '$app/navigation';

  function logout() {
    localStorage.removeItem('token');
    goto('/login');
  }
</script>

<style>
  nav {
    background-color: #f0f0f0;
    padding: 1rem;
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #ccc;
  }

  .nav-links {
    display: flex;
    gap: 1rem;
  }

  a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
  }

  button {
    background-color: #e63946;
    color: white;
    border: none;
    padding: 6px 12px;
    cursor: pointer;
    border-radius: 4px;
  }

  button:hover {
    background-color: #d62828;
  }
</style>

<nav>
  <div class="nav-links">
    <a href="/dashboard">Dashboard</a>
    <a href="/login">Login</a>
    <a href="/register">Register</a>
  </div>
  <button on:click={logout}>Logout</button>
</nav>

