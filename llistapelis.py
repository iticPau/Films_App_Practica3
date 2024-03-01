#!/bin/usr/python3

import json
from typing import List
from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula

class Llistapelis():
    def __init__ (self, persistencia_pelicula: IPersistencia_pelicula) -> None:
        self._pelicules = List[Pelicula]
        self._ult_id = 0
        self._persistencia_pelicula:IPersistencia_pelicula = persistencia_pelicula
        
    @property
    def pelicules(self) -> List[Pelicula]:
        return self._pelicules
    
    @property
    def ult_id(self) -> int:
        return self._ult_id

    @property
    def persistencia_pelicula(self) -> IPersistencia_pelicula:
        return self._persistencia_pelicula
    
    def __repr__(self):
        return self.toJSON()
    
    def toJSON(self):
        pelicules_dict = []
        for pelicula in self._pelicules:
            pelicules_dict.append(json.loads(pelicula.toJSON()))
        self_dict = {
            "pelicules": pelicules_dict
            }   
        return json.dumps(self_dict)

    def llegeix_de_disc(self, selec:int, id:int = None, any:int = None):
        if selec == '1':
            self._pelicules = self._persistencia_pelicula.totes_pag(id)
            self._ult_id = int(id) + 10
        elif selec == '2':
            self._pelicules = self._persistencia_pelicula.llegeix(any)
            
    def escriu_al_disc(self, selec:str, lista_peli:dict = None, lista_modificada:dict = None, id:int = None):         
        if selec == "crear":             
            peli = Pelicula(**lista_peli, persistencia = self._persistencia_pelicula)             
            if self._persistencia_pelicula.desa(peli): return True         
        if selec == "modificar":             
                if self._persistencia_pelicula.canvia(lista_modificada, id): return True 
