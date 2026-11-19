import reflex as rx
from ..config_cliente import TIENDA_CONFIG
from ..state.store_state import StoreState
from .navbar import navbar
from .filter_bar import filter_bar
from .product_card import product_card
from .cart_drawer import cart_drawer
from .product_modal import product_modal
from .footer import footer


def _empty_catalog_state() -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon("search-x", size=32, color=rx.color(color, 9)),
                background_color=rx.color(color, 3),
                padding="16px",
                border_radius="full",
            ),
            rx.heading(
                "No encontramos arreglos con esa búsqueda",
                size="5",
                weight="bold",
                color="#1a1a1a",
                text_align="center",
            ),
            rx.text(
                "Intenta con otro término o explora todas nuestras categorías disponibles.",
                size="2",
                color="gray",
                text_align="center",
                max_width="400px",
            ),
            rx.button(
                rx.icon("rotate-ccw", size=16),
                "Ver todo el catálogo",
                on_click=StoreState.limpiar_filtros,
                color_scheme=color,
                variant="soft",
                radius="full",
                size="3",
                margin_top="8px",
                cursor="pointer",
            ),
            align="center",
            spacing="3",
        ),
        padding_y="64px",
        padding_x="24px",
        width="100%",
        background_color="#fafafa",
        border="1px dashed #e0e0e0",
        border_radius="16px",
    )


def index_page() -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]

    return rx.flex(
        navbar(),
        # Contenedor principal
        rx.box(
            # Hero / Banner editorial de bienvenida
            rx.box(
                rx.vstack(
                    rx.badge(
                        "CATÁLOGO EN LÍNEA",
                        color_scheme=color,
                        variant="soft",
                        radius="full",
                        padding_x="14px",
                        padding_y="5px",
                        letter_spacing="0.1em",
                        font_weight="600",
                    ),
                    rx.heading(
                        TIENDA_CONFIG["nombre"],
                        size="9",
                        weight="bold",
                        color="#1a1a1a",
                        text_align="center",
                        line_height="1.1",
                    ),
                    rx.text(
                        TIENDA_CONFIG["eslogan"],
                        size="4",
                        color="gray",
                        text_align="center",
                        max_width="600px",
                        line_height="1.6",
                    ),
                    rx.box(
                        filter_bar(),
                        width="100%",
                        padding_top="16px",
                    ),
                    max_width="1200px",
                    margin="0 auto",
                    padding_x="24px",
                    padding_top="56px",
                    padding_bottom="32px",
                    spacing="4",
                    align="center",
                ),
                background=f"linear-gradient(180deg, {rx.color(color, 2)} 0%, #ffffff 100%)",
                width="100%",
            ),
            # Sección del Catálogo (Cuadrícula o Estado Vacío)
            rx.box(
                rx.cond(
                    StoreState.productos_filtrados.length() > 0,
                    rx.grid(
                        rx.foreach(StoreState.productos_filtrados, product_card),
                        columns=rx.breakpoints(initial="1", sm="2", md="3"),
                        spacing="6",
                        width="100%",
                    ),
                    _empty_catalog_state(),
                ),
                id="catalogo",
                max_width="1200px",
                margin="0 auto",
                padding_x="24px",
                padding_bottom="80px",
                width="100%",
            ),
            flex="1",
            width="100%",
        ),
        footer(),
        cart_drawer(),
        product_modal(),
        direction="column",
        width="100%",
        min_height="100vh",
    )