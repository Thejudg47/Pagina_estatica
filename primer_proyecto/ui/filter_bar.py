import reflex as rx
from ..config_cliente import TIENDA_CONFIG
from ..state.store_state import StoreState

def _category_pill(categoria: str) -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    is_active = StoreState.categoria_activa == categoria
    return rx.button(
        categoria,
        on_click=lambda: StoreState.seleccionar_categoria(categoria),
        color_scheme=color,
        variant=rx.cond(is_active, "solid", "outline"),
        radius="full",
        size="2",
        cursor="pointer",
    )

def filter_bar() -> rx.Component:
    return rx.vstack(
        rx.input(
            rx.input.slot(rx.icon("search", size=16)),
            placeholder="Buscar ramos, girasoles, cajas...",
            value=StoreState.busqueda,
            on_change=StoreState.actualizar_busqueda,
            width="100%",
            max_width="480px",
            size="3",
            radius="full",
        ),
        rx.flex(
            rx.foreach(StoreState.categorias, _category_pill),
            wrap="wrap",
            gap="2",
            justify="center",
        ),
        spacing="4",
        align="center",
        width="100%",
        padding_y="4",
    )