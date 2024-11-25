import json
import os

# Archivo para guardar los usuarios
ARCHIVO_USUARIOS = "usuarios.json"

# Clase Registro para representar a un usuario
class Registro:
    def __init__(self, nombre, edad, email, contraseña):
        self.nombre = nombre
        self.edad = edad
        self.email = email
        self.contraseña = contraseña
        self.puntuacion_triqui = 0
        self.listas = {}

    def to_dict(self):
        # Convertir el objeto a un diccionario para guardarlo en el archivo JSON
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "email": self.email,
            "contraseña": self.contraseña,
            "puntuacion_triqui": self.puntuacion_triqui,
            "listas": self.listas
        }

    @classmethod
    def from_dict(cls, data):
        # Asegurarse de que los datos contienen todas las claves necesarias
        nombre = data.get('nombre', 'Desconocido')
        edad = data.get('edad', '0')
        email = data.get('email', 'noemail@example.com')
        contraseña = data.get('contraseña', '1234')
        return cls(nombre, edad, email, contraseña)

    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Email: {self.email}, Puntuación Triqui: {self.puntuacion_triqui}"


# Diccionario de usuarios, donde la clave es el nombre de usuario
usuarios = {}

# Cargar usuarios desde el archivo JSON
def cargar_usuarios():
    global usuarios
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as archivo:
            try:
                data = json.load(archivo)
                for usuario, datos in data.items():
                    # Crear un objeto Registro para cada usuario
                    usuarios[usuario] = Registro.from_dict(datos)
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. El archivo podría estar corrupto o vacío.")
                usuarios = {}  # Reseteamos los usuarios
    else:
        usuarios = {}

# Guardar usuarios en el archivo JSON
def guardar_usuarios():
    data = {}
    for usuario, registro in usuarios.items():
        data[usuario] = registro.to_dict()  # Convertimos el objeto en diccionario
    with open(ARCHIVO_USUARIOS, "w") as archivo:
        json.dump(data, archivo, indent=4)

# Registrar un usuario
def registrar_usuario():
    print("=== Registro de Usuario ===")
    usuario = input("Ingrese un nombre de usuario: ")
    if usuario in usuarios:
        print("El nombre de usuario ya está en uso.")
        return False

    nombre = input("Ingrese su nombre: ")
    edad = input("Ingrese su edad: ")
    email = input("Ingrese su correo electrónico: ")
    contraseña = input("Ingrese una contraseña: ")

    # Crear el objeto Registro y agregarlo al diccionario de usuarios
    usuarios[usuario] = Registro(nombre, edad, email, contraseña)
    guardar_usuarios()
    print("Usuario registrado con éxito!")
    return True

# Iniciar sesión
def iniciar_sesion():
    print("=== Inicio de Sesión ===")
    usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    if usuario in usuarios and usuarios[usuario].contraseña == contraseña:
        print("Inicio de sesión exitoso!")
        return usuario
    else:
        print("Credenciales incorrectas.")
        return None

# Crear un tablero inicial vacío para el juego de Triqui
def crear_tablero():
    return [' ' for _ in range(9)]

# Mostrar el tablero en pantalla
def mostrar_tablero(tablero):
    print(f"{tablero[0]} | {tablero[1]} | {tablero[2]}")
    print("--+---+--")
    print(f"{tablero[3]} | {tablero[4]} | {tablero[5]}")
    print("--+---+--")
    print(f"{tablero[6]} | {tablero[7]} | {tablero[8]}")

# Verificar si hay un ganador
def verificar_ganador(tablero, jugador):
    combinaciones = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # filas
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columnas
        (0, 4, 8), (2, 4, 6)              # diagonales
    ]
    for combo in combinaciones:
        if tablero[combo[0]] == tablero[combo[1]] == tablero[combo[2]] == jugador:
            return True
    return False

# Verificar si el tablero está lleno (empate)
def tablero_lleno(tablero):
    return ' ' not in tablero

# Ejecutar el juego de Triqui
def jugar_triqui(usuario_actual):
    print("=== Juego de Triqui ===")
    tablero = crear_tablero()
    jugador_actual = 'X'
    juego_terminado = False

    while not juego_terminado:
        mostrar_tablero(tablero)
        print(f"Turno del jugador {jugador_actual}")
        try:
            movimiento = int(input("Seleccione una casilla (1-9): ")) - 1
            if tablero[movimiento] == ' ':
                tablero[movimiento] = jugador_actual
            else:
                print("Casilla ocupada, elige otra.")
                continue
        except (IndexError, ValueError):
            print("Movimiento no válido, elige una casilla entre 1 y 9.")
            continue

        if verificar_ganador(tablero, jugador_actual):
            mostrar_tablero(tablero)
            print(f"¡El jugador {jugador_actual} ha ganado!")
            if jugador_actual == 'X':
                # Si 'X' gana, el usuario actual es el que tiene la puntuación aumentada
                usuarios[usuario_actual].puntuacion_triqui += 1
            guardar_usuarios()  # Guardar los datos de usuario con la puntuación actualizada
            juego_terminado = True
        elif tablero_lleno(tablero):
            mostrar_tablero(tablero)
            print("¡Es un empate!")
            juego_terminado = True
        else:
            jugador_actual = 'O' if jugador_actual == 'X' else 'X'

