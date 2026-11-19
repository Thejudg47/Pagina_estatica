from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field

class ProductoDTO(BaseModel):
    """Objeto de transferencia de datos estandar para cualquier catalogo."""
    id: str
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    imagenes: List[str] = Field(default_factory=list)
    disponible: bool = True
    etiqueta: Optional[str] = None # Ej: "mas vendido", "Nuevo"

    @property
    def imagen_principal(self) -> str:
        return self.imagenes[0] if self.imagenes else "/arreglos/placeholder.png"

class ICatalogService(ABC):
    """Contrato que debe cumplir cualquier proveedor de catalogo"""

    @abstractmethod
    def get_all_products(self) -> List[ProductoDTO]:
        pass

    @abstractmethod
    def get_by_category(self, categoria: str) -> List[ProductoDTO]:
        pass
    