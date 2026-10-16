cola_pendientes = []   
pila_historial = []    
siguiente_id = 1


def mostrar_estado():
    print("\nPendientes:", cola_pendientes)
    print("Historial:", pila_historial)


# ---------- Funciones base ----------

def existe_pendiente(cliente, asunto):
    """Reto 5: True si ya hay una solicitud pendiente igual."""
    for s in cola_pendientes:
        if (s["cliente"].lower() == cliente.strip().lower()
                and s["asunto"].lower() == asunto.strip().lower()):
            return True
    return False


def registrar_solicitud(cliente, asunto):
    global siguiente_id
    if not cliente.strip() or not asunto.strip():
        return None

    solicitud = {
        "id": siguiente_id,
        "cliente": cliente.strip(),
        "asunto": asunto.strip(),
        "estado": "pendiente"
    }
    cola_pendientes.append(solicitud)      
    siguiente_id += 1
    return solicitud


def atender_siguiente():
    if not cola_pendientes:
        return None

    solicitud = cola_pendientes.pop(0)     
    pila_historial.append(solicitud)       
    return solicitud


def deshacer_ultima_atencion():
    if not pila_historial:
        return None

    solicitud = pila_historial.pop()       # sale la última atendida (LIFO)
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)   # vuelve al inicio de la cola
    return solicitud


# ---------- Retos ----------

def consultar_siguiente():
    """Reto 1: ver quién sigue sin sacarlo de la cola."""
    if not cola_pendientes:
        return None
    return cola_pendientes[0]


def buscar_por_id(id_buscado):
    """Reto 2: busca en pendientes y en historial. None si no existe."""
    for s in cola_pendientes:
        if s["id"] == id_buscado:
            return s
    for s in pila_historial:
        if s["id"] == id_buscado:
            return s
    return None


def cancelar_solicitud(id_buscado):
    """Reto 3: quita una solicitud pendiente sin alterar el orden de las demás."""
    for i, s in enumerate(cola_pendientes):
        if s["id"] == id_buscado:
            s["estado"] = "cancelada"
            return cola_pendientes.pop(i)
    return None


def deshacer_varias(cantidad):
    """Reto 4: deshace hasta 'cantidad' atenciones. Devuelve cuántas restauró."""
    restauradas = 0
    for _ in range(cantidad):
        if deshacer_ultima_atencion() is None:
            break
        restauradas += 1
    return restauradas


def estadisticas():
    """Reto 5: contadores."""
    return {
        "pendientes": len(cola_pendientes),
        "atendidas": len(pila_historial),
        "total_registradas": siguiente_id - 1
    }


# ---------- Menú ----------

def pedir_entero(mensaje):
    try:
        return int(input(mensaje))
    except ValueError:
        return None


def ejecutar_menu():
    while True:
        print("\n1. Registrar solicitud")
        print("2. Atender siguiente")
        print("3. Deshacer última atención")
        print("4. Mostrar estado")
        print("5. Consultar siguiente")
        print("6. Buscar por ID")
        print("7. Cancelar solicitud")
        print("8. Deshacer varias")
        print("9. Estadísticas")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            cliente = input("Cliente: ")
            asunto = input("Asunto: ")
            if existe_pendiente(cliente, asunto):
                print("Ya existe una solicitud pendiente igual")
            else:
                resultado = registrar_solicitud(cliente, asunto)
                print("Registrada:", resultado if resultado else "Datos inválidos")
        elif opcion == "2":
            print("Atendida:", atender_siguiente())
        elif opcion == "3":
            print("Restaurada:", deshacer_ultima_atencion())
        elif opcion == "4":
            mostrar_estado()
        elif opcion == "5":
            print("Siguiente:", consultar_siguiente())
        elif opcion == "6":
            id_b = pedir_entero("ID: ")
            print("Encontrada:", buscar_por_id(id_b) if id_b is not None else "ID inválido")
        elif opcion == "7":
            id_b = pedir_entero("ID a cancelar: ")
            print("Cancelada:", cancelar_solicitud(id_b) if id_b is not None else "ID inválido")
        elif opcion == "8":
            n = pedir_entero("¿Cuántas deshacer?: ")
            if n is None or n < 1:
                print("Número inválido")
            else:
                print("Restauradas:", deshacer_varias(n))
        elif opcion == "9":
            print(estadisticas())
        elif opcion == "0":
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    ejecutar_menu()