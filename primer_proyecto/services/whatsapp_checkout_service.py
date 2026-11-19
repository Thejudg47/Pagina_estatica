import urllib.parse
from ..contracts.checkout_contract import ICheckoutService, OrderRequestDTO

class WhatsAppCheckoutService(ICheckoutService):
    """Adaptador de salida que transforma una orden en un mensaje formateado de WhatsApp."""

    def __init__(self, telefono_destino: str, nombre_tienda: str, 
                 moneda: str = "MXN"):
        # Limpiamos espacios o simbolos por seguridad
        self._telefono = "".join(filter(str.isdigit, telefono_destino))
        self._nombre_tienda = nombre_tienda
        self._moneda = moneda

    def generate_checkout_action(self, order: OrderRequestDTO) -> str:
        lineas_productos = "\n".join(
            [
                f"• {item.cantidad}x {item.nombre} (${item.precio_unitario * item.cantidad:,.2f})"
                for item in order.items
            ]
        )

        bloque_dedicatoria = (
            f"\n*Dedicatoria:* \"{order.dedicatoria.strip()}\""
            if order.dedicatoria.strip()
            else "\n*Dedicatoria:* Sin mensaje"
        )

        mensaje = (
            f"Hola *{self._nombre_tienda}*, me gustaría realizar el siguiente pedido:\n\n"
            f"*Cliente:* {order.nombre_cliente}\n"
            f"*Productos:*\n{lineas_productos}\n\n"
            f"*Entrega:* {order.zona_envio}\n"
            f"*Fecha y horario:* {order.fecha_entrega} ({order.horario_entrega})"
            f"{bloque_dedicatoria}\n\n"
            f"Subtotal: ${order.subtotal:,.2f} {self._moneda}\n"
            f"Envío: ${order.costo_envio:,.2f} {self._moneda}\n"
            f"*Total a pagar: ${order.total:,.2f} {self._moneda}*"
        )

        texto_codificado = urllib.parse.quote(mensaje)
        return f"https://wa.me/{self._telefono}?text={texto_codificado}"