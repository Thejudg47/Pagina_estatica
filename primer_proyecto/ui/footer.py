import urllib.parse
import reflex as rx
from ..config_cliente import TIENDA_CONFIG


def _social_button(icon_name: str, label: str, url: str, color: str) -> rx.Component:
    return rx.link(
        rx.button(
            rx.icon(icon_name, size=16),
            label,
            variant="soft",
            color_scheme=color,
            size="2",
            cursor="pointer",
        ),
        href=url,
        is_external=True,
    )


def footer() -> rx.Component:
    color = TIENDA_CONFIG["color_primario"]
    telefono = "".join(filter(str.isdigit, TIENDA_CONFIG["telefono_whatsapp"]))
    mensaje_codificado = urllib.parse.quote(
        TIENDA_CONFIG.get("mensaje_whatsapp_directo", "Hola, quiero información.")
    )
    whatsapp_url = f"https://wa.me/{telefono}?text={mensaje_codificado}"

    redes = TIENDA_CONFIG.get("redes_sociales", {})

    # Construimos dinámicamente solo los botones de redes que tengan URL configurada
    botones_redes = []
    if redes.get("instagram"):
        botones_redes.append(_social_button("camera", "Instagram", redes["instagram"], color))
    if redes.get("facebook"):
        botones_redes.append(_social_button("share-2", "Facebook", redes["facebook"], color))
    if redes.get("tiktok"):
        botones_redes.append(_social_button("music-2", "TikTok", redes["tiktok"], color))

    return rx.box(
        rx.box(
            rx.grid(
                # Columna 1: Identidad de marca
                rx.vstack(
                    rx.hstack(
                        rx.icon("flower-2", size=24, color=rx.color(color, 9)),
                        rx.heading(TIENDA_CONFIG["nombre"], size="4", weight="bold"),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(
                        TIENDA_CONFIG["eslogan"],
                        size="2",
                        color="gray",
                        line_height="1.6",
                    ),
                    rx.hstack(*botones_redes, spacing="3", padding_top="12px")
                    if botones_redes
                    else rx.fragment(),
                    align="start",
                    spacing="3",
                ),
                # Columna 2: Dirección y Horarios
                rx.vstack(
                    rx.text("Visítanos", weight="bold", size="3"),
                    rx.hstack(
                        rx.icon("map-pin", size=17, color=rx.color(color, 9), style={"flex_shrink": "0", "margin_top": "3px"}),
                        rx.text(
                            TIENDA_CONFIG.get("direccion", ""),
                            size="2",
                            color="gray",
                            line_height="1.6",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.icon("clock", size=17, color=rx.color(color, 9), style={"flex_shrink": "0", "margin_top": "3px"}),
                        rx.text(
                            TIENDA_CONFIG.get("horario_atencion", ""),
                            size="2",
                            color="gray",
                            line_height="1.6",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    align="start",
                    spacing="3",
                ),
                # Columna 3: Atención directa por WhatsApp
                rx.vstack(
                    rx.text("¿Buscas un arreglo personalizado?", weight="bold", size="3"),
                    rx.text(
                        "Escríbenos directo y te ayudamos a armar el detalle ideal.",
                        size="2",
                        color="gray",
                        line_height="1.6",
                    ),
                    rx.box(
                        rx.link(
                            rx.button(
                                rx.icon("message-circle", size=18),
                                "Chatear por WhatsApp",
                                color_scheme="green",
                                size="3",
                                cursor="pointer",
                            ),
                            href=whatsapp_url,
                            is_external=True,
                        ),
                        padding_top="8px",
                    ),
                    align="start",
                    spacing="3",
                ),
                columns=rx.breakpoints(initial="1", md="3"),
                spacing="8",
                width="100%",
            ),
            rx.divider(margin_top="48px", margin_bottom="24px"),
            rx.text(
                f"© 2026 {TIENDA_CONFIG['nombre']}. Todos los derechos reservados.",
                size="2",
                color="gray",
                text_align="center",
                width="100%",
            ),
            max_width="1200px",
            margin="0 auto",
            padding_x="24px",
            padding_top="64px",
            padding_bottom="36px",
        ),
        id="contacto",
        margin_top="80px",
        background_color="#fafafa",
        border_top="1px solid #eaeaea",
        width="100%",
    )