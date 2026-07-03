const updateForestEffects = () => {
    const scrollVal = window.scrollY;
    const windowHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;
    
    const pandaDown = document.getElementById('panda-down');
    const pandaUp = document.getElementById('panda-up');
    
    // Calcular porcentaje de scroll para el movimiento
    const scrollableLimit = docHeight - windowHeight;
    const scrollPercent = Math.min(scrollVal / scrollableLimit, 1);
    
    // Rango de movimiento (ajusta el 150 para que no tape el footer)
    const moveRange = windowHeight - 150; 

    if (pandaDown && pandaUp) {
        // El de la izquierda baja
        pandaDown.style.top = (80 + (scrollPercent * moveRange)) + 'px';
        // El de la derecha sube
        pandaUp.style.top = (80 + ((1 - scrollPercent) * moveRange)) + 'px';
    }

    // Movimiento sutil de las hojas
    const leaves = document.querySelectorAll('.tree-leaf');
    leaves.forEach((leaf, i) => {
        const shift = Math.sin(scrollVal * 0.005 + i) * 10;
        leaf.style.marginTop = shift + 'px';
    });
    // Ajuste del botón flotante del manual para que no tape el footer
    const footer = document.querySelector('footer');
    const btnManual = document.querySelector('.btn-flotante-manual');
    if (footer && btnManual) {
        const footerRect = footer.getBoundingClientRect();
        if (footerRect.top < windowHeight) {
            const overlap = windowHeight - footerRect.top;
            btnManual.style.bottom = (20 + overlap) + 'px';
        } else {
            btnManual.style.bottom = '20px';
        }
    }
};

window.addEventListener('scroll', updateForestEffects);
window.addEventListener('resize', updateForestEffects);
document.addEventListener('DOMContentLoaded', updateForestEffects);