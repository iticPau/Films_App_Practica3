PREGUNTES:
¿Què fan els mètodes get_configuracio i get_persistències? 
El mètode get_configuration llegeix la configuració de l'aplicació d'un fitxer YAML i la torna com a diccionari de Python. 
El mètode get_persistencies està basat en configuració, torna un diccionari amb les instàncies necessàries per a la persistència de les dades de l'aplicació. Això pot incloure connexions a bases de dades, fitxers, etc. 

A processa_opcio veureu instruccions com aquestes: 
return { "0": lambda ctx : mostra_lent("Fins a la propera"), "1": lambda ctx : mostra_llista(ctx['listapelis']) } 
¿Què fa lambda? Com podria reescriure el codi sense fer servir lambda? Quina utilitat troba a fer servir lambda? 
Lambda és una funció anònima a Python que es pot utilitzar per definir funcions petites i simples en una sola línia de codi. El mateix codi es podria reescriure utilitzant funcions normalment definides: 
def opcio_0(ctx): show_slow("Fins a la propera") 
def opcio_1(ctx): show_list(ctx['listapelis']) 

¿Penseu que s'ha desacoblat prou la lògica de negoci de la lògica d'aplicació? Raoneu la resposta i digueu si hi ha alguna millora que es pugui fer. 
La lògica de negoci està parcialment desacoblada de la lògica de l'aplicació, ja que hi ha una separació entre les funcions relacionades amb la gestió de bases de dades i les funcions relacionades amb la interacció dels usuaris.