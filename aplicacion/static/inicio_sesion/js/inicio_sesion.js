document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const inputNombre = document.getElementById('login-username');
    const imgPreview = document.getElementById('avatar-preview');

    // 1. Limpiar inputs al cargar (excepto los ocultos)
    document.querySelectorAll('input:not([type="hidden"])').forEach(input => input.value = '');

    // 2. Avatar en tiempo real
    if (inputNombre && imgPreview) {
        inputNombre.addEventListener('input', () => {
            const nombre = inputNombre.value.trim() || "Lecto";
            imgPreview.src = `https://api.dicebear.com/6.x/bottts/svg?seed=${encodeURIComponent(nombre)}`;
            
            // Remover error si el usuario empieza a escribir de nuevo
            inputNombre.classList.remove('input-error');
        });
    }

    // 3. Validación al enviar
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            const inputActivo = document.querySelector('input[required]');
            if (!inputActivo) return true;

            const valor = inputActivo.value.trim();
            
            // Validar que no esté vacío
            if (!valor) {
                e.preventDefault();
                inputActivo.classList.add('input-error');
                return false;
            }
            
            // Si es el nombre del jugador, guardar en localStorage
            if (inputActivo.name === 'username') {
                if (valor.length > 100) {
                    e.preventDefault();
                    inputActivo.classList.add('input-error');
                    alert('El nombre es demasiado largo (máximo 100 caracteres).');
                    return false;
                }
                localStorage.setItem('nombreJugadorLectosoft', valor);
            }
            
            return true;
        });
    }

    // 4. Modo Administrador
    const adminLink = document.getElementById('admin-link');
    const backLink = document.getElementById('back-link');
    const loginCard = document.querySelector('.login-card');
    const loginTitle = document.querySelector('h2');
    const subtitle = document.querySelector('.subtitle');
    const avatarContainer = document.querySelector('.avatar-preview-container');
    const playerBtn = document.getElementById('player-btn');
    const adminBtn = document.getElementById('admin-btn');

    if (adminLink && backLink) {
        adminLink.addEventListener('click', () => {
            loginCard.classList.add('admin-mode');
            loginTitle.innerText = 'ADMINISTRADOR';
            inputNombre.placeholder = 'correo del administrador';
            inputNombre.type = 'email';
            inputNombre.name = 'admin_email';
            inputNombre.value = '';
            
            // Ocultar avatar en modo admin
            avatarContainer.style.display = 'none';
            
            // Alternar botones
            if (playerBtn) playerBtn.style.display = 'none';
            if (adminBtn) adminBtn.style.display = 'inline-flex';
            
            adminLink.style.display = 'none';
            backLink.style.display = 'block';
        });

        backLink.addEventListener('click', () => {
            loginCard.classList.remove('admin-mode');
            loginTitle.innerText = '¡BIENVENIDO!';
            inputNombre.placeholder = 'nombre del jugador';
            inputNombre.type = 'text';
            inputNombre.name = 'username';
            inputNombre.value = '';
            
            // Mostrar avatar
            avatarContainer.style.display = 'flex';
            
            // Alternar botones
            if (playerBtn) playerBtn.style.display = 'inline-flex';
            if (adminBtn) adminBtn.style.display = 'none';
            
            adminLink.style.display = 'block';
            backLink.style.display = 'none';
        });

        // 5. Autodisparador modo admin si viene de un redirect
        if (window.location.search.includes('admin=1')) {
            adminLink.click();
        }
    }

    // 6. Lógica del botón X (Cerrar)
    const closeBtn = document.getElementById('main-close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            const redirectLogin = (typeof URL_LOGIN !== 'undefined') ? URL_LOGIN : '/login/';
            window.location.href = redirectLogin;
        });
    }
});