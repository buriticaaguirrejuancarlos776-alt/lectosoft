// ============================================
// CUENTO: EL PATITO FEO
// ============================================
const cuento = [
    { parte: "PARTE 1", texto: "EN UNA TRANQUILA Y HERMOSA GRANJA, LLEGÓ LA PRIMAVERA. UNA MAMÁ PATA ESPERABA CON MUCHA ILUSIÓN A QUE SUS HUEVOS SE ROMPIERAN." },
    { parte: "PARTE 1-1", texto: "LOS DÍAS PASABAN Y ELLA LOS CUIDABA CON MUCHO AMOR, MANTENIÉNDOLOS SIEMPRE CÁLIDOS BAJO SUS PLUMAS." },
    { parte: "PARTE 2", texto: "PRONTO LOS CASCARONES SE ROMPIERON, UNO A UNO, DEJANDO SALIR A PEQUEÑOS Y HERMOSOS PATITOS." },
    { parte: "PARTE 2-2", texto: "PERO HABÍA UN HUEVO QUE ERA MUY GRANDE, DE COLOR EXTRAÑO, Y TARDÓ MUCHO MÁS TIEMPO EN ABRIRSE." },
    { parte: "PARTE 3", texto: "CUANDO POR FIN LO HIZO, LA MAMÁ PATA SE QUEDÓ MUY SORPRENDIDA AL VERLO SALIR." },
    { parte: "PARTE 3-3", texto: "ERA GRANDE, GRIS Y MUY DIFERENTE A TODOS SUS HERMANITOS QUE ERAN PEQUEÑOS Y AMARILLOS." },
    { parte: "PARTE 4", texto: "TRISTEMENTE, LOS DEMÁS ANIMALES DE LA GRANJA SE BURLABAN CONSTANTEMENTE DE ÉL." },
    { parte: "PARTE 4-4", texto: "LO MOLESTABAN PORQUE NO SE PARECÍA A LOS DEMÁS Y COMENZARON A LLAMARLO EL PATITO FEO." },
    { parte: "PARTE 5", texto: "SINTIÉNDOSE MUY TRISTE Y SOLO, EL PATITO LLORÓ DURANTE VARIAS NOCHES." },
    { parte: "PARTE 5-5", texto: "FINALMENTE DECIDIÓ MARCHARSE LEJOS DE LA GRANJA PARA BUSCAR SU VERDADERO LUGAR EN EL MUNDO." },
    { parte: "PARTE 6", texto: "DURANTE SU VIAJE ENFRENTÓ MUCHOS PELIGROS EN EL BOSQUE DESCONOCIDO." },
    { parte: "PARTE 6-6", texto: "LUEGO PASÓ UN INVIERNO EXTREMADAMENTE FRÍO Y SOLITARIO, ESCONDIDO ENTRE LAS RAMAS Y SIN NINGÚN AMIGO." },
    { parte: "PARTE 7", texto: "FINALMENTE, AL LLEGAR LA CÁLIDA PRIMAVERA, EL SOL VOLVIÓ A BRILLAR Y LAS FLORES BROTARON." },
    { parte: "PARTE 7-7", texto: "EL PATITO SE ACERCÓ LENTAMENTE A UN CRISTALINO ESTANQUE Y MIRÓ SU REFLEJO EN EL AGUA." },
    { parte: "FINAL", texto: "¡SE DIO CUENTA DE QUE NUNCA HABÍA SIDO UN PATITO FEO Y NO PODÍA CREER LO QUE VEÍA!" },
    { parte: "FINAL-2", texto: "HABÍA CRECIDO Y SE HABÍA CONVERTIDO EN EL CISNE MÁS ELEGANTE Y HERMOSO DE TODO EL LUGAR." }
];

let pageFlip;

const flipSound = new Howl({
    src: ['/static/inicio_sesion/audio/page-flip.mp3'],
    volume: 0.5
});

