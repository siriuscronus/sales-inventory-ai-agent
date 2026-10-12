# Arquitectura Lógica

## Piedmont Metals Sales & Inventory AI Agent

## Objetivo de arquitectura

La solución permitirá a usuarios de ventas y operaciones consultar información de inventario, precios, productos, cotizaciones y políticas internas mediante una interfaz conversacional.

El agente decidirá qué mecanismo utilizar según el tipo de solicitud:

- Datos operativos: Tools + base de datos.
- Conocimiento documental: RAG.
- Interpretación y generación de respuesta: LLM.

---

## C4 Model - Level 2

```mermaid
flowchart LR

    USER[Usuario de Ventas / Operaciones]

    subgraph PMONC["Piedmont Metals Sales & Inventory AI Agent"]

        UI["Web Chat\nStreamlit"]

        API["Backend API\nFastAPI"]

        AGENT["AI Agent\nOrquestación"]

        TOOLS["Tools / MCP Layer"]

        DB[("Operational Database\nSQLite")]

        RAG["RAG Service"]

        VDB[("Vector Database\nQdrant")]

        KB["Knowledge Base\nPolicies / Procedures / Catalog"]
    end

    LLM["LLM Provider\nGemini / Local Model"]

    QB["QuickBooks\nFuture Integration"]

    USER --> UI
    UI --> API
    API --> AGENT

    AGENT --> TOOLS
    TOOLS --> DB

    AGENT --> RAG
    RAG --> VDB
    KB --> VDB

    AGENT --> LLM

    TOOLS -. Future .-> QB