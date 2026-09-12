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
    if (mobileMenu) mobileMenu.hidden = true;
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add('is-visible');
  });
}, { threshold: 0.12 });

document.querySelectorAll('[data-reveal]').forEach((element) => revealObserver.observe(element));

// Preview V2: preserva o visual atual e melhora apenas comportamento e clareza.
const enhancementStyles = document.createElement('style');
enhancementStyles.textContent = `
  .experience-rail {
    overflow-x: auto !important;
    cursor: grab;
    touch-action: pan-y;
    user-select: none;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
    scroll-snap-type: x mandatory !important;
  }
  .experience-rail::-webkit-scrollbar { display: none; }
  .experience-rail.is-dragging { cursor: grabbing; }
  .experience-track {
    animation: none !important;
    transform: none !important;
    will-change: auto;
  }
  .experience-card { scroll-snap-align: center !important; }
  .experience-photo { -webkit-user-drag: none; user-select: none; }
  .card-more { cursor: pointer; }
  .card-more:focus-visible { outline: 2px solid var(--orange); outline-offset: 5px; }

  @media (width <= 759px) {
    .experience-rail {
      padding-inline: 16px !important;
      scroll-padding-inline: 16px;
    }
    .experience-track,
    .experience-set { gap: 12px !important; }
    .experience-card {
      flex: 0 0 calc(100vw - 32px) !important;
      max-width: calc(100vw - 32px) !important;
    }
  }
`;
document.head.appendChild(enhancementStyles);

const setLinkLabel = (link, label) => {
  if (!link) return;
  const arrow = link.querySelector('span');
  link.textContent = label + ' ';
  if (arrow) link.appendChild(arrow);
};

setLinkLabel(document.querySelector('.hero-actions .button-primary'), 'Quero meu passaporte +UM');
setLinkLabel(document.querySelector('.membership .button-dark'), 'Quero meu passaporte +UM');
setLinkLabel(document.querySelector('.sticky-mobile-cta'), 'Quero meu passaporte +UM');

const ticketStage = document.querySelector('.ticket-stage');
const ticketLabel = document.querySelector('.ticket-front .ticket-top span');
if (ticketLabel) ticketLabel.textContent = 'SEU PASSAPORTE';
if (ticketStage) {
  ticketStage.setAttribute('aria-label', 'Dois passaportes +UM interativos representando uma experiência em dobro. Toque e arraste para separar os passaportes.');
}

const membershipEyebrow = document.querySelector('.membership .eyebrow');
if (membershipEyebrow) {
  const dot = membershipEyebrow.querySelector('span');
  membershipEyebrow.textContent = ' seu passaporte para a cidade';
  if (dot) membershipEyebrow.prepend(dot);
}

document.querySelectorAll('.faq-list details').forEach((detail) => {
  const summary = detail.querySelector('summary');
  const answer = detail.querySelector('p');
  if (summary?.textContent.includes('delivery') && answer) {
    answer.textContent = 'Algumas experiências terão opção de delivery. A disponibilidade e as condições de cada parceiro aparecem na plataforma antes da emissão do cupom.';
  }
});