function construirLibro() {
    const flipbook = document.getElementById("flipbook");
    let html = `
        <div class="page page-cover page-cover-top" data-density="hard">
            <div class="page-content" style="margin: 0; width: 100%; height: 100%; padding: 0; position: relative; overflow: hidden;">
                <img src="/static/inicio_sesion/img/portada_patitofeo.png" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: fill;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 25%; z-index: 1; display: flex; justify-content: center; align-items: center; background: rgba(0,0,0,0.5);">
                    <h1 style="font-family: 'MedievalSharp', cursive; font-size: 50px; color: #f0d06f; text-shadow: 3px 3px 15px rgba(0,0,0,0.9); text-align: center;">El Patito Feo</h1>
                </div>
            </div>
        </div>
        <div class="page page-cover-inside" data-density="hard">
            <div class="page-content" style="padding: 0; width: 100%; height: 100%;">
                <img src="/static/inicio_sesion/img/patito1.png" style="width: 100%; height: 100%; object-fit: fill;">
            </div>
        </div>
        <div class="page">
            <div class="page-content text-page" style="justify-content: center; align-items: center;">
                <h1 style="font-size: 60px; font-family: 'MedievalSharp', cursive; color: #7b1113; text-align: center;">El Patito Feo</h1>
            </div>
        </div>
    `;

    cuento.forEach((item, index) => {
        let imgSrc = "/static/inicio_sesion/img/patito_feo.png";
        if (index <= 1) imgSrc = "/static/inicio_sesion/img/patito2.png";
        else if (index <= 3) imgSrc = "/static/inicio_sesion/img/patito3.png";
        else if (index <= 5) imgSrc = "/static/inicio_sesion/img/patito4.png";
        else if (index <= 7) imgSrc = "/static/inicio_sesion/img/patito5.png";
        else if (index <= 9) imgSrc = "/static/inicio_sesion/img/patito6.png";
        else if (index <= 11) imgSrc = "/static/inicio_sesion/img/patito7.png";
        else if (index <= 13) imgSrc = "/static/inicio_sesion/img/patito8.png";
        else imgSrc = "/static/inicio_sesion/img/patito_cisne.png";

        html += `
            <div class="page">
                <div class="page-content" style="padding: 0; width: 100%; height: 100%;">
                    <img src="${imgSrc}" style="width: 100%; height: 100%; object-fit: fill;">
                </div>
            </div>
            <div class="page">
                <div class="page-content text-page">
                    <h2 class="page-header">${item.parte}</h2>
                    <div class="page-text" id="texto-${index}"></div>
                    <div class="page-footer">${index + 1}</div>
                </div>
            </div>
        `;
    });

    html += `
        <div class="page page-cover-inside" data-density="hard">
            <div class="page-content" style="padding: 0; width: 100%; height: 100%;">
                <img src="/static/inicio_sesion/img/patito9.png" style="width: 100%; height: 100%; object-fit: fill;">
            </div>
        </div>
        <div class="page">
            <div class="page-content text-page" style="justify-content: center; align-items: center; padding: 100px;">
                <h2 style="font-family: 'MedievalSharp', cursive; color: #7b1113; font-size: 38px;">Moraleja</h2>
                <p style="font-size: 24px; text-align: center; font-style: italic;">"No importa haber nacido en un corral de patos si se ha salido de un huevo de cisne."</p>
            </div>
        </div>
        <div class="page page-cover page-cover-bottom" data-density="hard">
            <div class="page-content" style="margin: 0; width: 100%; height: 100%; padding: 0; position: relative; overflow: hidden;">
                <img src="/static/inicio_sesion/img/portada_finpatitofeo.png" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: fill; filter: brightness(0.5);">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; display: flex; justify-content: center; align-items: flex-start; padding-top: 50px;">
                    <h1 style="font-family: 'MedievalSharp', cursive; font-size: 80px; color: #f0d06f; text-shadow: 3px 3px 15px rgba(0,0,0,0.9);">FIN</h1>
                </div>
            </div>
        </div>
    `;
    flipbook.innerHTML = html;
}

