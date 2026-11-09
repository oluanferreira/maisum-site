// Carry only one explicit campaign affiliate to the existing official homepage.
// No persistent storage, organic attribution, payment or commission rules.
(() => {
  const values = new URLSearchParams(location.search).getAll('affiliate');
  if (values.length !== 1 || !/^[A-Za-z0-9_-]{1,128}$/.test(values[0])) return;
  document.querySelectorAll('a[href]').forEach((link) => {
    const destination = new URL(link.href, location.href);
    if (destination.origin !== location.origin || destination.pathname !== '/') return;
    destination.searchParams.set('affiliate', values[0]);
    link.href = destination.toString();
  });
})();
// This navigation enhancement never hides content or changes link destinations.
(() => {
  if (!('IntersectionObserver' in window)) return;
  const links = [...document.querySelectorAll('.bottom-nav a[data-section]')];
  const sections = links.map((link) => document.getElementById(link.dataset.section));
  const active = new Map();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => active.set(entry.target.id, entry.isIntersecting));
    const section = sections.find((item) => active.get(item.id));
    if (!section) return;
    links.forEach((link) => {
      if (link.dataset.section === section.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-15% 0px -55% 0px', threshold: 0 });
  sections.forEach((section) => observer.observe(section));
})();
