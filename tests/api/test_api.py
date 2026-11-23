"""Tests de la API (P. III) con `fastapi.testclient.TestClient` y `dependency_overrides`."""

import pytest

pytestmark = pytest.mark.skip(reason="TODO (P. III): implementar")


def test_health_returns_ok():
    # TODO: `GET /health` → 200 y `status == "ok"`.
    ...


def test_forecast_contract():
    # TODO: `POST /forecast` con un servicio de fakes → 200 y `Forecast.model_validate(response.json())` no falla.
    ...


def test_forecast_without_enough_history_returns_422():
    # TODO: el servicio lanza `InsufficientHistoryError` → 422 con `{"error": ...}`.
    ...
