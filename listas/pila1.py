stack = []
pos = 0

def push(item, stack, size):
    global pos
    if pos < size:
        stack.append(item)
        pos += 1
        return "Item pushed successfully"
    else:
        return "Pila llena..."

def pop(stack):
    global pos
    if isEmpty(stack):
        return "La pila esta vacía..."
    pos -= 1
    return stack.pop()

def show(stack):
    if isEmpty(stack):
        return "La pila esta vacía..."
    my_stack = ""
    my_stack += "┌" + "-"*8 + "┐\n"
    my_stack += "| PILA   |\n"
    for item in reversed(stack):
        my_stack += f"|" + "-"*8 + "|\n"
        my_stack += f"| {item:>6} |\n"
    my_stack += "└" + "-"*8 + "┘"
    return my_stack

def peek(stack):
    if isEmpty(stack):
        return "La pila esta vacía..."
    return stack[-1]

def isEmpty(stack):
    return not stack

def len_stack(stack):
    if isEmpty(stack):
        return "La pila esta vacía..."
    return len(stack)


def menu():
    size = int(input("Dime el tamaño de la pila: "))
    
    while True:
        print("\n--- MENÚ PILA ---")
        print("1. Push (Agregar elemento)")
        print("2. Pop (Eliminar elemento)")
        print("3. Peek (Ver tope de la pila)")
        print("4. Check isEmpty (Ver si está vacía)")
        print("5. Size (Cantidad de elementos)")
        print("6. Show (Mostrar pila)")
        print("7. Salir")
        
        opcion = input("Selecciona una opción (1-7): ")

        if opcion == "1":
            item = input("Dime el valor a agregar: ")
            print(push(item, stack, size))

        elif opcion == "2":
            print(pop(stack))

        elif opcion == "3":
            print("Tope (peek):", peek(stack))

        elif opcion == "4":
            if isEmpty(stack):
                print("¿Está vacía?: Sí")
            else:
                print("¿Está vacía?: No")

        elif opcion == "5":
            print("Cantidad de elementos:", len_stack(stack))

        elif opcion == "6":
            print(show(stack))

        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")


menu()