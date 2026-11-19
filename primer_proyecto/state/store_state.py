import reflex as rx
from typing import List, Dict
from ..config_cliente import TIENDA_CONFIG
from ..data_ejemplo import PRODUCTOS_DEMO
from ..contracts.catalog_contract import ProductoDTO
from ..contracts.checkout_contract import CartItemDTO, OrderRequestDTO
from ..services.catalog_service import GoogleSheetsCatalogService
from ..services.pricing_service import PricingService
from ..services.whatsapp_checkout_service import WhatsAppCheckoutService

# --- INYECCIÓN DE DEPENDENCIAS SOA ---
# Instanciamos los servicios una sola vez usando la configuración del cliente.
# Si mañana cambias WhatsApp por Stripe, solo cambias la clase aquí.
catalog_service = GoogleSheetsCatalogService(
    csv_url=TIENDA_CONFIG.get("google_sheets_csv_url", ""),
    fallback_products=PRODUCTOS_DEMO,
)

pricing_service = PricingService(
    zonas_envio=TIENDA_CONFIG["zonas_envio"]
)

checkout_service = WhatsAppCheckoutService(
    telefono_destino=TIENDA_CONFIG["telefono_whatsapp"],
    nombre_tienda=TIENDA_CONFIG["nombre"],
    moneda=TIENDA_CONFIG["moneda"],
)

