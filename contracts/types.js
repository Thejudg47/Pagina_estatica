/**
 * Contratos de datos (DTOs) de la arquitectura SOA.
 * Garantizan integridad estructural entre servicios y la capa visual.
 */

/**
 * @typedef {Object} ProductoDTO
 * @property {string} id
 * @property {string} nombre
 * @property {string} categoria
 * @property {number} precio
 * @property {string} descripcion
 * @property {string[]} imagenes
 * @property {string} etiqueta
 * @property {boolean} disponible
 */

/**
 * Crea y normaliza un ProductDTO válido.
 * @param {Partial<ProductoDTO>} raw
 * @returns {ProductoDTO}
 */
export function createProductoDTO(raw) {
  return {
    id: String(raw.id || "").trim(),
    nombre: String(raw.nombre || "Arreglo sin nombre").trim(),
    categoria: String(raw.categoria || "General").trim(),
    precio: Number.isFinite(Number(raw.precio)) ? Number(raw.precio) : 0,
    descripcion: String(raw.descripcion || "").trim(),
    imagenes: Array.isArray(raw.imagenes) && raw.imagenes.length > 0
      ? raw.imagenes
      : ["./assets/arreglos/placeholder.png"],
    etiqueta: String(raw.etiqueta || "").trim(),
    disponible: raw.disponible !== false,
  };
}

/**
 * @typedef {Object} CartItemDTO
 * @property {string} productId
 * @property {string} nombre
 * @property {number} precioUnitario
 * @property {number} cantidad
 */

/**
 * Crea un ítem normalizado para el carrito.
 * @param {ProductoDTO} producto
 * @param {number} cantidad
 * @returns {CartItemDTO}
 */
export function createCartItemDTO(producto, cantidad = 1) {
  return {
    productId: producto.id,
    nombre: producto.nombre,
    precioUnitario: producto.precio,
    cantidad: Math.max(1, Math.floor(cantidad)),
  };
}

/**
 * @typedef {Object} OrderRequestDTO
 * @property {string} nombreCliente
 * @property {string} zonaEnvio
 * @property {string} fechaEntrega
 * @property {string} horarioEntrega
 * @property {string} dedicatoria
 * @property {CartItemDTO[]} items
 * @property {number} subtotal
 * @property {number} costoEnvio
 * @property {number} total
 */