# Agente de IA de Ventas e Inventario para Piedmont Metals

## Aviso académico

Este repositorio contiene un prototipo académico desarrollado exclusivamente con fines educativos y de demostración.

No constituye un sistema oficial de Piedmont Metals ni está conectado a ningún entorno de producción. Los productos, precios, cantidades de inventario, políticas y procedimientos utilizados en el proyecto son datos ficticios creados para demostrar el funcionamiento de la solución.

---

## Descripción

El **Agente de IA de Ventas e Inventario para Piedmont Metals** es un prototipo conversacional orientado a apoyar consultas relacionadas con ventas, inventario y procedimientos operativos.

El sistema permite consultar información como:

- disponibilidad de productos;
- precios;
- búsqueda por SKU o descripción;
- cotizaciones básicas;
- productos con bajo inventario;
- procedimientos y políticas internas de demostración.

El agente utiliza diferentes fuentes dependiendo del tipo de pregunta.

---

## Problema de negocio

En una operación comercial, el personal puede necesitar consultar información distribuida entre diferentes fuentes para responder preguntas como:

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

La solución utiliza la siguiente arquitectura simplificada:

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