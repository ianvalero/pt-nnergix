# PT NNergix - Link Extractor API

API REST para extraer enlaces de URLs.
Construida con **FastAPI**, **PostgreSQL** y **BeautifulSoup**.

## 🛠️ Requisitos Previos
### Docker
- Docker Engine 20.10+
- Docker Compose 2.0+

## 🚀 Instalación y Ejecución
### 1. Clonar el repositorio
```bash
git clone https://github.com/ianvalero/pt-nnergix.git
cd pt_nnergix
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```env
DB_USER=nnergix_user
DB_PASSWORD=pon_tu_contraseña_aqui
DB_HOST=db
DB_PORT=5432
DB_NAME=nnergix_db
HTTP_PROXY=
HTTPS_PROXY=
NO_PROXY=localhost,127.0.0.1,db
```

### 3. Levantar la aplicación
```bash
docker compose up --build -d
```
La aplicación estará disponible en `http://localhost:8000`

### 4. Detener la aplicación
```bash
docker compose down
```
---

# 📚 Interacción con la API
## Documentación
La API proporciona documentación interactiva:
* **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔗 Ejemplo de Uso Principal - Scraper (Extraer enlaces)
**POST** `/api/v1/scraper/`

Extrae enlaces validos de una URL y registra el resultado en base de datos.

**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/scraper/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "http://example.com/",
  "follow_redirects": true,
  "timeout": 10
}'
```

**Response (201 Created):**
```json
{
  "id": 21,
  "created_at": "2026-06-13T17:44:08.523081",
  "url": {
    "id": 2,
    "url": "http://example.com/",
    "normalized_url": "http://example.com/",
    "created_at": "2026-06-13T17:44:08.523081"
  },
  "scraper_run": {
    "status": "SUCCESS",
    "http_status": 200,
    "response_time_ms": 436,
    "follow_redirects": true,
    "error_message": null,
    "id": 22,
    "created_at": "2026-06-14T11:57:59.438822",
    "links_count": 1,
    "links": [
      {
        "id": 44,
        "url": "https://iana.org/domains/example",
        "normalized_url": "https://iana.org/domains/example",
        "text": "Learn more"
      }
    ]
  }
}
```

*(Para ver la estructura de respuesta y el resto de endpoints del Historial, consulta la documentación en `/docs`).*
---

## ✅ Testing y CI/CD
El proyecto contiene tests automáticos creados con **Pytest**. Los tests utilizan una base de datos rápida en memoria (SQLite).

Cuenta con un pipeline automatizado en GitHub Actions que revisa el código cada vez que se sube y bloquea los cambios si no pasan los tests.
Si todo está correcto, compila la imagen de Docker.

Ejecutar tests en entorno local:
```bash
docker compose exec app uv run pytest tests/ -v
```

## ✨ Mejoras
En futuras actualizaciones incluiría las siguientes evoluciones:
* **Procesamiento Asíncrono (Workers):** Implementar **Redis o RabbitMQ** junto con Celery. Las peticiones HTTP largas deben encolarse para no bloquear la API, devolviendo un `job_id` al cliente.
* **Sesión de Base de Datos Asíncrona:** Migrar de `psycopg2` a `asyncpg` utilizando `AsyncSession` de SQLModel.
* **Soporte para Webs con JavaScript (SPA):** Integrar **Playwright o Selenium** para renderizar y extraer enlaces de webs que requieren ejecución de JS.
* **Seguridad y Control de Tráfico:**
    * Añadir autenticación mediante **API-Key** en los headers.
    * Implementar **Rate Limiting** si es una API externa para prevenir peticiones masivas y evitar que nuestra IP sea baneada por los sitios scrapeados.
* **Sistema de Caché:** Cachear resultados de URLs frecuentemente solicitadas para ahorrar ancho de banda y tiempo de procesamiento.