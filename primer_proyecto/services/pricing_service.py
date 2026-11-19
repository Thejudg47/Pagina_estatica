from typing import List, Dict, Tuple
from ..contracts.checkout_contract import CartItemDTO

class PricingService:
    """Servicio desacoplado para cálculo de subtotales, envíos y totales."""

    def __init__(self, zonas_envio: Dict[str, float]):
        self._zonas_envio = zonas_envio

    def calculate_subtotal(self, items: List[CartItemDTO]) -> float:
        return round(sum(item.precio_unitario * item.cantidad for item in items), 2)

    def get_shipping_cost(self, zona: str) -> float:
        return round(float(self._zonas_envio.get(zona, 0.0)), 2)

    def calculate_totals(
            self, items: List[CartItemDTO], zona_envio: str
    ) -> Tuple[float, float, float]:
        """Retorna (subtotal, costo_envio, total)."""
        subtotal = self.calculate_subtotal(items)
        envio = self.get_shipping_cost(zona_envio) if subtotal > 0 else 0.0
        total = round(subtotal + envio, 2)
        return subtotal, envio, total