let isEditing = false;

function stringToColor(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = Math.abs(hash % 360);
    return `hsl(${hue}, 100%, 75%)`; // Colores neón más claros (Lightness 75%)
}

function updateAvatar(name) {
    const imgElement = document.getElementById("avatar-image");
    const wrapperElement = document.querySelector(".avatar-wrapper");
    if (imgElement) {
        const seedName = name.trim() || "Lecto";
        const seed = encodeURIComponent(seedName);
        imgElement.src = `https://api.dicebear.com/6.x/bottts/svg?seed=${seed}`;
        
        if (wrapperElement) {
            const neonColor = stringToColor(seedName);
            wrapperElement.style.setProperty('--neon-color', neonColor);
        }
    }
}

function handleEditClick() {
    if (!isEditing) enterEditMode();
    else saveName();
}

function enterEditMode() {
    const container = document.getElementById("player-name-container");
    const textElement = document.getElementById("player-name-text");
    const imgIcon = document.getElementById("img-edit-icon");
    if (textElement) {
        isEditing = true;
        const currentName = textElement.innerText;
        container.innerHTML = '<span class="label-text">NOMBRE:</span>';
        const input = document.createElement("input");
        input.type = "text"; input.id = "player-name-input";
        input.value = currentName; input.className = "input-edit-name";
        container.appendChild(input);
        input.focus();
        imgIcon.src = iconAceptar;
        input.oninput = function() { updateAvatar(this.value); };
        input.onkeydown = (e) => { if(e.key === 'Enter') saveName(); };
    }
}

function saveName() {
    const container = document.getElementById("player-name-container");
    const input = document.getElementById("player-name-input");
    const imgIcon = document.getElementById("img-edit-icon");
    
    if (!input) return;
    
    const newName = input.value.trim();
    const oldName = localStorage.getItem('nombreJugadorLectosoft') || "Lecto";
    
    // Validar que no esté vacío
    if (!newName) {
        showCustomAlert('⚠️ ATENCIÓN', 'El nombre no puede estar vacío.');
        cancelarEdicion(container, imgIcon, oldName);
        return;
    }
    
    // Si el nombre no cambió
    if (newName === oldName) {
        cancelarEdicion(container, imgIcon, oldName);
        isEditing = false;
        return;
    }
    
    // Mostrar estado de carga
    container.innerHTML = '<span class="label-text">Nombre:</span><p id="player-name-text" style="color: #888;">Guardando...</p>';
    
    // Obtener CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCsrfToken();
    
    // Enviar actualización
    fetch('/api/actualizar-nombre-jugador/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            nombre_anterior: oldName,
            nombre_nuevo: newName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            container.innerHTML = `<span class="label-text">NOMBRE:</span><p id="player-name-text">${newName}</p>`;
            imgIcon.src = iconEditar;
            updateAvatar(newName);
            localStorage.setItem('nombreJugadorLectosoft', newName);
            showCustomAlert('✨ ¡LISTO! ✨', '¡Nombre actualizado correctamente!');
        } else {
            showCustomAlert('❌ ERROR', 'Error: ' + (data.message || 'No se pudo actualizar el nombre'));
            cancelarEdicion(container, imgIcon, oldName);
        }
        isEditing = false;
    })
    .catch(error => {
        console.error('Error:', error);
        showCustomAlert('❌ ERROR', 'Error de conexión');
        cancelarEdicion(container, imgIcon, oldName);
        isEditing = false;
    });
}

function showCustomAlert(title, message) {
    const overlay = document.getElementById('custom-alert-overlay');
    const titleEl = document.getElementById('custom-alert-title');
    const msgEl = document.getElementById('custom-alert-message');
    
    if (overlay && titleEl && msgEl) {
        titleEl.innerText = title;
        msgEl.innerText = message;
        overlay.style.display = 'flex';
    } else {
        // Fallback en caso de que no cargue el HTML
        alert(title + "\n" + message);
    }
}

function closeCustomAlert() {
    const overlay = document.getElementById('custom-alert-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

function cancelarEdicion(container, imgIcon, oldName) {
    container.innerHTML = `<span class="label-text">NOMBRE:</span><p id="player-name-text">${oldName}</p>`;
    imgIcon.src = iconEditar;
}

function getCsrfToken() {
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return '';
}

window.onload = () => {
    const nameText = document.getElementById("player-name-text");
    const nombreGuardado = localStorage.getItem('nombreJugadorLectosoft');
    if (nameText) {
        const nombreFinal = nombreGuardado || "Carmela";
        nameText.innerText = nombreFinal;
        updateAvatar(nombreFinal);
    }
};
