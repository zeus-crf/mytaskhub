document.addEventListener("DOMContentLoaded", () => {
  // ---------------------
  // Filtro 1 (status)
  // ---------------------
  const filter = document.getElementById('projectFilter');
  const projects = document.querySelectorAll('#projectsContainer .card');
  
  if (filter) {
    filter.addEventListener('change', () => {
      const value = filter.value;
      projects.forEach(card => {
        const status = card.getAttribute('data-status');
        card.style.display = (value === 'all' || value === status) ? 'block' : 'none';
      });
    });
  }

  // ---------------------
  // Filtro 2 (ordenação)
  // ---------------------
  const filter2 = document.getElementById('projectFilter2');
  const container = document.getElementById('projectsContainer');

  if (filter2) {
    filter2.addEventListener('change', () => {
      const value = filter2.value;
      const cards = Array.from(container.querySelectorAll('.card'));

      cards.sort((a, b) => {
        if (value === "tasks-desc") {
          return b.dataset.tasks - a.dataset.tasks; // Se eu preciso de um ordem decresente devo fazer b - a 
        } else if (value === "tasks-asc") {
          return a.dataset.tasks - b.dataset.tasks; // Se eu preciso de um ordem crescente devo fazer a - b
        } else if (value === "date-desc") { // Se eu preciso de um ordem decrescente devo fazer b - a 
          return new Date(b.dataset.date) - new Date(a.dataset.date);
        } else if (value === "date-asc") { // Se eu preciso de um ordem crescente devo fazer a - b
          return new Date(a.dataset.date) - new Date(b.dataset.date);
        }
      });

      cards.forEach(c => container.appendChild(c)); // insere no final do container (reorganiza a ordem)
    });
  }



  // ---------------------
  // Filtro 3 (Modo de exibição)
  // ---------------------

const filter3 = document.getElementById('projectFilter3');
const container3 = document.querySelector('.main'); // pega o elemento único

if (filter3 && container3) {
  filter3.addEventListener('change', () => {
    if (filter3.value === 'lista') {
      container3.classList.remove('main');
      container3.classList.add('lista');
    } else {
      container3.classList.add('main');
      container3.classList.remove('lista');
    }
  });
}

  // ---------------------
  // Modal de arquivamento
  // ---------------------
  const confirmModal = document.getElementById('confirmArchiveModal');
  if (confirmModal) {
    confirmModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      const url = button.getAttribute('data-url');
      const form = confirmModal.querySelector('#archiveForm');
      form.setAttribute('action', url);
    });
  }

  // ---------------------
  // Toasts
  // ---------------------
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach((toast, index) => {
    setTimeout(() => toast.classList.add('show'), 100 + index * 200);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 500);
    }, 3000 + index * 200);
  });
});
