const menuButton = document.querySelector('.menu-button');
const mobileMenu = document.querySelector('.mobile-menu');

menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!open));
  if (mobileMenu) mobileMenu.hidden = open;
});

mobileMenu?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuButton?.setAttribute('aria-expanded', 'false');
    mobileMenu.hidden = true;
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add('is-visible');
  });
}, { threshold: 0.12 });

document.querySelectorAll('[data-reveal]').forEach((element) => revealObserver.observe(element));

const experienceRail = document.querySelector('.experience-rail');
const experienceTrack = document.querySelector('.experience-track');
const experienceSets = [...document.querySelectorAll('.experience-set')];
const filterButtons = [...document.querySelectorAll('.experience-filters button')];

if (experienceRail && experienceTrack && experienceSets.length === 2) {
  const gastronomyCards = experienceSets[0].innerHTML;
  const moreCard = experienceSets[0].querySelector('.card-more')?.outerHTML ?? '';
  const otherExperiences = [
    {
      item: 'Creche canina',
      partner: 'Cão Primitivo',
      price: 'R$ 70,00',
      detail: 'Um dia de diversão para o seu amigo',
      image: '/assets/creche-canina.jpg',
    },
    {
      item: 'Corte + Barba',
      partner: 'Mens Club Barbearia',
      price: 'R$ 55,00',
      detail: 'Cuidado pessoal também pode ser em dobro',
      image: '/assets/corte-barba.jpeg',
    },
  ];

  const experienceCard = ({ item, partner, price, detail, image }) => `
    <article class="experience-card experience-photo-card" data-experience-card="true">
      <img class="experience-photo" src="${image}" alt="${item} no ${partner}" loading="lazy">
      <div class="experience-shade" aria-hidden="true"></div>
      <div class="experience-meta"><span>Outros</span></div>
      <div class="experience-plus" aria-hidden="true"><span>+</span>1</div>
      <div class="experience-copy">
        <p class="experience-partner">${partner}</p>
        <h3>${item}</h3>
        <p class="experience-detail">${detail}</p>
        <div class="experience-values"><div><span>Valor do item</span><strong>${price}</strong></div></div>
      </div>
    </article>`;

  const renderExperiences = (category) => {
    const cards = category === 'Gastronomia'
      ? gastronomyCards
      : otherExperiences.map(experienceCard).join('') + moreCard;

    experienceSets[0].innerHTML = cards;
    experienceSets[1].innerHTML = cards.replaceAll('<article ', '<article aria-hidden="true" ');
    experienceRail.setAttribute('aria-label', `Experiências de ${category}`);

    filterButtons.forEach((button) => {
      const active = button.textContent.trim() === category;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });

    experienceTrack.style.animation = 'none';
    void experienceTrack.offsetWidth;
    experienceTrack.style.animation = '';
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => renderExperiences(button.textContent.trim()));
  });
}
