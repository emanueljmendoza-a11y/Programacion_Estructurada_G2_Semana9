# Gestor de solicitudes: pilas y colas

**Autor:** Emanuel Mendoza

Sistema de atención de solicitudes de soporte técnico. Las solicitudes pendientes se atienden en orden de llegada (cola) y las atenciones recientes se registran para poder deshacerlas (pila). Está hecho con listas y funciones, sin clases.

## Archivos

- `app_consola.py`: versión de consola con menú.
- `logica.py`: cola, pila y funciones de negocio.
- `app.py`: rutas de Flask.
- `templates/index.html`: interfaz con Bootstrap.
- `requirements.txt`: dependencias (Flask).

## Cómo ejecutar

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir `http://127.0.0.1:5000`. Para la versión de consola: `python app_consola.py`.

## Retos resueltos

1. `consultar_siguiente()`: muestra el primer pendiente sin sacarlo de la cola.
2. `buscar_por_id()`: busca en pendientes y en el historial; devuelve `None` si no existe.
3. `cancelar_solicitud()`: elimina una solicitud pendiente sin alterar el orden de las demás.
4. `deshacer_varias()`: restaura varias atenciones y devuelve cuántas recuperó.
5. `estadisticas()` y `existe_pendiente()`: contadores y control de duplicados.

## ¿Por qué deshacer usa una pila y atender usa una cola?

Atender usa una cola (FIFO) porque las solicitudes deben resolverse en orden de llegada: la primera que llega es la primera que sale. Deshacer usa una pila (LIFO) porque lo último que se atendió es lo primero que se debe revertir. Si se deshiciera en otro orden, el historial quedaría desordenado y la solicitud restaurada perdería su prioridad original.

## Costo de `pop(0)` e `insert(0, ...)` y uso de `collections.deque`

En una lista de Python, `pop(0)` e `insert(0, ...)` tienen costo lineal, O(n), porque hay que desplazar todos los elementos restantes una posición. En una lista pequeña no se nota, pero con muchos elementos se vuelve lento.

`collections.deque` es una cola de dos extremos que hace `popleft()` y `appendleft()` en tiempo constante, O(1). Conviene usarlo cuando la cola es muy grande o hay muchas operaciones por segundo. En esta práctica se usan listas para entender primero cómo funcionan la cola y la pila, y `deque` queda como mejora posterior.

## ¿Qué cambiaría si hubiera solicitudes urgentes?

Una cola FIFO tradicional solo respeta el orden de llegada y no puede adelantar a nadie, así que una solicitud urgente tendría que esperar detrás de todas las anteriores. Para manejar prioridades se necesita una cola de prioridad, por ejemplo con el módulo `heapq`, que ordene primero por nivel de urgencia y, en caso de empate, por orden de llegada. Así las urgentes se atienden antes, y las del mismo nivel siguen siendo FIFO.
