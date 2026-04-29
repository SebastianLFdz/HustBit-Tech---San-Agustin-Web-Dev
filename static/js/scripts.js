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

/* INDEX.HTML */
// Navbar background change on scroll
window.addEventListener("scroll", function() {
  const nav = document.getElementById("siteNav");
  if (window.scrollY > 50) {
    nav.classList.add("scrolled");
  } else {
    nav.classList.remove("scrolled");
  }
});

/* ABOUT.HTML */
// Reveal animation engine
// Navbar scroll
(function(){
  const nav=document.getElementById('siteNav');
  function onScroll(){
    if(window.scrollY>50) nav.classList.add('scrolled'); else nav.classList.remove('scrolled');
  }
  onScroll();
  window.addEventListener('scroll',onScroll,{passive:true});
})();

// Reveal animation
(function(){
  const io=new IntersectionObserver((entries,obs)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target);}
    });
  },{threshold:0.12});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
})();

/* CONTACTO.HTML */
// Manejo del Modal de Éxito por URL
if (window.location.search.includes("exito=1")) {
    const modalElement = document.getElementById('modalExito');
    if (modalElement) {
        var myModal = new bootstrap.Modal(modalElement);
        myModal.show();
        // Limpia la URL para que no salga el modal al recargar
        history.replaceState(null, "", window.location.pathname);
    }
}

