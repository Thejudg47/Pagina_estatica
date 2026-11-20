import { TIENDA_CONFIG } from "../config/tienda.config.js";
import { PricingService } from "../services/pricing.service.js";

const pricing = new PricingService();

export function renderNavbar(totalArticulos) {
  const banner = TIENDA_CONFIG.bannerSuperior?.trim()
    ? `<div class="top-banner">${TIENDA_CONFIG.bannerSuperior}</div>`
    : "";

  const badge = totalArticulos > 0
    ? `<span class="badge-count">${totalArticulos}</span>`
    : "";

  return `
    <header class="navbar-sticky">
      ${banner}
      <div class="navbar-inner">
        <a href="#top" class="brand-link" data-action="go-home">
          <div class="brand-icon"><i data-lucide="flower-2"></i></div>
          <div>
            <div class="brand-title font-editorial">${TIENDA_CONFIG.nombre}</div>
            <div class="brand-subtitle">${TIENDA_CONFIG.subtitulo}</div>
          </div>
        </a>

        <div class="nav-actions">
          <nav class="nav-links">
            <a href="#catalogo">Catálogo</a>
            <a href="#contacto">Ubicación y Horarios</a>
          </nav>

          <button class="btn-primary" data-action="toggle-cart">
            <i data-lucide="shopping-bag" style="width:18px;height:18px;"></i>
            <span>Mi Pedido</span>
            ${badge}
          </button>
        </div>
      </div>
    </header>
  `;
}

export function renderHero(categorias, categoriaActiva, busqueda) {
  const pillsHtml = categorias
    .map(
      (cat) => `
      <button
        class="cat-pill ${cat === categoriaActiva ? "active" : ""}"
        data-action="select-category"
        data-category="${cat}"
      >
        ${cat}
      </button>
    `
    )
    .join("");

  return `
    <div class="hero-section" id="top">
      <div class="hero-inner">
        <span class="hero-pill">CATÁLOGO EN LÍNEA</span>
        <h1 class="hero-title">${TIENDA_CONFIG.nombre}</h1>
        <p class="hero-subtitle">${TIENDA_CONFIG.eslogan}</p>

        <div class="search-box">
          <i data-lucide="search"></i>
          <input
            type="text"
            id="search-input"
            class="search-input"
            placeholder="Buscar ramos, girasoles, cajas..."
            value="${busqueda}"
          />
        </div>

        <div class="category-pills">${pillsHtml}</div>
      </div>
    </div>
  `;
}

export function renderCatalog(productos, cargando) {
  if (cargando) {
    return `<div class="empty-state"><p>Cargando arreglos florales...</p></div>`;
  }

  if (productos.length === 0) {
    return `
      <div class="empty-state">
        <i data-lucide="search-x" style="width:36px;height:36px;color:var(--color-primario);"></i>
        <h3>No encontramos arreglos con esa búsqueda</h3>
        <p style="color:var(--texto-gris);font-size:14px;">Intenta con otro término o explora todas nuestras categorías disponibles.</p>
        <button class="btn-primary" data-action="clear-filters" style="margin-top:8px;">
          Ver todo el catálogo
        </button>
      </div>
    `;
  }

  const cardsHtml = productos
    .map((p) => {
      const promoBadge = p.etiqueta
        ? `<span class="card-badge-promo">${p.etiqueta}</span>`
        : "";
      const photosBadge =
        p.imagenes.length > 1
          ? `<span class="card-badge-photos"><i data-lucide="images" style="width:13px;height:13px;"></i> ${p.imagenes.length} fotos</span>`
          : "";

      return `
        <article class="product-card">
          <div class="card-image-wrap" data-action="open-modal" data-id="${p.id}">
            <img src="${p.imagenes[0]}" alt="${p.nombre}" referrerpolicy="no-referrer" onerror="this.src='${TIENDA_CONFIG.imagenFallback}'" />
            ${promoBadge}
            ${photosBadge}
          </div>
          <div class="card-body">
            <span class="card-category">${p.categoria}</span>
            <h2 class="card-title" data-action="open-modal" data-id="${p.id}">${p.nombre}</h2>
            <p class="card-desc">${p.descripcion}</p>
            <div class="card-footer">
              <div>
                <span class="price-label">Precio</span>
                <span class="price-value">${pricing.formatCurrency(p.precio)}</span>
                <span class="price-currency">${TIENDA_CONFIG.moneda}</span>
              </div>
              <button class="btn-primary" data-action="add-to-cart" data-id="${p.id}">
                <i data-lucide="shopping-bag" style="width:16px;height:16px;"></i>
                Agregar
              </button>
            </div>
          </div>
        </article>
      `;
    })
    .join("");

  return `<div class="products-grid">${cardsHtml}</div>`;
}

