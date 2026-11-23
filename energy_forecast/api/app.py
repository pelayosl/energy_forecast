"""Aplicación FastAPI.

Uso: uvicorn energy_forecast.api.app:app --reload
"""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Crea la app y registra los routers."""
    # TODO: `FastAPI(title="Energy Forecast API", version=...)`.
    # TODO: `app.include_router(health.router)` y `app.include_router(forecast.router)`.
    # TODO: manejadores de excepciones de dominio → códigos HTTP (§7): `InsufficientHistoryError` → 422,
    #       `ModelNotFoundError` → 503, `ExternalServiceError` → 502; error inesperado → 500 sin traza al cliente.
    # TODO: `setup_logging(...)` al arrancar.
    raise NotImplementedError


# TODO: descomentar cuando `create_app` esté implementada.
# app = create_app()
