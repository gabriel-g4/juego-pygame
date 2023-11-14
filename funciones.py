import pygame
import os
import sqlite3

def cargar_imagenes(path_parcial: str, lista_nombre_animaciones: list, scale: int)-> list:
    '''Carga todas las imagenes y animaciones del personaje enviado'''

    lista_animaciones = []

    for animacion in lista_nombre_animaciones:
        lista_temporal = []
        numero_frames = len(os.listdir(f"{path_parcial}\{animacion}"))
        for i in range(numero_frames):
            img = pygame.image.load(f"{path_parcial}\{animacion}\{i}.png").convert_alpha()
            img = pygame.transform.scale_by(img, scale)
            lista_temporal.append(img)
        lista_animaciones.append(lista_temporal)

    return lista_animaciones

def cargar_mundo(nivel)-> list:
    '''Devuelve una lista con los datos del nivel (tiles) que luego debe ser procesada.'''
    mapa_nivel = []
    with open(f"NIVELES\level{nivel}_data.csv", "r") as archivo:
        for linea in archivo:
            linea = linea.replace("\n", "")
            linea = linea.split(",")

            for i in range(len(linea)):
                linea[i] = int(linea[i])

            mapa_nivel.append(linea)

    return mapa_nivel


################SQLITE

def crear_tablas():
    with sqlite3.connect("database.db") as conexion:
        try:
        
            crear_tabla = ''' create table Puntajes
            (
            id integer primary key autoincrement,
            nombre text,
            score integer
            )
            '''
            conexion.execute(crear_tabla)
            print("se creo la tabla de scores")
        except sqlite3.OperationalError:
            print("La tabla ya existe")

def insertar(nombre, score):
    score = int(score)
    with sqlite3.connect("database.db") as conexion:
        try:
            conexion.execute("insert into Puntajes(nombre,score) values (?,?)", (nombre, score))

            conexion.commit()
            print("Se ejecuto correctamente")
        except:
            print("Error")

def limpiar_tabla():
    with sqlite3.connect("database.db") as conexion:
            try:
                conexion.execute("DELETE FROM Puntajes")

                conexion.commit()
                print("Se ejecuto correctamente")
            except:
                print("Error")

def seleccionar()-> list:
    '''Devuelve una lista de 10 tuplas ya ordenadas de mayor score a menor'''
    with sqlite3.connect("database.db") as conexion:
            seleccion = []
            try:
                cursor = conexion.execute("SELECT * FROM Puntajes ORDER BY score DESC LIMIT 5")
                for fila in cursor:
                    seleccion.append(fila)

                conexion.commit()
            except:
                print("Error")
                seleccion = None
            
            return seleccion

def eliminar_dato(id):
    with sqlite3.connect("database.db") as conexion:
        try:
            conexion.execute("DELETE FROM Puntajes WHERE id=?", (id))

            conexion.commit()
            print("Se ejecuto correctamente")
        except:
            print("Error")