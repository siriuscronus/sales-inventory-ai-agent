# Diagramas de Secuencia

## Piedmont Metals Sales & Inventory AI Agent

Este documento representa los principales flujos de ejecución
implementados en el prototipo.

---

## 1. Consulta operacional simple

### Caso

> ¿Cuánto cuesta el SKU IJOIST-16-20?

Esta consulta puede resolverse localmente sin utilizar el LLM.

```mermaid
sequenceDiagram

    actor U as Usuario
    participant UI as Streamlit
    participant API as FastAPI
    participant SEC as Security Gateway
    participant A as Orchestrator
    participant T as Pricing Tool
    participant DB as SQLite

    U->>UI: ¿Cuánto cuesta el SKU IJOIST-16-20?
    UI->>API: POST /agent
    API->>SEC: Validar consulta
    SEC-->>API: Consulta permitida

    API->>A: run_agent(query)
    A->>A: Identificar intención: price
    A->>T: get_product_price(SKU)
    T->>DB: SELECT producto y precio
    DB-->>T: Precio = 42.50
    T-->>A: Resultado estructurado

    A-->>API: Respuesta local
    API-->>UI: JSON
    UI-->>U: Precio unitario $42.50