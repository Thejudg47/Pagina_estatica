from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class CartItemDTO(BaseModel):
    product_id: str
    nombre: str
    precio_unitario: float
    cantidad: int

class OrderRequestDTO(BaseModel):
    items: List[CartItemDTO]
    zona_envio: str
    costo_envio: float
    fecha_entrega: str
    horario_entrega: str
    dedicatoria: str = ""
    nombre_cliente: str
    subtotal: float
    total: float

class ICheckoutService(ABC):
    """Contrato para procesar el cierre de venta (WhatsApp, Stripe, MercadoPago)."""

    @abstractmethod
    def generate_checkout_action(self, order: OrderRequestDTO) -> str:
        """Retorna una URL de redirección (ej. link de WhatsApp o pasarela de pago)."""
        pass