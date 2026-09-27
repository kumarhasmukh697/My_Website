(function () {
  "use strict";

  /* -------------------------------------------------------------
   * Mobile sidebar
   * ----------------------------------------------------------- */
  const header = document.querySelector('#header');
  const headerToggleBtn = document.querySelector('.header-toggle');

  function headerToggle() {
    if (!header || !headerToggleBtn) return;
    header.classList.toggle('header-show');
    headerToggleBtn.classList.toggle('is-open');
    const icon = headerToggleBtn.querySelector('.bi');
    if (icon) {
      icon.classList.toggle('bi-list', !header.classList.contains('header-show'));
      icon.classList.toggle('bi-x', header.classList.contains('header-show'));
    }
  }

  if (headerToggleBtn) headerToggleBtn.addEventListener('click', headerToggle);

  document.querySelectorAll('#navmenu a').forEach((link) => {
    link.addEventListener('click', () => {
      if (header && header.classList.contains('header-show')) headerToggle();
    });
  });

  /* -------------------------------------------------------------
   * Preloader
   * ----------------------------------------------------------- */
  const preloader = document.querySelector('#preloader');
  window.addEventListener('load', () => {
    if (preloader) preloader.remove();
  });

  /* -------------------------------------------------------------
   * Scroll-to-top
   * ----------------------------------------------------------- */
  const scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) scrollTop.classList.toggle('active', window.scrollY > 100);
  }

  if (scrollTop) {
    scrollTop.addEventListener('click', (event) => {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  window.addEventListener('scroll', toggleScrollTop, { passive: true });
  window.addEventListener('load', toggleScrollTop);

  /* -------------------------------------------------------------
   * AOS replacement using IntersectionObserver
   * ----------------------------------------------------------- */
  const animatedElements = document.querySelectorAll('[data-aos]');

  if ('IntersectionObserver' in window) {
    const animationObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        const delay = window.innerWidth <= 768 ? 0 : Number(entry.target.dataset.aosDelay || 0);
        window.setTimeout(() => entry.target.classList.add('aos-visible'), delay);
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12 });

    animatedElements.forEach((element) => animationObserver.observe(element));
  } else {
    animatedElements.forEach((element) => element.classList.add('aos-visible'));
  }

  /* -------------------------------------------------------------
   * Typed text replacement
   * ----------------------------------------------------------- */
  const typedElement = document.querySelector('.typed');

  if (typedElement) {
    const strings = (typedElement.dataset.typedItems || '').split(',').map(s => s.trim()).filter(Boolean);
    if (strings.length) {
      let stringIndex = 0;
      let characterIndex = 0;
      let deleting = false;

      function typeLoop() {
        const current = strings[stringIndex];
        typedElement.textContent = current.slice(0, characterIndex);

        if (!deleting && characterIndex < current.length) {
          characterIndex += 1;
          setTimeout(typeLoop, 100);
          return;
        }

        if (!deleting) {
          deleting = true;
          setTimeout(typeLoop, 2000);
          return;
        }

        if (characterIndex > 0) {
          characterIndex -= 1;
          setTimeout(typeLoop, 50);
          return;
        }

        deleting = false;
        stringIndex = (stringIndex + 1) % strings.length;
        setTimeout(typeLoop, 250);
      }

      typeLoop();
    }
  }

  /* -------------------------------------------------------------
   * Portfolio filtering replacement for Isotope
   * ----------------------------------------------------------- */
  document.querySelectorAll('.isotope-layout').forEach((layout) => {
    const filters = layout.querySelectorAll('.isotope-filters [data-filter]');
    const items = layout.querySelectorAll('.isotope-item');

    filters.forEach((filterButton) => {
      filterButton.addEventListener('click', () => {
        filters.forEach((button) => button.classList.remove('filter-active'));
        filterButton.classList.add('filter-active');

        const selector = filterButton.dataset.filter;
        items.forEach((item) => {
          const show = selector === '*' || item.matches(selector);
          item.style.display = show ? '' : 'none';
        });
      });
    });
  });

  /* -------------------------------------------------------------
   * Vanilla lightbox replacement for GLightbox
   * ----------------------------------------------------------- */
  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox-overlay';
  lightbox.innerHTML = '<button class="lightbox-close" type="button" aria-label="Close">&times;</button><img alt="">';
  document.body.appendChild(lightbox);

  const lightboxImage = lightbox.querySelector('img');
  const closeLightbox = () => {
    lightbox.classList.remove('active');
    lightboxImage.src = '';
  };

  document.querySelectorAll('.glightbox').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      lightboxImage.src = link.href;
      lightboxImage.alt = link.getAttribute('title') || '';
      lightbox.classList.add('active');
    });
  });

  lightbox.querySelector('.lightbox-close').addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeLightbox();
  });

  /* -------------------------------------------------------------
   * Simple project-details slider replacement for Swiper
   * ----------------------------------------------------------- */
  document.querySelectorAll('.portfolio-details-slider').forEach((slider) => {
    const wrapper = slider.querySelector('.swiper-wrapper');
    const slides = slider.querySelectorAll('.swiper-slide');
    const pagination = slider.querySelector('.swiper-pagination');
    if (!wrapper || slides.length <= 1) return;

    let currentSlide = 0;
    const bullets = [];

    function showSlide(index) {
      currentSlide = (index + slides.length) % slides.length;
      wrapper.style.transform = `translateX(-${currentSlide * 100}%)`;
      bullets.forEach((bullet, i) => {
        bullet.classList.toggle('active', i === currentSlide);
        bullet.classList.toggle('swiper-pagination-bullet-active', i === currentSlide);
      });
    }

    slides.forEach((_, index) => {
      const bullet = document.createElement('button');
      bullet.type = 'button';
      bullet.className = 'swiper-pagination-bullet';
      bullet.setAttribute('aria-label', `Go to image ${index + 1}`);
      bullet.addEventListener('click', () => showSlide(index));
      pagination.appendChild(bullet);
      bullets.push(bullet);
    });

    showSlide(0);

    setInterval(() => showSlide(currentSlide + 1), 5000);
  });

  /* -------------------------------------------------------------
   * Scrollspy
   * ----------------------------------------------------------- */
  const navLinks = document.querySelectorAll('.navmenu a[href^="#"]');

  function updateScrollspy() {
    const position = window.scrollY + 200;

    navLinks.forEach((link) => {
      const hash = link.getAttribute('href');
      const section = document.querySelector(hash);
      if (!section) return;

      const active = position >= section.offsetTop && position <= section.offsetTop + section.offsetHeight;
      link.classList.toggle('active', active);
    });
  }

  window.addEventListener('scroll', updateScrollspy, { passive: true });
  window.addEventListener('load', updateScrollspy);

  /* -------------------------------------------------------------
   * Hash-link positioning
   * ----------------------------------------------------------- */
  window.addEventListener('load', () => {
    if (!window.location.hash) return;
    const section = document.querySelector(window.location.hash);
    if (!section) return;

    setTimeout(() => section.scrollIntoView({ behavior: 'smooth' }), 100);
  });
})();
