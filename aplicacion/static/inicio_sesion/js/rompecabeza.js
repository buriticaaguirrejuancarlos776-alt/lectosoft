// // Función para generar las piezas del rompecabezas
// function crearPiezas(urlImagen, filas = 3, columnas = 3) {
//     const contenedorJuego = document.getElementById('juego-area');
//     contenedorJuego.style.gridTemplateColumns = `repeat(${columnas}, 1fr)`;

//     for (let i = 0; i < filas * columnas; i++) {
//         const pieza = document.createElement('div');
//         pieza.classList.add('pieza');
        
//         // Calculamos qué parte de la imagen mostrar en cada cuadro
//         const x = (i % columnas) * (100 / (columnas - 1));
//         const y = Math.floor(i / columnas) * (100 / (filas - 1));

//         pieza.style.backgroundImage = `url(${urlImagen})`;
//         pieza.style.backgroundSize = `${columnas * 100}% ${filas * 100}%`;
//         pieza.style.backgroundPosition = `${x}% ${y}%`;
        
//         // Hacer la pieza "arrastrable"
//         pieza.draggable = true;
//         contenedorJuego.appendChild(pieza);
//     }
// }