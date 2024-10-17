"""
primero instala las librerías necesarias
para ejecutar el programa correctamente

comandos:
pip install requests
"""
import requests
import os
import json
import glob

#declaración de errores
class BajoError(Exception):
    pass
class AltoError(Exception):
    pass
class SinFavoritosError(Exception):
    pass
class PokemonNoFavoritoError(Exception):
    pass

class Pokemon:
    def __init__(self, nombre: str, id: int):
        self.nombre = nombre
        self.id = id

    def toString(self):
        print(f"Nº: {self.id} - Nombre: {str(self.nombre).capitalize()}")

"""
las siguientes funciones dan funcionalidad
al menú de la aplicación
"""
#función para buscar pokémon dentro de la pokeapi
def buscar_pokemon(data1, data2):

    print("\n--- DATOS GENERALES ---")
    print("Nombre: ", str(data1["species"]["name"]).capitalize())
    print("Número en la Pokédex Nacional: ", data1["id"])
    print("Peso: ", float(data1["weight"]/10), "kg")
    print("Altura: ", float(data1["height"]/10), "m")
    print("Tipo(s): ")
    for type in data1["types"]:
        print(str(traductor_tipo(type["type"]["name"])).capitalize())
    
    print("\n--- ENTRADAS EN LA POKÉDEX ---")
    #filtra las descripciones de la pokédex para mostrar solo las que estén en español
    for i in range(1, len(data2["flavor_text_entries"])):
        if data2["flavor_text_entries"][i]["language"]["name"] == "es":
            print("\n", traductor_titulo(data2["flavor_text_entries"][i]["version"]["name"]), ": ",data2["flavor_text_entries"][i]["flavor_text"])

#función para registrar un pokémon como favorito
def guardar_pokemon(data1, data2):

    json_file1 = f"{(data1["species"]["name"])}1.json"
    json_file2 = f"{(data1["species"]["name"])}2.json"

    if not os.path.exists("./pokemon_favoritos"):
        os.mkdir("./pokemon_favoritos")

    with open(f"./pokemon_favoritos/{json_file1}", "w") as json_data:
        json.dump(data1, json_data)
    with open(f"./pokemon_favoritos/{json_file2}", "w") as json_data:
        json.dump(data2, json_data)

    print("\n--- AÑADIDO ---")
    print(f"{str(data1["species"]["name"]).capitalize()} se ha registrado entre tus pokémon favoritos")

#función para borrar un pokémon de favoritos
def borrar_pokemon(data1):

    try:
        no_favorito(data1)
        sin_favoritos()

        os.remove(f"./pokemon_favoritos/{(data1["species"]["name"])}1.json")
        os.remove(f"./pokemon_favoritos/{(data1["species"]["name"])}2.json")

        print("\n--- ELIMINADO ---")
        if os.path.exists("./pokemon_favoritos") and os.path.isdir("./pokemon_favoritos") and not os.listdir("./pokemon_favoritos"):
            os.rmdir("./pokemon_favoritos")
        print(f"{str(data1["species"]["name"]).capitalize()} se ha eliminado de tus pokémon favoritos")

    except PokemonNoFavoritoError:
        print(f"{str(data1["species"]["name"]).capitalize()} no está en tu lista de favoritos")

    except SinFavoritosError:
        print("No tienes ningún pokémon registrado como favorito")

#función para mostrar la lista de pokémon favoritos
def mostrar_lista():

    try:
        sin_favoritos()

        print("\n--- TUS POKÉMON FAVORITOS ---")
        contador = 0 #contador para obviar los archivos [nombre_pokemon]2.json
        for archivo in glob.glob("./pokemon_favoritos/*", recursive=True):
            if (contador % 2):
                with open(archivo, "r") as json_data:   
                    pokedata = json.load(json_data) #creamos el diccionario pokedata

                    nombre = pokedata["name"]
                    id = pokedata["id"]
                    
                    pokemon = Pokemon(nombre, id)
                    pokemon.toString()
            contador += 1

    except SinFavoritosError:
        print("No tienes ningún pokémon registrado como favorito")