function escribirTexto(texto, index) {
    const elemento = document.getElementById(`texto-${index}`);
    if (!elemento || elemento.innerHTML.length > 0) return;
    let i = 0;
    function escribir() {
        if (i < texto.length) {
            elemento.innerHTML += texto.charAt(i);
            i++;
            setTimeout(escribir, 25);
        }
    }
    escribir();
}

function iniciarLibro() {
    let startPage = 0;
    if (window.userProgress.paginasLeidas > 0) {
        if (window.userProgress.paginasLeidas >= cuento.length) {
            startPage = 0;
        } else {
            startPage = 3 + (window.userProgress.paginasLeidas * 2);
            const totalPages = 3 + (cuento.length * 2) + 3; 
            if (startPage >= totalPages) startPage = totalPages - 1;
        }
    }

    pageFlip = new St.PageFlip(flipbook, {
        width: 650, height: 850, size: "stretch", minWidth: 420, maxWidth: 1050, minHeight: 580, maxHeight: 1350,
        showCover: true, flippingTime: 900, usePortrait: false, startPage: startPage, autoSize: true, drawShadow: true
    });

    // --- CONFIGURACIÓN DE PARADAS DEL AHORCADO ---
    window.userProgress.paginasAhorcado = [12, 24, 32];
    
    pageFlip.loadFromHTML(document.querySelectorAll(".page"));

    function checkAhorcado(pIndex) {
        if (pIndex >= 3) {
            const cIndex = pIndex - 3;
            if (window.userProgress.paginasAhorcado.includes(cIndex)) {
                if (!window.userProgress.paradasVistas.has(cIndex)) {
                    window.userProgress.paradasVistas.add(cIndex);
                    window.pageBeforeAhorcado = pIndex;
                    
                    const bc = document.getElementById("book-container");
                    const np = document.getElementById("next-page");
                    const pp = document.getElementById("prev-page");
                    if (bc) bc.style.pointerEvents = "none";
                    if (np) np.style.pointerEvents = "none";
                    if (pp) pp.style.pointerEvents = "none";

                    setTimeout(() => {
                        mostrarAhorcado(cIndex);
                    }, 200);
                }
            }
        }
    }

    // Comprobar si al cargar ya estamos en una página de ahorcado pendiente
    checkAhorcado(startPage);

    // Escribir el texto de la página inicial
    const initialCuentoPageIndex = startPage - 3;
    if (initialCuentoPageIndex >= 0 && initialCuentoPageIndex % 2 === 0) {
        const initialStoryIndex = initialCuentoPageIndex / 2;
        if (initialStoryIndex >= 0 && initialStoryIndex < cuento.length) {
            escribirTexto(cuento[initialStoryIndex].texto, initialStoryIndex);
        }
    }

    pageFlip.on("flip", (e) => {
        const pageIndex = e.data;
        const cuentoPageIndex = pageIndex - 3;
        
        console.log(`FLIP: pageIndex=${pageIndex}, cuentoPageIndex=${cuentoPageIndex}`);
        // --- LÓGICA DE ACTIVACIÓN EN PÁGINAS DE AHORCADO ---
        checkAhorcado(pageIndex);

        if (cuentoPageIndex > 0) {
            const paginasLeidas = Math.floor(cuentoPageIndex / 2);
            if (paginasLeidas > window.userProgress.paginasLeidas) {
                window.userProgress.paginasLeidas = paginasLeidas;
                guardarProgreso(paginasLeidas);
            }
        }

        if (cuentoPageIndex >= 0 && cuentoPageIndex % 2 === 0) {
            const storyIndex = cuentoPageIndex / 2;
            if (storyIndex >= 0 && storyIndex < cuento.length) {
                escribirTexto(cuento[storyIndex].texto, storyIndex);
            }
        }

        const prevBtn = document.getElementById("prev-page");
        const nextBtn = document.getElementById("next-page");
        const scene = document.querySelector(".scene");
        const ultimoIndex = 3 + (cuento.length * 2) + 2;

        scene.classList.remove("is-closed-front", "is-closed-back");
        prevBtn.classList.remove("arrow-hidden");
        nextBtn.classList.remove("arrow-hidden");

        if (pageIndex === 0) {
            prevBtn.classList.add("arrow-hidden");
            scene.classList.add("is-closed-front");
        } else if (pageIndex === ultimoIndex) {
            nextBtn.classList.add("arrow-hidden");
            scene.classList.add("is-closed-back");

            if (!window.userProgress.invitacionMostrada) {
                window.userProgress.invitacionMostrada = true;
                
                // Calcular estadisticas reales
                const juegosJugados = window.userProgress.ahorcadosJugados || 3;
                const juegosGanados = window.userProgress.ahorcadosGanados || 0;
                const totalFallos = window.userProgress.fallosTotales || 0;
                const fallosMaximos = juegosJugados * 6;
                let porcentaje = 100 - ((totalFallos / fallosMaximos) * 100);
                if (porcentaje < 0) porcentaje = 0;
                
                // --- GUARDAR HISTORIAL LECTURA COMPLETO ---
                fetch('/api/guardar-progreso/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        paginas_leidas: window.userProgress.paginasLeidas,
                        puzzle_id: window.userProgress.puzzleId,
                        nombre_jugador: window.userProgress.nombreJugador,
                        historial_lectura: {
                            paginas_leidas: window.userProgress.paginasLeidas,
                            preguntas_totales: juegosJugados,
                            preguntas_correctas: juegosGanados,
                            porcentaje_comprension: parseFloat(porcentaje.toFixed(1))
                        }
                    })
                }).catch(e => console.error("Error al guardar historial de lectura completo:", e));

                setTimeout(() => {
                    let modal = document.getElementById('puzzle-invitation-modal');
                    if (!modal) {
                        modal = document.createElement('div');
                        modal.innerHTML = `
                            <div id="puzzle-invitation-modal" style="display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 12000; justify-content: center; align-items: center; backdrop-filter: blur(10px); font-family: 'Fredoka One', cursive;">
                                <div style="position: relative; background: linear-gradient(180deg, #e0c3fc 0%, #8ec5fc 100%); padding: 50px 40px; border-radius: 50px; border: 12px solid #fff; box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 0 20px rgba(255,255,255,0.8); text-align: center; width: 700px; max-width: 95%; transform: scale(1); animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55); overflow: hidden;">
                                    
                                    <!-- Elementos decorativos de fondo -->
                                    <img src="/static/inicio_sesion/img/nube_finallectura.png" style="position: absolute; top: 20px; left: 30px; height: 80px; object-fit: contain; opacity: 0.9; animation: float 3s ease-in-out infinite;">
                                    <img src="/static/inicio_sesion/img/estrella_finallectura.png" style="position: absolute; top: 40px; right: 40px; height: 70px; object-fit: contain; opacity: 0.9; animation: float 4s ease-in-out infinite;">
                                    <div style="position: absolute; top: 110px; left: 80px; font-size: 30px; opacity: 0.8; animation: float 2.5s ease-in-out infinite;">✨</div>
                                    <div style="position: absolute; top: 90px; right: 100px; font-size: 35px; opacity: 0.8; animation: float 3.5s ease-in-out infinite;">🌟</div>

                                    <!-- Personajes laterales -->
                                    <img src="/static/inicio_sesion/img/dinosahurio_finallectura.png" style="position: absolute; bottom: -10px; left: 10px; height: 160px; object-fit: contain; animation: hop 2s infinite;">
                                    <img src="/static/inicio_sesion/img/oso_finallectura.png" style="position: absolute; bottom: -10px; right: 10px; height: 160px; object-fit: contain; animation: hop 2.5s infinite;">

                                    <!-- Título Multicolor -->
                                    <h2 style="font-size: 75px; margin-bottom: 15px; display: flex; justify-content: center; gap: 3px; position: relative; z-index: 2; text-shadow: 3px 3px 0 #fff, -3px -3px 0 #fff, 3px -3px 0 #fff, -3px 3px 0 #fff, 6px 6px 0px rgba(0,0,0,0.2);">
                                        <span style="color: #ff6b6b;">¡</span>
                                        <span style="color: #ff9f43;">F</span>
                                        <span style="color: #feca57;">e</span>
                                        <span style="color: #1dd1a1;">l</span>
                                        <span style="color: #54a0ff;">i</span>
                                        <span style="color: #5f27cd;">c</span>
                                        <span style="color: #ff9ff3;">i</span>
                                        <span style="color: #ff6b6b;">d</span>
                                        <span style="color: #ff9f43;">a</span>
                                        <span style="color: #feca57;">d</span>
                                        <span style="color: #1dd1a1;">e</span>
                                        <span style="color: #54a0ff;">s</span>
                                        <span style="color: #5f27cd;">!</span>
                                    </h2>
                                    
                                    <p style="color: #1a1a1a; font-size: 30px; margin-bottom: 40px; font-weight: bold; text-shadow: 2px 2px 0px rgba(255,255,255,0.8); position: relative; z-index: 2; line-height: 1.4;">
                                        ¡Has terminado el cuento!<br>
                                        <span style="color: #000;">¿Quieres ir a armar tu rompecabezas?</span>
                                    </p>

                                    <div style="display: flex; justify-content: center; gap: 25px; position: relative; z-index: 2;">
                                        <button onclick="window.location.href='/juego_rompecabeza/' + window.userProgress.puzzleId + '/'" style="background: linear-gradient(to bottom, #43a047, #1b5e20); color: white; border: 6px solid #fff; padding: 15px 35px; font-size: 26px; font-family: 'Fredoka One', cursive; border-radius: 40px; cursor: pointer; transition: 0.2s; box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset 0 -5px 0 rgba(0,0,0,0.2);" onmouseover="this.style.transform='scale(1.1) translateY(-5px)'" onmouseout="this.style.transform='scale(1) translateY(0)'">
                                            🧩 ¡SÍ, VAMOS!
                                        </button>
                                        <button onclick="document.getElementById('puzzle-invitation-modal').style.display='none'" style="background: linear-gradient(to bottom, #ff5252, #c0392b); color: white; border: 6px solid #fff; padding: 15px 35px; font-size: 26px; font-family: 'Fredoka One', cursive; border-radius: 40px; cursor: pointer; transition: 0.2s; box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset 0 -5px 0 rgba(0,0,0,0.2);" onmouseover="this.style.transform='scale(1.1) translateY(-5px)'" onmouseout="this.style.transform='scale(1) translateY(0)'">
                                            ✖ Cerrar
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <style>
                            @keyframes bounceIn {
                                0% { transform: scale(0.3); opacity: 0; }
                                50% { transform: scale(1.05); opacity: 1; }
                                70% { transform: scale(0.9); }
                                100% { transform: scale(1); }
                            }
                            @keyframes float {
                                0% { transform: translateY(0px); }
                                50% { transform: translateY(-15px); }
                                100% { transform: translateY(0px); }
                            }
                            @keyframes hop {
                                0% { transform: scaleX(var(--flip, 1)) translateY(0px); }
                                20% { transform: scaleX(var(--flip, 1)) translateY(-20px); }
                                40% { transform: scaleX(var(--flip, 1)) translateY(0px); }
                                100% { transform: scaleX(var(--flip, 1)) translateY(0px); }
                            }
                            </style>
                        `;
                        document.body.appendChild(modal.firstElementChild);
                        document.head.insertAdjacentHTML('beforeend', modal.querySelector('style').outerHTML);
                    } else {
                        modal.style.display = "flex";
                    }
                }, 1000);
            }
        }
    });

    const ultimoIndexInit = 3 + (cuento.length * 2) + 2;
    const sceneInit = document.querySelector(".scene");
    const prevBtnInit = document.getElementById("prev-page");
    const nextBtnInit = document.getElementById("next-page");

    sceneInit.classList.remove("is-closed-front", "is-closed-back");
    prevBtnInit.classList.remove("arrow-hidden");
    nextBtnInit.classList.remove("arrow-hidden");

    if (startPage === 0) {
        prevBtnInit.classList.add("arrow-hidden");
        sceneInit.classList.add("is-closed-front");
    } else if (startPage >= ultimoIndexInit) {
        nextBtnInit.classList.add("arrow-hidden");
        sceneInit.classList.add("is-closed-back");
    }
}

