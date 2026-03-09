document.addEventListener("scroll", () => {
  document.querySelectorAll(".fade-scroll").forEach(el => {
    const pos = el.getBoundingClientRect().top;
    const windowHeight = window.innerHeight * 0.85;
    if (pos < windowHeight) el.classList.add("visible");
  });
});

// Navbar scroll behavior
const nav = document.getElementById("siteNav");
window.addEventListener("scroll", () => {
  if (window.scrollY > 50) nav.classList.add("scrolled");
  else nav.classList.remove("scrolled");
});

// Reveal animation
const reveals = document.querySelectorAll(".reveal");
const obs = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add("visible");
  });
}, { threshold: 0.2 });
reveals.forEach((r) => obs.observe(r));

// Parallax hero
const hero = document.getElementById("hero");
window.addEventListener("scroll", () => {
  if (window.innerWidth > 768) {
    const offset = window.scrollY * 0.4;
    hero.style.backgroundPositionY = `${offset}px`;
  }
});