#función para calcular la efectividad de ataques de determinado tipo contra el pokémon escogido
def calculadora(data1):
    tipo_ofensivo = input("\n--- LISTA DE TIPOS ---"
        "\nNormal, Lucha, Volador, Veneno, Tierra,"
        "\nRoca, Bicho, Fantasma, Acero, Fuego,"
        "\nAgua, Planta, Eléctrico, Psíquico,"
        "\nHielo, Dragón, Siniestro, Hada\n"
        "\nElige el tipo del movimiento: ").lower().capitalize()
    print("")
    
    base = 1
    daño = 1

    #funciones de cálculo de daño por cada tipo
    supereficaz = lambda x: x * 2
    poco_eficaz = lambda x: x / 2
    neutro = lambda x: x
    inmune = lambda x: x * 0

    for type in data1["types"]:
        tipo_defensivo = str(traductor_tipo(type["type"]["name"])).capitalize()
        match(tipo_ofensivo):
            case "Normal":
                match(tipo_defensivo):
                    case "Acero" | "Roca" :
                        daño = daño * poco_eficaz(base)
                    case "Fantasma":
                        daño = daño * inmune(base)
                    case _:
                        daño = daño * neutro(base)
            case "Lucha":
                match(tipo_defensivo):
                    case "Acero" | "Hielo" | "Normal" | "Roca" | "Siniestro":
                        daño = daño * supereficaz(base)
                    case "Bicho" | "Hada" | "Psíquico" | "Veneno" | "Volador":
                        daño = daño * poco_eficaz(base)
                    case "Fantasma":
                        daño = daño * inmune(base)
                    case _:
                        daño = daño * neutro(base)
            case "Volador":
                match(tipo_defensivo):
                    case "Bicho" | "Lucha" | "Planta":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Eléctrico" | "Roca":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Veneno":
                match(tipo_defensivo):
                    case "Planta" | "Hada":
                        daño = daño * supereficaz(base)
                    case "Fantasma" | "Roca" | "Tierra" | "Veneno":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Tierra":
                match(tipo_defensivo):
                    case "Acero" | "Eléctrico" | "Roca" | "Veneno" | "Fuego":
                        daño = daño * supereficaz(base)
                    case "Bicho" | "Planta":
                        daño = daño * poco_eficaz(base)
                    case "Volador":
                        daño = daño * inmune(base)
                    case _:
                        daño = daño * neutro(base)
            case "Roca":
                match(tipo_defensivo):
                    case "Bicho" | "Fuego" | "Hielo" | "Volador":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Lucha" | "Tierra":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Bicho":
                match(tipo_defensivo):
                    case "Planta" | "Psíquico" | "Siniestro":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Fantasma" | "Fuego" | "Hada" | "Lucha" | "Veneno" | "Volador":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Fantasma":
                match(tipo_defensivo):
                    case "Fantasma" | "Psíquico":
                        daño = daño * supereficaz(base)
                    case "Siniestro":
                        daño = daño * poco_eficaz(base)
                    case "Normal":
                        daño = daño * inmune(base)
                    case _:
                        daño = daño * neutro(base)
            case "Acero":
                match(tipo_defensivo):
                    case "Hada" | "Hielo" | "Roca":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Agua" | "Eléctrico" | "Fuego":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Fuego":
                match(tipo_defensivo):
                    case "Acero" | "Bicho" | "Hielo" | "Planta":
                        daño = daño * supereficaz(base)
                    case "Agua" | "Dragón" | "Fuego" | "Roca":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Agua":
                match(tipo_defensivo):
                    case "Fuego" | "Roca" | "Tierra":
                        daño = daño * supereficaz(base)
                    case "Agua" | "Dragón" | "Planta":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Planta":
                match(tipo_defensivo):
                    case "Agua" | "Roca" | "Tierra":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Bicho" | "Dragón" | "Fuego" | "Planta" | "Veneno" | "Volador":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Eléctrico":
                match(tipo_defensivo):
                    case "Agua" | "Volador":
                        daño = daño * supereficaz(base)
                    case "Dragón" | "Eléctrico" | "Planta":
                        daño = daño * poco_eficaz(base)
                    case "Tierra":
                        daño = daño * inmune(base)
                    case _:
                        daño = daño * neutro(base)
            case "Psíquico":
                match(tipo_defensivo):
                    case "Lucha" | "Veneno":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Psíquico":
                        daño = daño * poco_eficaz(base)
                    case "Siniestro":
                        daño = daño * inmune(base)
                    case _:
                        daño = daño * neutro(base)
            case "Hielo":
                match(tipo_defensivo):
                    case "Dragón" | "Planta" | "Tierra" | "Volador":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Agua" | "Fuego" | "Hielo":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Dragón":
                match(tipo_defensivo):
                    case "Dragón":
                        daño = daño * supereficaz(base)
                    case "Acero":
                        daño = daño * poco_eficaz(base)
                    case "Hada":
                        daño = daño * inmune(base)
                    case _:
                        daño = daño * neutro(base)
            case "Siniestro":
                match(tipo_defensivo):
                    case "Fantasma" | "Psíquico" | "Roca" | "Veneno" | "Fuego":
                        daño = daño * supereficaz(base)
                    case "Hada" | "Lucha" | "Siniestro":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
            case "Hada":
                match(tipo_defensivo):
                    case "Dragón" | "Lucha" | "Siniestro":
                        daño = daño * supereficaz(base)
                    case "Acero" | "Fuego" | "Veneno":
                        daño = daño * poco_eficaz(base)
                    case _:
                        daño = daño * neutro(base)
    
    if (daño == 4):
        print("¡¡ES SUPEREFICAZ!!")
    if (daño == 2):
        print("¡Es supereficaz!")
    if (daño == 0.5):
        print("No es muy eficaz")
    if (daño == 0.25):
        print("No es muy eficaz...")
    print(f"{str(data1["species"]["name"]).capitalize()} recibe daño x{daño} de los movimientos de tipo {tipo_ofensivo}")


