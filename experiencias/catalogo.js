(() => {
  const form = document.getElementById('catalog-controls');
  const search = document.getElementById('catalog-search');
  const cards = [...document.querySelectorAll('.experience-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const count = document.getElementById('results-count');
  const reset = document.getElementById('reset-filters');
  const empty = document.getElementById('empty-state');
  if (!form || !search || !count || !cards.length) return;
  const normal = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR');
  let category = 'todas';
  const initial = new URLSearchParams(location.search);
  const requestedCategory = initial.get('categoria');
  if (filters.some((button) => button.dataset.filter === requestedCategory)) category = requestedCategory;
  search.value = (initial.get('busca') || '').slice(0, 160);
  form.hidden = false;
  function apply(updateURL = true) {
    const query = normal(search.value.trim());
    let total = 0;
    cards.forEach((card) => {
      const visible = (category === 'todas' || card.dataset.category === category) && normal(card.dataset.search).includes(query);
      card.hidden = !visible;
      if (visible) total++;
    });
    filters.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    count.textContent = `${total} ${total === 1 ? 'benefício gastronômico para explorar' : 'benefícios gastronômicos para explorar'}`;
    empty.hidden = total > 0;
    reset.hidden = !query && category === 'todas';
    if (updateURL) {
      const url = new URL(location.href);
      query ? url.searchParams.set('busca', search.value.trim()) : url.searchParams.delete('busca');
      category === 'todas' ? url.searchParams.delete('categoria') : url.searchParams.set('categoria', category);
      url.searchParams.delete('experiencia');
      history.replaceState(null, '', url);
    }
  }
  search.addEventListener('input', () => apply());
  form.addEventListener('submit', (event) => { event.preventDefault(); apply(); });
  filters.forEach((button) => button.addEventListener('click', () => { category = button.dataset.filter; apply(); }));
  function clear() { search.value = ''; category = 'todas'; apply(); search.focus(); }
  reset.addEventListener('click', clear);
  document.getElementById('empty-reset')?.addEventListener('click', clear);
  apply(false);
  const selectedId = initial.get('experiencia');
  const selected = cards.find((card) => card.dataset.id === selectedId);
  if (selected) {
    search.value = ''; category = 'todas'; apply(false);
    selected.querySelector('details').open = true;
    selected.classList.add('highlighted');
    requestAnimationFrame(() => selected.scrollIntoView({ block: 'start', behavior: 'instant' }));
  }
  cards.forEach((card) => {
    const img = card.querySelector('img');
    if (!img) return;
    const onError = () => card.classList.add('image-error');
    img.addEventListener('error', onError);
    if (img.complete && !img.naturalWidth) onError();
  });
})();
