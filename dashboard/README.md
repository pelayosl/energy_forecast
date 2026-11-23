# Dashboard (Proyecto III)

TODO: elegir tecnología (Streamlit, Dash, …) y documentarla en `ARCHITECTURE.md`.

Reglas (D6): el dashboard **solo consume la API por HTTP**; nunca accede a la BD ni al CSV.

Vistas previstas:

- **Producto**: histórico de demanda, botón de previsión (`POST /forecast`), gráfica de las 24 h y explicación IA.
- **Operación**: `/health`, error de las previsiones en el tiempo (`/metrics`), estado del pipeline (`/pipeline/status`).
