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
  const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
  }, { threshold: 0.07 }) : null;
  if (observer && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.section-heading, .experience-card, .steps li, .membership-story, .passport-offer').forEach(el => { el.classList.add('will-reveal'); observer.observe(el); });
  }
})();
