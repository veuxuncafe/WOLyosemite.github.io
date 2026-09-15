const themeButton = document.querySelector('.theme-toggle');
const savedTheme = localStorage.getItem('veuxuncafe-theme');
if (savedTheme === 'dark') document.body.classList.add('dark');
if (themeButton) {
  const updateThemeLabel = () => { themeButton.textContent = document.body.classList.contains('dark') ? '浅色模式' : '深色模式'; };
  updateThemeLabel();
  themeButton.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    localStorage.setItem('veuxuncafe-theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    updateThemeLabel();
  });
}

const filters = document.querySelectorAll('[data-filter]');
const articles = document.querySelectorAll('.article-item');
filters.forEach((filter) => filter.addEventListener('click', () => {
  filters.forEach((item) => item.classList.remove('active'));
  filter.classList.add('active');
  const selected = filter.dataset.filter;
  articles.forEach((article) => { article.hidden = selected !== 'all' && article.dataset.category !== selected; });
}));
