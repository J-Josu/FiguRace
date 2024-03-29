<h1> Grupo <img src="https://media.giphy.com/media/lkTunMhUitIEITABuS/giphy.gif" height="40"/></h1>


## Indice

- [Integrantes](#integrantes)
- [Guia primer uso:](#guia-primer-uso)
- [Fuentes](#fuentes)
- [Modo desarollador](#modo-desarollador)
- [Comentarios adicionales](#comentarios-adicionales)


<br />


## Integrantes

Fabian Martinez Rincon | Josue Suarez | Lucas Gallardo | Iñaki Agustin Lapeyre
--- | --- | --- | ---
![@FabianMartinez](https://avatars.githubusercontent.com/u/55964635?s=150&v=1) | ![@josu-dev](https://avatars.githubusercontent.com/josu-dev?s=150&v=1) | ![@Lucas-Andres-GF](https://avatars.githubusercontent.com/u/91075804?s=150&v=1) | ![@KinnaGt](https://avatars.githubusercontent.com/KinnaGt?s=150&v=1)
[@fabian-martinez-rincon](https://github.com/fabian-martinez-rincon) | [@josu-dev](https://github.com/josu-dev) | [@Lucas-Andres-GF](https://github.com/Lucas-Andres-GF) | [@KinnaGt](https://github.com/KinnaGt)


<br />


## Guia primer uso:

1. ### Requerimientos de sistema

    Se necesita tener python version mayor o igual a 3.10

    > En caso de que no, una de estas guías puede ser de ayuda:
    > - [Windows](https://docs.python.org/es/3.10/using/windows.html)
    > - [Linux](https://docs.python.org/es/3.10/using/unix.html)
    > - [Mac](https://docs.python.org/es/3.10/using/mac.html)

1. ### Obtener el repositorio

    Existen dos maneras:

    - Clonar el repositorio por medio de SSH o HTTPS

    - Descargar el .zip (luego descomprimirlo)

1. ### Instalación de dependencias

    Las dependencias son:

    - Juego: [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/)

    - Datasets: [notebook](https://jupyter.org/), [pandas](https://pandas.pydata.org/)

    - Analysis: [notebook](https://jupyter.org/), [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/)

    Para su instalación:

    1. Primero abrir una terminal/consola en la ubicación donde descargo el contenido del repositorio

    2. Luego ejecutar el siguiente comando
        ```bash
        pip install -r requirements.txt
        ```

1. ### Ejecución

    Ejecución de los diferentes apartados:

    > Se asume que se encuentra en una terminal/consola en la ubicación donde descargo el contenido del repositorio y realizo los pasos previos de la guía

    - **Juego**

        ```bash
        py figurace.py
        ```

    - **Procesamiento Datasets**

        Esta sección se encuentra en la carpeta dataset_section

        El procesamiento de los datasets se encuentra como un script de python o un cuaderno interactivo de [JupyterNotebook](https://jupyter.org/) en la carpeta second_assignment

        Los datasets a procesar en la carpeta base_datasets

    - **Análisis de eventos**

        Esta sección se encuentra en la carpeta analysis_section

        El análisis de los eventos generados al jugar partidas se encuentra como un cuaderno interactivo de [JupyterNotebook](https://jupyter.org/)


<br />


## Fuentes

- Datasets:

    [Spotify](https://www.kaggle.com/datasets/muhmores/spotify-top-100-songs-of-20152019) | [Lagos](https://www.ign.gob.ar/NuestrasActividades/Geografia/DatosArgentina/Lagos) | [FIFA 2021](https://www.kaggle.com/datasets/aayushmishra1512/fifa-2021-complete-player-data?resource=download)
    --- | --- | --- 
    <img src = "https://user-images.githubusercontent.com/55964635/170844079-de18c35d-138a-4c24-af09-c74086ffcab8.jpg" width = "150" height = "150" alt = "ejemplo" align = "center" /> | <img src = "https://user-images.githubusercontent.com/55964635/170844002-7aa0ba0d-7b8b-4c2c-adfa-2adec352e59c.jpg" width = "150" height = "150" alt = "ejemplo" align = "center" /> | <img src = "https://user-images.githubusercontent.com/55964635/170844054-57c7460d-62d0-4cc1-988e-32232ef88e15.jpg" width = "150" height = "150" alt = "ejemplo" align = "center" />

- Imágenes:

    - [README.md](https://pixabay.com/es/)

    - [Menu del juego](https://romannurik.github.io/AndroidAssetStudio/icons-notification.html)

    - Las demas de creación propia


<br />


## Modo desarollador

Se puede iniciar el juego en modo dev (desarrollador), este modo fue pensado para desarrollar la aplicacion de una manera mas facil. Este modo se activa al ejecutar la aplicacion con el argumento extra `--dev`

```bash
py figurace.py --dev
```

Por defecto el modo dev inicia la aplicacion en la pantalla de seleccion de perfiles y a su vez pone un tiempo de inactividad maximo de 5 segundos para el cierre automatico de la aplicacion (si se juega una partida se desactiva el cierre automatico).

Los argumentos adicionales para este modo siguen el siguiente formato:

--(nombre argumento)=(valor para el argumento)

Los argumentos posibles son:

| Nombre | Valor/es | Descripcion | Ejemplo |
| :-: | :-: | :-: | :-: |
| help | | Informa en consola sobre los argumentos posibles en el modo dev | <nobr>`--help`</nobr> |
| to | duracion (segundos) | El tiempo de inactividad para el cierre de la aplicacion | <nobr>`--to=10`</nobr> |
| is | pantalla inicial (SCREEN_NAME) | La pantalla en la cual iniciar la aplicacion | <nobr>`--is=-MENU-`</nobr> |
| el | booleano (true o false) | Habilita el logeo en consola informacion sobre los eventos | <nobr>`--el=true`</nobr> |


<br />


## Comentarios adicionales

La carpeta .vscode contiene configuraciones particulares de este proyecto para el editor VisualStudioCode

La carpeta typings, los tipados necesarios de la librería PySimpleGUI para que el LanguageServer pueda funcionar adecuadamente al hacer el static type checking

La carpeta documents contiene enunciados y otros archivos relaciones a que se tenía que realizar con el proyecto

La carpeta presentation_section contiene el material para el cierre del trabajo y su presentacion
