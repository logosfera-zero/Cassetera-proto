
### CASSETERA
### Descripción y contexto
---
CASSETERA (Cableoperador Antiguo Solicita Subvalorar Elementos Tecnológicamente Evolucionados en Recursos Analógicos).

Sirve para crear un proceso de batch que convierta todos los archivos de video ubicados en config['rutaleer'] en el formato requerido por un cableoperador para su distribución en una señal analógica y la consiguiente aplicación de la mosca.

En específico, este script sin realizarle más modificaciones permite convertir materiales de alta definición (1920x1080) de relación de aspecto 16:9, con codificación H.264 (puede ser otra admitida por FFMPEG) con contenedores MP4 o MOV en materiales MPEG2 de 8Mbps de bitrate con una relación 4:3, aplicando barras negras arriba y abajo (Letterbox) y con una imagen o gráfico superpuesto (un archivo PNG con transparencia para aplicar mosca de canal o programa).


### Casos de uso

Este pequeño script se diseñó para ser utilizado en la siguiente situación que enfrentó UNITV (El canal público universitario de la UNGS):

UNITV produce enteramente su contenido en formato digital de alta definición 16:9 y consiguió espacio televisivo dentro de la grilla de un
canal de cable local, cuya propiedad es de la misma empresa de distribución de cable. Dicho canal utiliza el estandar analógico SD PAL 4:3.

Las entregas de las emisiones de UNITV debían ser en formato MPEG2 720x576 4:3 de duración de casi una hora con todos los elementos gráficos incluidos. Y el inconveniente se encontraba en el proceso de exportación y render para crear ese archivo en calidad estándar de dicha duración.

Puesto que el proceso de exportar dicho video duraba mucho más tiempo que la duración del mismo, y considerando que otros materiales en alta definición y codificación H264 (que consume más recursos del procesador) se exportaban más rápido, se decidió crear una serie de procesos en batch que permitiera contar con una copia del contenido original del canal (HD 16:9) en calidad SD 4:3.

Entonces el proceso de edición y export ya no requerirán realizar la aplicación de superposición de gráficos, una decodicación de un formato y su conversión a otro, con un proceso de downgrande en el medio. Sino que el proceso de edición se realiza nativamente en MPEG2 720x576 4:3.


### Guía de usuario
---

El archivo cassetera.py puede colocarse en cualquier lugar del sistema y con permisos de ejecución. Este archivo de python está optimizado para utilzizarse en windows, pero su ejecución en linux debe ser posible sencillamente cambiando comandos horribles de windows por los de linux (move por mv, copy por cp, etc etc.)

Se debe editar el mismo con un editor de texto y cambiarse los valores de las rutas de los ejecutables y de la ubicación de las carpetas.

Estos son los valores que deben cambiarse:
```
config['rutaffmpeg'] = "C:\\DMAOPS\\FFMPEG\\ffmpeg.exe"
config['rutaleer'] =  "D:\\Videos\\Desktop"
config['rutainter'] = "D:\\\\inter\\"
config['rutaexport'] = "D:\\\\export\\"
config['moscapal'] = "C:\\DMAOPS\\ASSETS\\moscaPAL.png"
```

**Nota: Recordar que las rutas en windows deben contener doble barra por cada barra**  
    Ejemplo: _"C:\\" debería escribirse "C:\\\\"_  

_rutaffmpeg_ debe apuntar a un binario o ejecutable de ffmpeg.  
  
_rutaleer_   debe apuntar a la carpeta donde se leeran todos los archivos .mp4 y/o .mov que se van a convertir. También se puede dejar la cadena vacía "" y el software solicitará se pegue la ruta de manera interactiva durante la ejecución (útil para cuando el resto de la configuración no varía, pero se requieren varias pasadas a diferentes carpetas de lecturas).
  
_rutainter_  debe apuntar a una carpeta temporal dobde se realizará el primer proceso de conversión, se recominda que sea en una unidad de rápida lectura/escritura y con suficiente espacio. Aunque luego este programa se encargará de eliminar su contenido.  
  
_rutaexport_ debe apuntar a la carpeta final donde se encontrará todo el material ya convertido y con la gráfica aplicada.  
  
_moscapal_   debe apuntar a un archivo (preferente) PNG que contendrá una mosca o un logo. Esta imagen debe coincidir con el tamaño y resolución final de salida de este programa (por defecto debe ser 720x576).  
  

_config['filtroffmpeg']_ no es necesario cambiarlo, así como está permite la conversión a PAL, pero realizando ajustes se puede convertir a otros formatos deseados.
  
_config['metadata']_ no funciona aún, puesto que la idea es poder incorporar esta metadata, pero no se encontro soporte en exiftool o ffmpeg para poder escribir metadata en archivos .mpg


 	
### Guía de instalación
---

1. Descargar la última versión desde [La página de releases](https://github.com/logosfera-zero/Cassetera-proto/releases)
2. Descomprimir el archivo _cassetera.zip_.
3. Instalar las dependencias indicadas más abajo, y correr el comando para instalar las librerias requeridas de python.
4. Abrir el archivo cassetera.py y cambiar la configuración explicada anteriormente.


#### Dependencias

Para utilizar Cassetera, se requieren instalar los siguientes programas:

* **Python 3.5** - *(o superior)* - [Python](https://www.python.org/downloads/)
    * Se debe instalar el gestor de paquetes PIP 

* **Paquete Audiovisual** - [Logos](https://www.logos.net.ar/software/paquete-audiovisual) o en su defecto **ffmpeg** - [ffmpeg](https://www.ffmpeg.org/)
   
* **Librerias de Python** -   *Instalar con el siguiente comando
    
```
pip install requests colorama
```


### Autor/es
---
* **Ignacio Tula** - (https://www.logos.net.ar/nosotros/ignacio-tula)



### Licencia 
---
Cassetera está disponible bajo la licencia de software libre GNU GENERAL PUBLIC LICENSE Version 3