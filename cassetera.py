#!/usr/bin/env python
""" 
Programa principal de Cassetera (Cableoperador Antigua Solicita Subvalorar 
Elementos Tecnológicamente Evolucionados en Recursos Analógicos).

Sirve para crear un proceso de batch que convierta todos los archivos de video
ubicados en config['rutaleer'] en el formato requerido por un cableoperador
para su distribución en una señal analógica y la consiguiente aplicación de la mosca.


"""


# IMPORTS (NO TOCAR)
from colorama import Back, Fore, init
import requests
import json
import os
import sys
from time import sleep
from os import listdir
from os.path import isfile, join
import subprocess
from subprocess import Popen 
clear = lambda: os.system('cls')

init()


# CREDITOS
__author__ = "Ignacio Tula"
__copyright__ = "Ignacio Tula, Logos Consultora, Logosfera, Zero, 2018"
__credits__ = ["Ignacio Tula", "Tamara Polo"]
__license__ = "AGPL"
__version__ = "1.0.1"
__maintainer__ = "Ignacio Tula"
__email__ = "itula@logos.net.ar"
__status__ = "Prototipo"


# CONFIGURACIÓN (MODIFICAR SEGÚN SEA NECESARIO)
config = {}

    #Cambiar estos valores para indiquen una ruta válida
config['rutaffmpeg'] = "C:\\DMAOPS\\FFMPEG\\ffmpeg.exe"
config['rutaleer'] =  ""
config['rutainter'] = "D:\\\\inter\\"
config['rutaexport'] = "D:\\\\export\\"
config['moscapal'] = "C:\\DMAOPS\\ASSETS\\moscaPAL.png"

    #No cambiar este valor
config['marcaError'] = 0
    # Esto se puede adecuar para que sea ntsc o pal
config['filtroffmpeg'] = '-filter:v "pad=iw:iw*3/4:(ow-iw)/2:(oh-ih)/2,scale=720:576" -c:a copy'
config['metadata'] = '-map_metadata 0 -metadata comment=\"www.logos.net.ar ESTUVO AQUI. Mediante prototipo Cassetera. Ondemand. LOGOS\"'

# OTRAS VARIABLES PARA INICIALIZAR
listadoArchivo = []





#
#
# DEFINICIÓN DE FUNCIONES
#
#



#
# MANEJO DE ARCHIVOS
#

# Guardar los archivos mp4 y mov en la lista 
def obtenerArchivosDeDirectorio(rutaLeer):

    for i in listdir(rutaLeer):    
        
        rutaCompletaArchivoActual = rutaLeer + "\\" + i
        
        if (isfile(rutaCompletaArchivoActual) and esteArchivoEsVideo(i)):
            
            print( Back.BLACK + Fore.WHITE + "\n Agregando " + Fore.LIGHTBLUE_EX + i + Fore.WHITE + ".")
            listadoArchivo.append(rutaCompletaArchivoActual)
        
        else:
            
            print( Fore.RED + "\n La entrada " + i + " no es un archivo de video")

    return listadoArchivo


def crearComandoDeConversionPal(archivo):
    cadena =  "\"" + config['rutaffmpeg'] + "\""
    cadena += " -y -i " + "\"" + archivo + "\""
    cadena += " " + config['filtroffmpeg'] + " -c:v libx264 -r 25 -b:v 3M -maxrate 5M -bufsize 5M -pass 1"
    cadena += " " + "\"" +  archivo.replace(config['rutaleer'],config['rutainter']) + "\""
    return cadena


def crearComandoDeSuperposicionDeMosca(archivo):
    cadena =  "\"" + config['rutaffmpeg'] + "\""
    cadena += " -y -i " + "\"" + archivo.replace(config['rutaleer'],config['rutainter']) + "\""
    cadena += " -i " + "\"" +  config['moscapal'] + "\"" 
    cadena += ' -filter_complex \"[0:v][1:v]overlay = 0:0\" -c:v mpeg2video -b:v 8000k -r 25 -ar 48000 -b:a 256k'
    cadena += " " + "\"" + archivo.replace(config['rutaleer'],config['rutaexport']).replace(".mp4","_ltbx.mpg") + "\" " + config['metadata']
    return cadena






