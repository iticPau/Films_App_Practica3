#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector
import logging
from llistapelis import Llistapelis

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
    
    def totes_pag(self, id:int) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = f"SELECT * FROM PELICULA WHERE ID >= {id} LIMIT 10"
        cursor.execute(query)
        result = cursor.fetchall()
        resultat = []
        for peli in result:
            resultat.append(Pelicula(peli[1], peli[2], peli[3], peli[4], self, peli[0]))
        return resultat
    
    def desa(self, pelicula: Pelicula) -> bool:
        cursor = self._conn.cursor()
        query = f"INSERT INTO PELICULA (ID, TITULO, ANYO, PUNTUACION, VOTOS) VALUES ({pelicula.id},{pelicula.titol}, {pelicula.any}, {pelicula.puntuacio}, {pelicula.vots});"
        cursor.execute(query)
        self._conn.commit()
        cursor.close()
        return True
    
    def llegeix(self, anyo: int) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        consulta = "SELECT ID, TITULO, ANYO, PUNTUACION, VOTOS FROM PELICULA WHERE ANYO = %s;"
        cursor.execute(consulta, (anyo,))
        registres = cursor.fetchall()
        cursor.close()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1], registre[2], registre[3], registre[4], self, registre[0])
            resultat.append(pelicula)
        return resultat
    
    def canvia(self, lista:dict, id:int) -> bool:         
        cursor = self._conn.cursor(buffered=True)         
        if lista["selec"] == "titulo":             
            query = f"UPDATE PELICULA SET TITULO='{lista['valor']}' WHERE id = {id}"         
        cursor.execute(query)         
        self._conn.commit()         
        return True
