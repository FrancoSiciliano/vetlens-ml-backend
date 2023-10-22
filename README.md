# Información académica
Este repositorio forma parte del Proyecto Final de Ingeniería de los estudiantes Gamietea Julián y Siciliano Franco de la carrera Ingeniería en Informática de la Universidad Argentina de la Empresa. Contactos: 

Julián Gamietea: jgamietea@uade.edu.ar

Franco Siciliano: frsiciliano@uade.edu.ar
# VetLens Machine Learning Service Backend
**Versión de Pyhton necesaria: 3.9**

Este es el servicio de backend encargado de manejar el servicio de clasificaicón de una lesión de piel de un perro.

## Librerias
En el archivo `requirements.txt` podrán encontrarse las diferentes librerías que requieren instalación para poder correr el programa.

Para instalar dichas dependencias basta con correr el siguiente comando:
`pip install -r requirements.txt`

## Uso
Una vez instaladas, basta con correr el comando: `python main.py`. Una vez ejecutado, se encenderá el servicio en la ip `http://127.0.0.1:8000/`

### Endpoints
El servidor cuenta con un único endpoint: 
`http://127.0.0.1:8000/infer/`

El mismo únicamente recibe una imagen y devuelve un mensaje en formato JSON que contiene el resultado de la clasificación. El mismo tiene la siguiente estructura:

```
{

"dermatofitosis": 0.X,

"dermatitis_piotraumatica'": 0.X,

"miasis": 0.X,

"no discernible": 0.X,

"result": <Nombre de la enfermedad con mayor probabilidad>

}
```

### Contenerización
En el repositorio se encuentra un Dockerfile a partir del cuál puede construirse rápidamente una imagen del servicio, que permitirá correr el servidor de forma rápida e independiente de la máquina en la que se encuentra.

Para ello, primero se debe contar con docker instalado en el dispositivo, y luego se deben ejecutar los siguientes comandos:

1. En el directorio donde se encuentra el Dockerfile correr: `docker build -t python-api .`
2. Ejecutar el comando: `docker run -dp 127.0.0.1:8000:8000 python-api`