export function renderCartDrawer(state, totales) {
  if (!state.carritoAbierto) return "";

  const zonasOptions = Object.keys(TIENDA_CONFIG.zonasEnvio)
    .map(
      (z) =>
        `<option value="${z}" ${z === state.zonaEnvio ? "selected" : ""}>${z} (${pricing.formatCurrency(
          TIENDA_CONFIG.zonasEnvio[z]
        )})</option>`
    )
    .join("");

  const horariosOptions = TIENDA_CONFIG.horariosEntrega
    .map(
      (h) =>
        `<option value="${h}" ${h === state.horarioEntrega ? "selected" : ""}>${h}</option>`
    )
    .join("");

  const itemsHtml = state.carrito
    .map(
      (item) => `
      <div class="cart-item">
        <div>
          <div style="font-weight:700;font-size:14px;">${item.nombre}</div>
          <div style="font-size:12px;color:var(--texto-gris);">${pricing.formatCurrency(item.precioUnitario)} c/u</div>
        </div>
        <div class="qty-controls">
          <button class="qty-btn" data-action="dec-qty" data-id="${item.productId}">-</button>
          <span style="font-weight:700;min-width:18px;text-align:center;">${item.cantidad}</span>
          <button class="qty-btn" data-action="inc-qty" data-id="${item.productId}">+</button>
          <button class="icon-btn" data-action="remove-item" data-id="${item.productId}" title="Eliminar">
            <i data-lucide="trash-2" style="width:15px;height:15px;color:#dc2626;"></i>
          </button>
        </div>
      </div>
    `
    )
    .join("");

  const previewHtml = state.dedicatoria.trim()
    ? `
      <div class="dedication-preview">
        <div style="font-size:11px;font-weight:700;letter-spacing:0.08em;color:var(--color-primario-oscuro);">
          ✨ VISTA PREVIA DE TU TARJETA
        </div>
        <p class="dedication-quote">“${state.dedicatoria}”</p>
        <div style="font-size:12px;color:#8c7f77;font-family:'Playfair Display',serif;">— ${TIENDA_CONFIG.nombre}</div>
      </div>
    `
    : "";

  const bodyHtml =
    state.carrito.length === 0
      ? `
        <div style="text-align:center;padding:64px 0;color:var(--texto-gris);">
          <i data-lucide="shopping-bag" style="width:40px;height:40px;margin-bottom:8px;"></i>
          <p>Tu carrito está vacío</p>
        </div>
      `
      : `
        <div>${itemsHtml}</div>

        <div class="form-group">
          <strong style="font-size:15px;">Datos de Entrega</strong>
          <input type="text" class="form-input" id="input-cliente" placeholder="Tu nombre completo *" value="${state.nombreCliente}" />
          <select class="form-select" id="select-zona">${zonasOptions}</select>
          <div class="form-row">
            <input type="date" class="form-input" id="input-fecha" value="${state.fechaEntrega}" />
            <select class="form-select" id="select-horario">${horariosOptions}</select>
          </div>
          <textarea class="form-textarea" id="input-dedicatoria" rows="3" placeholder="Mensaje para la tarjeta de dedicatoria (opcional)...">${state.dedicatoria}</textarea>
          ${previewHtml}
        </div>

        <div style="display:flex;flex-direction:column;gap:6px;padding-top:8px;border-top:1px solid var(--borde-suave);">
          <div style="display:flex;justify-content:space-between;color:var(--texto-gris);font-size:14px;">
            <span>Subtotal:</span><span>${pricing.formatCurrency(totales.subtotal)}</span>
          </div>
          <div style="display:flex;justify-content:space-between;color:var(--texto-gris);font-size:14px;">
            <span>Envío:</span><span>${pricing.formatCurrency(totales.costoEnvio)}</span>
          </div>
          <div style="display:flex;justify-content:space-between;font-weight:700;font-size:18px;margin-top:4px;">
            <span>Total:</span>
            <span style="color:var(--color-primario-oscuro);">${pricing.formatCurrency(totales.total)} ${TIENDA_CONFIG.moneda}</span>
          </div>
        </div>

        ${
          state.errorCheckout
            ? `<div style="background:#fef2f2;color:#b91c1c;padding:10px;border-radius:8px;font-size:13px;">${state.errorCheckout}</div>`
            : ""
        }

        <button class="btn-whatsapp" data-action="checkout-whatsapp">
          <i data-lucide="send" style="width:18px;height:18px;"></i>
          Enviar Pedido por WhatsApp
        </button>
      `;

  return `
    <div class="drawer-backdrop" data-action="toggle-cart"></div>
    <aside class="drawer-panel">
      <div class="drawer-header">
        <h2 style="font-size:22px;">Tu Pedido</h2>
        <button class="icon-btn" data-action="toggle-cart"><i data-lucide="x"></i></button>
      </div>
      ${bodyHtml}
    </aside>
  `;
}

