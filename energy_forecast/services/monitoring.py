"""Caso de uso (P. III): comparar las previsiones emitidas con la demanda real."""

from datetime import datetime

from energy_forecast.infrastructure.repositories import ObservationRepository, PredictionRepository


class MonitoringService:
    """Calcula el error de las previsiones ya verificables (predicción vs real)."""

    def __init__(self, observations: ObservationRepository, predictions: PredictionRepository) -> None:
        self._observations = observations
        self._predictions = predictions

    def error_metrics(self, start: datetime, end: datetime) -> dict[str, float]:
        """MAE / RMSE / MAPE de las predicciones con `target_time_utc` entre `start` y `end`."""
        # TODO (P. III): unir `predictions.between(start, end)` con `observations.range(start, end)` por hora
        #       y aplicar `evaluate` (dominio). Lo expone `/metrics` y lo muestra el dashboard.
        raise NotImplementedError
