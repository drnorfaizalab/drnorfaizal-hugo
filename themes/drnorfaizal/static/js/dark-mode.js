// Dark mode toggle
const saved = localStorage.getItem('darkMode');
if (saved === 'true') {
  document.documentElement.classList.add('dark-mode');
}

const toggle = document.getElementById('dark-mode-toggle');
if (toggle) {
  toggle.addEventListener('click', () => {
    const isDark = document.documentElement.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDark);
  });
}