export function renderProductModal(producto, imagenActivaIdx) {
  if (!producto) return "";

  const imgActual = producto.imagenes[imagenActivaIdx] || producto.imagenes[0];
  const thumbsHtml =
    producto.imagenes.length > 1
      ? `<div class="modal-thumbs">${producto.imagenes
          .map(
            (img, idx) => `
            <img
              src="${img}"
              class="modal-thumb ${idx === imagenActivaIdx ? "active" : ""}"
              referrerpolicy="no-referrer"
              data-action="select-modal-img"
              data-index="${idx}"
              onerror="this.src='${TIENDA_CONFIG.imagenFallback}'"
            />`
          )
          .join("")}</div>`
      : "";

  return `
    <div class="modal-backdrop" data-action="close-modal-backdrop">
      <div class="modal-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
          <span class="card-category">${producto.categoria}</span>
          <button class="icon-btn" data-action="close-modal"><i data-lucide="x"></i></button>
        </div>

        <img src="${imgActual}" class="modal-main-img" referrerpolicy="no-referrer" onerror="this.src='${TIENDA_CONFIG.imagenFallback}'" />
        ${thumbsHtml}

        <div style="margin-top:18px;display:flex;flex-direction:column;gap:10px;">
          <h2 style="font-size:28px;">${producto.nombre}</h2>
          <p style="color:var(--texto-gris);line-height:1.6;">${producto.descripcion}</p>
          <div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;padding-top:14px;border-top:1px solid var(--borde-suave);">
            <div>
              <span class="price-label">Precio</span>
              <span class="price-value" style="font-size:24px;">${pricing.formatCurrency(producto.precio)}</span>
              <span class="price-currency">${TIENDA_CONFIG.moneda}</span>
            </div>
            <button class="btn-primary" data-action="add-to-cart-modal" data-id="${producto.id}" style="padding:12px 24px;">
              <i data-lucide="shopping-bag" style="width:18px;height:18px;"></i>
              Agregar al Pedido
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
}

export function renderFooter() {
  const phone = TIENDA_CONFIG.whatsappNumero.replace(/\D/g, "");
  const waDirect = `https://wa.me/${phone}?text=${encodeURIComponent(
    `Hola ${TIENDA_CONFIG.nombre}, me gustaría información sobre un arreglo personalizado.`
  )}`;

  const redes = [];
  if (TIENDA_CONFIG.redes?.instagram) {
    redes.push(`<a href="${TIENDA_CONFIG.redes.instagram}" target="_blank" class="cat-pill" style="text-decoration:none;">Instagram</a>`);
  }
  if (TIENDA_CONFIG.redes?.facebook) {
    redes.push(`<a href="${TIENDA_CONFIG.redes.facebook}" target="_blank" class="cat-pill" style="text-decoration:none;">Facebook</a>`);
  }

  return `
    <div class="site-footer">
      <div class="footer-inner">
        <div class="footer-grid">
          <div class="footer-col">
            <div style="display:flex;align-items:center;gap:8px;">
              <i data-lucide="flower-2" style="color:var(--color-primario);"></i>
              <h3 style="font-size:20px;">${TIENDA_CONFIG.nombre}</h3>
            </div>
            <p style="color:var(--texto-gris);font-size:14px;line-height:1.6;">${TIENDA_CONFIG.eslogan}</p>
            <div style="display:flex;gap:8px;margin-top:4px;">${redes.join("")}</div>
          </div>

          <div class="footer-col">
            <strong style="font-size:15px;">Visítanos</strong>
            <p style="color:var(--texto-gris);font-size:14px;line-height:1.6;">📍 ${TIENDA_CONFIG.direccion}</p>
            <p style="color:var(--texto-gris);font-size:14px;line-height:1.6;">🕒 ${TIENDA_CONFIG.horarioAtencion}</p>
          </div>

          <div class="footer-col">
            <strong style="font-size:15px;">¿Buscas un arreglo personalizado?</strong>
            <p style="color:var(--texto-gris);font-size:14px;line-height:1.6;">Escríbenos directo y te ayudamos a armar el detalle ideal.</p>
            <div>
              <a href="${waDirect}" target="_blank" class="btn-whatsapp" style="text-decoration:none;display:inline-flex;width:auto;padding:12px 20px;">
                Chatear por WhatsApp
              </a>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          © 2026 ${TIENDA_CONFIG.nombre}. Todos los derechos reservados.
        </div>
      </div>
    </div>
  `;
}