#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector
import logging

class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        pass
        #falta codi
    
    def desa(self, pelicula: Pelicula) -> Pelicula:
        #Aqui creamos la nueva pelicula creada.
        cursor = self._conn.cursor(buffered=True)
        consulta = "INSERT INTO PELICULA (titulo, anyo, puntuacion, votos) VALUES (%s, %s, %s, %s);"
        valors = (pelicula.titol, pelicula.anyo, pelicula.puntuacion, pelicula.votos)
        cursor.execute(consulta, valors)
        self._conn.commit()
        cursor.close()
        return pelicula
    
    def llegeix(self, any: int) -> List[Pelicula]:
        #Lista todas las peliculas por ANYO:
        cursor = self._conn.cursor(buffered=True)
        consulta = "SELECT id, titulo, anyo, puntuacion, votos FROM PELICULA WHERE anyo = %s;"
        cursor.execute(consulta, (any,))
        registres = cursor.fetchall()
        cursor.close()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
            resultat.append(pelicula)
        return resultat
    
    def canvia(self, id: int, nuevo_titulo: str) -> Pelicula:
        #Aqui modificamos el titulo de la pelicula segun su id y le añadimos un nuevo titulo.
        cursor = self._conn.cursor(buffered=True)
        consulta = "UPDATE PELICULA SET titulo = %s WHERE id = %s;"
        valors = (nuevo_titulo, id)
        cursor.execute(consulta, valors)
        self._conn.commit()
        cursor.close()
        return id
