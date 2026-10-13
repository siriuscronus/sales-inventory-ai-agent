# Estándar de Nombres y SKU de Productos

> Documento ficticio creado exclusivamente para el prototipo académico del
> Piedmont Metals Sales & Inventory AI Agent.
> No representa un estándar operativo oficial de PMONC.

## Objetivo

Definir criterios básicos de demostración para identificar productos
de forma consistente mediante SKU y nombres descriptivos.

## Principios generales

Cada producto deberá tener un SKU único.

El SKU deberá facilitar la identificación de características relevantes
del producto cuando sea posible.

Los nombres de productos deberán utilizar una descripción consistente
que permita diferenciarlos de productos similares.

## Ejemplo de SKU

Un I-Joist de 16 pulgadas de profundidad y 20 pies de longitud puede
representarse mediante:

IJOIST-16-20

Donde:

IJOIST identifica la familia del producto.

16 representa la profundidad nominal en pulgadas.

20 representa la longitud en pies.

## Lumber

Los productos de madera dimensional pueden utilizar el siguiente formato:

LUMBER-2X6-16

Donde:

LUMBER identifica la categoría.

2X6 representa las dimensiones nominales.

16 representa la longitud en pies.

## LVL

Las vigas LVL pueden utilizar un formato similar a:

LVL-175-16-14

Donde:

LVL identifica el tipo de producto.

175 representa un espesor nominal de 1.75 pulgadas.

16 representa la profundidad.

14 representa la longitud en pies.

## Reglas de búsqueda

Cuando un usuario no conozca el SKU exacto, el sistema podrá buscar utilizando:

nombre del producto,

categoría,

dimensiones,

longitud,

o descripción.

El sistema deberá devolver posibles coincidencias antes de asumir un SKU
cuando exista ambigüedad.

## Productos duplicados

Si existen múltiples registros que representan el mismo producto,
el sistema deberá evitar asumir automáticamente cuál es el registro correcto.

Los productos duplicados deberán ser identificados para revisión antes
de realizar procesos automatizados que dependan de inventario o precio.

## Nota

Este documento contiene únicamente información ficticia utilizada
para demostrar el funcionamiento de un sistema RAG.