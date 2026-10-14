# Agente de IA de Ventas e Inventario para Piedmont Metals

## Aviso académico

Este repositorio contiene un prototipo académico desarrollado exclusivamente con fines educativos y de demostración.

No constituye un sistema oficial de Piedmont Metals ni está conectado a ningún entorno de producción. Los productos, precios, cantidades de inventario, políticas y procedimientos utilizados en el proyecto son datos ficticios creados para demostrar el funcionamiento de la solución.

---

## Descripción

El **Agente de IA de Ventas e Inventario para Piedmont Metals** es un prototipo conversacional orientado a apoyar consultas relacionadas con ventas, inventario y procedimientos operativos.

El sistema permite consultar:

- disponibilidad de productos;
- precios;
- búsqueda por SKU o descripción;
- cotizaciones básicas;
- productos con bajo inventario;
- procedimientos y políticas internas de demostración.

El agente selecciona diferentes fuentes según el tipo de consulta.

---

## Problema de negocio

En una operación comercial, el personal puede necesitar consultar información distribuida entre distintas fuentes para responder preguntas como:

- ¿Tenemos suficiente inventario?
- ¿Cuál es el precio de este producto?
- ¿Cuál es el SKU correcto?
- ¿Cuánto costaría una cantidad determinada?
- ¿Qué procedimiento se debe seguir cuando no existe suficiente inventario?

Realizar estas consultas manualmente puede aumentar el tiempo de respuesta y la posibilidad de errores.

El propósito del agente es centralizar estas consultas y seleccionar automáticamente la fuente adecuada para responderlas.

---

## Objetivo

Desarrollar un agente de inteligencia artificial capaz de interpretar consultas de ventas e inventario y decidir cuándo utilizar:

- herramientas operativas;
- una base de datos;
- recuperación de conocimiento mediante RAG;
- un modelo de lenguaje.

---

## Arquitectura

```text
Usuario
   |
   v
Streamlit
   |
   v
FastAPI
   |
   v
Control de Seguridad
   |
   v
Agente / Orquestador
   |
   +------> Herramientas ------> SQLite
   |
   +------> RAG --------------> Qdrant
   |
   +------> Gemini
```

También se incluye un servidor MCP para exponer las mismas capacidades a clientes compatibles:

```text
Cliente MCP
    |
    v
Servidor MCP
    |
    +------> Herramientas ------> SQLite
    |
    +------> RAG --------------> Qdrant
```

Documentación relacionada:

- [Arquitectura lógica](docs/architecture.md)
- [Diagramas de secuencia](docs/sequence-diagram.md)

---

## Componentes principales

| Componente | Función |
|---|---|
| Streamlit | Interfaz conversacional |
| FastAPI | API del sistema |
| Agente / Orquestador | Interpreta la consulta y selecciona recursos |
| SQLite | Datos operativos de productos, precios e inventario |
| Herramientas | Consultas de inventario, precios, productos y cotizaciones |
| RAG | Recuperación de procedimientos y políticas |
| Qdrant | Base de datos vectorial |
| Gemini | Generación de respuestas para consultas complejas |
| MCP | Interoperabilidad con clientes externos |

---

## Fuentes de información

### Datos operativos

La información de productos, precios e inventario proviene de **SQLite** mediante herramientas específicas:

```text
check_inventory
get_product_price
search_product
calculate_quote
get_low_stock_items
```

### Conocimiento documental

Las políticas y procedimientos se consultan mediante **RAG**:

```text
Base de conocimiento
        |
        v
    Embeddings
        |
        v
      Qdrant
        |
        v
Recuperación semántica
```

La herramienta utilizada para consultar este conocimiento es:

```text
search_knowledge
```

---

## Ejemplo de funcionamiento

Consulta:

```text
Necesito 20 unidades del SKU IJOIST-16-20.
¿Tenemos suficiente inventario y qué procedimiento debemos seguir si no alcanza?
```

El agente puede consultar SQLite para obtener inventario y precio, recuperar procedimientos mediante RAG y Qdrant, y utilizar Gemini para consolidar la respuesta.

---

## Seguridad

El prototipo incluye controles básicos para:

- validar las consultas;
- detectar información sensible;
- limitar el alcance del agente;
- proteger las herramientas;
- evitar el uso de archivos `.env` dentro del repositorio.

Las consultas fuera del dominio del agente pueden rechazarse sin necesidad de utilizar el modelo de lenguaje.

---

## Estructura del proyecto

```text
sales-inventory-ai-agent/
│
├── app/
│   ├── agent/
│   ├── api/
│   ├── database/
│   ├── mcp_server/
│   ├── rag/
│   ├── security/
│   └── tools/
│
├── docs/
│   ├── architecture.md
│   └── sequence-diagram.md
│
├── frontend/
│   └── app.py
│
├── knowledge_base/
├── tests/
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/siriuscronus/sales-inventory-ai-agent.git
cd sales-inventory-ai-agent
```

### 2. Instalar dependencias

```bash
uv sync --locked
```

### 3. Configurar la API Key

```bash
cp .env.example .env
```

Agregar la clave de Gemini dentro del archivo `.env`:

```text
GEMINI_API_KEY=SU_API_KEY
```

El archivo `.env` no debe subirse a GitHub.

---

## Preparar los datos

### Base de datos

```bash
uv run python -m app.database.seed
```

### Base vectorial

```bash
uv run python -m app.rag.vector_store
```

---

## Ejecutar la aplicación

### FastAPI

```bash
uv run uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

### Streamlit

En otra terminal:

```bash
uv run streamlit run frontend/app.py --server.port 8501
```

### Servidor MCP

En otra terminal:

```bash
uv run python -m app.mcp_server.server
```

### Cliente MCP

Con el servidor MCP activo:

```bash
uv run python -m app.mcp_server.test_client
```

---

## Pruebas

```bash
uv run pytest -v
```

Resultado validado:

```text
13 passed
```

---

## Tecnologías utilizadas

- Python 3.13
- FastAPI
- Streamlit
- SQLite
- Qdrant
- Sentence Transformers
- Google Gemini
- Model Context Protocol
- pytest
- uv
- GitHub Codespaces

---

## Estado del prototipo

El prototipo implementa y valida:

- consultas de inventario;
- consultas de precios;
- búsqueda de productos;
- cotizaciones básicas;
- detección de bajo inventario;
- RAG con Qdrant;
- integración con Gemini;
- controles básicos de seguridad;
- API con FastAPI;
- interfaz con Streamlit;
- servidor y cliente MCP;
- pruebas automatizadas.

---

## Evolución futura

Como evolución del prototipo podrían incorporarse integraciones con sistemas empresariales como QuickBooks, órdenes de compra, órdenes de venta, facturación, autenticación y despliegue cloud.

Estas funcionalidades no forman parte del alcance actual del proyecto.

---

## Propósito académico

El proyecto demuestra cómo combinar agentes de IA, herramientas, RAG, una base de datos vectorial, un LLM, una API y MCP para resolver un caso de negocio relacionado con ventas e inventario.
