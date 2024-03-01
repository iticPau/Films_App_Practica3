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


def procesa_opcio(context):
    return {
        "0": lambda ctx : mostra_lent("Fins la propera"),
        "1": lambda ctx : mostra_llista(ctx['llistapelis']),
        "2": lambda ctx : mostra_llista(ctx['llistapelis']),
        "3": lambda ctx : mostra_llista(ctx['llistapelis']),
        "4": lambda ctx : mostra_llista(ctx['llistapelis'])
    }.get(context["opcio"], lambda ctx : mostra_lent("opcio incorrecta!!!"))(context)

def database_update(selec:str, lista_peli:dict = None, lista_modifica:dict = None, id:int = None) -> bool:
    logging.basicConfig(filename = 'pelicules.log', encoding = 'utf-8', level = logging.DEBUG)     
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)     
    persistencia = get_persistencies(la_meva_configuracio)     
    films = Llistapelis(persistencia["pelicula"])     
    if (films.escriu_al_disc(selec, lista_peli, lista_modifica, id)): return True

def database_read(selec:int, id:int = None, any:int = None):
    logging.basicConfig(filename = 'pelicules.log', encoding = 'utf-8', level = logging.DEBUG)
    la_meva_configuracio = get_configuracio(RUTA_FITXER_CONFIGURACIO)
    persistencia = get_persistencies(la_meva_configuracio)
    films = Llistapelis(persistencia["pelicula"])
    films.llegeix_de_disc(selec, id, any)
    return films


def bucle_principal(context):
    opcio = None
    while opcio != '0':
        print("0.- Salir de la aplicación.")
        print("1.- Mostrar películas")
        print("2.- Modificar titulo por id")
        print("3.- Crea una nueva pelicula")
        opcio = input("Elije una opción: ")
        if opcio == '1':
            print("1.- Mostrar las primeras 10 películas")
            print("2.- Mostrar películas por año")
            opcio = input("Elije una opción: ")
            if opcio == '1':
                id = input("Escribe la ID por donde quieres empezar: ")
                films = database_read(selec=opcio, id=id)
                context["llistapelis"] = films
                print(films)
                while True:
                    entrada = input("Presiona 10 para mostrar las siguientes 10 películas, o '0' para salir: ")
                    os.system('clear')
                    if entrada == '10':
                        id = films.ult_id
                        films = database_read(selec=opcio, id = id)
                        context["llistapelis"] = films
                        print(films)
                    elif entrada == '0':
                        break
                    else:
                        print("Entrada no válida")
            elif opcio == '2':
                any = input("Escribe un ANYO para buscar las películas: ")
                films = database_read(selec=opcio, any=any)
                print(films)
                context["llistapelis"] = films
                input("Presiona Enter para continuar:")
        elif opcio == '2':             
                id = input("Escribe el ID de la pelicula para cambiar:")             
                lista_modificada = input("Escribe TITULO en minusuculas para poder cambiar-lo:")             
                nuevo_valor = input("Escribe el nuevo TITULO:")             
                lista = {"selec":lista_modificada, "valor": nuevo_valor}                         
                if database_update(selec = "modificar", lista_modifica = lista, id = id): 
                    print("¡Pelicula modificada!")             
                input("Presiona Enter para continuar:")
        elif opcio == '3':
            id = input("Escribe el ID de la nueva pelicula: ")
            lista_peli = {"id":None, "titol": None, "any":None, "puntuacio":None, "vots":None}
            lista_peli["id"] = id
            lista_peli["titol"] = input("Escribe el TITULO de la nueva pelicula: ")
            lista_peli["any"] = input("Escribe el ANYO de la nueva pelicula: ")
            lista_peli["puntuacio"] = input("Escribe la PUNTUACION de la nueva pelicula: ")
            lista_peli["vots"] = input("Escribe los VOTOS de la nueva pelicula: ")
            if database_update(selec="crear", lista_peli=lista_peli, id=id): 
                print("¡Pelicula añadida!")             
            input("Presiona Enter para continuar:")
        elif opcio != '0':
            print("OPCIÓN INCORRECTA")
    print("¡SALIR!")


def main():
    context = {"llistapelis": None}
    landing_text()
    bucle_principal(context)


if __name__ == "__main__":
    main()