# Ver puntuaciones
def ver_puntuaciones():
    print("=== Puntuaciones de Triqui ===")
    for usuario, datos in usuarios.items():
        print(f"{usuario}: {datos.puntuacion_triqui} puntos")

# Crear una nueva lista para el usuario
def crear_lista(usuario):
    nombre_lista = input("Ingrese el nombre de la lista: ")
    if nombre_lista in usuarios[usuario].listas:
        print("La lista ya existe.")
    else:
        usuarios[usuario].listas[nombre_lista] = []
        guardar_usuarios()
        print(f"Lista '{nombre_lista}' creada con éxito.")

# Agregar un elemento a una lista
def agregar_a_lista(usuario):
    nombre_lista = input("Ingrese el nombre de la lista a la que desea agregar un elemento: ")
    if nombre_lista not in usuarios[usuario].listas:
        print(f"La lista '{nombre_lista}' no existe.")
    else:
        elemento = input("Ingrese el elemento a agregar: ")
        usuarios[usuario].listas[nombre_lista].append(elemento)
        guardar_usuarios()
        print(f"Elemento '{elemento}' agregado a la lista '{nombre_lista}'.")

# Eliminar una lista
def eliminar_lista(usuario):
    nombre_lista = input("Ingrese el nombre de la lista que desea eliminar: ")
    if nombre_lista not in usuarios[usuario].listas:
        print(f"La lista '{nombre_lista}' no existe.")
    else:
        del usuarios[usuario].listas[nombre_lista]
        guardar_usuarios()
        print(f"Lista '{nombre_lista}' eliminada con éxito.")

# Eliminar un elemento de una lista
def eliminar_elemento_lista(usuario):
    nombre_lista = input("Ingrese el nombre de la lista de la cual desea eliminar un elemento: ")
    if nombre_lista not in usuarios[usuario].listas:
        print(f"La lista '{nombre_lista}' no existe.")
    else:
        lista = usuarios[usuario].listas[nombre_lista]
        if not lista:
            print("La lista está vacía. No se pueden eliminar elementos.")
        else:
            print(f"Elementos en la lista '{nombre_lista}': {lista}")
            elemento = input("Ingrese el elemento que desea eliminar: ")
            if elemento in lista:
                lista.remove(elemento)
                guardar_usuarios()
                print(f"Elemento '{elemento}' eliminado de la lista '{nombre_lista}'.")
            else:
                print(f"El elemento '{elemento}' no está en la lista.")

# Ver las listas del usuario
def ver_listas(usuario):
    if not usuarios[usuario].listas:
        print("No tienes listas creadas.")
    else:
        print("Tus listas:")
        for nombre_lista, elementos in usuarios[usuario].listas.items():
            print(f"{nombre_lista}: {elementos}")

# Programa principal
def main():
    cargar_usuarios()
    print("Bienvenido al sistema de manejo de usuarios, listas y Triqui!")

    while True:
        print("\nSeleccione una opción:")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Ver puntuaciones de Triqui")
        print("4. Salir")

        opcion = input("Ingrese el número de la opción: ")

        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            usuario_actual = iniciar_sesion()
            if usuario_actual:
                while True:
                    print("\nOpciones de usuario:")
                    print("1. Jugar Triqui")
                    print("2. Crear una lista")
                    print("3. Agregar a una lista")
                    print("4. Eliminar una lista")
                    print("5. Eliminar un elemento de una lista")
                    print("6. Ver listas")
                    print("7. Volver al menú principal")

                    opcion_usuario = input("Seleccione una opción: ")

                    if opcion_usuario == '1':
                        jugar_triqui(usuario_actual)
                    elif opcion_usuario == '2':
                        crear_lista(usuario_actual)
                    elif opcion_usuario == '3':
                        agregar_a_lista(usuario_actual)
                    elif opcion_usuario == '4':
                        eliminar_lista(usuario_actual)
                    elif opcion_usuario == '5':
                        eliminar_elemento_lista(usuario_actual)
                    elif opcion_usuario == '6':
                        ver_listas(usuario_actual)
                    elif opcion_usuario == '7':
                        break
                    else:
                        print("Opción no válida.")
        elif opcion == '3':
            ver_puntuaciones()
        elif opcion == '4':
            print("Gracias por usar el sistema. ¡Adiós!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
