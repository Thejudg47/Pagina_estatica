import { TIENDA_CONFIG } from "./config/tienda.config.js";
import { createCartItemDTO } from "./contracts/types.js";
import { CatalogService } from "./services/catalog.service.js";
import { PricingService } from "./services/pricing.service.js";
import { CheckoutService } from "./services/checkout.service.js";
import {
  renderNavbar,
  renderHero,
  renderCatalog,
  renderCartDrawer,
  renderProductModal,
  renderFooter,
} from "./ui/components.js";

const catalogService = new CatalogService();
const pricingService = new PricingService();
const checkoutService = new CheckoutService();

const STORAGE_KEY = "floreria_cart_v1";

const state = {
  productos: [],
  cargando: true,
  categoriaActiva: "Todos",
  busqueda: "",
  carrito: JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"),
  carritoAbierto: false,
  productoModal: null,
  imagenModalIdx: 0,
  nombreCliente: "",
  zonaEnvio: Object.keys(TIENDA_CONFIG.zonasEnvio)[0],
  fechaEntrega: "",
  horarioEntrega: TIENDA_CONFIG.horariosEntrega[0],
  dedicatoria: "",
  errorCheckout: "",
  varianteModalIdx: 0,
};

function applyThemeConfig() {
  document.title = TIENDA_CONFIG.nombre;
  const root = document.documentElement;
  root.style.setProperty("--color-primario", TIENDA_CONFIG.colorPrimario);
  root.style.setProperty("--color-primario-oscuro", TIENDA_CONFIG.colorPrimarioOscuro);
  root.style.setProperty("--color-primario-suave", TIENDA_CONFIG.colorPrimarioSuave);
}

function saveCart() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.carrito));
}