document.getElementById("next-page").addEventListener("click", () => {
    flipSound.play();
    pageFlip.flipNext();
});

document.getElementById("prev-page").addEventListener("click", () => {
    flipSound.play();
    pageFlip.flipPrev();
});

function mostrarAhorcado(pageIndex = null) {
    const modal = document.getElementById('ahorcado-modal');
    const iframe = document.getElementById('ahorcado-iframe');
    const totalParadas = window.userProgress.paginasAhorcado.length;
    const piezasRestantes = window.userProgress.totalPiezas - window.userProgress.fichasDesbloqueadas;
    
    const rewardBase = Math.ceil(window.userProgress.totalPiezas / totalParadas);
    const reward = Math.min(rewardBase, piezasRestantes > 0 ? piezasRestantes : 0);
    
    window.userProgress.ultimoReward = reward;

    const pregCuentos = {
        12: [
            { p: "¿Qué estación llegó a la hermosa granja?", r: "PRIMAVERA" },
            { p: "¿Cómo era el huevo que tardó más en abrirse?", r: "GRANDE" },
            { p: "¿Cómo se sintió la mamá pata al verlo salir?", r: "SORPRENDIDA" },
            { p: "¿Quién cuidaba a los patitos con mucho amor?", r: "MAMA" }
        ],
        24: [
            { p: "¿Cómo llamaban al patito los demás animales?", r: "FEO" },
            { p: "¿A dónde decidió marcharse el patito?", r: "LEJOS" },
            { p: "¿En qué estación pasó frío y soledad el patito?", r: "INVIERNO" },
            { p: "¿En dónde miró el patito su nuevo reflejo?", r: "ESTANQUE" }
        ],
        32: [
            { p: "¿Qué ave descubrió que era realmente?", r: "CISNE" },
            { p: "¿Cómo era el ave en la que se había convertido?", r: "ELEGANTE" },
            { p: "¿Qué se dio cuenta de que nunca había sido?", r: "FEO" },
            { p: "¿En qué se había convertido al crecer?", r: "HERMOSO" }
        ]
    };

    let params = `?mode=embedded&player=${encodeURIComponent(window.userProgress.nombreJugador)}&reward=${reward}&puzzle=${window.userProgress.puzzleId}`;
    
    if (pageIndex !== null && pregCuentos[pageIndex]) {
        const opciones = pregCuentos[pageIndex];
        const elegida = opciones[Math.floor(Math.random() * opciones.length)];
        params += `&pregunta=${encodeURIComponent(elegida.p)}&respuesta=${encodeURIComponent(elegida.r)}`;
    }

    iframe.src = `/ahorcado/${params}`;
    modal.style.display = 'flex';
}

