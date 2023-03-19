/* JS for the Digital Oasis design */

/* Interactive Water Ripples */
const rippleElements = document.querySelectorAll('.ripple-element');

rippleElements.forEach(element => {
  element.addEventListener('mousedown', (event) => {
    const ripple = document.createElement('div');
    ripple.classList.add('ripple');
    ripple.style.top = `${event.clientY - element.offsetTop}px`;
    ripple.style.left = `${event.clientX - element.offsetLeft}px`;
    element.appendChild(ripple);
    setTimeout(() => {
      ripple.remove();
    }, 1000);
  });
});
