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
