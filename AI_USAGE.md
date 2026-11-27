# Uso de IA

En este documento se recogen las herramientas de inteligencia artificial generativa empleadas en este sistema.

## IA dentro del sistema

| Campo | Valor |
|---|---|
| Proveedor | **NVIDIA API Catalog** (`https://integrate.api.nvidia.com/v1`), llamado con `huggingface_hub.InferenceClient(base_url=...)` |
| Tarea | `chat_completion` |
| Modelo | `nvidia/nemotron-3.5-super-vl-120b-a12b` (configurable con `NVIDIA_MODEL`) |
| Para qué | Explicar en lenguaje natural la previsión de 24 h a partir de un resumen numérico (`ForecastSummary`) calculado por el dominio. El LLM solo redacta, no calcula cifras ni sustituye al modelo sklearn |
| Modo en tests y CI | `mock` (`AI_PROVIDER=mock`, sin `NVIDIA_API_KEY`): plantilla determinista, sin red |
| Si el proveedor falla | La previsión no falla, se usa la explicación del mock |

**Por qué no un modelo del Hub de Hugging Face.** El modelo del curso (`mistralai/Mistral-7B-Instruct-v0.3`) no tenía
ningún proveedor de inferencia activo en Hugging Face (noviembre de 2026) y las cuentas gratuitas ya no incluyen
créditos para Inference Providers. NVIDIA API Catalog es gratuito para prototipos, es compatible con la API de OpenAI y permite usar el mismo `InferenceClient` del curso.

**Qué se ajustó tras probarlo con llamadas reales:**

- Nemotron es un modelo con razonamiento. Con el razonamiento activo gastó 196 de los 200 tokens razonando y la
  respuesta salió cortada (`finish_reason=length`), así que se desactiva (`enable_thinking=False`). Sin él responde
  en 1-1,5 s.
- Una respuesta vacía o cortada se trata como fallo del proveedor y activa el *fallback* al mock.
- Se eliminan los posibles bloques `<think>...</think>` de la respuesta, por si el razonamiento se reactiva.

Condiciones de uso: gratuito con el NVIDIA Developer Program solo para prototipos, investigación y pruebas, con límite
de peticiones por minuto. La clave (`NVIDIA_API_KEY`) solo vive en el `.env`, que está en `.gitignore`.

## IA como asistente de desarrollo

Se han empleado asistentes de código para el desarrollo del proyecto ii, aunque en absoluto con la profundidad y
exhaustividad que se utilizarán en el proyecto iii. Para este proyecto, se ha utilizado con el fin de optimizar algunos
procesos, ayuda con librerías y funciones que desconocía previamente, para supervisar el cumplimiento de la arquitectura
en capas, ayuda en la implementación de tests, y para documentación del código y la elaboración del README.

Criterio general: ninguna salida de la IA se aceptó sin revisarla y ejecutar los tests.

## Proyecto III — registro por tarea

