import reflex as rx
from ..config_cliente import TIENDA_CONFIG
from ..state.store_state import StoreState


def navbar() -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    banner_texto = TIENDA_CONFIG.get("banner_superior", "").strip()

    top_banner = (
        rx.box(
            rx.text(
                banner_texto,
                size="1",
                weight="medium",
                color="white",
                text_align="center",
            ),
            background_color=rx.color(color, 10),
            padding_y="1.5",
            width="100%",
        )
        if banner_texto
        else rx.fragment()
    )

    return rx.box(
        # 1. Cintillo superior de confianza (Top Announcement Bar)
        rx.box(
            rx.text(
                "Entregas el mismo día • Pedidos directos sin comisiones",
                size="1",
                weight="medium",
                color="white",
                text_align="center",
            ),
            background_color=rx.color(color, 10),
            padding_y="1.5",
            width="100%",
        ),
        # 2. Barra principal de navegación
        rx.box(
            rx.hstack(
                # Logo + Nombre (Clicable hacia el inicio)
                rx.link(
                    rx.hstack(
                        rx.center(
                            rx.icon("flower-2", size=22, color="white"),
                            background_color=rx.color(color, 9),
                            padding="2",
                            border_radius="full",
                            box_shadow="0 2px 8px rgba(0,0,0,0.12)",
                        ),
                        rx.vstack(
                            rx.heading(
                                TIENDA_CONFIG["nombre"],
                                size="4",
                                weight="bold",
                                color="#1a1a1a",
                                line_height="1.1",
                            ),
                            rx.text(
                                "FLORES & DETALLES",
                                size="1",
                                weight="medium",
                                color=rx.color(color, 10),
                                letter_spacing="0.08em",
                            ),
                            spacing="0",
                            align="start",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    href="/",
                    on_click=StoreState.ir_al_inicio,
                    underline="none",
                    cursor="pointer",
                ),
                rx.spacer(),
                # Enlaces rápidos (visibles en tablet/desktop)
                rx.hstack(
                    rx.link(
                        "Catálogo",
                        href="#catalogo",
                        size="2",
                        weight="medium",
                        color="gray",
                        underline="none",
                        _hover={"color": rx.color(color, 10)},
                    ),
                    rx.link(
                        "Ubicación y Horarios",
                        href="#contacto",
                        size="2",
                        weight="medium",
                        color="gray",
                        underline="none",
                        _hover={"color": rx.color(color, 10)},
                    ),
                    spacing="6",
                    display=["none", "none", "flex"],
                    margin_right="4",
                ),
                # Botón de Carrito estilizado
                rx.button(
                    rx.icon("shopping-bag", size=18),
                    rx.text("Mi Pedido", display=["none", "inline"], weight="medium"),
                    rx.cond(
                        StoreState.total_articulos > 0,
                        rx.badge(
                            StoreState.total_articulos,
                            color_scheme="gray",
                            variant="solid",
                            radius="full",
                        ),
                    ),
                    on_click=StoreState.toggle_carrito,
                    color_scheme=color,
                    variant="solid",
                    radius="full",
                    size="3",
                    cursor="pointer",
                    box_shadow="0 2px 6px rgba(0,0,0,0.08)",
                ),
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding_x="4",
                padding_y="3",
                align="center",
            ),
            background_color="rgba(255, 255, 255, 0.95)",
            backdrop_filter="blur(12px)",
            border_bottom="1px solid #ececec",
            width="100%",
        ),
        position="sticky",
        top="0",
        z_index="50",
        width="100%",
    )