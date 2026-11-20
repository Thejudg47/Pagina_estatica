import { TIENDA_CONFIG } from "../config/tienda.config.js";
import { createProductoDTO } from "../contracts/types.js";

export class CatalogService {
  /**
   * Obtiene todos los productos disponibles desde Google Sheets (CSV).
   * @returns {Promise<import("../contracts/types.js").ProductoDTO[]>}
   */
  async getAllProducts() {
    const csvUrl = TIENDA_CONFIG.googleSheetsCsvUrl?.trim();
    if (!csvUrl || csvUrl === "TU_ENLACE_CSV_DE_GOOGLE_SHEETS_AQUI") {
      console.warn("URL de Google Sheets no configurada. Cargando catálogo vacío.");
      return [];
    }

    try {
      // Añadimos timestamp para evitar caché agresivo del navegador al editar precios
      const separator = csvUrl.includes("?") ? "&" : "?";
      const response = await fetch(`${csvUrl}${separator}t=${Date.now()}`);

      if (!response.ok) {
        throw new Error(`Error HTTP ${response.status} al leer Google Sheets`);
      }

      const csvText = await response.text();
      return this._parseCsvToProducts(csvText);
    } catch (error) {
      console.error("Error en CatalogService:", error);
      return [];
    }
  }

  /**
   * Parsea texto CSV respetando comillas y comas internas.
   * @param {string} csvText
   */
  _parseCsvToProducts(csvText) {
    const rows = this._parseCsvRows(csvText);
    if (rows.length < 2) return [];

    const headers = rows[0].map((h) => h.trim().toLowerCase());
    const products = [];

    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];
      if (row.every((cell) => !cell.trim())) continue;

      const record = {};
      headers.forEach((header, idx) => {
        record[header] = (row[idx] || "").trim();
      });

      const dispRaw = (record.disponible || "true").toLowerCase();
      const disponible = !["no", "false", "0"].includes(dispRaw);
      if (!disponible) continue;

      const id = record.id || `prod-${i}`;
      // Lee exactamente la columna imagen_url de tu tabla
      const rawImg = record.imagen_url || record.imagenes || record.imagen || "";
      const imagenes = this._resolveImages(rawImg, id);

      products.push(
        createProductoDTO({
          id,
          nombre: record.nombre,
          categoria: record.categoria || "General",
          precio: this._parsePrice(record.precio),
          descripcion: record.descripcion,
          imagenes,
          etiqueta: record.etiqueta,
          disponible: true,
        })
      );
    }

    return products;
  }

  /**
   * Parser RFC-4180 ligero para CSV.
   */
  _parseCsvRows(text) {
    const rows = [];
    let currentRow = [];
    let currentCell = "";
    let insideQuotes = false;

    for (let i = 0; i < text.length; i++) {
      const char = text[i];
      const nextChar = text[i + 1];

      if (insideQuotes) {
        if (char === '"' && nextChar === '"') {
          currentCell += '"';
          i++;
        } else if (char === '"') {
          insideQuotes = false;
        } else {
          currentCell += char;
        }
      } else {
        if (char === '"') {
          insideQuotes = true;
        } else if (char === ",") {
          currentRow.push(currentCell);
          currentCell = "";
        } else if (char === "\r" && nextChar === "\n") {
          currentRow.push(currentCell);
          rows.push(currentRow);
          currentRow = [];
          currentCell = "";
          i++;
        } else if (char === "\n" || char === "\r") {
          currentRow.push(currentCell);
          rows.push(currentRow);
          currentRow = [];
          currentCell = "";
        } else {
          currentCell += char;
        }
      }
    }

    if (currentCell.length > 0 || currentRow.length > 0) {
      currentRow.push(currentCell);
      rows.push(currentRow);
    }

    return rows;
  }

  _parsePrice(rawPrice) {
    const cleaned = String(rawPrice || "0").replace(/[^0-9.]/g, "");
    const value = parseFloat(cleaned);
    return Number.isFinite(value) ? value : 0;
  }

  /**
   * Resuelve múltiples imágenes separadas por coma y convierte enlaces de Google Drive.
   */
  _resolveImages(rawImages, productId) {
    if (!rawImages) {
      return [`${TIENDA_CONFIG.rutaImagenesLocal}${productId}.jpg`];
    }

    const urls = rawImages
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean)
      .map((item) => this._normalizeDriveUrl(item));

    return urls.length > 0 ? urls : [TIENDA_CONFIG.imagenFallback];
  }

  /**
   * Convierte enlaces compartidos de Google Drive en URLs directas de imagen rápida.
   */
  _normalizeDriveUrl(url) {
    if (!url.startsWith("http")) {
      return `${TIENDA_CONFIG.rutaImagenesLocal}${url}`;
    }

    // Si tu Apps Script ya generó el enlace lh3.googleusercontent.com, lo usamos directo
    if (url.includes("lh3.googleusercontent.com")) {
      return url;
    }

    // Si alguien pega un enlace normal de Google Drive, lo convertimos también
    const fileIdMatch =
      url.match(/\/file\/d\/([a-zA-Z0-9_-]+)/) ||
      url.match(/[?&]id=([a-zA-Z0-9_-]+)/);

    if (url.includes("drive.google.com") && fileIdMatch && fileIdMatch[1]) {
      return `https://lh3.googleusercontent.com/d/${fileIdMatch[1]}`;
    }

    return url;
  }
}