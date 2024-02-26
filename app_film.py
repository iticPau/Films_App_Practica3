import os, yaml, sys, time, json
from persistencia_pelicula_mysql import Persistencia_pelicula_mysql
from llistapelis import Llistapelis
import logging

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
RUTA_FITXER_CONFIGURACIO = os.path.join(THIS_PATH, 'configuracio.yml') 
print(RUTA_FITXER_CONFIGURACIO)

def get_configuracio(ruta_fitxer_configuracio) -> dict:
    config = {}
    with open(ruta_fitxer_configuracio, 'r') as conf:
        config = yaml.safe_load(conf)
    return config

def get_persistencies(conf: dict) -> dict:
    credencials = {}
    if conf["base de dades"]["motor"].lower().strip() == "mysql":
        credencials['host'] = conf["base de dades"]["host"]
        credencials['user'] = conf["base de dades"]["user"]
        credencials['password'] = conf["base de dades"]["password"]
        credencials['database'] = conf["base de dades"]["database"]
        return {
            'pelicula': Persistencia_pelicula_mysql(credencials)
        }
    else:
        return {
            'pelicula': None
        }
    
def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()


def landing_text():
    os.system('clear')
    print("Benvingut a la app de pel·lícules")
    time.sleep(1)
    msg = "Desitjo que et sigui d'utilitat!"
    mostra_lent(msg)
    input("Prem la tecla 'Enter' per a continuar")
    os.system('clear')

def mostra_lent(missatge, v=0.05):
    for c in missatge:
        print(c, end='')
        sys.stdout.flush()
        time.sleep(v)
    print()

def mostra_llista(llistapelicula):
    os.system('clear')
    mostra_lent(json.dumps(json.loads(llistapelicula.toJSON()), indent=4), v=0.01)

def mostra_seguents(llistapelicula):
    os.system('clear')

def mostra_menu():
    print("0.- Salir")
    print("1.- Muestra las 10 primeras peliculas: ")
    print("2.- Muestra peliculas segun el anyo: ")
    print("3.- Afageix una nova pelicula: ")
    print("4.- Cambia el titulo de la pelicula por ID: ")

def mostra_menu_next10():
    print("0.- Salir")
    print("2.- Muestra las siguentes 10 peliculas")


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis']),
        "2": lambda ctx : mostra_llista(ctx['llistapelis']),
        "3": lambda ctx : mostra_llista(ctx['llistapelis']),
        "4": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_read(context:dict, id:int = None, anyo:int = None):
    logging.basicConfig(filename='pelicules.log', encoding='utf-8', level=logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencia = get_persistencies(la_meva_configuracio)
    films = Llistapelis(persistencia["pelicula"])
    films.llegeix_de_disc(context, id, anyo)
    return films

def bucle_principal(context):
    opcio = None
    films = None

    while opcio != '0':
        mostra_menu()
        opcio = input("Selecciona una opció: ")
        context["opcio"] = opcio
        if context["opcio"] == '1':
            id = input("Introduce una ID para poder empezar: ")
            films = database_read(context, id = id)
            mostra_menu_next10()                
        elif context["opcio"] == '2':
            anyo = input("Introduce un ANYO para buscar las pelis de ese anyo: ")
            films = database_read(None, anyo, context)
        elif context["opcio"] == '3':
            titol = input("El TITULO para la nueva pelicula: ")
            anyo = input("El ANYO para la nueva pelicula: ")
            puntuacion = input("La PUNTUACION para la nueva pelicula: ")
            votos = input("Los VOTOS para la nueva pelicula: ")
            films = database_read(None, anyo, titol, puntuacion,votos, context)
        context["llistapelis"] = films
        if films is not None:
            procesa_opcio(context)
            #falta codi


def main():
    context = {
        "llistapelis": None
    }
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
