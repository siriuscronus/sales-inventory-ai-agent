# Arquitectura Lógica

## Piedmont Metals Sales & Inventory AI Agent

## 1. Objetivo de arquitectura

La solución permite a usuarios de ventas y operaciones consultar información relacionada con inventario, precios, productos, cotizaciones y procedimientos mediante una interfaz conversacional.

El sistema combina información operativa estructurada, conocimiento documental y modelos de lenguaje, manteniendo separadas las fuentes de verdad:

- **Datos operativos:** Tools + SQLite.
- **Conocimiento documental:** RAG + Qdrant.
- **Interpretación y generación:** Gemini.
- **Interoperabilidad:** Model Context Protocol (MCP).

El agente evita utilizar el LLM cuando una consulta puede resolverse localmente mediante reglas, routers o herramientas operativas.

---

## 2. C4 Model - Level 2

```mermaid
flowchart LR

    USER["Usuario de Ventas / Operaciones"]

    subgraph SYSTEM["Piedmont Metals Sales & Inventory AI Agent"]

        UI["Web Chat
        Streamlit
        Puerto 8501"]

        API["Backend API
        FastAPI
        Puerto 8000"]

        SEC["Security Gateway
        Input Guardrails
        PII Protection
        Scope Control"]

        AGENT["AI Agent / Orchestrator
        Routing
        Tool Selection
        Context Composition"]

        TOOLS["Business Tools
        Inventory
        Pricing
        Quotes
        Product Search
        Low Stock"]

        RAG["RAG Service
        Chunking
        Embeddings
        Semantic Retrieval"]

        MCP["MCP Server
        Streamable HTTP
        Puerto 8001
        6 Tools"]

        DB[("SQLite Database
        Products
        Inventory
        Prices")]

        VDB[("Qdrant Vector Store
        Knowledge Embeddings")]

        KB["Knowledge Base
        Policies
        Procedures
        SKU Standards"]
    end

    GEMINI["Google Gemini
    3.8 Flash
    3.6 Flash
    3.5 Flash-Lite
    Fallback"]

    MCPCLIENT["External MCP Client"]

    USER --> UI
    UI -->|HTTP POST /agent| API

    API --> SEC
    SEC --> AGENT

    AGENT --> TOOLS
    TOOLS --> DB

    AGENT --> RAG
    RAG --> VDB
    KB --> RAG

    AGENT --> GEMINI

    MCPCLIENT -->|MCP / Streamable HTTP| MCP

    MCP --> TOOLS
    MCP --> RAG