"""Dependencias inyectadas en las rutas (`Depends`)."""

from energy_forecast.config import Settings
from energy_forecast.services.forecast import ForecastService


def get_settings() -> Settings:
    """Configuración cacheada para toda la vida del proceso."""
    # TODO: `load_settings()` envuelto en `functools.lru_cache`.
    raise NotImplementedError


def get_forecast_service() -> ForecastService:
    """`ForecastService` construido una sola vez (el modelo se carga al arrancar, no en cada petición)."""
    # TODO: `build_forecast_service(get_settings())` cacheado. En tests se sustituye con
    #       `app.dependency_overrides[get_forecast_service]` por un servicio con fakes.
    raise NotImplementedError