"""
las siguientes son funciones auxiliares
para evitar código duplicado
"""
#función que recoge los datos de la api y los pasa a otra función que los manejará
def cargar_datos(opcion):

    pokemon = input("\nIntroduce el nombre o el ID del pokémon: ").lower()
    respuesta1 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")

    try:
        if respuesta1.status_code == 200:
            data1 = respuesta1.json()
            respuesta2 = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{data1["species"]["name"]}/")
            data2 = respuesta2.json()

            match opcion:
                case "1":
                    buscar_pokemon(data1, data2)
                case "2":
                    guardar_pokemon(data1, data2)
                case "3":
                    borrar_pokemon(data1)
                case "5":
                    calculadora(data1)
        else:
            pokemon_inexistente(int(pokemon))

    except BajoError:
        print("No existe un pokémon con ID 0")

    except AltoError:
        print("No existen más de 1025 pokémon")

    except ValueError:
        print("El pokémon introducido no existe")


"""
las siguientes funciones traducen
partes de la api que están en
inglés para un mejor entendimiento
"""
#función que traduce al español los tipos de los pokémon
def traductor_tipo(tipo):
    match tipo:
        case "normal":
            return "normal"
        case "fighting":
            return "lucha"
        case "flying":
            return "volador"
        case "poison":
            return "veneno"
        case "ground":
            return "tierra"
        case "rock":
            return "roca"
        case "bug":
            return "bicho"
        case "ghost":
            return "fantasma"
        case "steel":
            return "acero"
        case "fire":
            return "fuego"
        case "water":
            return "agua"
        case "grass":
            return "planta"
        case "electric":
            return "electrico"
        case "psychic":
            return "psíquico"
        case "ice":
            return "hielo"
        case "dragon":
            return "dragón"
        case "dark":
            return "siniestro"
        case "fairy":
            return "hada"
        case "unknown":
            return "desconocido"
        case "shadow":
            return "sombrío"