class StoreState(rx.State):
    """Orquestador de estado de la tienda (conecta UI con los servicios SOA)."""

    # Estado del Catálogo
    productos: List[ProductoDTO] = []
    categorias: List[str] = ["Todos"]
    categoria_activa: str = "Todos"
    busqueda: str = ""

    # Estado del Carrito (guardamos diccionario {product_id: CartItemDTO})
    carrito: Dict[str, CartItemDTO] = {}
    carrito_abierto: bool = False

    # Estado de Vista Rápida / Galería Multi-imagen
    producto_detalle: ProductoDTO | None = None
    foto_activa_idx: int = 0

    def abrir_detalle(self, producto: ProductoDTO):
        self.producto_detalle = producto
        self.foto_activa_idx = 0

    def cerrar_detalle(self):
        self.producto_detalle = None
        self.foto_activa_idx = 0

    def seleccionar_foto(self, idx: int):
        self.foto_activa_idx = idx

    def siguiente_foto(self):
        if self.producto_detalle and self.producto_detalle.imagenes:
            total = len(self.producto_detalle.imagenes)
            self.foto_activa_idx = (self.foto_activa_idx + 1) % total

    def anterior_foto(self):
        if self.producto_detalle and self.producto_detalle.imagenes:
            total = len(self.producto_detalle.imagenes)
            self.foto_activa_idx = (self.foto_activa_idx - 1) % total

    # Datos de Entrega y Dedicatoria (Checkout)
    nombre_cliente: str = ""
    zona_envio: str = list(TIENDA_CONFIG["zonas_envio"].keys())[0]
    fecha_entrega: str = ""
    horario_entrega: str = TIENDA_CONFIG["horarios_entrega"][0]
    dedicatoria: str = ""
    error_checkout: str = ""

    # --- EVENTOS DE CICLO DE VIDA Y CATÁLOGO ---
    def cargar_catalogo(self):
        """Se ejecuta al abrir la página (on_mount) para traer datos frescos de Sheets."""
        catalog_service.reload()
        self.productos = catalog_service.get_all_products()
        self.categorias = catalog_service.get_categories()

    def seleccionar_categoria(self, categoria: str):
        self.categoria_activa = categoria

    def actualizar_busqueda(self, texto: str):
        self.busqueda = texto

    @rx.var
    def productos_filtrados(self) -> List[ProductoDTO]:
        """Filtra por categoría y barra de búsqueda en tiempo real."""
        lista = catalog_service.get_by_category(self.categoria_activa)
        if self.busqueda.strip():
            q = self.busqueda.strip().lower()
            lista = [
                p for p in lista
                if q in p.nombre.lower() or q in p.descripcion.lower()
            ]
        return lista

    # --- GESTIÓN DEL CARRITO ---
    def toggle_carrito(self):
        self.carrito_abierto = not self.carrito_abierto
        self.error_checkout = ""

    def agregar_al_carrito(self, product_id: str):
        producto = next((p for p in self.productos if p.id == product_id), None)
        if not producto:
            return

        if product_id in self.carrito:
            item_actual = self.carrito[product_id]
            self.carrito[product_id] = CartItemDTO(
                product_id=item_actual.product_id,
                nombre=item_actual.nombre,
                precio_unitario=item_actual.precio_unitario,
                cantidad=item_actual.cantidad + 1,
            )
        else:
            self.carrito[product_id] = CartItemDTO(
                product_id=producto.id,
                nombre=producto.nombre,
                precio_unitario=producto.precio,
                cantidad=1,
            )

        return rx.toast.success(
            f"¡{producto.nombre} agregado a tu pedido!",
            position="bottom-right",
            duration=2500,
        )

    def incrementar_cantidad(self, product_id: str):
        """Incrementa cantidad desde el carrito lateral sin disparar toast."""
        if product_id not in self.carrito:
            return
        item_actual = self.carrito[product_id]
        self.carrito[product_id] = CartItemDTO(
            product_id=item_actual.product_id,
            nombre=item_actual.nombre,
            precio_unitario=item_actual.precio_unitario,
            cantidad=item_actual.cantidad + 1,
        )

    def disminuir_cantidad(self, product_id: str):
        if product_id not in self.carrito:
            return
        item_actual = self.carrito[product_id]
        if item_actual.cantidad > 1:
            self.carrito[product_id] = CartItemDTO(
                product_id=item_actual.product_id,
                nombre=item_actual.nombre,
                precio_unitario=item_actual.precio_unitario,
                cantidad=item_actual.cantidad - 1,
            )
        else:
            del self.carrito[product_id]

    def eliminar_del_carrito(self, product_id: str):
        if product_id in self.carrito:
            del self.carrito[product_id]

    # --- VARIABLES COMPUTADAS FINANCIERAS (DELEGADAS A PricingService) ---
    @rx.var
    def items_carrito_lista(self) -> List[CartItemDTO]:
        return list(self.carrito.values())

    @rx.var
    def total_articulos(self) -> int:
        return sum(item.cantidad for item in self.carrito.values())

    @rx.var
    def subtotal(self) -> float:
        sub, _, _ = pricing_service.calculate_totals(
            self.items_carrito_lista, self.zona_envio
        )
        return sub

    @rx.var
    def costo_envio(self) -> float:
        _, env, _ = pricing_service.calculate_totals(
            self.items_carrito_lista, self.zona_envio
        )
        return env

    @rx.var
    def total_final(self) -> float:
        _, _, tot = pricing_service.calculate_totals(
            self.items_carrito_lista, self.zona_envio
        )
        return tot

    # --- SETTERS PARA FORMULARIO DE ENTREGA ---
    def set_nombre_cliente(self, val: str):
        self.nombre_cliente = val

    def set_zona_envio(self, val: str):
        self.zona_envio = val

    def set_fecha_entrega(self, val: str):
        self.fecha_entrega = val

    def set_horario_entrega(self, val: str):
        self.horario_entrega = val

    def set_dedicatoria(self, val: str):
        self.dedicatoria = val

    # --- CIERRE DE PEDIDO (DELEGADO A CheckoutService) ---
    def procesar_pedido(self):
        """Valida datos mínimos, arma el OrderRequestDTO y redirige al proveedor de salida."""
        if not self.carrito:
            self.error_checkout = "Tu carrito está vacío."
            return
        if not self.nombre_cliente.strip():
            self.error_checkout = "Por favor escribe tu nombre para el pedido."
            return
        if not self.fecha_entrega.strip():
            self.error_checkout = "Selecciona una fecha de entrega."
            return

        self.error_checkout = ""

        orden = OrderRequestDTO(
            items=self.items_carrito_lista,
            zona_envio=self.zona_envio,
            costo_envio=self.costo_envio,
            fecha_entrega=self.fecha_entrega,
            horario_entrega=self.horario_entrega,
            dedicatoria=self.dedicatoria,
            nombre_cliente=self.nombre_cliente.strip(),
            subtotal=self.subtotal,
            total=self.total_final,
        )

        url_destino = checkout_service.generate_checkout_action(orden)
        return rx.redirect(url_destino, external=True)

    def ir_al_inicio(self):
        """Restablece filtros, cierra paneles y lleva al inicio."""
        self.categoria_activa = "Todos"
        self.busqueda = ""
        self.carrito_abierto = False
        self.producto_detalle = None
        return rx.redirect("/")

    def limpiar_filtros(self):
        self.categoria_activa = "Todos"
        self.busqueda = ""