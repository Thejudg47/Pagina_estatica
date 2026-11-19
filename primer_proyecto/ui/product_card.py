import reflex as rx
from ..config_cliente import TIENDA_CONFIG
from ..contracts.catalog_contract import ProductoDTO
from ..state.store_state import StoreState


def product_card(producto: ProductoDTO) -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    moneda = TIENDA_CONFIG.get("moneda", "MXN")
    total_fotos = producto.imagenes.length()

    return rx.box(
        rx.vstack(
            # 1. Contenedor de imagen clicable con badges
            rx.box(
                rx.image(
                    src=producto.imagenes[0],
                    fallback="/arreglos/placeholder.png",
                    alt=producto.nombre,
                    width="100%",
                    height="250px",
                    object_fit="cover",
                    cursor="pointer",
                    on_click=lambda: StoreState.abrir_detalle(producto),
                ),
                # Etiqueta promocional superior izquierda
                rx.cond(
                    producto.etiqueta,
                    rx.badge(
                        producto.etiqueta,
                        color_scheme=color,
                        variant="solid",
                        radius="full",
                        padding_x="10px",
                        padding_y="4px",
                        position="absolute",
                        top="12px",
                        left="12px",
                        box_shadow="0 2px 8px rgba(0,0,0,0.18)",
                    ),
                ),
                # Indicador oscuro translúcido de galería (si hay más de 1 foto)
                rx.cond(
                    total_fotos > 1,
                    rx.hstack(
                        rx.icon("images", size=13, color="white"),
                        rx.text(f"{total_fotos} fotos", size="1", weight="medium", color="white"),
                        spacing="1",
                        align="center",
                        padding_x="10px",
                        padding_y="4px",
                        border_radius="full",
                        background_color="rgba(17, 17, 17, 0.72)",
                        backdrop_filter="blur(4px)",
                        position="absolute",
                        bottom="12px",
                        right="12px",
                        cursor="pointer",
                        on_click=lambda: StoreState.abrir_detalle(producto),
                    ),
                ),
                position="relative",
                width="100%",
                overflow="hidden",
                background_color="#f5f5f5",
            ),
            # 2. Cuerpo de información y compra
            rx.vstack(
                rx.text(
                    producto.categoria.upper(),
                    size="1",
                    weight="bold",
                    letter_spacing="0.08em",
                    color=rx.color(color, 10),
                ),
                rx.heading(
                    producto.nombre,
                    size="5",
                    weight="bold",
                    color="#1a1a1a",
                    line_height="1.25",
                    cursor="pointer",
                    on_click=lambda: StoreState.abrir_detalle(producto),
                    _hover={"color": rx.color(color, 10)},
                ),
                rx.text(
                    producto.descripcion,
                    size="2",
                    color="gray",
                    line_height="1.5",
                    no_of_lines=2,
                ),
                rx.spacer(),
                rx.divider(margin_y="8px", opacity="0.6"),
                # Pie de tarjeta: Precio + Botón Agregar
                rx.hstack(
                    rx.vstack(
                        rx.text("Precio", size="1", color="gray", line_height="1"),
                        rx.hstack(
                            rx.text(
                                f"${producto.precio:,.2f}",
                                size="5",
                                weight="bold",
                                color="#1a1a1a",
                            ),
                            rx.text(
                                moneda,
                                size="1",
                                weight="medium",
                                color="gray",
                            ),
                            align="baseline",
                            spacing="1",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("shopping-bag", size=16),
                        "Agregar",
                        on_click=lambda: StoreState.agregar_al_carrito(producto.id),
                        color_scheme=color,
                        variant="solid",
                        radius="full",
                        size="2",
                        padding_x="16px",
                        cursor="pointer",
                    ),
                    width="100%",
                    align="center",
                ),
                padding="18px",
                spacing="2",
                align="start",
                flex="1",
                width="100%",
            ),
            height="100%",
            spacing="0",
            width="100%",
        ),
        background_color="white",
        border="1px solid #ececec",
        border_radius="16px",
        overflow="hidden",
        box_shadow="0 2px 10px rgba(0, 0, 0, 0.03)",
        transition="all 0.25s ease",
        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "0 12px 28px rgba(0, 0, 0, 0.08)",
            "border_color": rx.color(color, 6),
        },
        height="100%",
        width="100%",
    )