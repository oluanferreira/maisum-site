// Preserve only an explicit, valid campaign affiliate on the official purchase path.
// Organic visits remain unassigned. No cookies/storage, default affiliate or payout logic.
(() => {
  const affiliates = new URLSearchParams(window.location.search).getAll('affiliate');
  if (affiliates.length !== 1 || !/^[A-Za-z0-9_-]{1,128}$/.test(affiliates[0])) return;

  document.querySelectorAll('a[href]').forEach((link) => {
    const destination = new URL(link.href, window.location.href);
    const checkout = destination.origin === 'https://pay.cakto.com.br' &&
      destination.pathname === '/3e7t64x_1061003';
    const ownPage = destination.origin === window.location.origin &&
      ['/', '/links', '/links/'].includes(destination.pathname);
    if (!checkout && !ownPage) return;
    destination.searchParams.set('affiliate', affiliates[0]);
    link.href = destination.toString();
  });
})();
