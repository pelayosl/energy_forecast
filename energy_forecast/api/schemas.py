"""Contratos HTTP propios de la API. La respuesta de `/forecast` reutiliza `domain.models.Forecast` (§7)."""

from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    ts: datetime


class ForecastRequest(BaseModel):
    origin: datetime | None = None
    explain: bool = True


class ErrorResponse(BaseModel):
    error: str


# TODO (P. III): esquemas de `/history`, `/metrics` y `/pipeline/status`.
