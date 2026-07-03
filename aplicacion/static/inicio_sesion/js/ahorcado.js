document.addEventListener('DOMContentLoaded', () => {
            if (window.location.search.includes('mode=embedded')) {
                document.body.classList.add('embedded');
            }
        });
        const banco = [
            { p: "¿De qué color es la capuchita?", r: "ROJO" },
            { p: "¿Dónde vivía la niña?", r: "BOSQUE" },
            { p: "¿Cómo se sentía Caperucita?", r: "FELIZ" },
            { p: "¿Con quién le gustaba jugar?", r: "ANIMALES" }
        ];

        let palabraActual = "";
        let preguntaActiva = null;
        let fallos = 0;
        let score = window.gameConfig.puntos || 0;
        let fichas = window.gameConfig.fichas || 0;
        const urlParams = new URLSearchParams(window.location.search);
        const rewardParam = urlParams.get('reward');
        const premioFichas = rewardParam !== null && rewardParam !== "" ? parseInt(rewardParam) : 3;
        const nombreJugadorActual = window.gameConfig.nombreJugador;
        let tiempo = 120;
        let timerInterval = null;

        // Orden: pie izq, pie der, mano izq, mano der, cuerpo, cabeza
        const ordenDesaparicion = [4, 5, 1, 2, 3, 0];

        // EFECTOS DE SONIDO
        let globalAudioCtx = null;
        let isMuted = false;

        function getAudioCtx() {
            if (!globalAudioCtx) {
                globalAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (globalAudioCtx.state === 'suspended') {
                globalAudioCtx.resume();
            }
            return globalAudioCtx;
        }

        function toggleMute() {
            isMuted = !isMuted;
            const btn = document.getElementById('btn-mute');
            const icon = document.getElementById('mute-icon');
            
            if (isMuted) {
                icon.innerText = '🔇';
                btn.style.background = 'rgba(255, 50, 50, 0.7)';
            } else {
                icon.innerText = '🔊';
                btn.style.background = 'rgba(0,0,0,0.5)';
            }
        }



        // Función para reproducir un sonido cómico de error ("Boing / Caída")
        function playErrorSound() {
            if (isMuted) return;
            try {
                const audioCtx = getAudioCtx();
                
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                
                osc.type = 'sawtooth'; // Onda tipo retro-game
                
                // Efecto de silbato cayendo (Slide whistle)
                osc.frequency.setValueAtTime(450, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.4);
                
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
                
                osc.start(audioCtx.currentTime);
                osc.stop(audioCtx.currentTime + 0.5);

            } catch(e) {
                console.log("Audio no soportado o bloqueado por el navegador", e);
            }
        }

        // Función para reproducir sonido de derrota (Womp womp womp cómico)
        function playDefeatSound() {
            if (isMuted) return;
            try {
                const audioCtx = getAudioCtx();
                
                function playNote(freq, startTime, duration, type='square') {
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.type = type; // Sonido de videojuego retro
                    osc.frequency.value = freq;
                    
                    gain.gain.setValueAtTime(0.1, startTime);
                    gain.gain.setTargetAtTime(0.01, startTime + duration - 0.1, 0.1);
                    
                    osc.start(startTime);
                    osc.stop(startTime + duration);
                }

                const now = audioCtx.currentTime;
                // Womp womp womp
                playNote(250, now, 0.3);
                playNote(230, now + 0.4, 0.3);
                playNote(210, now + 0.8, 0.3);
                
                // Wooooomp (caída final)
                const oscF = audioCtx.createOscillator();
                const gainF = audioCtx.createGain();
                oscF.connect(gainF);
                gainF.connect(audioCtx.destination);
                oscF.type = 'square';
                oscF.frequency.setValueAtTime(190, now + 1.2);
                oscF.frequency.linearRampToValueAtTime(90, now + 2.2); 
                
                gainF.gain.setValueAtTime(0.1, now + 1.2);
                gainF.gain.exponentialRampToValueAtTime(0.01, now + 2.2);
                oscF.start(now + 1.2);
                oscF.stop(now + 2.4);

            } catch(e) {
                console.log("Audio no soportado", e);
            }
        }

        // Sonido de "Pop" o toque de madera al presionar una letra
        function playTypeSound() {
            if (isMuted) return;
            try {
                const audioCtx = getAudioCtx();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                
                osc.type = 'sine'; 
                // Pitch drop muy rápido para crear un sonido de "burbuja" o "pop"
                osc.frequency.setValueAtTime(600, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.05);
                
                gain.gain.setValueAtTime(0, audioCtx.currentTime);
                gain.gain.linearRampToValueAtTime(0.4, audioCtx.currentTime + 0.01);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);
                
                osc.start(audioCtx.currentTime);
                osc.stop(audioCtx.currentTime + 0.1);
            } catch(e) {
                console.log(e);
            }
        }

        // Sonido de victoria cuando ganan el nivel (Fanfarria muy divertida)
        function playWinSound() {
            if (isMuted) return;
            try {
                const audioCtx = getAudioCtx();
                
                function playNote(freq, startTime, duration, type='square') {
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    
                    osc.type = type; // square para sonido de 8-bits retro
                    osc.frequency.value = freq;
                    
                    gain.gain.setValueAtTime(0.15, startTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, startTime + duration);
                    
                    osc.start(startTime);
                    osc.stop(startTime + duration);
                }
                
                const now = audioCtx.currentTime;
                
                // Fanfarria estilo Super Mario / Nivel completado
                // Tres notas rápidas ascendentes
                playNote(392.00, now, 0.12); // Sol
                playNote(523.25, now + 0.12, 0.12); // Do
                playNote(659.25, now + 0.24, 0.12); // Mi
                
                // Pequeña pausa, nota más alta
                playNote(783.99, now + 0.38, 0.2); // Sol agudo
                
                // Bajadita rápida
                playNote(659.25, now + 0.58, 0.12); // Mi
                
                // Explosión final súper alta (con un pequeño barrido de frecuencia)
                const oscF = audioCtx.createOscillator();
                const gainF = audioCtx.createGain();
                oscF.connect(gainF);
                gainF.connect(audioCtx.destination);
                oscF.type = 'square';
                
                oscF.frequency.setValueAtTime(783.99, now + 0.70); // Sol agudo
                oscF.frequency.exponentialRampToValueAtTime(1046.50, now + 0.75); // Sube a Do rapidísimo (efecto "Wahoo!")
                
                gainF.gain.setValueAtTime(0.15, now + 0.70);
                gainF.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
                
                oscF.start(now + 0.70);
                oscF.stop(now + 1.6);
                
                // Acompañamiento tipo campanita brillante por encima
                function playSparkle(freq, startTime) {
                    playNote(freq, startTime, 0.3, 'sine');
                }
                playSparkle(1046.50, now);
                playSparkle(1318.51, now + 0.12);
                playSparkle(1567.98, now + 0.24);
                playSparkle(2093.00, now + 0.70);

            } catch(e) {}
        }

        // Sonido de "Tick" para el temporizador (últimos 5 segundos)
        function playTickSound() {
            if (isMuted) return;
            try {
                const audioCtx = getAudioCtx();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                
                osc.type = 'square'; // Sonido agudo de alerta
                osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                
                gain.gain.setValueAtTime(0, audioCtx.currentTime);
                gain.gain.linearRampToValueAtTime(0.1, audioCtx.currentTime + 0.01);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                
                osc.start(audioCtx.currentTime);
                osc.stop(audioCtx.currentTime + 0.15);
            } catch(e) {}
        }

        function presionarTecla(letra) {
            if (document.getElementById('modal-resultado').style.display === 'flex') return;
            if (fallos >= 6) return;

            const btnLetra = letra.toUpperCase();
            const btns = document.querySelectorAll('.key-btn');

            // Buscar si la letra existe en el teclado virtual
            let existe = false;
            for (let btn of btns) {
                if (btn.innerText.toUpperCase() === btnLetra) {
                    existe = true;
                    break;
                }
            }

            if (existe && palabraActual.length < preguntaActiva.r.length) {
                palabraActual += btnLetra;
                actualizarTablero();
            }
        }

        function crearTeclado() {
            const kb = document.getElementById('keyboard');
            const abc = "AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZ";
            kb.innerHTML = "";

            abc.split('').forEach(letra => {
                const b = document.createElement('button');
                b.className = "key-btn";
                b.innerText = letra;
                b.onclick = () => presionarTecla(letra);
                kb.appendChild(b);
            });

            // Botón borrar
            const btnDel = document.createElement('button');
            btnDel.className = "key-btn backspace-btn";
            btnDel.innerText = "⌫";
            btnDel.onclick = () => {
                if (fallos >= 6) return;
                palabraActual = palabraActual.slice(0, -1);
                actualizarTablero();
            };
            kb.appendChild(btnDel);

            // Botón aceptar
            const btnOk = document.createElement('button');
            btnOk.className = "key-btn accept-btn";
            btnOk.innerText = "ACEPTAR";
            btnOk.onclick = verificar;
            kb.appendChild(btnOk);
        }

        function actualizarTablero() {
            const display = document.getElementById('word-box');
            display.innerText = palabraActual.padEnd(preguntaActiva.r.length, "_");

            // Ajustar tamaño de fuente si la palabra es muy larga
            if (preguntaActiva.r.length > 8) {
                display.style.fontSize = "3.5rem";
            } else {
                display.style.fontSize = "5rem";
            }
        }

        function iniciar() {
            const params = new URLSearchParams(window.location.search);
            const pCustom = params.get('pregunta');
            const rCustom = params.get('respuesta');

            if (pCustom && rCustom) {
                preguntaActiva = { p: pCustom, r: rCustom.toUpperCase() };
            } else {
                preguntaActiva = banco[Math.floor(Math.random() * banco.length)];
            }
            document.getElementById('pregunta-text').innerText = preguntaActiva.p;
            palabraActual = "";
            fallos = 0;
            document.getElementById('oportunidades').innerText = "6";
            document.querySelectorAll('.panda-part').forEach(p => {
                p.classList.remove('falling');
                p.style.opacity = "";
                p.style.transform = "";
            });
            actualizarTablero();

            tiempo = 120;
            document.getElementById('tiempo').innerText = "02:00";
            if (timerInterval) clearInterval(timerInterval);
            timerInterval = setInterval(() => {
                if (document.getElementById('modal-resultado').style.display === 'flex' || document.getElementById('modal-tiempo').style.display === 'flex') return;
                
                tiempo--;
                const m = Math.floor(tiempo / 60).toString().padStart(2, '0');
                const s = (tiempo % 60).toString().padStart(2, '0');
                document.getElementById('tiempo').innerText = `${m}:${s}`;
                
                if (tiempo <= 5 && tiempo > 0) {
                    playTickSound();
                    // Efecto visual de parpadeo en rojo
                    const tiempoBox = document.getElementById('tiempo');
                    tiempoBox.style.color = '#ff4757';
                    setTimeout(() => {
                        tiempoBox.style.color = ''; // Vuelve a blanco
                    }, 500);
                }
                
                if (tiempo <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById('modal-tiempo-titulo').innerText = "¡TIEMPO AGOTADO!";
                    document.getElementById('modal-tiempo-mensaje').innerText = "Se te acabó el tiempo para responder la pregunta.";
                    document.getElementById('modal-tiempo').style.display = 'flex';

                    // Aplicar penalización de 50 puntos
                    (async () => {
                        const penalizacion = -50;
                        const res = await enviarResultado(penalizacion, 0);
                        if (res && res.status === 'success') {
                            score = res.puntuacion_total;
                            document.getElementById('puntos').innerText = score;
                        } else {
                            score = Math.max(0, score + penalizacion);
                            document.getElementById('puntos').innerText = score;
                        }
                    })();
                }
            }, 1000);
        }

        async function enviarResultado(puntosASumar, fichasASumar) {
            const urlParams = new URLSearchParams(window.location.search);
            const playerName = urlParams.get('player') || "";
            const puzzleId = urlParams.get('puzzle') || "";

            try {
                const bodyData = {
                    sumar_fichas: fichasASumar,
                    puntuacion: puntosASumar,
                    nombre_jugador: playerName || nombreJugadorActual,
                    historial_ahorcado: {
                        palabra: preguntaActiva ? preguntaActiva.r : palabraActual,
                        tiempo_respuesta: parseFloat((120 - tiempo).toFixed(1)),
                        intentos: fallos,
                        resultado: puntosASumar > 0 // Si gano puntos es que acerto
                    }
                };
                if (puzzleId) {
                    bodyData.puzzle_id = puzzleId;
                }

                const response = await fetch('/api/guardar-progreso/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(bodyData)
                });

                const result = await response.json();
                if (!response.ok) {
                    console.error("Error del servidor:", result.message);
                }
                return result;
            } catch (error) {
                console.error("Error de conexión:", error);
            }
        }

        async function verificar() {
            if (fallos >= 6) return;
            if (palabraActual.length < preguntaActiva.r.length) return;

            if (palabraActual === preguntaActiva.r) {
                playWinSound();
                const premioPuntos = 100;
                // premioFichas ya está definido al inicio desde los params


                // Actualizar UI localmente
                score += premioPuntos;
                fichas += premioFichas;
                document.getElementById('puntos').innerText = score;
                document.getElementById('fichas').innerText = fichas;

                // Esperar a que se guarde en la BD antes de cerrar
                const res = await enviarResultado(premioPuntos, premioFichas);
                if (res && res.status === 'success') {
                    score = res.puntuacion_total;
                    fichas = res.fichas;
                    document.getElementById('puntos').innerText = score;
                    document.getElementById('fichas').innerText = fichas;
                }

                const isEmbedded = window.location.search.includes('mode=embedded');
                if (isEmbedded) {
                    setTimeout(() => {
                        window.parent.postMessage({
                            type: 'ahorcado_terminado',
                            ganado: true,
                            fallos: fallos
                        }, '*');
                    }, 500);
                } else {
                    setTimeout(() => {
                        const mensajePiezas = premioFichas > 0 ? ` y ${premioFichas} piezas mágicas` : '';
                        mostrarModalResultado(
                            "¡EXCELENTE!",
                            `¡Has acertado la palabra!<br><span style="color: #55efc4;">Ganaste ${premioPuntos} puntos${mensajePiezas}</span>`,
                            "#2ecc71"
                        );
                    }, 100);
                }
            } else {
                if (fallos < 6) {
                    const idParte = ordenDesaparicion[fallos];
                    const parte = document.getElementById(`part-${idParte}`);
                    parte.classList.add('falling');
                    playErrorSound();
                    fallos++;
                    document.getElementById('oportunidades').innerText = 6 - fallos;
                    palabraActual = "";
                    actualizarTablero();

                    if (fallos === 6) {
                        playDefeatSound();
                        setTimeout(async () => {
                            const penalizacion = -50;
                            document.getElementById('modal-tiempo-titulo').innerText = "¡OH NO!";
                            document.getElementById('modal-tiempo-mensaje').innerHTML = `El panda se ha ido.<br>Respuesta: <b>${preguntaActiva.r}</b>`;
                            document.getElementById('modal-tiempo').style.display = 'flex';

                            // 1. Guardar penalización en el servidor inmediatamente
                            const res = await enviarResultado(penalizacion, 0);

                            // 2. Actualizar score local y UI con el valor real del servidor
                            if (res && res.status === 'success') {
                                score = res.puntuacion_total;
                                document.getElementById('puntos').innerText = score;
                            } else {
                                // Fallback local si falla el server
                                score = Math.max(0, score + penalizacion);
                                document.getElementById('puntos').innerText = score;
                            }
                        }, 900);
                    }
                }
            }
        }

        function cerrarModalResultado() {
            document.getElementById('modal-resultado').style.display = 'none';
            iniciar();
        }

        function mostrarModalResultado(titulo, mensaje, colorBtn) {
            document.getElementById('modal-res-titulo').innerText = titulo;
            document.getElementById('modal-res-mensaje').innerHTML = mensaje;
            const btn = document.querySelector('.btn-result');
            btn.style.background = colorBtn;
            btn.style.boxShadow = `0 10px 20px ${colorBtn}4D`;
            document.getElementById('modal-resultado').style.display = 'flex';
        }

        function opcionReiniciar() {
            const isEmbedded = window.location.search.includes('mode=embedded');
            if (isEmbedded) {
                window.parent.postMessage('reiniciar_cuento', '*');
            } else {
                window.location.reload();
            }
        }

        function opcionContinuarSinFichas() {
            const isEmbedded = window.location.search.includes('mode=embedded');
            if (isEmbedded) {
                window.parent.postMessage({
                    type: 'ahorcado_terminado',
                    ganado: false,
                    fallos: fallos
                }, '*');
            } else {
                cerrarModalResultado(); // Solo para salir del modal si no está incrustado
                document.getElementById('modal-tiempo').style.display = 'none';
                iniciar();
            }
        }


        // EVENTOS DE TECLADO FÍSICO
        function manejarTecladoFisico(e) {
            // Evitar comportamiento por defecto de la tecla Enter (como pulsar botones en foco)
            if (e.key.toUpperCase() === 'ENTER') {
                e.preventDefault();
                e.stopPropagation();
                if (document.getElementById('modal-resultado').style.display !== 'flex') {
                    verificar();
                }
                return;
            }

            if (document.getElementById('modal-resultado').style.display === 'flex') return;
            const letra = e.key.toUpperCase();
            
            if (letra === 'BACKSPACE') {
                e.preventDefault(); // Evitar volver atrás en el navegador
                palabraActual = palabraActual.slice(0, -1);
                actualizarTablero();
                return;
            }

            // Solo procesar si es un solo carácter (evita Shift, Control, etc.)
            if (e.key.length === 1) {
                presionarTecla(letra);
            }
        }

        document.addEventListener('keydown', manejarTecladoFisico);

        // ESCUCHAR TECLAS DEL PADRE (Si está en un iframe)
        try {
            if (window.parent && window.parent !== window) {
                window.parent.document.addEventListener('keydown', manejarTecladoFisico);
                
                // Remover el listener cuando se cierra/descarga el iframe para evitar bugs
                window.addEventListener('unload', () => {
                    try {
                        window.parent.document.removeEventListener('keydown', manejarTecladoFisico);
                    } catch (e) {}
                });
            }
        } catch (err) {
            console.log("Modo independiente.");
        }

        crearTeclado();
        iniciar();

function aplicarEscalaResponsiva() {
        const minWidth = 1100; // Ancho base de diseño
        const screenWidth = window.innerWidth;
        
        if (screenWidth < minWidth) {
            const scale = screenWidth / minWidth;
            document.body.style.transform = `scale(${scale})`;
            document.body.style.transformOrigin = 'top left';
            document.body.style.width = `${minWidth}px`;
            document.body.style.minHeight = `${window.innerHeight / scale}px`;
            document.documentElement.style.overflowX = 'hidden';
            document.body.style.overflowX = 'hidden';
        } else {
            document.body.style.transform = 'none';
            document.body.style.width = '100%';
            document.body.style.minHeight = '100vh';
        }
    }
    window.addEventListener('resize', aplicarEscalaResponsiva);
    window.addEventListener('DOMContentLoaded', aplicarEscalaResponsiva);
    aplicarEscalaResponsiva();