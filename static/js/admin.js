document.addEventListener('DOMContentLoaded', () => {

  // --- 1. VARIABLES GLOBALES ---
  let baseDeDatosMuebles = [];
  let slotActivo = null;
  const modalElement = document.getElementById('modal-seleccion-mueble');
  const modalBootstrap = new bootstrap.Modal(modalElement);

  let desgloseDeMuebles = {};
  let tipoCocinaActual = null;
  let resumenDiv = document.getElementById('simulador-resumen');
  let listaDesgloseUI = document.getElementById('lista-desglose-muebles');

  // --- 2. POSICIONES ---
  const posiciones = {
    pequena: [
      { top: '60%', left: '3.5%', w: '236px', h: '348px', tipo: 'inferior'},
      { top: '60%', left: '27%',  w: '233px', h: '348px', tipo: 'inferior'},
      { top: '60%', left: '50%',  w: '230px', h: '348px', tipo: 'inferior'},
      { top: '60%', left: '73%',  w: '236px', h: '348px', tipo: 'inferior'},
      { top: '11.37%', left: '3.5%', w: '236px', h: '275px', tipo: 'superior'},
      { top: '11.37%', left: '27%',  w: '233px', h: '275px', tipo: 'superior'},
      { top: '11.37%', left: '50%',  w: '230px', h: '275px', tipo: 'superior'},
      { top: '11.37%', left: '73%',  w: '236px', h: '275px', tipo: 'superior'},
    ],
    cocinaL: [
      { top: '9%',  left: '2%',  w: '16%', h: '36%', tipo: 'superior'},
      { top: '13%', left: '22%', w: '12%', h: '33%', tipo: 'superior'},
      { top: '15%', left: '37%', w: '20%', h: '31%', tipo: 'superior'},
      { top: '13%', left: '60%', w: '13%', h: '32%', tipo: 'superior'},
      { top: '10%', left: '76%', w: '15%', h: '35%', tipo: 'superior'},
      { top: '59%', left: '3%',  w: '15%', h: '27%', tipo: 'inferior'},
      { top: '58%', left: '21%', w: '13%', h: '26%', tipo: 'inferior'},
      { top: '58%', left: '37%', w: '20%', h: '24%', tipo: 'inferior'},
      { top: '58%', left: '60%', w: '12%', h: '26%', tipo: 'inferior'},
      { top: '59%', left: '76%', w: '15%', h: '27%', tipo: 'inferior'},
    ],
    grande: [
      { top: '60%', left: '5%',  w: '100px', h: '150px', tipo: 'inferior'},
      { top: '60%', left: '20%', w: '100px', h: '150px', tipo: 'inferior'},
      { top: '60%', left: '35%', w: '100px', h: '150px', tipo: 'inferior'},
      { top: '60%', left: '70%', w: '100px', h: '150px', tipo: 'inferior'},
      { top: '30%', left: '5%',  w: '100px', h: '100px', tipo: 'superior'},
      { top: '30%', left: '20%', w: '100px', h: '100px', tipo: 'superior'},
      { top: '30%', left: '35%', w: '100px', h: '100px', tipo: 'superior'},
      { top: '30%', left: '70%', w: '100px', h: '100px', tipo: 'superior'},
    ]
  };

  // --- 3. FONDOS ---
  const fondosCocina = {
    pequena: [
      { nombre: 'Fondo Clásico (Pequeño)',       img: '/static/img/fondos/pequeño/cocina-pequena-fondo.png' },
      { nombre: 'Fondo Verde Salvaje (Pequeño)', img: '/static/img/fondos/pequeño/Fondo Verde - 8(4x4).png' },
      { nombre: 'Fondo Marmol (Pequeño)',        img: '/static/img/fondos/pequeño/Fondo Marmol - 8(4x4).png' },
      { nombre: 'Fondo Madera (Pequeño)',        img: '/static/img/fondos/pequeño/Fondo Madera- 8(4x4).png' },
    ],
    cocinaL: [
      { nombre: 'Madera Normal (En L)',  img: '/static/img/fondos/cocinaL/cocina-l-madera-normal.png' },
      { nombre: 'Madera Blanca (En L)', img: '/static/img/fondos/cocinaL/cocina-l-madera-blanca.png' },
      { nombre: 'Mármol (En L)',        img: '/static/img/fondos/cocinaL/cocina-l-marmol.png' },
      { nombre: 'Verde (En L)',         img: '/static/img/fondos/cocinaL/cocina-l-verde.png' },
    ],
    grande: [
      { nombre: 'Fondo Clásico (Grande)', img: '/static/img/fondos/grande/cocina-grande-fondo.jpg' },
      { nombre: 'Fondo Mármol (Grande)',  img: '/static/img/cocina-grande-fondo-marmol.jpg' },
    ]
  };

  // --- 4. RUTAS JSON ---
  const rutasMuebles = {
    pequena: '/static/muebles_pequena.json',
    cocinaL: '/static/muebles_l.json',
    grande:  '/static/muebles_grande.json'
  };

  // --- 5. OBTENER ELEMENTOS DEL DOM ---
  const selDiv       = document.getElementById('simulador-seleccion');
  const simArea      = document.getElementById('simulador-area');
  const btnPequena   = document.getElementById('btn-cocina-pequena');
  const btnGrande    = document.getElementById('btn-cocina-grande');
  const btnCocinaL   = document.getElementById('btn-cocina-l');
  const simFondo     = document.getElementById('simulador-fondo');
  const simSlots     = document.getElementById('simulador-slots');
  const selFondoDiv  = document.getElementById('simulador-seleccion-fondo');
  const fondosGridUI = document.getElementById('fondos-opciones-grid');
  const btnExportar  = document.getElementById('btn-exportar-pdf');

  const modalTitulo        = document.getElementById('modal-titulo');
  const modalCuerpoGrid    = document.getElementById('modal-cuerpo');
  const modalPreview       = document.getElementById('modal-preview');
  const btnVolverGrid      = document.getElementById('btn-volver-grid');
  const btnAddMueble       = document.getElementById('btn-add-mueble');
  const previewNombre      = document.getElementById('preview-nombre-mueble');
  const carouselIndicators = document.getElementById('carousel-preview-indicators');
  const carouselInner      = document.getElementById('carousel-preview-inner');

  // --- 6. FUNCIÓN: Cargar JSON de muebles ---
  function cargarMueblesPorTipo(tipo) {
    const ruta = rutasMuebles[tipo];
    fetch(ruta)
      .then(response => {
        if (!response.ok) throw new Error(`No se encontró: ${ruta}`);
        return response.json();
      })
      .then(data => {
        baseDeDatosMuebles = data;
        console.log(`Muebles cargados desde: ${ruta}`);
      })
      .catch(error => console.error('Error cargando JSON:', error));
  }

  // --- 7. FUNCIÓN: Iniciar simulador (muestra selección de fondo) ---
  function iniciarSimulador(tipo) {
    selDiv.classList.add('hidden');
    selFondoDiv.classList.remove('hidden');
    tipoCocinaActual = tipo;
    cargarMueblesPorTipo(tipo);

    fondosGridUI.innerHTML = '';
    const fondos = fondosCocina[tipo];
    if (fondos) {
      fondos.forEach(fondo => {
        fondosGridUI.innerHTML += `
          <div class="col-md-4">
            <a href="#" class="fondo-opcion" data-img-src="${fondo.img}">
              <img src="${fondo.img}" alt="${fondo.nombre}">
              <h6>${fondo.nombre}</h6>
            </a>
          </div>
        `;
      });
      fondosGridUI.querySelectorAll('.fondo-opcion').forEach(opcion => {
        opcion.addEventListener('click', seleccionarFondo);
      });
    }
  }

  // --- 8. FUNCIÓN: Seleccionar fondo y mostrar área ---
  function seleccionarFondo(e) {
    e.preventDefault();
    const imgSrc = e.currentTarget.dataset.imgSrc;
    selFondoDiv.classList.add('hidden');
    simArea.classList.remove('hidden');
    simFondo.src = imgSrc;
    dibujarSlots(tipoCocinaActual);
  }

  // --- 9. FUNCIÓN: Dibujar slots sobre el fondo ---
  function dibujarSlots(tipo) {
    simSlots.innerHTML = '';
    resumenDiv.classList.remove('hidden');
    desgloseDeMuebles = {};
    actualizarDesgloseUI();

    const slotsConfig = posiciones[tipo];
    if (slotsConfig && slotsConfig.length > 0) {
      slotsConfig.forEach((pos, index) => {
        const slot = document.createElement('div');
        slot.className = 'mueble-slot';
        slot.dataset.slotId = index;
        slot.dataset.tipo   = pos.tipo;
        slot.style.top    = pos.top;
        slot.style.left   = pos.left;
        slot.style.width  = pos.w;
        slot.style.height = pos.h;
        slot.innerHTML = '<i class="fa-solid fa-plus"></i>';

        slot.addEventListener('click', (e) => {
          slotActivo = e.currentTarget;
          abrirModalConMuebles(slotActivo.dataset.tipo);
        });
        simSlots.appendChild(slot);
      });
    }
  }

  // --- 10. FUNCIÓN: Abrir modal con cuadrícula de muebles ---
  function abrirModalConMuebles(tipoSlot) {
    mostrarGridView(tipoSlot);
    modalCuerpoGrid.querySelectorAll('.mueble-opcion').forEach(opcion => {
      opcion.addEventListener('click', handleGridClick);
    });
    modalBootstrap.show();
  }

  // --- 11. FUNCIÓN: Mostrar cuadrícula dentro del modal ---
  function mostrarGridView(tipoSlot) {
    if (tipoSlot) {
      const mueblesFiltrados = baseDeDatosMuebles.filter(m => m.tipo === tipoSlot);
      modalCuerpoGrid.innerHTML = '';

      // Opción "Quitar mueble"
      modalCuerpoGrid.innerHTML += `
        <div class="col-md-4">
          <a href="#" class="mueble-opcion" data-id="limpiar">
            <div style="width:100%;height:120px;display:grid;place-content:center;font-size:30px;color:#777;">
              <i class="fa-solid fa-ban"></i>
            </div>
            <h6>Quitar mueble</h6>
          </a>
        </div>
      `;

      mueblesFiltrados.forEach(mueble => {
        modalCuerpoGrid.innerHTML += `
          <div class="col-md-4">
            <a href="#" class="mueble-opcion" data-id="${mueble.id}">
              <img src="${mueble.imagen_grid}" alt="${mueble.nombre}">
              <h6>${mueble.nombre}</h6>
            </a>
          </div>
        `;
      });
    }

    modalTitulo.textContent = `Selecciona un mueble ${tipoSlot || ''}`;
    modalCuerpoGrid.classList.remove('hidden');
    modalPreview.classList.add('hidden');
    btnVolverGrid.classList.add('hidden');
  }

  // --- 12. FUNCIÓN: Clic en una opción de la cuadrícula ---
  function handleGridClick(e) {
    e.preventDefault();
    const muebleId = e.currentTarget.dataset.id;

    if (muebleId === 'limpiar') {
      slotActivo.style.backgroundImage = 'none';
      slotActivo.innerHTML = '<i class="fa-solid fa-plus"></i>';
      slotActivo.style.border = '2px dashed var(--gold)';

      const slotId = slotActivo.dataset.slotId;
      delete desgloseDeMuebles[slotId];
      actualizarDesgloseUI();

      modalBootstrap.hide();
      slotActivo = null;
    } else {
      const mueble = baseDeDatosMuebles.find(m => m.id === muebleId);
      if (mueble) mostrarPreview(mueble);
    }
  }

  // --- 13. FUNCIÓN: Mostrar preview del mueble seleccionado ---
  function mostrarPreview(mueble) {
    modalTitulo.textContent = mueble.nombre;
    modalCuerpoGrid.classList.add('hidden');
    modalPreview.classList.remove('hidden');
    btnVolverGrid.classList.remove('hidden');

    previewNombre.textContent = mueble.nombre;
    btnAddMueble.dataset.imgSlot       = mueble.imagen_slot;
    btnAddMueble.dataset.muebleId      = mueble.id;
    btnAddMueble.dataset.muebleNombre  = mueble.nombre;
    btnAddMueble.dataset.muebleAncho   = mueble.ancho_cm;
    btnAddMueble.dataset.muebleAlto    = mueble.alto_cm;

    carouselIndicators.innerHTML = '';
    carouselInner.innerHTML = '';

    mueble.preview_cf.forEach((imgUrl, index) => {
      const esActiva = index === 0 ? 'active' : '';
      carouselIndicators.innerHTML += `
        <button type="button" data-bs-target="#carousel-mueble" data-bs-slide-to="${index}"
                class="${esActiva}" ${esActiva ? 'aria-current="true"' : ''}></button>
      `;
      carouselInner.innerHTML += `
        <div class="carousel-item ${esActiva}">
          <img src="${imgUrl}" alt="Vista ${index + 1} de ${mueble.nombre}">
        </div>
      `;
    });
  }

  // --- 14. FUNCIÓN: Actualizar tabla de desglose ---
  function actualizarDesgloseUI() {
    listaDesgloseUI.innerHTML = '';
    const ids = Object.keys(desgloseDeMuebles);

    if (ids.length === 0) {
      listaDesgloseUI.innerHTML = `
        <tr>
          <td colspan="3" class="text-center text-muted">Aún no has añadido muebles.</td>
        </tr>
      `;
    } else {
      ids.forEach(slotId => {
        const m = desgloseDeMuebles[slotId];
        listaDesgloseUI.innerHTML += `
          <tr>
            <td><strong>${m.nombre}</strong></td>
            <td>${m.ancho}</td>
            <td>${m.alto}</td>
          </tr>
        `;
      });
    }
  }

  // --- 15. EVENTOS ---
  btnPequena.addEventListener('click', (e) => { e.preventDefault(); iniciarSimulador('pequena'); });
  btnGrande.addEventListener('click',  (e) => { e.preventDefault(); iniciarSimulador('grande'); });
  if (btnCocinaL) {
    btnCocinaL.addEventListener('click', (e) => { e.preventDefault(); iniciarSimulador('cocinaL'); });
  }

  btnExportar.addEventListener('click', () => { window.print(); });

  btnVolverGrid.addEventListener('click', () => { mostrarGridView(); });

  btnAddMueble.addEventListener('click', (e) => {
    const dataset   = e.currentTarget.dataset;
    const slotId    = slotActivo.dataset.slotId;

    desgloseDeMuebles[slotId] = {
      nombre: dataset.muebleNombre,
      ancho:  dataset.muebleAncho,
      alto:   dataset.muebleAlto
    };

    slotActivo.style.backgroundImage = `url(${dataset.imgSlot})`;
    slotActivo.innerHTML  = '';
    slotActivo.style.border = '1px solid var(--gold)';

    modalBootstrap.hide();
    e.currentTarget.blur();
    slotActivo = null;
    actualizarDesgloseUI();
  });

});