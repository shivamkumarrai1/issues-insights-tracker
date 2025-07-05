<script>
  import '$lib/app.css';
  import Nav from '$lib/Nav.svelte';

  let darkMode = false;

  // Load saved theme from localStorage
  if (typeof window !== 'undefined') {
    darkMode = localStorage.getItem('theme') === 'dark';
    updateTheme();
  }

  function toggleDarkMode() {
    darkMode = !darkMode;
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
    updateTheme();
  }

  function updateTheme() {
    document.documentElement.classList.toggle('dark', darkMode);
  }
</script>

<!-- Dark Mode Toggle -->
<button
  on:click={toggleDarkMode}
  style="
    position: fixed;
    top: 1rem;
    right: 1rem;
    padding: 0.4rem 1rem;
    border: none;
    border-radius: 5px;
    background-color: var(--btn-bg);
    color: var(--btn-text);
    cursor: pointer;
    z-index: 999;
  "
>
  {darkMode ? '🌙 Dark' : '☀️ Light'}
</button>

<!-- Shared navigation bar -->
<Nav />

<main class="p-8">
  <slot />
</main>

