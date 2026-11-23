"""`GET /health`: ¿está vivo el servicio?"""

from fastapi import APIRouter

from energy_forecast.api.schemas import HealthResponse

router = APIRouter(tags=["ops"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Respuesta inmediata, sin tocar BD, modelo ni IA."""
    # TODO: devolver `HealthResponse(status="ok", ts=<ahora en UTC>)`.
    raise NotImplementedError
