/* =========================================
   LÓGICA DEL MODO CLARO PARA ADMINISTRADOR
   ========================================= */

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle-btn');
    const sunIcon = document.getElementById('theme-sun');
    const moonIcon = document.getElementById('theme-moon');
    
    // Función para actualizar la UI del botón
    function setToggleUI(theme) {
        if (!sunIcon || !moonIcon) return;
        
        if (theme === 'light') {
            // Estilo del Sol cuando está inactivo (modo claro = luna activa)
            sunIcon.style.opacity = '0.5';
            sunIcon.style.background = 'transparent';
            sunIcon.style.boxShadow = 'none';
            
            // Estilo de la Luna (activa en modo claro porque indica el tema que se puede cambiar o simplemente el botón activo)
            // Wait, usually Sun = Light Mode, Moon = Dark Mode. 
            // If it's light mode, the Sun should be highlighted.
            sunIcon.style.opacity = '1';
            sunIcon.style.background = '#ffffff';
            sunIcon.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
            sunIcon.style.borderRadius = '50%';
            
            moonIcon.style.opacity = '0.5';
            moonIcon.style.background = 'transparent';
            moonIcon.style.boxShadow = 'none';
        } else {
            // Dark Mode: Moon is highlighted
            sunIcon.style.opacity = '0.5';
            sunIcon.style.background = 'transparent';
            sunIcon.style.boxShadow = 'none';
            
            moonIcon.style.opacity = '1';
            moonIcon.style.background = '#1e293b';
            moonIcon.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
            moonIcon.style.borderRadius = '50%';
        }
    }

    // Cargar preferencia guardada
    const currentTheme = localStorage.getItem('adminTheme') || 'dark';
    if (currentTheme === 'light') {
        document.body.classList.add('light-mode');
    }
    setToggleUI(currentTheme);

    // Evento de click en el botón
    if (toggleBtn) {
        toggleBtn.style.cursor = 'pointer';
        toggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            
            const newTheme = isLight ? 'light' : 'dark';
            localStorage.setItem('adminTheme', newTheme);
            setToggleUI(newTheme);
        });
    }
});
