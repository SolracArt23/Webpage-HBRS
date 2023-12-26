document.addEventListener("DOMContentLoaded", function() {
    const sections = document.querySelectorAll('section');
    let index = 0;
  
    window.addEventListener('scroll', function() {
      // Calcula la posición actual de la ventana de visualización
      const currentPosition = window.scrollY;
  
      // Comprueba en qué sección se encuentra la ventana
      sections.forEach(function(section, i) {
        const sectionTop = section.offsetTop - 50; // Puedes ajustar este valor según tus necesidades
  
        if (currentPosition >= sectionTop) {
          index = i;
        }
      });
  
      // Activa la clase 'active' en la sección actual y desactiva en las demás
      sections.forEach(function(section, i) {
        if (i === index) {
          section.classList.add('active');
        } else {
          section.classList.remove('active');
        }
      });
    });
  });
  