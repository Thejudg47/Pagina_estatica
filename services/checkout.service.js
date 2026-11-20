import { TIENDA_CONFIG } from "../config/tienda.config.js";
import { PricingService } from "./pricing.service.js";

export class CheckoutService {
  constructor() {
    this.pricing = new PricingService();
  }

  /**
   * Valida los datos del pedido y genera la URL de WhatsApp.
   * @param {import("../contracts/types.js").OrderRequestDTO} order
   * @returns {{ ok: boolean, error?: string, whatsappUrl?: string }}
   */
  buildWhatsAppOrder(order) {
    if (!order.items || order.items.length === 0) {
      return { ok: false, error: "Tu carrito está vacío." };
    }
    if (!order.nombreCliente || !order.nombreCliente.trim()) {
      return { ok: false, error: "Por favor escribe tu nombre completo." };
    }
    if (!order.fechaEntrega) {
      return { ok: false, error: "Selecciona una fecha de entrega." };
    }

    const lines = [
      `🌸 *NUEVO PEDIDO — ${TIENDA_CONFIG.nombre.toUpperCase()}* 🌸`,
      "",
      `👤 *Cliente:* ${order.nombreCliente.trim()}`,
      `📍 *Entrega:* ${order.zonaEnvio}`,
      `📅 *Fecha:* ${order.fechaEntrega}`,
      `⏰ *Horario:* ${order.horarioEntrega}`,
      "",
      "🛍️ *Detalle del Pedido:*",
    ];

    order.items.forEach((item) => {
      const lineTotal = this.pricing.formatCurrency(item.precioUnitario * item.cantidad);
      lines.push(`• ${item.cantidad}x ${item.nombre} (${lineTotal})`);
    });

    lines.push("");
    lines.push(`Subtotal: ${this.pricing.formatCurrency(order.subtotal)}`);
    lines.push(`Envío: ${this.pricing.formatCurrency(order.costoEnvio)}`);
    lines.push(`*TOTAL: ${this.pricing.formatCurrency(order.total)} ${TIENDA_CONFIG.moneda}*`);

    if (order.dedicatoria && order.dedicatoria.trim()) {
      lines.push("");
      lines.push("💌 *Mensaje para tarjeta:*");
      lines.push(`_"${order.dedicatoria.trim()}"_`);
    }

    const encodedMessage = encodeURIComponent(lines.join("\n"));
    const phone = TIENDA_CONFIG.whatsappNumero.replace(/\D/g, "");

    return {
      ok: true,
      whatsappUrl: `https://wa.me/${phone}?text=${encodedMessage}`,
    };
  }
}