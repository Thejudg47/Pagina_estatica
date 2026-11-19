# plantilla_floreria/config_cliente.py

TIENDA_CONFIG = {
    "nombre": "Florería Jardín Real",
    "eslogan": "Arreglos florales frescos con entrega el mismo día",
    "banner_superior": "Entregas el mismo día • Pedidos directos sin comisiones",  # Déjalo en "" para ocultarlo
    "telefono_whatsapp": "526681234567",
    "mensaje_whatsapp_directo": "Hola, me gustaría pedir informes sobre sus arreglos florales.",
    "direccion": "Av. Gabriel Leyva #450, Col. Centro, Los Mochis, Sinaloa.",
    "horario_atencion": "Lunes a Sábado: 8:30 AM - 7:30 PM | Domingos: 9:00 AM - 2:00 PM",
    "redes_sociales": {
        "instagram": "https://instagram.com/floreriajardinreal",
        "facebook": "https://facebook.com/floreriajardinreal",
        "tiktok": "",  # Si se deja vacío, no se muestra el botón
    },
    "moneda": "MXN",
    "color_primario": "pink",
    # Pega aquí el enlace publicado como CSV de Google Sheets:
    "google_sheets_csv_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1BpURkkGiLokJxoT5GCRS0pkVTNuIw1k6r75eOLcFHNS3ofucOHD7cjZWXgF2ethMlq5M-V68VaIx/pub?gid=0&single=true&output=csv",
    "zonas_envio": {
        "Recoger en tienda": 0,
        "Zona Centro": 60,
        "Zona Norte / Sur": 90,
        "Alrededores": 130,
    },
    "horarios_entrega": [
        "Mañana (9:00 AM - 1:00 PM)",
        "Tarde (1:00 PM - 5:00 PM)",
        "Noche (5:00 PM - 8:00 PM)",
    ]
}