El Proyecto III se desarrolla con un agente de código (Claude Code) siguiendo el protocolo de
[`DEVELOPMENT_PLAN.md`](DEVELOPMENT_PLAN.md) §6: una rama y una PR por paso del plan, tests primero, revisión del diff y
una entrada aquí por paso, incluidas las sugerencias rechazadas. El contexto del agente está en
[`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md) y su configuración en `.claude/`.

### 2026-11-23 — Preparación: base del proyecto, análisis y plan

- **Herramienta y modelo:** Claude Code (app de escritorio) · `claude-opus-5-5`.
- **Objetivo:** copiar el Proyecto II como base de un repositorio propio, analizar qué pide el Proyecto III y escribir
  el plan de desarrollo.
- **Proceso:** copia sin `.venv` ni cachés y comprobación con `diff`; venv nuevo y `pytest` (350 passed); lectura
  del enunciado, de los temas 4 y 5 y del PDF de requisitos del diagrama; análisis de huecos frente al código;
  borrador del plan con decisiones D1–D7, que el usuario aceptó.
- **Aceptado:** copiar la muestra de un año a `data/` para que los tests no dependan de una ruta fuera del repo;
  corregir la ruta relativa de `DATASET_PATH`; el plan por fases.
- **Rechazado / corregido:** la ruta `../../dsia-dataset` heredada del Proyecto II (apuntaba fuera del workspace en
  la nueva ubicación).
- **Verificación:** `pytest -q` → 350 passed, 3 skipped (tests de la API pendientes).

### 2026-11-23 — Selección de skills y herramientas del agente

- **Herramienta y modelo:** Claude Code · `claude-opus-5-5` (búsqueda web y lectura de la documentación oficial).
- **Objetivo:** elegir skills que mejoren el código generado (FastAPI, Streamlit, despliegue, revisión).
- **Aceptado:** skill oficial de FastAPI (incluida en el paquete instalado), skills oficiales de Streamlit
  (`streamlit skills`), plugin de Render (decisión en el paso 5.0), `gh` y las skills integradas `/code-review`,
  `/security-review`, `run`, `dataviz`, `update-config` y `skill-creator`. Tabla en `DEVELOPMENT_PLAN.md` §6.1.
- **Rechazado:** skills comunitarias de FastAPI/Streamlit (las oficiales siguen la versión instalada), plugins de
  revisión comunitarios y CodeRabbit (duplican `/code-review`; CodeRabbit envía el código a un tercero), el plugin
  Data (orientado a data warehouses) y el plugin MCP de GitHub (basta con `gh`). De la skill de FastAPI se descartan
  sus consejos sobre FastAPI Cloud, el CLI `fastapi`, uv y OpenTelemetry, que chocan con D2/D4.

### 2026-11-23 — Paso 0.2: contexto del agente, permisos, hook y skills del proyecto

- **Herramienta y modelo:** Claude Code · `claude-opus-5-5` · skills `update-config` y `skill-creator`.
- **Objetivo:** que cualquier sesión del agente arranque con el contexto, las reglas y el protocolo del proyecto.
- **Aceptado:** `AGENTS.md` como fuente única (con `CLAUDE.md` importándolo); `.claude/settings.json` con comandos de
  solo lectura y `pytest` permitidos y lectura/edición de `.env` denegada; hook que ejecuta la suite rápida tras
  editar un `.py`; skills `step-start` y `step-finish` que codifican el protocolo.
- **Rechazado / ajustado:** el hook con `jq` que propone la plantilla (no está instalado en Windows): se escribió en
  Python con la librería estándar. Un hook síncrono: la suite tarda ~31 s, así que corre en segundo plano
  (`asyncRewake`) y solo avisa si falla. Las evaluaciones automáticas de `skill-creator`: las skills describen un
  procedimiento fijo y se validan usándolas en cada paso.
- **Verificación:** prueba del hook con un payload simulado (`.py` → suite en verde, `.md` → no hace nada);
  `settings.json` validado como JSON. `/code-review` encontró que la regla `Bash(git branch*)` aprobaba también
  `git branch -D`; se sustituyó por las formas de solo lectura. El `grep` de claves `nvapi-` daba falsos positivos con
  los valores de prueba y se acotó a claves de longitud real.
- **Cambio de protocolo pedido por el usuario:** el agente no hace commits, push ni PR; deja los cambios sin preparar
  y entrega un plan de commits que el usuario ejecuta (recogido en `AGENTS.md`, el plan §6 y `step-finish`).

### 2026-11-23 — Pasos 0.3, 0.5 y 0.4: limpieza, dependencias acotadas y CI

- **Herramienta y modelo:** Claude Code · `claude-opus-5-5`.
- **Objetivo:** dejar el repositorio independiente del Proyecto II, con dependencias reproducibles y CI propio.
- **Aceptado:** rutas `proyecto_ii/` sustituidas en README, ARCHITECTURE y `scripts/run_pipeline.sh`;
  `requirements.txt` (ejecución) con versiones acotadas desde la versión probada hasta la siguiente mayor y
  `requirements-dev.txt` (tests; `httpx` pasa aquí porque solo lo usa `TestClient`); `.python-version` = 3.12;
  `urllib3` declarado porque `weather_client.py` lo importa directamente; workflow con dos jobs (tests con umbral de
  cobertura del 80 % e integración sobre la muestra versionada).
- **Rechazado / pospuesto:** añadir `ruff` al CI (dependencia nueva: pendiente de aprobación del usuario); ejecutar en
  CI los tests de integración con llamadas reales a Open-Meteo y NVIDIA (necesitan red y clave); quitar las marcas
  "(P. III)" de ARCHITECTURE y los `TODO (P. III)` del código (señalan trabajo pendiente; se resuelven en cada paso).
- **Verificación:** venv limpio con Python 3.12.14 → `pip check` sin conflictos, `pytest -q` 350 passed / 3 skipped;
  comandos de ambos jobs del CI ejecutados en local (cobertura 95,5 %; integración 2 passed); YAML validado.