# Devuelve V o F según si el nombre del archivo coincide con el de un video 
def esteArchivoEsVideo(nombreArchivo):

    if ( nombreArchivo[-3:] == "mp4" or nombreArchivo[-3:] == "MP4"):
        return True
    
    elif ( nombreArchivo[-3:] == "mov" or nombreArchivo[-3:] == "MOV"):
        return True
    
    else:
        print(nombreArchivo[-3:])
        return False


# Resuelve la existencia de una carpeta en la ruta de lectura
def existeRutaLectura():
    if (os.path.isdir(config['rutaleer'])):
        return Back.YELLOW + Fore.GREEN + " OK  " + Fore.WHITE
        
    else:
        config['marcaError'] += 1
        return Back.YELLOW + Fore.RED + "ERROR" + Fore.WHITE



# Resuelve la existencia de una carpeta en la ruta temporal
def existeRutaTemporal():
    if (os.path.isdir(config['rutainter'])):
        return Back.YELLOW + Fore.GREEN + " OK  " + Fore.WHITE
        
    else:
        config['marcaError'] += 1
        return Back.YELLOW + Fore.RED + "ERROR" + Fore.WHITE



# Resuelve la existencia de una carpeta en la ruta de escritura final
def existeRutaFinal():
    if (os.path.isdir(config['rutaexport'])):
        return Back.YELLOW + Fore.GREEN + " OK  " + Fore.WHITE
        
    else:
        config['marcaError'] += 1
        return Back.YELLOW + Fore.RED + "ERROR" + Fore.WHITE



# Resuelve la existencia de una carpeta en la ruta de escritura final
def existeRutaMoscal():
    if (isfile(config['moscapal'])):
        return Back.YELLOW + Fore.GREEN + " OK  " + Fore.WHITE
        
    else:
        config['marcaError'] += 1
        return Back.YELLOW + Fore.RED + "ERROR" + Fore.WHITE



# Resuelve la existencia de una carpeta en la ruta de escritura final
def existeRutaffmpeg():
    if (isfile(config['rutaffmpeg'])):
        return Back.YELLOW + Fore.GREEN + " OK  " + Fore.WHITE
        
    else:
        config['marcaError'] += 1
        return Back.YELLOW + Fore.RED + "ERROR" + Fore.WHITE

def procesoprevio():
    if (isfile(os.getcwd()+"//proceso1.bat")):
        GUIpopupProcesoExistente(1)
        subprocess.Popen("move /y proceso1.bat proceso1.bak", stdout=subprocess.PIPE, shell=True)
        
    
    if (isfile(os.getcwd()+"//proceso2.bat")):
        GUIpopupProcesoExistente(2)
        subprocess.Popen("move /y proceso2.bat proceso2.bak", stdout=subprocess.PIPE, shell=True)



#
# MANEJO DE LA INTERFAZ DE USUARIO
#

# Imprimir encabezado inicial de interface
def GUIencabezadoInicial():
    print(Back.RED + "               " + Back.GREEN + Fore.BLACK + "                                                                                                         " )
    print(Back.RED + "   CASSETERA   " + Back.GREEN + Fore.BLACK + "Cableoperador Antiguo Solicita Subvalorar Elementos Tecnológicamente Evolucionados en Recursos Analógicos" )
    print(Back.RED + "               " + Back.GREEN + Fore.BLACK + "                                                                                                         " )
    print(Back.BLUE +  Fore.WHITE +  "Desarrollado por LOGOS (www.logos.net.ar). Software Libre para cooperativas, emprendedores, ONG y universidades públicas")
    Back.BLACK + Fore.WHITE

def GUItituloActitividadActual(titulo):
    print("\n")
    print( Back.RED + Fore.WHITE + "A continuación:  " + titulo + Back.BLACK + Fore.WHITE)
    

def GUImostrarConfiguracion():
    print("\n")
    print( Back.CYAN +  Fore.RED + "          Cassetera da play con esta configuración actual                                 ")
    print( Back.CYAN +  Fore.BLACK + "Ruta de lectura  : " + Fore.WHITE + config['rutaleer'] + ( " " * (85 - 19 -  len(config['rutaleer']))    ) + existeRutaLectura()  )
    print( Back.CYAN +  Fore.BLACK + "Ruta temporal    : " + Fore.WHITE + config['rutainter'] + ( " " * (85 - 19 -  len(config['rutainter']))  ) + existeRutaTemporal() )
    print( Back.CYAN +  Fore.BLACK + "Ruta Export Final: " + Fore.WHITE + config['rutaexport'] + ( " " * (85 - 19 -  len(config['rutaexport']))) + existeRutaFinal()    )
    print( Back.CYAN +  Fore.BLACK + "Ruta PNG Mosca   : " + Fore.WHITE + config['moscapal'] + ( " " * (85 - 19 -  len(config['moscapal']))    ) + existeRutaMoscal()   )
    print( Back.CYAN +  Fore.BLACK + "                                                                                          " )
    print( Back.CYAN +  Fore.BLACK + "FFMPEG           : " + Fore.WHITE + config['rutaffmpeg'] + ( " " * (85 - 19 -  len(config['rutaffmpeg']))) + existeRutaffmpeg()   )

    Back.BLACK + Fore.WHITE

