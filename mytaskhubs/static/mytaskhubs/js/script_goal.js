function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie("csrftoken");

document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll(".task-checkbox");
    const circle = document.querySelector(".progress-circle-large");
    const progressBar = document.getElementById("taskProgressBar");
    const barSpan = document.getElementById("barProgress");

    // Função para atualizar progresso
    function updateProgress(progress) {
        // Atualiza círculo (apenas preenchimento, sem número)
        circle.style.setProperty("--progress", progress);
        // Atualiza barra horizontal
        progressBar.style.width = progress + "%";
        // Atualiza porcentagem próxima da barra
        barSpan.textContent = progress + "%";
    }

    // Calcula progresso inicial baseado nas checkboxes marcadas
    function calculateProgress() {
        const total = checkboxes.length;
        let completed = 0;
        checkboxes.forEach(cb => { if (cb.checked) completed++; });
        return total > 0 ? Math.round((completed / total) * 100) : 0;
    }

    // Inicializa progresso ao carregar a página
    updateProgress(calculateProgress());

    // Atualiza progresso quando uma checkbox muda
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            const taskId = this.dataset.taskId;
            const completed = this.checked;

            fetch(`/update_task/${taskId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ completed })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Atualiza progresso do círculo e da barra
                    updateProgress(data.progress);
                } else {
                    console.error("Erro na resposta:", data.error);
                }
            })
            .catch(error => console.error("Erro no fetch:", error));
        });
    });
});



