/* JS for the Celestial Canvas design */

/* Interactive Nebula Particles */
const nebulaParticles = document.querySelectorAll('.nebula-particle');

nebulaParticles.forEach(particle => {
  particle.addEventListener('mouseenter', () => {
    particle.classList.add('active');
  });

  particle.addEventListener('mouseleave', () => {
    particle.classList.remove('active');
  });
});

/* Shimmering Buttons */
const buttons = document.querySelectorAll('.button');

buttons.forEach(button => {
  button.addEventListener('mouseenter', () => {
    button.classList.add('shimmer');
  });

  button.addEventListener('mouseleave', () => {
    button.classList.remove('shimmer');
  });
});

/* JS for the Celestial Canvas design */

/* Hero Parallax Effect */
const hero = document.querySelector('.hero');

window.addEventListener('scroll', () => {
  const scrollPosition = window.pageYOffset;
  hero.style.backgroundPositionY = `${scrollPosition * 0.7}px`;
});

/* Scroll-to-Top Button */
const scrollTopButton = document.querySelector('.scroll-top');

scrollTopButton.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});
