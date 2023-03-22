/* JS for the Steamcraft Station design */

/* Interactive Gear Elements */
const gears = document.querySelectorAll('.gear');

gears.forEach(gear => {
  gear.addEventListener('mouseenter', () => {
    gear.classList.add('active');
  });

  gear.addEventListener('mouseleave', () => {
    gear.classList.remove('active');
  });
});

/* Animated Steam Elements */
const steamElements = document.querySelectorAll('.steam-element');

steamElements.forEach(element => {
  element.addEventListener('mouseenter', () => {
    element.classList.add('active');
  });

  element.addEventListener('mouseleave', () => {
    element.classList.remove('active');
  });
});
