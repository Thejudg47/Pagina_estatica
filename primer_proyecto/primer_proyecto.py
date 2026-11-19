"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .config_cliente import TIENDA_CONFIG
from .state.store_state import StoreState
from .ui.main_page import index_page
from typing import Literal, cast

AccentColor = Literal[
    "tomato", "red", "ruby", "crimson", "pink", "plum", "purple", "violet",
    "iris", "indigo", "blue", "cyan", "teal", "jade", "green", "grass",
    "brown", "orange", "sky", "mint", "lime", "yellow", "amber", "gold",
    "bronze", "gray"
]

class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap",
    ],
    style={
        "scroll_behavior": "smooth",
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "& h1, & h2, & h3, & .rt-Heading": {
            "font_family": "'Playfair Display', serif",
        },
    },
    theme=rx.theme(
        appearance="light",
        accent_color=cast(AccentColor, TIENDA_CONFIG["color_primario"]),
        radius="medium",
    )
)
app.add_page(
    index_page,
    route="/",
    title=TIENDA_CONFIG["nombre"],
    description=TIENDA_CONFIG["eslogan"],
    on_load=StoreState.cargar_catalogo,
)
