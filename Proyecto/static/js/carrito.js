document.addEventListener('DOMContentLoaded', function() {
    // Variables
    let carrito = [];
    const carritoLista = document.getElementById('carrito-lista');
    const totalElemento = document.getElementById('total-precio');
    const carritoVacio = document.getElementById('carrito-vacio');
    const carritoModal = new bootstrap.Modal(document.getElementById('carritoModal'));
    const pedidoForm = document.getElementById('pedido-form');

    // 1. Abrir modal al hacer clic en el icono del carrito
    document.querySelector('.boton_carrito').addEventListener('click', function() {
        actualizarCarrito();
        carritoModal.show();
    });

    // 2. Función para agregar productos al carrito
    function agregarAlCarrito(event) {
        event.preventDefault();
        const card = event.target.closest('.card');

        const productoInfo = {
            id: card.dataset.id,
            nombre: card.querySelector('.card-title').textContent,
            precio: parseFloat(card.querySelector('.text-danger').textContent.replace('Precio: €', '')),
            cantidad: 1
        };

        const productoExistente = carrito.find(item => item.id === productoInfo.id);

        if (productoExistente) {
            productoExistente.cantidad++;
        } else {
            carrito.push(productoInfo);
        }

        mostrarNotificacion(`€${productoInfo.nombre} añadido al carrito`);
        actualizarCarrito();
    }

    // 3. Actualizar visualización del carrito
    function actualizarCarrito() {
        carritoLista.innerHTML = '';
        let total = 0;

        if (carrito.length === 0) {
            carritoVacio.style.display = 'block';
        } else {
            carritoVacio.style.display = 'none';
            carrito.forEach(producto => {
                const item = document.createElement('div');
                item.classList.add('item-carrito');
                item.innerHTML = `
                    <div>
                        <h6>${producto.nombre}</h6>
                        <p class="mb-0">€${producto.precio.toFixed(2)}</p>
                    </div>
                    <div class="d-flex align-items-center">
                        <div class="controles-cantidad">
                            <button class="disminuir" data-id="${producto.id}">-</button>
                            <span>${producto.cantidad}</span>
                            <button class="aumentar" data-id="${producto.id}">+</button>
                        </div>
                        <button class="btn-eliminar" data-id="${producto.id}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                `;
                carritoLista.appendChild(item);
                total += producto.precio * producto.cantidad;
            });
        }

        totalElemento.textContent = `€${total.toFixed(2)}`;
        agregarEventosBotones();
    }

    // 4. Funciones para modificar cantidades
    function agregarEventosBotones() {
        document.querySelectorAll('.disminuir').forEach(boton => {
            boton.addEventListener('click', function() {
                const id = this.dataset.id;
                const producto = carrito.find(item => item.id === id);
                producto.cantidad > 1 ? producto.cantidad-- : carrito = carrito.filter(item => item.id !== id);
                actualizarCarrito();
            });
        });

        document.querySelectorAll('.aumentar').forEach(boton => {
            boton.addEventListener('click', function() {
                const id = this.dataset.id;
                carrito.find(item => item.id === id).cantidad++;
                actualizarCarrito();
            });
        });

        document.querySelectorAll('.btn-eliminar').forEach(boton => {
            boton.addEventListener('click', function() {
                carrito = carrito.filter(item => item.id !== this.dataset.id);
                actualizarCarrito();
            });
        });
    }

    // 5. Enviar pedido al servidor (CON LA MODIFICACIÓN SOLICITADA)
    pedidoForm.addEventListener('submit', function(e) {
        e.preventDefault();

        if (carrito.length === 0) {
            alert('El carrito está vacío');
            return;
        }

        if (!confirm('¿Confirmar pedido?')) return;

        // Mostrar loader (modificación solicitada)
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML; // Guardar texto original
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
        submitBtn.disabled = true;

        // Crear input oculto con datos del carrito
        let inputCarrito = document.createElement('input');
        inputCarrito.type = 'hidden';
        inputCarrito.name = 'carrito';
        inputCarrito.value = JSON.stringify(carrito);
        this.appendChild(inputCarrito);

        // Enviar formulario
        this.submit();

        // Opcional: Restaurar botón si hay error (se ejecutaría si el submit falla)
        setTimeout(() => {
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }, 5000);
    });

    // 6. Notificación estilo "toast"
    function mostrarNotificacion(mensaje) {
        const notificacion = document.createElement('div');
        notificacion.className = 'position-fixed bottom-0 end-0 p-3';
        notificacion.style.zIndex = '1100';
        notificacion.innerHTML = `
            <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header" style="background-color: #E0B5C6; color: white;">
                    <strong class="me-auto">Carrito</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">${mensaje}</div>
            </div>
        `;
        document.body.appendChild(notificacion);
        setTimeout(() => notificacion.remove(), 3000);
    }

    // 7. Eventos para botones "Añadir al carrito"
    document.querySelectorAll('.btn_custom').forEach(boton => {
        boton.addEventListener('click', agregarAlCarrito);
    });
});