"""`POST /forecast`: previsión de 24 h (mismo `ForecastService` que el CLI)."""

from fastapi import APIRouter, Depends

from energy_forecast.api.dependencies import get_forecast_service
from energy_forecast.api.schemas import ErrorResponse, ForecastRequest
from energy_forecast.domain.models import Forecast
from energy_forecast.services.forecast import ForecastService

router = APIRouter(tags=["forecast"])


@router.post(
    "/forecast",
    response_model=Forecast,
    responses={422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
)
def forecast(
    request: ForecastRequest, service: ForecastService = Depends(get_forecast_service)
) -> Forecast:
    """Valida la petición y devuelve el `Forecast` del servicio tal cual (es el contrato de salida)."""
    # TODO: `return service.forecast(request.origin, request.explain)`.
    # TODO: la ruta no contiene lógica: los errores de dominio los traducen los manejadores de `app.py`.
    raise NotImplementedError


# TODO (P. III): `GET /history`, `POST /explain`, `GET /metrics` (MonitoringService) y `GET /pipeline/status`.
