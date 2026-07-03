document.addEventListener('DOMContentLoaded', () => {
    const inputBuscador = document.getElementById('inputBuscador');
    const todasLasTarjetas = Array.from(document.querySelectorAll('.book-card'));
    const paginationControls = document.getElementById('pagination-controls');
    
    let itemsPerPage = 3;
    let currentPage = 1;
    let filteredCards = [...todasLasTarjetas];

    function renderPagination() {
        paginationControls.innerHTML = '';
        const totalPages = Math.ceil(filteredCards.length / itemsPerPage);

        if (totalPages <= 1) return; // No mostrar paginación si hay 1 o menos páginas

        // Botón Anterior
        const btnPrev = document.createElement('button');
        btnPrev.innerHTML = '⬅️';
        btnPrev.className = 'btn-page-infantil';
        btnPrev.onclick = () => {
            if (currentPage > 1) {
                currentPage--;
                updateView();
            }
        };
        if (currentPage === 1) btnPrev.style.opacity = '0.5';
        paginationControls.appendChild(btnPrev);

        // Botones de Número
        for (let i = 1; i <= totalPages; i++) {
            const btnNum = document.createElement('button');
            btnNum.innerHTML = i;
            btnNum.className = 'btn-page-infantil';
            if (i === currentPage) {
                btnNum.classList.add('active');
            }
            btnNum.onclick = () => {
                currentPage = i;
                updateView();
            };
            paginationControls.appendChild(btnNum);
        }

        // Botón Siguiente
        const btnNext = document.createElement('button');
        btnNext.innerHTML = '➡️';
        btnNext.className = 'btn-page-infantil';
        btnNext.onclick = () => {
            if (currentPage < totalPages) {
                currentPage++;
                updateView();
            }
        };
        if (currentPage === totalPages) btnNext.style.opacity = '0.5';
        paginationControls.appendChild(btnNext);
    }

    function updateView() {
        // Ocultar todos forzando !important para vencer al CSS
        todasLasTarjetas.forEach(t => {
            t.style.setProperty('display', 'none', 'important');
        });

        // Mostrar solo los de la página actual
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        
        const cardsToShow = filteredCards.slice(startIndex, endIndex);
        cardsToShow.forEach(t => {
            t.style.setProperty('display', 'flex', 'important');
        });

        renderPagination();
    }

    inputBuscador.addEventListener('keyup', function() {
        let filtro = this.value.toLowerCase();
        
        filteredCards = todasLasTarjetas.filter(tarjeta => {
            let nombreLibro = tarjeta.getAttribute('data-name');
            return nombreLibro.includes(filtro);
        });

        currentPage = 1; // Volver a la primera página al buscar
        updateView();
    });

    // Iniciar
    updateView();
});