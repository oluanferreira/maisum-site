/* The official journey carries only one explicit, valid campaign affiliate.
   It never reads cookies/storage, assigns an organic visitor, or changes payment rules. */
(() => {
  const values = new URLSearchParams(location.search).getAll('affiliate');
  if (values.length === 1 && /^[A-Za-z0-9_-]{1,128}$/.test(values[0])) {
    document.querySelectorAll('[data-checkout], [data-catalog]').forEach(link => {
      const url = new URL(link.getAttribute('href'), location.href);
      if (url.origin === location.origin || (url.origin === 'https://app.appmaisum.com.br' && url.pathname === '/checkout/black-friday')) {
        url.searchParams.set('affiliate', values[0]); link.href = url.toString();
      }
    });
  }
  const button = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobile-nav');
  const close = () => { button.setAttribute('aria-expanded', 'false'); button.setAttribute('aria-label', 'Abrir menu'); menu.hidden = true; };
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open)); button.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu'); menu.hidden = !open;
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) { close(); button.focus(); } });
  document.addEventListener('click', e => { if (!menu.hidden && !menu.contains(e.target) && !button.contains(e.target)) close(); });
  const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
  }, { threshold: 0.07 }) : null;
  if (observer && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.section-heading, .experience-card, .steps li, .membership-story, .passport-offer').forEach(el => { el.classList.add('will-reveal'); observer.observe(el); });
  }
})();