function showToast(message) {
  const container = document.getElementById("app-toast-container");
  const toast = document.createElement("div");
  toast.className = "toast-item";
  toast.innerHTML = `<span>🌸</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 2600);
}

function getFilteredProducts() {
  return state.productos.filter((p) => {
    const matchCat =
      state.categoriaActiva === "Todos" || p.categoria === state.categoriaActiva;
    const q = state.busqueda.toLowerCase().trim();
    const matchSearch =
      !q ||
      p.nombre.toLowerCase().includes(q) ||
      p.descripcion.toLowerCase().includes(q) ||
      p.categoria.toLowerCase().includes(q);
    return matchCat && matchSearch;
  });
}

function getCategories() {
  const cats = new Set(state.productos.map((p) => p.categoria).filter(Boolean));
  return ["Todos", ...Array.from(cats)];
}

function renderAll() {
  const totalArticulos = state.carrito.reduce((sum, i) => sum + i.cantidad, 0);
  const totales = pricingService.calculateTotals(state.carrito, state.zonaEnvio);

  document.getElementById("app-navbar").innerHTML = renderNavbar(totalArticulos);
  document.getElementById("app-hero").innerHTML = renderHero(
    getCategories(),
    state.categoriaActiva,
    state.busqueda
  );
  document.getElementById("catalogo").innerHTML = renderCatalog(
    getFilteredProducts(),
    state.cargando
  );
  document.getElementById("contacto").innerHTML = renderFooter();
  document.getElementById("app-cart-drawer").innerHTML = renderCartDrawer(state, totales);
  document.getElementById("app-product-modal").innerHTML = renderProductModal(
    state.productoModal,
    state.imagenModalIdx,
    state.varianteModalIdx,
  );

  // Re-inicializar iconos de Lucide tras cada render
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// --- Delegación global de eventos ---
document.addEventListener("click", (e) => {
  const target = e.target.closest("[data-action]");
  if (!target) return;

  const action = target.dataset.action;
  const id = target.dataset.id;

  if (action === "go-home" || action === "clear-filters") {
    state.categoriaActiva = "Todos";
    state.busqueda = "";
    state.carritoAbierto = false;
    state.productoModal = null;
    renderAll();
  }

  if (action === "toggle-cart") {
    state.carritoAbierto = !state.carritoAbierto;
    state.errorCheckout = "";
    renderAll();
  }

  if (action === "select-category") {
    state.categoriaActiva = target.dataset.category;
    renderAll();
  }

  if (action === "add-to-cart" || action === "add-to-cart-modal") {
    const prod = state.productos.find((p) => p.id === id);
    if (!prod) return;

    const hasVariants = prod.variantes && prod.variantes.length > 0;
    const selectedVariant = hasVariants
      ? prod.variantes[action === "add-to-cart-modal" ? state.varianteModalIdx : 0]
      : null;

    const newItem = createCartItemDTO(prod, 1, selectedVariant);
    const existing = state.carrito.find((i) => i.cartKey === newItem.cartKey);

    if (existing) {
      existing.cantidad += 1;
    } else {
      state.carrito.push(newItem);
    }

    saveCart();
    if (action === "add-to-cart-modal") state.productoModal = null;
    renderAll();
    showToast(`¡${newItem.nombre} agregado a tu pedido!`);
  }

  if (action === "inc-qty") {
    const key = target.dataset.key;
    const item = state.carrito.find((i) => i.cartKey === key);
    if (item) item.cantidad += 1;
    saveCart();
    renderAll();
  }

  if (action === "dec-qty") {
    const key = target.dataset.key;
    const idx = state.carrito.findIndex((i) => i.cartKey === key);
    if (idx !== -1) {
      if (state.carrito[idx].cantidad > 1) {
        state.carrito[idx].cantidad -= 1;
      } else {
        state.carrito.splice(idx, 1);
      }
      saveCart();
      renderAll();
    }
  }

  if (action === "remove-item") {
    const key = target.dataset.key;
    state.carrito = state.carrito.filter((i) => i.cartKey !== key);
    saveCart();
    renderAll();
  }

  if (action === "open-modal") {
    state.productoModal = state.productos.find((p) => p.id === id) || null;
    state.imagenModalIdx = 0;
    state.varianteModalIdx = 0;
    renderAll();
  }

  if (action === "close-modal") {
    state.productoModal = null;
    renderAll();
  }

  if (action === "close-modal-backdrop" && e.target.classList.contains("modal-backdrop")) {
    state.productoModal = null;
    renderAll();
  }

  if (action === "select-modal-img") {
    state.imagenModalIdx = Number(target.dataset.index || 0);
    renderAll();
  }

  if (action === "select-variant") {
    state.varianteModalIdx = Number(target.dataset.index || 0);
    renderAll();
  }


  if (action === "checkout-whatsapp") {
    const totales = pricingService.calculateTotals(state.carrito, state.zonaEnvio);
    const res = checkoutService.buildWhatsAppOrder({
      nombreCliente: state.nombreCliente,
      zonaEnvio: state.zonaEnvio,
      fechaEntrega: state.fechaEntrega,
      horarioEntrega: state.horarioEntrega,
      dedicatoria: state.dedicatoria,
      items: state.carrito,
      subtotal: totales.subtotal,
      costoEnvio: totales.costoEnvio,
      total: totales.total,
    });

    if (!res.ok) {
      state.errorCheckout = res.error;
      renderAll();
    } else {
      state.errorCheckout = "";
      window.open(res.whatsappUrl, "_blank");
    }
  }
});

// --- Inputs reactivos ---
document.addEventListener("input", (e) => {
  if (e.target.id === "search-input") {
    const cursorPos = e.target.selectionStart;
    state.busqueda = e.target.value;
    renderAll();
    const inputAfter = document.getElementById("search-input");
    if (inputAfter) {
      inputAfter.focus();
      inputAfter.setSelectionRange(cursorPos, cursorPos);
    }
  }

  if (e.target.id === "input-cliente") state.nombreCliente = e.target.value;
  if (e.target.id === "input-fecha") state.fechaEntrega = e.target.value;

  if (e.target.id === "input-dedicatoria") {
    const cursorPos = e.target.selectionStart;
    state.dedicatoria = e.target.value;
    renderAll();
    const areaAfter = document.getElementById("input-dedicatoria");
    if (areaAfter) {
      areaAfter.focus();
      areaAfter.setSelectionRange(cursorPos, cursorPos);
    }
  }
});

document.addEventListener("change", (e) => {
  if (e.target.id === "select-zona") {
    state.zonaEnvio = e.target.value;
    renderAll();
  }
  if (e.target.id === "select-horario") {
    state.horarioEntrega = e.target.value;
  }
});

// --- Inicialización ---
async function init() {
  applyThemeConfig();
  renderAll();
  state.productos = await catalogService.getAllProducts();
  state.cargando = false;
  renderAll();
}

init();