window.userProgress.ahorcadosJugados = window.userProgress.ahorcadosJugados || 0;
window.userProgress.ahorcadosGanados = window.userProgress.ahorcadosGanados || 0;
window.userProgress.fallosTotales = window.userProgress.fallosTotales || 0;

window.addEventListener('message', (event) => {
    if (event.data === 'ahorcado_ganado') {
        window.userProgress.ahorcadosJugados += 1;
        window.userProgress.ahorcadosGanados += 1;
        cerrarAhorcado(false);
    } else if (event.data === 'continuar_sin_fichas') {
        window.userProgress.ahorcadosJugados += 1;
        window.userProgress.fallosTotales += 6;
        cerrarAhorcado(true);
    } else if (typeof event.data === 'object' && event.data.type === 'ahorcado_terminado') {
        window.userProgress.ahorcadosJugados += 1;
        window.userProgress.fallosTotales += (event.data.fallos || 0);
        if (event.data.ganado) {
            window.userProgress.ahorcadosGanados += 1;
            cerrarAhorcado(false);
        } else {
            cerrarAhorcado(true);
        }
    } else if (event.data === 'reiniciar_cuento') {
        reiniciarCuento();
    }
});

function cerrarAhorcado(sinFichas = false) {
    const modal = document.getElementById('ahorcado-modal');
    const iframe = document.getElementById('ahorcado-iframe');
    modal.style.display = 'none';
    iframe.src = '';
    
    if (!sinFichas) {
        // Actualizar progreso local (sin guardar de nuevo en BD porque el ahorcado ya lo hizo)
        const anterior = window.userProgress.fichasDesbloqueadas;
        const reward = window.userProgress.ultimoReward || 0;
        window.userProgress.fichasDesbloqueadas += reward;
        actualizarWidgetPuzzle();
        for (let i = 1; i <= 3; i++) {
            const piezaIndex = anterior + (i - 1);
            const cont = document.getElementById(`cont-pieza-${i}`);
            const elem = document.getElementById(`pieza-${i}-img`);
            const txt = document.getElementById(`txt-pieza-${i}`);
            if (cont) {
                if (i <= reward && piezaIndex < window.userProgress.totalPiezas) {
                    cont.style.display = 'flex';
                    configurarPiezaVisual(`pieza-${i}-img`, piezaIndex);
                    if (txt) txt.innerText = "PIEZA #" + (piezaIndex + 1);
                } else {
                    cont.style.display = 'none';
                }
            }
        }
        const overlay = document.getElementById('victory-overlay');
        if (overlay && reward > 0) {
            overlay.style.display = 'flex';
        } else {
            const bc = document.getElementById("book-container");
            const np = document.getElementById("next-page");
            const pp = document.getElementById("prev-page");
            if (bc) bc.style.pointerEvents = "auto";
            if (np) np.style.pointerEvents = "auto";
            if (pp) pp.style.pointerEvents = "auto";

            if (window.pageBeforeAhorcado !== undefined && window.pageBeforeAhorcado !== null) {
                pageFlip.turnToPage(window.pageBeforeAhorcado);
                window.pageBeforeAhorcado = null;
            }
        }
    } else {
        const bc = document.getElementById("book-container");
        const np = document.getElementById("next-page");
        const pp = document.getElementById("prev-page");
        if (bc) bc.style.pointerEvents = "auto";
        if (np) np.style.pointerEvents = "auto";
        if (pp) pp.style.pointerEvents = "auto";

        if (window.pageBeforeAhorcado !== undefined && window.pageBeforeAhorcado !== null) {
            pageFlip.turnToPage(window.pageBeforeAhorcado);
            window.pageBeforeAhorcado = null;
        }
    }
}

