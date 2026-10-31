// Theme switching logic (Dark / Light mode)
(function() {
  const THEME_STORAGE_KEY = 'interview_master_theme';

  function getPreferredTheme() {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    if (savedTheme) {
      return savedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem(THEME_STORAGE_KEY, theme);
    updateThemeIcon(theme);
  }

  function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('theme-toggle-icon');
    if (!themeIcon) return;
    if (theme === 'dark') {
      themeIcon.className = 'bi bi-sun-fill text-warning';
    } else {
      themeIcon.className = 'bi bi-moon-stars-fill text-primary';
    }
  }

  // Apply immediately on load
  const initialTheme = getPreferredTheme();
  setTheme(initialTheme);

  document.addEventListener('DOMContentLoaded', () => {
    updateThemeIcon(getPreferredTheme());
    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(nextTheme);
      });
    }
  });
})();
