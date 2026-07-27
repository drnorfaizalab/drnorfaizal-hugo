// Mobile nav toggle
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
  });
}

// Sticky header shadow on scroll
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 10);
  });
}

// Meta Pixel — Contact event on all booking/WhatsApp CTAs
document.addEventListener('click', function(e) {
  if (e.target.closest('.whatsapp-float, .btn-whatsapp, .btn-cta, .btn-appointment')) {
    if (typeof fbq === 'function') fbq('track', 'Contact');
  }
});
