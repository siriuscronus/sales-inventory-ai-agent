# Piedmont Metals Sales & Inventory AI Agent

## Descripción

**Piedmont Metals Sales & Inventory AI Agent** es un prototipo académico de un agente de inteligencia artificial orientado a apoyar procesos de ventas, inventario y consulta operativa mediante una interfaz conversacional.

El sistema permite consultar información relacionada con:

- productos;
- inventario;
- precios;
- cotizaciones;
- productos con bajo inventario;
- políticas y procedimientos operativos.

La solución combina **Tools**, una base de datos operacional, **RAG**, una base vectorial, un modelo de lenguaje y una capa de interoperabilidad mediante **Model Context Protocol (MCP)**.

> **Importante:** todos los productos, precios, cantidades, procedimientos y demás datos utilizados en este repositorio son ficticios o fueron creados exclusivamente para fines académicos y demostrativos.

---

## Problemática

En una operación comercial de materiales de construcción, el personal puede necesitar consultar información distribuida entre diferentes fuentes para responder preguntas como:

- ¿Tenemos suficiente inventario?
- ¿Cuál es el precio vigente de un producto?
- ¿Cuál es el SKU correcto?
- ¿Cuánto costaría una determinada cantidad?
- ¿Qué productos necesitan reposición?
- ¿Qué procedimiento debe seguirse cuando no existe suficiente inventario?
- ¿Existe un producto alternativo?

Cuando estas consultas requieren revisar manualmente múltiples fuentes, aumenta el tiempo de respuesta y existe mayor posibilidad de errores.

El prototipo demuestra cómo un agente de IA puede centralizar este tipo de consultas y seleccionar automáticamente la fuente de información apropiada.

---

## Objetivo

Construir un agente de inteligencia artificial capaz de interpretar solicitudes relacionadas con ventas e inventario y decidir qué recurso utilizar para responderlas.

La solución implementa:

- **SQLite** para información operacional;
- **Business Tools** para inventario, precios, búsqueda y cotización;
- **RAG** para conocimiento documental;
- **Qdrant** como base vectorial;
- **Sentence Transformers** para embeddings;
- **Google Gemini** para razonamiento y generación de respuestas;
- **FastAPI** como Backend API;
- **Streamlit** como interfaz conversacional;
- **MCP Server** para exponer las capacidades del sistema mediante Model Context Protocol;
- **Security Guardrails** para controlar alcance y entradas;
- **pytest** para pruebas automatizadas.

---

## Alcance del MVP

El prototipo implementa las siguientes capacidades:

1. Consultar inventario.
2. Consultar precios.
3. Buscar productos.
4. Calcular cotizaciones básicas.
5. Identificar productos con bajo inventario.
6. Consultar políticas y procedimientos mediante RAG.
7. Combinar información operacional y documental.
8. Rechazar consultas fuera del dominio del agente.
9. Exponer Tools mediante MCP.
10. Proporcionar una interfaz Web Chat.

---

## Arquitectura

La arquitectura lógica está documentada mediante C4 Model Level 2 y diagramas de secuencia.

Documentos:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/sequence-diagram.md`](docs/sequence-diagram.md)

Vista simplificada:

```text
Usuario
   |
   v
Streamlit Web Chat
   |
   v
FastAPI Backend
   |
   v
Security Gateway
   |
   v
AI Agent / Orchestrator
   |
   +------> Business Tools ------> SQLite
   |
   +------> RAG -----------------> Qdrant
   |                                ^
   |                                |
   |                         Knowledge Base
   |
   +------> Gemini
               |
               v
         Respuesta final