async function reiniciarCuento() {
    window.userProgress.paginasLeidas = 0;
    try {
        await fetch('/api/guardar-progreso/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                paginas_leidas: 0,
                puzzle_id: window.userProgress.puzzleId,
                nombre_jugador: window.userProgress.nombreJugador
            })
        });
    } catch (e) { console.error("Error reiniciando progreso:", e); }
    window.location.reload();
}

function configurarPiezaVisual(id, index) {
    const elem = document.getElementById(id);
    if (!elem) return;
    const d = window.userProgress.puzzleDificultad;
    const baseSize = 450;
    const pieceSize = baseSize / d;
    const x = (index % d) * pieceSize;
    const y = Math.floor(index / d) * pieceSize;
    elem.style.backgroundPosition = `-${x}px -${y}px`;
}

function actualizarWidgetPuzzle() {
    const actual = window.userProgress.fichasDesbloqueadas;
    const total = window.userProgress.totalPiezas;
    if (document.getElementById('fichas-actuales')) document.getElementById('fichas-actuales').innerText = actual;
    if (document.getElementById('fichas-totales')) document.getElementById('fichas-totales').innerText = total;
    const elemFill = document.getElementById('puzzle-progress-fill');
    if (elemFill) {
        const porcentaje = Math.min((actual / total) * 100, 100);
        elemFill.style.width = porcentaje + "%";
    }
}

