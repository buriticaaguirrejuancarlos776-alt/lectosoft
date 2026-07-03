// document.addEventListener('DOMContentLoaded', function() {
//     const gridObjetivo = document.getElementById('grid-objetivo');
//     const cajaFichas = document.getElementById('caja-fichas');
//     const imgUrl = "{{ puzzle.imagen.url }}";
//     const dificultad = parseInt(gridObjetivo.getAttribute('data-dificultad')); // Recuperamos la dificultad desde el atributo data

//     const gridSize = dificultad * dificultad;
//     const cellSize = 450 / dificultad;

//     // Modificar el grid en CSS dinámicamente según la dificultad
//     gridObjetivo.style.gridTemplateColumns = `repeat(${dificultad}, 1fr)`;
//     gridObjetivo.style.gridTemplateRows = `repeat(${dificultad}, 1fr)`;

//     // Crear huecos con índice
//     for (let i = 0; i < gridSize; i++) {
//         const hueco = document.createElement('div');
//         hueco.className = 'hueco';
//         hueco.dataset.index = i;
//         gridObjetivo.appendChild(hueco);
//     }

//     // Crear piezas
//     let pieces = [];
//     for (let i = 0; i < gridSize; i++) {
//         let x = (i % dificultad) * cellSize;  // Calcula la posición en X
//         let y = Math.floor(i / dificultad) * cellSize; // Calcula la posición en Y

//         let div = document.createElement('div');
//         div.className = 'piece';
//         div.style.backgroundImage = `url(${imgUrl})`;
//         div.style.backgroundPosition = `-${x}px -${y}px`;
//         div.style.width = `${cellSize - 10}px`; // Establecemos el tamaño de la pieza
//         div.style.height = `${cellSize - 10}px`;
//         div.draggable = true;
//         div.dataset.index = i;

//         pieces.push(div);
//     }

//     // Mezclar piezas
//     pieces.sort(() => Math.random() - 0.5);
//     pieces.forEach(p => cajaFichas.appendChild(p));

//     let pieceBeingDragged = null;

//     document.addEventListener('dragstart', (e) => {
//         if (e.target.classList.contains('piece')) {
//             pieceBeingDragged = e.target;
//         }
//     });

//     document.addEventListener('dragover', (e) => {
//         e.preventDefault();
//     });

//     document.addEventListener('drop', (e) => {
//         if (e.target.classList.contains('hueco') && e.target.children.length === 0) {
//             const huecoIndex = e.target.dataset.index;
//             const piezaIndex = pieceBeingDragged.dataset.index;

//             if (huecoIndex === piezaIndex) {
//                 // Correcto
//                 e.target.appendChild(pieceBeingDragged);
//                 pieceBeingDragged.style.width = `${cellSize}px`; // Ajusta el tamaño de la pieza
//                 pieceBeingDragged.style.height = `${cellSize}px`;
//                 pieceBeingDragged.style.border = "none";
//             } else {
//                 // Incorrecto → regresa a la caja
//                 cajaFichas.appendChild(pieceBeingDragged);
//                 pieceBeingDragged.style.width = `${cellSize - 10}px`; // Tamaño estándar
//                 pieceBeingDragged.style.height = `${cellSize - 10}px`;
//                 pieceBeingDragged.style.border = "2px solid var(--text-main)";
//             }
//         }
//         else if (e.target.id === "caja-fichas") {
//             cajaFichas.appendChild(pieceBeingDragged);
//             pieceBeingDragged.style.width = `${cellSize - 10}px`;
//             pieceBeingDragged.style.height = `${cellSize - 10}px`;
//             pieceBeingDragged.style.border = "2px solid var(--text-main)";
//         }
//     });
// });