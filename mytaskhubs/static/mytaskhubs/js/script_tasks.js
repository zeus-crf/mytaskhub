document.addEventListener('DOMContentLoaded', () => {

// Filtro 1 (status)

const filter = document.getElementById('taskFilter');
const tasks = document.querySelectorAll('#tasksContainer .card');

if (filter) {
    filter.addEventListener('change', () => {
       const value = filter.value;
       tasks.forEach(card => {
       const status = card.getAttribute('data-status');
       card.style.display = (value === 'all' || value === status) ? 'block' : 'none';
       }); 
    });
}

// Filtro 2 (ordenação)
const filter2 = document.getElementById('taskFilter2');
const container = document.querySelector('#tasksContainer'); // Se for classe
// const container = document.getElementById('tasksContainer'); // Se for id

const prioridadePeso = {
  'A': 3, // Alta
  'M': 2, // Média
  'B': 1  // Baixa
};

if (filter2) {
  filter2.addEventListener('change', () => {
    const value = filter2.value;
    const cards = Array.from(document.querySelectorAll('.card'));

  cards.sort((a, b) => {
  if (value === 'data-desc') {
    return new Date(b.dataset.date) - new Date(a.dataset.date); // mais recentes
  } else if (value === 'data-asc') {
    return new Date(a.dataset.date) - new Date(b.dataset.date); // mais antigas
  } else if (value === 'prio-desc') {
    return prioridadePeso[b.dataset.prio] - prioridadePeso[a.dataset.prio]; // Alta -> Baixa
  } else if (value === 'prio-asc') {
    return prioridadePeso[a.dataset.prio] - prioridadePeso[b.dataset.prio]; // Baixa -> Alta
  }
  });

    cards.forEach(c => container.appendChild(c));
  });
}



// Filtro 3 (Modo de exibição)
const filter3 = document.getElementById('taskFilter3');
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
