import reflex as rx
from ..config_cliente import TIENDA_CONFIG
from ..state.store_state import StoreState


def _thumbnail_item(img_url: str, idx: int) -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    is_selected = StoreState.foto_activa_idx == idx
    return rx.box(
        rx.image(
            src=img_url,
            fallback="/arreglos/placeholder.png",
            width="60px",
            height="60px",
            object_fit="cover",
            border_radius="6px",
        ),
        border=rx.cond(
            is_selected,
            f"2px solid {rx.color(color, 9)}",
            "2px solid transparent",
        ),
        opacity=rx.cond(is_selected, "1", "0.65"),
        border_radius="8px",
        padding="2px",
        cursor="pointer",
        on_click=lambda: StoreState.seleccionar_foto(idx),
    )


def product_modal() -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    prod = StoreState.producto_detalle

    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                prod,
                rx.vstack(
                    # Encabezado con botón cerrar
                    rx.hstack(
                        rx.badge(prod.categoria.upper(), color_scheme=color, variant="soft"),
                        rx.spacer(),
                        rx.icon_button(
                            rx.icon("x", size=18),
                            on_click=StoreState.cerrar_detalle,
                            variant="ghost",
                            color_scheme="gray",
                            cursor="pointer",
                        ),
                        width="100%",
                        align="center",
                    ),
                    # Visor principal de imagen con flechas
                    rx.box(
                        rx.image(
                            src=prod.imagenes[StoreState.foto_activa_idx],
                            fallback="/arreglos/placeholder.png",
                            alt=prod.nombre,
                            width="100%",
                            height="340px",
                            object_fit="cover",
                            border_radius="10px",
                        ),
                        rx.cond(
                            prod.imagenes.length() > 1,
                            rx.fragment(
                                rx.icon_button(
                                    rx.icon("chevron-left", size=20),
                                    on_click=StoreState.anterior_foto,
                                    position="absolute",
                                    left="10px",
                                    top="50%",
                                    transform="translateY(-50%)",
                                    radius="full",
                                    variant="solid",
                                    color_scheme="gray",
                                    cursor="pointer",
                                ),
                                rx.icon_button(
                                    rx.icon("chevron-right", size=20),
                                    on_click=StoreState.siguiente_foto,
                                    position="absolute",
                                    right="10px",
                                    top="50%",
                                    transform="translateY(-50%)",
                                    radius="full",
                                    variant="solid",
                                    color_scheme="gray",
                                    cursor="pointer",
                                ),
                            ),
                        ),
                        position="relative",
                        width="100%",
                    ),
                    # Tira de miniaturas (solo si hay más de 1 foto)
                    rx.cond(
                        prod.imagenes.length() > 1,
                        rx.hstack(
                            rx.foreach(
                                prod.imagenes,
                                lambda url, i: _thumbnail_item(url, i),
                            ),
                            spacing="2",
                            wrap="wrap",
                            justify="center",
                            width="100%",
                        ),
                    ),
                    # Título, descripción completa y acción de compra
                    rx.vstack(
                        rx.heading(prod.nombre, size="6", weight="bold"),
                        rx.text(prod.descripcion, size="3", color="gray"),
                        spacing="2",
                        align="start",
                        width="100%",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.text(
                            f"${prod.precio:,.2f} {TIENDA_CONFIG['moneda']}",
                            size="6",
                            weight="bold",
                            color=rx.color(color, 10),
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("shopping-bag", size=18),
                            "Agregar al carrito",
                            on_click=[
                                StoreState.agregar_al_carrito(prod.id),
                                StoreState.cerrar_detalle,
                            ],
                            color_scheme=color,
                            size="3",
                            cursor="pointer",
                        ),
                        width="100%",
                        align="center",
                    ),
                    spacing="4",
                    width="100%",
                ),
            ),
            max_width="540px",
            padding="5",
        ),
        open=StoreState.producto_detalle != None,
        on_open_change=lambda is_open: rx.cond(~is_open, StoreState.cerrar_detalle(), rx.noop()),
    )