/**
 * Contratos de datos (DTOs) de la arquitectura SOA.
 * Garantizan integridad estructural entre servicios y la capa visual.
 */

/**
 * @typedef {Object} ProductVariantDTO
 * @property {string} nombre
 * @property {number} precio
 */

/**
 * @typedef {Object} ProductDTO
 * @property {string} id
 * @property {string} nombre
 * @property {string} categoria
 * @property {number} precio
 * @property {string} descripcion
 * @property {string[]} imagenes
 * @property {string} etiqueta
 * @property {boolean} disponible
 * @property {ProductVariantDTO[]} variantes
 */

/**
 * Crea y normaliza un ProductDTO válido.
 * @param {Partial<ProductDTO>} raw
 * @returns {ProductDTO}
 */
export function createProductDTO(raw) {
  const variantes = Array.isArray(raw.variantes) ? raw.variantes : [];
  const precioBase = Number.isFinite(Number(raw.precio)) ? Number(raw.precio) : 0;
  // Si hay variantes, el precio base de referencia será el de la primera variante si precio es 0
  const precioFinal =
    variantes.length > 0 && precioBase <= 0 ? variantes[0].precio : precioBase;

  return {
    id: String(raw.id || "").trim(),
    nombre: String(raw.nombre || "Arreglo sin nombre").trim(),
    categoria: String(raw.categoria || "General").trim(),
    precio: precioFinal,
    descripcion: String(raw.descripcion || "").trim(),
    imagenes:
      Array.isArray(raw.imagenes) && raw.imagenes.length > 0
        ? raw.imagenes
        : ["./assets/arreglos/placeholder.png"],
    etiqueta: String(raw.etiqueta || "").trim(),
    disponible: raw.disponible !== false,
    variantes,
  };
}

/**
 * @typedef {Object} CartItemDTO
 * @property {string} cartKey        // Clave única: "id" o "id::variante"
 * @property {string} productId
 * @property {string} nombre
 * @property {string} variante
 * @property {number} precioUnitario
 * @property {number} cantidad
 */

/**
 * Crea un ítem normalizado para el carrito.
 * @param {ProductDTO} producto
 * @param {number} cantidad
 * @param {ProductVariantDTO | null} varianteObj
 * @returns {CartItemDTO}
 */
export function createCartItemDTO(producto, cantidad = 1, varianteObj = null) {
  const varianteNombre = varianteObj ? varianteObj.nombre : "";
  const precioUnitario = varianteObj ? varianteObj.precio : producto.precio;
  const cartKey = varianteNombre ? `${producto.id}::${varianteNombre}` : producto.id;

  return {
    cartKey,
    productId: producto.id,
    nombre: varianteNombre ? `${producto.nombre} (${varianteNombre})` : producto.nombre,
    variante: varianteNombre,
    precioUnitario,
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