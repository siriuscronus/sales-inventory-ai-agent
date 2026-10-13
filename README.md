# Piedmont Metals Sales & Inventory AI Agent

## Descripción

Piedmont Metals Sales & Inventory AI Agent es un prototipo de agente de inteligencia artificial diseñado para apoyar las operaciones comerciales, de inventario y atención interna de PMONC.

El objetivo del sistema es permitir que empleados autorizados puedan consultar información relacionada con productos, inventario, precios, cotizaciones y políticas operativas mediante una interfaz conversacional.

El agente combinará:

- una base de datos operativa para inventario, productos y precios,
- herramientas (tools) para ejecutar consultas específicas,
- una base de conocimiento mediante RAG,
- un modelo de lenguaje para interpretar solicitudes y generar respuestas,
- y, en una fase posterior, integración mediante MCP con otros sistemas empresariales.

---

## Problemática

PMONC maneja productos y materiales utilizados en proyectos de construcción y operaciones comerciales.

Parte de la información necesaria para atender una venta o preparar una cotización puede encontrarse distribuida entre diferentes fuentes, procesos y sistemas.

Entre los principales retos se encuentran:

- consultar disponibilidad real de productos,
- verificar precios,
- identificar productos mediante SKU,
- detectar inconsistencias o duplicidades en nombres y códigos,
- preparar cálculos para cotizaciones,
- consultar procedimientos internos,
- determinar productos con bajo inventario,
- localizar rápidamente información relevante para ventas y operaciones.

Actualmente, muchas de estas consultas requieren intervención manual y conocimiento específico del personal.

El prototipo busca demostrar cómo un agente de IA puede centralizar estas consultas y facilitar el acceso a información operativa.

---

## Objetivo

Construir un agente de inteligencia artificial capaz de interpretar preguntas relacionadas con las operaciones de Piedmont Metals y decidir automáticamente qué fuente de información debe consultar.

El agente deberá ser capaz de utilizar:

- Tools para información operativa,
- una base de datos para productos, inventario y precios,
- RAG para políticas, procedimientos y documentación,
- un LLM para interpretar preguntas y generar respuestas,
- MCP como futura capa estándar de integración con herramientas empresariales.

---

## Alcance del prototipo

El MVP se concentrará inicialmente en cuatro capacidades principales:

1. Consultar inventario.
2. Consultar precios.
3. Calcular cotizaciones básicas.
4. Consultar políticas y procedimientos internos.

El prototipo utilizará datos simulados o anonimizados para evitar publicar información comercial sensible de PMONC.

---

## Casos de uso

### UC01 - Consultar inventario

Ejemplo:

> ¿Cuántos I-Joists de 16 pulgadas de profundidad y 20 pies de largo tenemos disponibles?

El agente deberá identificar el producto y utilizar una Tool para consultar la base de datos de inventario.

Respuesta esperada:

> Actualmente hay 14 unidades disponibles en inventario.

---

### UC02 - Consultar precio

Ejemplo:

> ¿Cuál es el precio actual del OSB 23/32 de 4x8?

El agente utilizará una Tool para consultar el precio asociado al producto.

---

### UC03 - Calcular una cotización

Ejemplo:

> Necesito 10 unidades de OSB 23/32 de 4x8. ¿Tenemos suficiente inventario y cuál sería el subtotal?

El agente deberá:

1. identificar el producto,
2. consultar inventario,
3. consultar precio,
4. verificar disponibilidad,
5. calcular el subtotal,
6. generar una respuesta consolidada.

---

### UC04 - Consultar políticas y procedimientos

Ejemplo:

> ¿Cuál es el procedimiento cuando un producto solicitado no tiene suficiente inventario?

El agente utilizará RAG para consultar la base de conocimiento de Piedmont Metals.

---

### UC05 - Detectar productos con bajo inventario

Ejemplo:

> ¿Qué productos necesitan reposición?

El agente ejecutará una Tool que identifique productos cuyo inventario se encuentre por debajo del nivel mínimo definido.

---

### UC06 - Buscar productos

Ejemplo:

> Busca productos relacionados con I-Joists de 20 pies.

El agente podrá consultar el catálogo utilizando descripción, SKU, dimensiones u otros atributos.

---

## Arquitectura lógica inicial

```text
Usuario
   |
   v
Interfaz Web / Chat
   |
   v
FastAPI Backend
   |
   v
Piedmont Metals AI Agent
   |
   +------> Tools
   |          |
   |          +--> Consultar inventario
   |          +--> Consultar precio
   |          +--> Calcular cotización
   |          +--> Detectar bajo inventario
   |          |
   |          v
   |       SQLite
   |
   +------> RAG
   |          |
   |          v
   |       Qdrant
   |          |
   |          v
   |   Base de Conocimiento
   |
   v
LLM