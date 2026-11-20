import { TIENDA_CONFIG } from "../config/tienda.config.js";

export class PricingService {
  /**
   * Calcula subtotal, costo de envío y total final.
   * @param {import("../contracts/types.js").CartItemDTO[]} items
   * @param {string} zonaEnvio
   */
  calculateTotals(items, zonaEnvio) {
    const subtotal = items.reduce(
      (acc, item) => acc + item.precioUnitario * item.cantidad,
      0
    );

    const costoEnvio =
      subtotal > 0 ? Number(TIENDA_CONFIG.zonasEnvio[zonaEnvio] ?? 0) : 0;

    return {
      subtotal,
      costoEnvio,
      total: subtotal + costoEnvio,
    };
  }

  formatCurrency(amount) {
    return `$${Number(amount || 0).toLocaleString("es-MX", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;
  }
}