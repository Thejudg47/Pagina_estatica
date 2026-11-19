/**
 * Configuración central de la tienda.
 * Único archivo que el desarrollador o cliente necesita editar para personalizar el negocio.
 */
export const TIENDA_CONFIG = {
  // Identidad de marca
  nombre: "Florería Jardín Real",
  subtitulo: "FLORES & DETALLES",
  eslogan: "Arreglos florales frescos con entrega el mismo día",
  bannerSuperior: "Entregas el mismo día • Pedidos directos sin comisiones", // Dejar en "" para ocultar

  // Paleta de color boutique (hexadecimal para máxima libertad estética)
  colorPrimario: "#d63384",      // Rosa mexicano / magenta boutique
  colorPrimarioOscuro: "#a61e61",
  colorPrimarioSuave: "#fce8f3",

  // Contacto y WhatsApp (código de país + número sin espacios ni signos)
  whatsappNumero: "526681234567",
  direccion: "Av. Gabriel Leyva #450, Col. Centro, Los Mochis, Sinaloa.",
  horarioAtencion: "Lunes a Sábado: 8:30 AM - 7:30 PM | Domingos: 9:00 AM - 2:00 PM",

  // Redes sociales (dejar en "" las que no se usen)
  redes: {
    instagram: "https://instagram.com",
    facebook: "https://facebook.com",
    tiktok: "",
  },

  // Fuente de datos (Enlace CSV publicado desde Google Sheets)
  // Pega aquí tu enlace de "Archivo > Compartir > Publicar en la web > CSV"
  googleSheetsCsvUrl: "https://docs.google.com/spreadsheets/d/e/2PACX-1vR1BpURkkGiLokJxoT5GCRS0pkVTNuIw1k6r75eOLcFHNS3ofucOHD7cjZWXgF2ethMlq5M-V68VaIx/pub?gid=0&single=true&output=csv",

  // Carpeta de respaldo local si algún producto aún no tiene foto en Drive
  rutaImagenesLocal: "./assets/arreglos/",
  imagenFallback: "./assets/arreglos/placeholder.png",

  // Logística y cobros
  moneda: "MXN",
  zonasEnvio: {
    "Recoger en tienda": 0,
    "Zona Centro": 50,
    "Zona Norte / Residencial": 80,
    "Zona Sur / Periferia": 100,
  },
  horariosEntrega: [
    "Mañana (9:00 AM - 1:00 PM)",
    "Tarde (1:00 PM - 5:00 PM)",
    "Noche (5:00 PM - 8:00 PM)",
  ],
};