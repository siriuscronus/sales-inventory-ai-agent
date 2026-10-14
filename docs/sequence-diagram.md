# Diagramas de Secuencia

## Agente de IA de Ventas e Inventario para Piedmont Metals

Este documento muestra los principales flujos de ejecución del prototipo.

---

## 1. Consulta simple de precio

### Caso

```text
¿Cuánto cuesta el SKU IJOIST-16-20?
```

```mermaid
sequenceDiagram

    actor U as Usuario
    participant UI as Streamlit
    participant API as FastAPI
    participant SEC as Control de Seguridad
    participant A as Orquestador
    participant T as Herramienta de Precio
    participant DB as SQLite

    U->>UI: Consultar precio
    UI->>API: POST /agent
    API->>SEC: Validar consulta
    SEC-->>API: Consulta permitida

    API->>A: Procesar consulta
    A->>T: get_product_price(SKU)

    T->>DB: Consultar precio
    DB-->>T: Precio encontrado

    T-->>A: Resultado
    A-->>API: Respuesta
    API-->>UI: JSON
    UI-->>U: Mostrar precio
```

Este tipo de consulta puede resolverse sin utilizar Gemini.

---

## 2. Consulta compleja

### Caso

```text
Necesito 20 unidades del SKU IJOIST-16-20.
¿Tenemos suficiente inventario y qué procedimiento debemos seguir si no alcanza?
```

```mermaid
sequenceDiagram

    actor U as Usuario
    participant UI as Streamlit
    participant API as FastAPI
    participant SEC as Control de Seguridad
    participant A as Orquestador
    participant T as Herramienta de Cotización
    participant DB as SQLite
    participant R as Servicio RAG
    participant Q as Qdrant
    participant L as Gemini

    U->>UI: Solicitud compleja
    UI->>API: POST /agent
    API->>SEC: Validar consulta
    SEC-->>API: Consulta permitida

    API->>A: Procesar consulta

    A->>T: calculate_quote()
    T->>DB: Consultar inventario y precio
    DB-->>T: Datos operativos
    T-->>A: Resultado de cotización

    A->>R: search_knowledge()
    R->>Q: Búsqueda semántica
    Q-->>R: Información relevante
    R-->>A: Procedimiento recuperado

    A->>L: Enviar contexto operativo y documental
    L-->>A: Respuesta consolidada

    A-->>API: Resultado final
    API-->>UI: JSON
    UI-->>U: Mostrar respuesta
```

Este flujo combina información operacional y conocimiento documental.

---

## 3. Consulta fuera del alcance

### Caso

```text
Dame código Python para sumar dos números.
```

```mermaid
sequenceDiagram

    actor U as Usuario
    participant UI as Streamlit
    participant API as FastAPI
    participant SEC as Control de Seguridad
    participant A as Orquestador

    U->>UI: Consulta fuera del dominio
    UI->>API: POST /agent
    API->>SEC: Validar consulta
    SEC-->>API: Entrada permitida

    API->>A: Procesar consulta
    A->>A: Evaluar alcance

    A-->>API: out_of_scope
    API-->>UI: JSON
    UI-->>U: Consulta fuera del alcance
```

La consulta puede rechazarse sin utilizar Gemini.

---

## 4. Flujo MCP

```mermaid
sequenceDiagram

    participant C as Cliente MCP
    participant M as Servidor MCP
    participant T as Herramientas
    participant DB as SQLite
    participant R as Servicio RAG
    participant Q as Qdrant

    C->>M: Descubrir herramientas
    M-->>C: Lista de herramientas

    C->>M: Ejecutar check_inventory
    M->>T: check_inventory(SKU)
    T->>DB: Consultar inventario
    DB-->>T: Resultado
    T-->>M: Resultado estructurado
    M-->>C: Respuesta

    C->>M: Ejecutar search_knowledge
    M->>R: search_knowledge(consulta)
    R->>Q: Búsqueda semántica
    Q-->>R: Información relevante
    R-->>M: Resultado
    M-->>C: Respuesta
```

El servidor MCP reutiliza las mismas herramientas y servicios del sistema principal.

---

## Resumen

El prototipo implementa cuatro tipos principales de flujo:

- consulta operacional simple;
- consulta compleja;
- control de alcance;
- acceso mediante MCP.

Los datos operativos provienen de SQLite y el conocimiento documental se recupera mediante RAG y Qdrant.
