// Forward only a single explicit, valid campaign affiliate to owned navigation
// and the verified Black Friday purchase entry. Organic visits remain unassigned.
// No persistent storage, arbitrary query forwarding, or commission rules.
(() => {
  const values = new URLSearchParams(location.search).getAll('affiliate');
  if (values.length !== 1 || !/^[A-Za-z0-9_-]{1,128}$/.test(values[0])) return;
  const localPaths = new Set(['/', '/links', '/links/', '/experiencias', '/experiencias/']);
  document.querySelectorAll('a[href]').forEach((link) => {
    const destination = new URL(link.href, location.href);
    const ownedPage = destination.origin === location.origin && localPaths.has(destination.pathname);
    const purchaseEntry = destination.origin === 'https://app.appmaisum.com.br' && destination.pathname === '/checkout/black-friday';
    if (!ownedPage && !purchaseEntry) return;
    destination.searchParams.set('affiliate', values[0]);
    link.href = destination.toString();
  });
})();
