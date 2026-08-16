document.documentElement.classList.add('js');

const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('.menu-button');

const updateHeader = () => header?.classList.toggle('scrolled', window.scrollY > 18);
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

menuButton?.addEventListener('click', () => {
  const open = header.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.querySelector('.sr-only').textContent = open ? '메뉴 닫기' : '메뉴 열기';
});

document.querySelectorAll('.site-nav a').forEach((link) => link.addEventListener('click', () => {
  header?.classList.remove('open');
  menuButton?.setAttribute('aria-expanded', 'false');
}));

const revealElements = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  revealElements.forEach((element) => observer.observe(element));
} else {
  revealElements.forEach((element) => element.classList.add('visible'));
}

const hashTarget = location.hash ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null;
hashTarget?.querySelectorAll('.reveal').forEach((element) => element.classList.add('visible'));
hashTarget?.classList.toggle('visible', hashTarget.classList.contains('reveal'));
document.querySelectorAll('[data-year]').forEach((element) => {
  element.textContent = new Date().getFullYear();
});