// O “toque e arraste” do hero passa a funcionar de verdade.
if (ticketStage) {
  let activePointer = null;
  let startX = 0;
  let startY = 0;
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

  const resetTickets = () => {
    ticketStage.classList.remove('is-touching', 'is-exploring');
    ticketStage.style.setProperty('--front-x', '0px');
    ticketStage.style.setProperty('--back-x', '0px');
    ticketStage.style.setProperty('--card-y', '0px');
    ticketStage.style.setProperty('--back-y', '0px');
    ticketStage.style.setProperty('--tilt-x', '0deg');
    ticketStage.style.setProperty('--tilt-y', '0deg');
    activePointer = null;
  };

  ticketStage.addEventListener('pointerdown', (event) => {
    activePointer = event.pointerId;
    startX = event.clientX;
    startY = event.clientY;
    ticketStage.setPointerCapture?.(event.pointerId);
    ticketStage.classList.add('is-touching');
  });

  ticketStage.addEventListener('pointermove', (event) => {
    if (event.pointerId !== activePointer) return;
    const dx = clamp(event.clientX - startX, -120, 120);
    const dy = clamp(event.clientY - startY, -55, 55);
    ticketStage.style.setProperty('--front-x', `${dx * 0.72}px`);
    ticketStage.style.setProperty('--back-x', `${-dx * 0.42}px`);
    ticketStage.style.setProperty('--card-y', `${dy * 0.28}px`);
    ticketStage.style.setProperty('--back-y', `${-dy * 0.14}px`);
    ticketStage.style.setProperty('--tilt-x', `${clamp(-dy / 12, -5, 5)}deg`);
    ticketStage.style.setProperty('--tilt-y', `${clamp(dx / 16, -7, 7)}deg`);
    ticketStage.classList.toggle('is-exploring', Math.abs(dx) > 10);
  });

  ['pointerup', 'pointercancel', 'lostpointercapture'].forEach((name) => {
    ticketStage.addEventListener(name, resetTickets);
  });

  ticketStage.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    event.preventDefault();
    const exploring = ticketStage.classList.toggle('is-exploring');
    ticketStage.style.setProperty('--front-x', exploring ? '-55px' : '0px');
    ticketStage.style.setProperty('--back-x', exploring ? '38px' : '0px');
  });
}

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
      <img class="experience-photo" src="${image}" alt="${item} no ${partner}" loading="lazy" draggable="false">
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

  let loopWidth = 1;
  let stepWidth = 1;
  let interacting = false;
  let resumeTimer = null;
  let normalizeTimer = null;

  const measureRail = () => {
    const firstSetLeft = experienceSets[0].offsetLeft;
    const secondSetLeft = experienceSets[1].offsetLeft;
    loopWidth = Math.max(1, secondSetLeft - firstSetLeft);

    const cards = experienceSets[0].querySelectorAll('.experience-card');
    if (cards.length > 1) {
      stepWidth = Math.max(1, cards[1].offsetLeft - cards[0].offsetLeft);
    } else if (cards[0]) {
      stepWidth = Math.max(1, cards[0].getBoundingClientRect().width);
    }
  };

  const normalizeRail = () => {
    measureRail();
    if (experienceRail.scrollLeft < loopWidth - 2) return;
    experienceRail.style.scrollSnapType = 'none';
    experienceRail.scrollLeft -= loopWidth;
    requestAnimationFrame(() => {
      experienceRail.style.scrollSnapType = '';
    });
  };

  const scheduleNormalize = (delay = 500) => {
    clearTimeout(normalizeTimer);
    normalizeTimer = setTimeout(normalizeRail, delay);
  };

  const pauseAutoplay = () => {
    interacting = true;
    clearTimeout(resumeTimer);
    resumeTimer = setTimeout(() => {
      interacting = false;
      scheduleNormalize(100);
    }, 2200);
  };

  const wireMoreCards = () => {
    experienceTrack.querySelectorAll('.card-more').forEach((card) => {
      card.setAttribute('role', 'link');
      card.setAttribute('tabindex', '0');
      card.setAttribute('aria-label', 'Ver todas as experiências +UM');
      const copy = card.querySelector('p');
      if (copy) copy.textContent = 'Veja todas as experiências';
      const go = () => {
        window.location.href = 'https://app.appmaisum.com.br';
      };
      card.addEventListener('click', go);
      card.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          go();
        }
      });
    });
  };

  const advanceRail = () => {
    if (interacting || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    measureRail();
    experienceRail.scrollBy({ left: stepWidth, behavior: 'smooth' });
    scheduleNormalize(750);
  };

  experienceRail.addEventListener('pointerdown', () => {
    experienceRail.classList.add('is-dragging');
    pauseAutoplay();
  });

  ['pointerup', 'pointercancel', 'pointerleave'].forEach((name) => {
    experienceRail.addEventListener(name, () => {
      experienceRail.classList.remove('is-dragging');
      pauseAutoplay();
      scheduleNormalize(250);
    });
  });

  experienceRail.addEventListener('wheel', pauseAutoplay, { passive: true });

  const renderExperiences = (category) => {
    const cards = category === 'Gastronomia'
      ? gastronomyCards
      : otherExperiences.map(experienceCard).join('') + moreCard;

    experienceSets[0].innerHTML = cards;
    experienceSets[1].innerHTML = cards.replaceAll('<article ', '<article aria-hidden="true" ');
    experienceRail.setAttribute('aria-label', `Experiências de ${category}. Arraste para explorar.`);

    filterButtons.forEach((button) => {
      const active = button.textContent.trim() === category;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });

    experienceRail.scrollLeft = 0;
    requestAnimationFrame(() => {
      measureRail();
      wireMoreCards();
    });
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => renderExperiences(button.textContent.trim()));
  });

  window.addEventListener('resize', () => {
    measureRail();
    scheduleNormalize(50);
  });

  experienceRail.querySelectorAll('img').forEach((img) => img.setAttribute('draggable', 'false'));
  measureRail();
  wireMoreCards();
  setInterval(advanceRail, 4200);
}
