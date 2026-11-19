# Docker · MindTrack

Contenedor para ejecutar la aplicación Streamlit con los **modelos y reportes ya versionados** en el repositorio. No entrena al arrancar.

## Docker Hub (imagen publicada)

| Campo | Valor |
|-------|--------|
| **Página del proyecto** | https://hub.docker.com/r/danielhsk/mindtrack |
| **Imagen** | `docker.io/danielhsk/mindtrack:latest` (también `1.0.0`) |
| **Digest (latest)** | `sha256:b899b09dd94bd25b659beb980d2b688f42512e9ec0f06004e88ca2fa165cecc3` |
| **Repositorio GitHub** | https://github.com/Danielhsk/MindTrack |

```bash
docker pull danielhsk/mindtrack:latest
docker run --rm -p 8501:8501 danielhsk/mindtrack:latest
```

Con Compose (archivo `docker-compose.hub.yml` en la raíz del repo):

```bash
docker compose -f docker-compose.hub.yml up -d
```

**Publicación (mantenedores):** workflow `.github/workflows/docker-publish.yml` con secrets `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN`, o `docker login` + `docker push danielhsk/mindtrack:latest` desde máquina local.

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows / macOS) o Docker Engine + Compose (Linux)

## Inicio rápido

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Abrir en el navegador: **http://localhost:8501**

Detener: `Ctrl+C` o `docker compose down`

## Solo Docker (sin Compose)

```bash
docker build -t mindtrack:latest .
docker run --rm -p 8501:8501 mindtrack:latest
```

## Qué incluye la imagen

| Ruta en imagen | Uso |
|----------------|-----|
| `app/streamlit_app.py` | Entrypoint Streamlit |
| `src/` | Preprocesamiento, inferencia, SHAP, UI |
| `models/*.joblib` + `metadata.json` | Motor de producción (`production_model_key`) |
| `data/` | Dataset (Laboratorio / trazabilidad) |
| `reports/` | CSV y PNG del experimento |
| `.streamlit/config.toml` | Tema y `headless` |

## Regenerar modelos (host, no contenedor)

Si cambias datos o hiperparámetros:

```bash
python scripts/train_and_export.py
docker compose build --no-cache
docker compose up
```

## Variables de entorno útiles

| Variable | Efecto |
|----------|--------|
| `STREAMLIT_SERVER_HEADLESS=true` | Sin abrir navegador en el servidor |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false` | Sin telemetría de uso |

## Despliegue

- **Académico / demo:** `docker compose` en VM o laptop del equipo.
- **Alternativa:** [Streamlit Cloud](https://streamlit.io/cloud) con el mismo entrypoint (`app/streamlit_app.py`).
- La imagen no incluye GPU; XGBoost y SHAP corren en CPU.

## Solución de problemas

| Síntoma | Acción |
|---------|--------|
| Puerto 8501 ocupado | En `docker-compose.yml` usar `"8502:8501"` |
| Faltan modelos | Ejecutar `train_and_export.py` y volver a `docker build` |
| Healthcheck falla al inicio | Esperar ~40 s (SHAP / imports en frío) |

Ver también: [README.md](../README.md) · [models/README.md](../models/README.md)