#función que traduce al español los títulos de los juegos de las descripciones de la pokédex
def traductor_titulo(titulo):
    match(titulo):
        case "red":
            return "Pokémon Edición Roja"
        case "blue":
            return "Pokémon Edición Azul"
        case "yellow":
            return "Pokémon Edición Amarilla"
        case "gold":
            return "Pokémon Edición Oro"
        case "silver":
            return "Pokémon Edición Plata"
        case "crystal":
            return "Pokémon Edición Cristal"
        case "ruby":
            return "Pokémon Edición Rubí"
        case "sapphire":
            return "Pokémon Edición Zafiro"
        case "emerald":
            return "Pokémon Edición Esmeralda"
        case "firered":
            return "Pokémon Edición Rojo Fuego"
        case "leafgreen":
            return "Pokémon Edición Verde Hoja"
        case "diamond":
            return "Pokémon Edición Diamante"
        case "pearl":
            return "Pokémon Edición Perla"
        case "platinum":
            return "Pokémon Edición Platino"
        case "heartgold":
            return "Pokémon Edición Oro HeartGold"
        case "soulsilver":
            return "Pokémon Edición Plata SoulSilver"
        case "black":
            return "Pokémon Edición Negra"
        case "white":
            return "Pokémon Edición Blanca"
        case "black-2":
            return "Pokémon Edición Negra 2"
        case "white-2":
            return "Pokémon Edición Blanca 2"
        case "x":
            return "Pokémon X"
        case "y":
            return "Pokémon Y"
        case "omega-ruby":
            return "Pokémon Rubí Omega"
        case "alpha-sapphire":
            return "Pokémon Zafiro Alfa"
        case "sun":
            return "Pokémon Sol"
        case "moon":
            return "Pokémon Luna"
        case "ultra-sun":
            return "Pokémon Ultra Sol"
        case "ultra-moon":
            return "Pokémon Ultra Luna"
        case "lets-go-pikachu":
            return "Pokémon Let's Go Pikachu"
        case "lets-go-eevee":
            return "Pokémon Let's Go Eevee"
        case "shield":
            return "Pokémon Escudo"
        case "sword":
            return "Pokémon Espada"
        case "legends-arceus":
            return "Pokémon Leyendas Arceus"
        case _:
            return titulo

"""
las siguientes funciones controlan
posibles errores en la ejecución
del código
"""
#función para controlar que se introduzca un número que exista en la pokédex
def pokemon_inexistente(numero: int):
    if numero == 0:
        raise BajoError()
    elif numero >= 1026:
        raise AltoError()
    
#función para controlar si el pokémon no está registrado en favoritos
def no_favorito(data1):
    if os.path.exists("./pokemon_favoritos") and not os.path.isfile(f"./pokemon_favoritos/{(data1["species"]["name"])}1.json") and not os.path.isfile(f"./pokemon_favoritos/{(data1["species"]["name"])}2.json"):
        raise PokemonNoFavoritoError()

#función para controlar si no hay pokémon favoritos registrados
def sin_favoritos():
    if not os.path.exists("./pokemon_favoritos"):
        raise SinFavoritosError()


"""
#MENÚ DEL PROGRAMA
"""
while True:
    print("\n\n--- POKÉDEX ---")
    print("1. Buscar pokémon")
    print("2. Guardar pokémon como favorito")
    print("3. Eliminar un pokémon de favoritos")
    print("4. Mostrar lista de favoritos")
    print("5. Calcular efectividad")
    print("6. Salir")

    opcion = input("\nSelecciona una opción: ")

    match opcion:
        case "1" | "2" | "3" | "5":
            cargar_datos(opcion)
        case "4":
            mostrar_lista()
        case "6":
            print("Se ha cerrado la Pokédex")
            break
        case _:
            print("Opción no válida. Elige una opción del 1 al 6.")