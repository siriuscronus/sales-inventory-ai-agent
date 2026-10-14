# Arquitectura Lógica

## Agente de IA de Ventas e Inventario para Piedmont Metals

## Objetivo

La arquitectura permite consultar información de productos, inventario, precios, cotizaciones y procedimientos mediante una interfaz conversacional.

El sistema mantiene separadas sus fuentes de información:

- **SQLite:** productos, precios e inventario.
- **RAG + Qdrant:** políticas y procedimientos.
- **Gemini:** interpretación y generación de respuestas complejas.
- **MCP:** acceso externo a las mismas herramientas del sistema.

---

## Diagrama de Arquitectura

```mermaid
flowchart LR

    U["Usuario"]
    UI["Interfaz Web<br/>Streamlit"]
    API["API<br/>FastAPI"]
    SEC["Control de Seguridad"]
    A["Agente / Orquestador"]

    T["Herramientas de Negocio"]
    DB[("SQLite")]

    R["Servicio RAG"]
    Q[("Qdrant")]
    KB["Base de Conocimiento"]

    L["Google Gemini"]

    C["Cliente MCP"]
    M["Servidor MCP"]

    U --> UI
    UI --> API
    API --> SEC
    SEC --> A

    A --> T
    T --> DB

    A --> R
    R --> Q
    KB --> R

    A --> L

    C --> M
    M --> T
    M --> R