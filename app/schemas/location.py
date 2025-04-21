from pydantic import BaseModel, Field


class Location(BaseModel):
    latitude: float = Field(..., description="Latitud de la ubicación del usuario")
    longitude: float = Field(..., description="Longitud de la ubicación del usuario")
