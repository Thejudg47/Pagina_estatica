import reflex as rx
from ..config_cliente import TIENDA_CONFIG
from ..contracts.checkout_contract import CartItemDTO
from ..state.store_state import StoreState


def _cart_item_row(item: CartItemDTO) -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    return rx.hstack(
        rx.vstack(
            rx.text(item.nombre, weight="bold", size="2", color="#1a1a1a"),
            rx.text(f"${item.precio_unitario:,.2f} c/u", size="1", color="gray"),
            spacing="0",
            align="start",
            max_width="185px",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("minus", size=13),
                on_click=lambda: StoreState.disminuir_cantidad(item.product_id),
                size="1",
                variant="soft",
                color_scheme="gray",
                cursor="pointer",
            ),
            rx.text(item.cantidad, weight="bold", size="2", padding_x="4px"),
            rx.icon_button(
                rx.icon("plus", size=13),
                on_click=lambda: StoreState.incrementar_cantidad(item.product_id),
                size="1",
                variant="soft",
                color_scheme=color,
                cursor="pointer",
            ),
            rx.icon_button(
                rx.icon("trash-2", size=14),
                on_click=lambda: StoreState.eliminar_del_carrito(item.product_id),
                size="1",
                variant="ghost",
                color_scheme="red",
                margin_left="4px",
                cursor="pointer",
            ),
            align="center",
            spacing="1",
        ),
        width="100%",
        padding_y="10px",
        border_bottom="1px solid #f0f0f0",
        align="center",
    )


def _dedication_card_preview() -> rx.Component:
    """Vista previa en vivo simulando cómo quedará impresa la tarjeta física."""
    color = TIENDA_CONFIG["color_primario"]
    return rx.cond(
        StoreState.dedicatoria.strip() != "",
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("sparkles", size=12, color=rx.color(color, 9)),
                    rx.text(
                        "VISTA PREVIA DE TU TARJETA",
                        size="1",
                        weight="bold",
                        letter_spacing="0.08em",
                        color=rx.color(color, 10),
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.box(
                    rx.text(
                        f"“{StoreState.dedicatoria}”",
                        style={
                            "font_family": "'Playfair Display', serif",
                            "font_style": "italic",
                            "font_size": "15px",
                            "line_height": "1.6",
                            "color": "#2c2420",
                            "white_space": "pre-wrap",
                        },
                        text_align="center",
                    ),
                    padding_y="12px",
                    padding_x="8px",
                    width="100%",
                ),
                rx.text(
                    f"— {TIENDA_CONFIG['nombre']}",
                    size="1",
                    color="#8c7f77",
                    style={"font_family": "'Playfair Display', serif"},
                ),
                align="center",
                spacing="2",
                width="100%",
            ),
            width="100%",
            padding="16px",
            margin_top="6px",
            background_color="#fcf9f5",
            border=f"1px solid {rx.color(color, 5)}",
            border_radius="12px",
            box_shadow="0 4px 12px rgba(0, 0, 0, 0.04)",
        ),
    )


def cart_drawer() -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    zonas = list(TIENDA_CONFIG["zonas_envio"].keys())
    horarios = TIENDA_CONFIG["horarios_entrega"]

    return rx.drawer.root(
        rx.drawer.overlay(z_index="99"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    # Encabezado del Drawer
                    rx.hstack(
                        rx.heading("Tu Pedido", size="5", color="#1a1a1a"),
                        rx.spacer(),
                        rx.icon_button(
                            rx.icon("x", size=18),
                            on_click=StoreState.toggle_carrito,
                            variant="ghost",
                            color_scheme="gray",
                            cursor="pointer",
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.divider(),
                    # Contenido scrollable
                    rx.cond(
                        StoreState.total_articulos > 0,
                        rx.vstack(
                            # Lista de artículos
                            rx.vstack(
                                rx.foreach(StoreState.items_carrito_lista, _cart_item_row),
                                width="100%",
                                spacing="1",
                            ),
                            rx.divider(),
                            # Formulario de entrega
                            rx.vstack(
                                rx.text("Datos de Entrega", weight="bold", size="3", color="#1a1a1a"),
                                rx.input(
                                    placeholder="Tu nombre completo *",
                                    value=StoreState.nombre_cliente,
                                    on_change=StoreState.set_nombre_cliente,
                                    width="100%",
                                ),
                                rx.select(
                                    zonas,
                                    value=StoreState.zona_envio,
                                    on_change=StoreState.set_zona_envio,
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.input(
                                        type="date",
                                        value=StoreState.fecha_entrega,
                                        on_change=StoreState.set_fecha_entrega,
                                        width="50%",
                                    ),
                                    rx.select(
                                        horarios,
                                        value=StoreState.horario_entrega,
                                        on_change=StoreState.set_horario_entrega,
                                        width="50%",
                                    ),
                                    width="100%",
                                    spacing="2",
                                ),
                                rx.text_area(
                                    placeholder="Mensaje para la tarjeta de dedicatoria (opcional)...",
                                    value=StoreState.dedicatoria,
                                    on_change=StoreState.set_dedicatoria,
                                    width="100%",
                                    rows="3",
                                ),
                                # Tarjeta de dedicatoria en vivo
                                _dedication_card_preview(),
                                width="100%",
                                spacing="2",
                            ),
                            rx.divider(),
                            # Desglose de totales
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Subtotal:", color="gray"),
                                    rx.spacer(),
                                    rx.text(f"${StoreState.subtotal:,.2f}"),
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.text("Envío:", color="gray"),
                                    rx.spacer(),
                                    rx.text(f"${StoreState.costo_envio:,.2f}"),
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.text("Total:", weight="bold", size="4", color="#1a1a1a"),
                                    rx.spacer(),
                                    rx.text(
                                        f"${StoreState.total_final:,.2f} {TIENDA_CONFIG['moneda']}",
                                        weight="bold",
                                        size="4",
                                        color=rx.color(color, 10),
                                    ),
                                    width="100%",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            # Mensaje de validación si falta algún dato
                            rx.cond(
                                StoreState.error_checkout != "",
                                rx.callout(
                                    StoreState.error_checkout,
                                    icon="triangle-alert",
                                    color_scheme="red",
                                    size="1",
                                    width="100%",
                                ),
                            ),
                            rx.button(
                                rx.icon("send", size=18),
                                "Enviar Pedido por WhatsApp",
                                on_click=StoreState.procesar_pedido,
                                color_scheme="green",
                                size="3",
                                width="100%",
                                cursor="pointer",
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        # Estado vacío
                        rx.center(
                            rx.vstack(
                                rx.icon("shopping-bag", size=40, color="gray"),
                                rx.text("Tu carrito está vacío", color="gray"),
                                align="center",
                                spacing="2",
                            ),
                            padding_y="9",
                            width="100%",
                        ),
                    ),
                    height="100%",
                    width="100%",
                    overflow_y="auto",
                ),
                top="0",
                right="0",
                left="auto",
                height="100vh",
                width="100%",
                max_width="420px",
                padding="24px",
                background_color="white",
                box_shadow="-4px 0 24px rgba(0,0,0,0.12)",
                z_index="100",
            )
        ),
        open=StoreState.carrito_abierto,
        direction="right",
    )