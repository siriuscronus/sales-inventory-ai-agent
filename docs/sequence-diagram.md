# Diagrama de Secuencia

## Caso: consulta de inventario y cotización

Escenario:

> El usuario necesita 20 I-Joists de 20 pies y quiere saber si hay suficiente inventario y cuál sería el subtotal.

```mermaid
sequenceDiagram

    actor U as Usuario
    participant UI as Web Chat
    participant API as FastAPI
    participant A as AI Agent
    participant T as Tools
    participant DB as SQLite
    participant LLM as LLM

    U->>UI: Necesito 20 I-Joists de 20 pies.<br/>¿Hay suficiente inventario y cuál es el subtotal?

    UI->>API: Enviar consulta
    API->>A: Procesar solicitud

    A->>A: Identificar intención

    A->>T: search_product("I-Joist 20 ft")
    T->>DB: Buscar producto
    DB-->>T: SKU encontrado
    T-->>A: Producto identificado

    A->>T: check_inventory(SKU)
    T->>DB: Consultar inventario
    DB-->>T: 14 unidades
    T-->>A: Stock = 14

    A->>T: get_product_price(SKU)
    T->>DB: Consultar precio
    DB-->>T: Precio unitario
    T-->>A: Precio

    A->>A: Comparar cantidad solicitada vs disponible

    A->>LLM: Generar respuesta con resultados
    LLM-->>A: Respuesta redactada

    A-->>API: Resultado
    API-->>UI: Respuesta final
    UI-->>U: Mostrar disponibilidad,<br/>faltante y subtotal posible