def GUIpopupProcesoExistente(nro):
    print ("\n\n\n\n" + Back.RED + Fore.WHITE + (" " * 120) + "\n" + "                             YA EXISTE PROCESO " + str(nro) + " DE BATCH PREVIOS, SE BACKAPERAN LOS MISMOS                             \n" +  (" " * 120)  )
    sleep(5.00)



#
# MANEJO DE ERROR
#


# Detiene la cassetera si hay error
def detencionPorError():   
    if (config['marcaError'] > 0):
        print ("\n\n\n\n" + Back.RED + Fore.WHITE + (" " * 120) + "\n" + "                                   EXISTEN ERRORES EN LAS RUTAS CORRIJA LA SITUACIÓN                                   \n" +  (" " * 120)  )
        sleep(20.00)
        exit()





# EJECUCIÓN DEL SOFTWARE

clear()
GUIencabezadoInicial()
if (config['rutaleer'] == ""):
	a = input("Pegá la ruta a convertir: ")
	config['rutaleer'] = a
GUImostrarConfiguracion()
detencionPorError()
GUItituloActitividadActual("Leeremos los archivos de la ruta de lectura")
sleep(5.00)
listadoArchivo = obtenerArchivosDeDirectorio(config['rutaleer'])
clear()
GUIencabezadoInicial()
procesoprevio()
batch1 = open("proceso1.bat","w")
batch2 = open("proceso2.bat","w")
GUItituloActitividadActual("Crearemos el proceso de batch para convertir cada archivo detectado")
print("\n\n")

for i in listadoArchivo:
    comando = crearComandoDeConversionPal(i)
    batch1.write(comando + "\n")
    print(Back.WHITE + Fore.BLACK + "\nAsi se convierte:\n" + Back.GREEN + Fore.BLACK + comando )
    comando = crearComandoDeSuperposicionDeMosca(i)
    print(Back.WHITE + Fore.BLACK + "\nAsi se superpone mosca:\n" + Back.RED + Fore.BLACK + comando )
    batch2.write(comando + "\n")
    print(Back.BLACK + Fore.WHITE + "\n\n")
    sleep(3)
    

clear()
GUIencabezadoInicial()
GUItituloActitividadActual("Cerraremos los archivos del proceso de batch")
print(Back.BLACK)
batch1.close()
batch2.close()
sleep(5.00)

clear()
GUIencabezadoInicial()
GUItituloActitividadActual("Comenzaremos la ejecución del proceso 1, se deja paso al proceso externo")
print(Back.WHITE + Fore.RED + "")
p = Popen("proceso1.bat", cwd=r"." )
stdout, stderr = p.communicate()
sleep(5.00)

clear()
GUIencabezadoInicial()
GUItituloActitividadActual("Comenzaremos la ejecución del proceso 2, se deja paso al proceso externo")
print(Back.WHITE + Fore.BLUE + "")
p = Popen("proceso2.bat", cwd=r"." )
stdout, stderr = p.communicate()
sleep(5.00)

print(Back.BLACK)
clear()
GUIencabezadoInicial()
GUItituloActitividadActual("Eliminaremos los archivos temporales que fueron creados")
subprocess.Popen("del /q \"" + config['rutainter'] + "*\"" , stdout=subprocess.PIPE, shell=True)
sleep(5.00)




clear()
GUIencabezadoInicial()
print ("\n\n\n\n" + Back.GREEN + Fore.WHITE + (" " * 120) + "\n" + "                                        EL CASSETTE A TERMINADO, PASA AL LADO B                                        \n" +  (" " * 120)  )
print (Back.BLACK + Fore.WHITE + "Presiona la tecla ENTER para cerrar")
a = input()