function cerrarVictoria() {
    const overlay = document.getElementById('victory-overlay');
    overlay.style.transition = 'opacity 0.3s ease';
    overlay.style.opacity = '0';
    setTimeout(() => {
        overlay.style.display = 'none';
        overlay.style.opacity = '1';

        const bc = document.getElementById("book-container");
        const np = document.getElementById("next-page");
        const pp = document.getElementById("prev-page");
        if (bc) bc.style.pointerEvents = "auto";
        if (np) np.style.pointerEvents = "auto";
        if (pp) pp.style.pointerEvents = "auto";

        if (window.pageBeforeAhorcado !== undefined && window.pageBeforeAhorcado !== null) {
            pageFlip.turnToPage(window.pageBeforeAhorcado);
            window.pageBeforeAhorcado = null;
        }
    }, 300);
}

async function guardarProgreso(paginas = 0, fichas = 0) {
    try {
        const body = { 
            paginas_leidas: paginas,
            puzzle_id: window.userProgress.puzzleId,
            nombre_jugador: window.userProgress.nombreJugador
        };
        if (fichas > 0) body.sumar_fichas = fichas;

        await fetch('/api/guardar-progreso/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
    } catch (e) { console.error("Error guardando progreso:", e); }
}

document.addEventListener("mousemove", (e) => {
    const container = document.getElementById("book-container");
    const x = (window.innerWidth / 2 - e.pageX) / 60;
    const y = (window.innerHeight / 2 - e.pageY) / 120;
    if (container) container.style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
});

window.onload = () => {
    construirLibro();
    iniciarLibro();
    actualizarWidgetPuzzle();
}

function createParticle() {
    const fairy = document.getElementById("fairy");
    if (!fairy) return;
    const scene = document.querySelector(".scene");
    if (!scene) return;
    const particle = document.createElement("div");
    particle.classList.add("particle");
    const rect = fairy.getBoundingClientRect();
    const sceneRect = scene.getBoundingClientRect();
    const offsetX = (Math.random() - 0.5) * 30;
    const offsetY = (Math.random() - 0.5) * 30;
    particle.style.left = (rect.left - sceneRect.left) + rect.width / 2 + offsetX + "px";
    particle.style.top = (rect.top - sceneRect.top) + rect.height / 2 + offsetY + "px";
    const colors = [{ main: '#00fbff', glow: '#00aaff' }, { main: '#00e5ff', glow: '#006eff' }, { main: '#ffffff', glow: '#00fbff' }];
    const color = colors[Math.floor(Math.random() * colors.length)];
    particle.style.background = color.main;
    particle.style.boxShadow = `0 0 10px ${color.main}, 0 0 20px ${color.glow}`;
    if (Math.random() > 0.4) particle.style.clipPath = "polygon(50% 0%, 60% 40%, 100% 50%, 60% 60%, 50% 100%, 40% 60%, 0% 50%, 40% 40%)";
    const drift = (Math.random() - 0.5) * 140;
    particle.style.setProperty('--x-drift', `${drift}px`);
    const size = Math.random() * 6 + 2;
    particle.style.width = size + "px";
    particle.style.height = size + "px";
    particle.style.animationDuration = (Math.random() * 1 + 1) + "s";
    particle.style.opacity = Math.random() * 0.4 + 0.6;
    scene.appendChild(particle);
    setTimeout(() => { particle.remove(); }, 2000);
}
setInterval(createParticle, 50);
