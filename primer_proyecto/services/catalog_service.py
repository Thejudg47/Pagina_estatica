from typing import List, Optional
import csv
import io
import urllib.request
from ..contracts.catalog_contract import ICatalogService, ProductoDTO
import re

def _normalize_single_url(raw_url: str) -> str:
    clean_url = raw_url.strip()
    if "drive.google.com" in clean_url:
        match = re.search(r"(?:/file/d/|id=)([a-zA-Z0-9_-]+)", clean_url)
        if match:
            return f"https://lh3.googleusercontent.com/d/{match.group(1)}"
    return clean_url

def _resolve_image_list(product_id: str, raw_field: str = "") -> List[str]:
    """Convierte una cadena separada por comas en una lista limpia de URLs de imagen."""
    if raw_field and raw_field.strip():
        urls = [
            _normalize_single_url(part)
            for part in raw_field.split(",")
            if part.strip()
        ]
        if urls:
            return urls

    # Respaldo local por convención si no hay URLs en Sheets
    safe_id = product_id.strip()
    return [f"/arreglos/{safe_id}.png"]

class LocalCatalogService(ICatalogService):
    """Proveedor de catálogo basado en datos locales estáticos."""

    def __init__(self, raw_products: List[dict]):
        # Validamos y convertimos los diccionarios a objetos DTO al instanciar
        self._products: List[ProductoDTO] = []
        for item in raw_products:
            if not item.get("disponible", True):
                continue
            item_copy = dict(item)
            raw_imgs = item_copy.pop("imagen_url", "")
            if "imagenes" not in item_copy:
                item_copy["imagenes"] = _resolve_image_list(item_copy["id"], raw_imgs)
            self._products.append(ProductoDTO(**item_copy))

    def get_all_products(self):
        return self._products

    def get_by_category(self, categoria: str) -> List[ProductoDTO]:
        if not categoria or categoria.lower() == "todos":
            return self._products
        return [
            p for p in self._products if p.categoria.lower() == categoria.lower()
        ]

    def get_categories(self) -> List[str]:
        """Utilidad extra para generar pestañas de filtro dinámicas en la UI."""
        categorias = sorted(list({p.categoria for p in self._products}))
        return ["Todos"] + categorias

class GoogleSheetsCatalogService(ICatalogService):
    """Proveedor de catálogo conectado en tiempo real a una hoja pública de Google Sheets (CSV)."""

    def __init__(self, csv_url: str, fallback_products: Optional[List[dict]] = None):
        self._csv_url = csv_url
        self._fallback_products = fallback_products or []
        self._products: List[ProductoDTO] = self._load_from_sheets()

    def _parse_bool(self, value: str) -> bool:
        return str(value).strip().lower() in ("true", "1", "si", "sí", "verdadero", "yes")

    def _load_from_sheets(self) -> List[ProductoDTO]:
        if not self._csv_url or "2PACK-..." in self._csv_url:
            return self._load_fallback()

        try:
            req = urllib.request.Request(
                self._csv_url, headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                raw_text = response.read().decode("utf-8-sig")

            reader = csv.DictReader(io.StringIO(raw_text))
            productos_validos: List[ProductoDTO] = []

            for row in reader:
                # Ignorar filas vacías o productos marcados como no disponibles
                if not row.get("id") or not row.get("nombre"):
                    continue
                if not self._parse_bool(row.get("disponible", "true")):
                    continue

                prod_id = row["id"].strip()
                etiqueta_limpia = row.get("etiqueta", "").strip() or None
                raw_imgs = row.get("imagenes") or row.get("imagen_url") or ""

                producto = ProductoDTO(
                    id=prod_id,
                    nombre=row["nombre"].strip(),
                    descripcion=row.get("descripcion", "").strip(),
                    precio=float(str(row["precio"]).replace("$", "").replace(",", "").strip()),
                    categoria=row.get("categoria", "General").strip() or "General",
                    # imagen_url=row.get("imagen_url", "").strip(),
                    # imagen_url=self._normalize_image_url(row.get("imagen_url", "")),
                    imagenes=_resolve_image_list(prod_id, raw_imgs),
                    disponible=True,
                    etiqueta=etiqueta_limpia,
                )
                productos_validos.append(producto)

            return productos_validos if productos_validos else self._load_fallback()

        except Exception as e:
            print(f"[GoogleSheetsCatalogService] Error leyendo Sheets, usando respaldo: {e}")
            return self._load_fallback()

    def _load_fallback(self) -> List[ProductoDTO]:
        productos = []
        for item in self._fallback_products:
            if not item.get("disponible", True):
                continue
            item_copy = dict(item)
            raw_imgs = item_copy.pop("imagen_url", "")
            if "imagenes" not in item_copy:
                item_copy["imagenes"] = _resolve_image_list(item_copy["id"], raw_imgs)
            productos.append(ProductoDTO(**item_copy))
        return productos

    def reload(self) -> None:
        """Permite refrescar el catálogo bajo demanda sin reiniciar la app."""
        self._products = self._load_from_sheets()

    def get_all_products(self) -> List[ProductoDTO]:
        return self._products

    def get_by_category(self, categoria: str) -> List[ProductoDTO]:
        if not categoria or categoria.lower() == "todos":
            return self._products
        return[
            p for p in self._products if p.categoria.lower() == categoria.lower()
        ]

    def get_categories(self) -> List[str]:
        categorias = sorted(list({p.categoria for p in self._products}))
        return ["Todos"] + categorias

    def _normalize_image_url(self, url: str) -> str:
        """Convierte enlaces compartidos de Google Drive en URLs directas de imagen."""
        url = url.strip()
        if not url:
            return "/arreglos/placeholder.jpg"  # Imagen por defecto si dejan la celda vacía

        # Detecta patrones de Google Drive: /file/d/ID/ o id=ID
        match = re.search(r"(?:/file/d/|id=)([a-zA-Z0-9_-]+)", url)
        if "drive.google.com" in url and match:
            file_id = match.group(1)
            return f"https://lh3.googleusercontent.com/d/{file_id}"
        return url