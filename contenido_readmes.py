# -*- coding: utf-8 -*-
"""Contenido profesional de los README del portafolio.

Cada entrada asocia la ruta relativa del repositorio (bajo la raiz de
copias locales) con una tupla de bloques: (encabezado o None, cuerpo).
El primer bloque sin encabezado es la introducción; el resto son
secciones con título propio. La sección final de licencia la anade el
generador (reescribir_readmes.generar_readme).
"""

CONTENIDO = {
    "publico/juego-7-letras": (
        "Juego de palabras tipo puzzle en el que cada ronda propone una letra central y seis "
        "letras a su alrededor, dispuestas en forma de panal. El objetivo es encontrar todas "
        "las palabras válidas que se pueden formar con ellas.",
        ("Características", """- Rondas aleatorias: cada partida elige al azar un bloque de palabras desde `json/siete_letras.json`.
- Tablero en panal (colmena) con una letra central y seis letras laterales.
- Reglas clásicas: la palabra debe tener al menos 3 letras, incluir la letra del centro y existir en el listado de la ronda.
- Botones Borrar, Cambiar (baraja las letras laterales) y Aplicar (valida la palabra formada).
- Retroalimentación inmediata con mensajes de acierto, aviso y error.
- Contador de progreso PA/TP (palabras acertadas / total de la ronda) y listado de palabras encontradas."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Datos del juego en formato JSON.
- Tipografías e iconos de Google Fonts."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local (por ejemplo, `python -m http.server`).

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
juego-7-letras/
├── index.html
├── css/                   # estilos del tablero en panal
├── js/                    # lógica del juego
├── json/                  # bloques de palabras de cada ronda
└── icon/                  # favicon
```"""),
    ),
    "publico/juego-memoriza-carta": (
        "Juego de memoria en el navegador: un tablero de cartas con animales que hay que "
        "voltear por parejas hasta encontrar todas las iguales.",
        ("Características", """- Tablero de cartas generado y barajado al azar en cada partida.
- Mecánica de memoria clásica: se voltean dos cartas por turno y las parejas iguales permanecen descubiertas.
- Control de estado del tablero para evitar jugadas invalidas mientras se comprueba una pareja.
- Botón de reinicio para empezar una partida nueva en cualquier momento.
- Modal de victoria al completar todas las parejas, con opción de jugar de nuevo."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Imagenes de animales propias incluidas en el repositorio."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
juego-memoriza-carta/
├── index.html
├── css/                   # estilos del tablero y las cartas
├── js/                    # lógica del juego
├── img/                   # imagenes de las cartas
└── LICENSE
```"""),
    ),
    "publico/juego-palabra-oculta": (
        "Juego de adivinanza de palabras en la línea de Wordle: hay que descubrir la palabra "
        "oculta de cinco letras en un máximo de seis intentos.",
        ("Características", """- Tablero de 6 intentos por 5 letras con la palabra oculta seleccionada al azar.
- Teclado en pantalla y entrada por teclado físico.
- Comprobación de cada intento con retroalimentación visual letra a letra.
- Mensajes de estado que guian al jugador durante la partida.
- Banco de palabras cargado desde `json/palabras_ocultas.json`."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Datos de palabras en formato JSON."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
juego-palabra-oculta/
├── index.html
├── css/                   # estilos del tablero y el teclado
├── js/                    # lógica del juego
├── json/                  # banco de palabras
└── icon/                  # favicon
```"""),
    ),
    "publico/juego-serpiente": (
        "Juego clásico de la serpiente en el navegador: controla el reptil para comer la "
        "comida, crece con cada bocado y evita chocar con los bordes o con su propio cuerpo.",
        ("Características", """- Tablero de juego en cuadrícula con la serpiente y la comida generadas por posiciones aleatorias.
- Control por teclado (flechas) y botones de dirección en pantalla.
- Puntuación actualizada con cada comida y fin de partida al chocar.
- Velocidad de juego regulada por intervalo y reinicio automático tras el final.
- Pantalla de fin de juego con la puntuación obtenida."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Canvas o DOM para el renderizado del tablero."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
juego-serpiente/
├── index.html
├── css/                   # estilos del tablero y los controles
├── js/                    # lógica del juego
└── icon/                  # favicon
```"""),
    ),
    "publico/juego-sopa-letras": (
        "Sopa de letras en el navegador: encuentra todas las palabras de la lista ocultas en "
        "una cuadrícula de 12x12, marcando las letras que las componen.",
        ("Características", """- Cuadrícula de 12x12 generada al azar a partir de un listado de palabras.
- Selección de las letras con el ratón o la pantalla táctil para marcar una palabra.
- Barra de progreso y contador de palabras encontradas.
- Modal de victoria al completar todas las palabras de la sopa.
- Sopas de letras cargadas desde `json/sopas_letras.json`."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Datos de las sopas en formato JSON."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
juego-sopa-letras/
├── index.html
├── css/                   # estilos de la cuadrícula
├── js/                    # lógica del juego
├── json/                  # sopas y listas de palabras
└── icon/                  # favicon
```"""),
    ),
    "publico/juego-sudoku": (
        "Juego de Sudoku clásico de 9x9 en el navegador: completa cada tablero sin repetir "
        "números en filas, columnas ni regiones.",
        ("Características", """- Tableros de 9x9 cargados desde `json/sudokus.json` y elegidos al azar.
- Selección de casilla con el ratón o el teclado y entrada de números con el teclado numerico en pantalla.
- Resaltado de la casilla activa para facilitar la lectura de la fila, la columna y la region.
- Comprobación de victoria al completar el tablero correctamente, con modal de felicitación.
- Botón de reinicio para volver a empezar el mismo tablero."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Tableros de juego en formato JSON."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
juego-sudoku/
├── index.html
├── css/                   # estilos del tablero
├── js/                    # lógica del juego
├── json/                  # tableros de sudoku
└── icon/                  # favicon
```"""),
    ),
    "publico/juego-tic-tac-toe": (
        "Juego clásico del tres en raya (tic-tac-toe) para dos jugadores en el navegador.",
        ("Características", """- Tablero de 3x3 donde dos jugadores alternan turnos con las fichas X y O.
- Detección automática de victoria (tres en línea) y de empate.
- Indicación del jugador en turno durante la partida.
- Botón de reinicio para empezar una partida nueva."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
juego-tic-tac-toe/
├── index.html
├── css/                   # estilos del tablero
├── js/                    # lógica del juego
└── icon/                  # favicon
```"""),
    ),
    "publico/web-algoritmos": (
        "Página web con tarjetas de repaso de algoritmos clásicos de programación: cada "
        "tarjeta muestra el nombre del algoritmo, una descripción breve y un icono.",
        ("Características", """- Catálogo de algoritmos conocidos (compresión, búsqueda, estructuras de datos, etc.).
- Tarjetas interactivas tipo flashcard que se voltean para consultar la descripción.
- Cada tarjeta incluye icono ilustrativo asociado al algoritmo.
- Interfaz sencilla en español, sin necesidad de registro."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
web-algoritmos/
├── index.html
├── css/                   # estilos de las tarjetas
├── js/                    # datos de algoritmos y lógica de las tarjetas
└── icon/                  # favicon
```"""),
    ),
    "publico/web-calculadora": (
        "Calculadora web con las operaciones aritmeticas basicas, pensada para usarse "
        "directamente desde el navegador.",
        ("Características", """- Suma, resta, multiplicación y división.
- Operaciones encadenadas con pantalla de resultado y limpieza total (AC).
- Botones de borrado del último dígito y de la operación en curso.
- Interfaz responsive con botones accesibles por ratón o pantalla táctil."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-calculadora/
├── index.html
├── css/                   # estilos de la calculadora
├── js/                    # lógica de calculo
└── icon/                  # favicon
```"""),
    ),
    "publico/web-calculadora-edad": (
        "Calculadora de edad que indica los años, meses y días transcurridos desde una fecha "
        "de nacimiento, con actualización inmediata.",
        ("Características", """- Selección de la fecha de nacimiento mediante un campo de fecha.
- Cálculo automático de la edad en años, meses y días.
- Resultado presentado de forma clara y legible al instante.
- Interfaz en español con diseño simple y responsive."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-calculadora-edad/
├── index.html
├── css/                   # estilos de la interfaz
├── js/                    # lógica del calculo de edad
└── icon/                  # favicon
```"""),
    ),
    "publico/web-calendario": (
        "Calendario mensual interactivo que muestra el mes actual y permite navegar entre "
        "meses anteriores y posteriores.",
        ("Características", """- Vista mensual con la distribución correcta de los días por semana.
- Navegación entre meses mediante controles anterior y siguiente.
- Resaltado del día actual.
- Generado por completo con JavaScript a partir de la fecha del sistema."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-calendario/
├── index.html
├── css/                   # estilos del calendario
├── js/                    # lógica de generación del mes
└── icon/                  # favicon
```"""),
    ),
    "publico/web-codi-wiki": (
        "Wiki de lenguajes de programación y paradigmas: consulta la historia, las ventajas y "
        "desventajas, los usos y ejemplos de código de cada tema.",
        ("Características", """- Contenido organizado por lenguajes de programación y paradigmas (programación orientada a objetos, funcional e imperativa).
- Fichas con descripción, historia, ventajas y desventajas, usos habituales y ejemplos de código.
- Menú lateral para navegar entre los temas.
- Vista de detalle generada dinámicamente desde los datos."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- Contenido estructurado en datos JavaScript (JS)."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-codi-wiki/
├── index.html
├── css/                   # estilos de la wiki
├── js/                    # datos de contenido y lógica de la interfaz
└── icon/                  # favicon
```"""),
    ),
    "publico/web-codigos-http": (
        "Página de referencia con los códigos de estado HTTP organizados por categorías, "
        "mostrando el significado de cada uno en tarjetas.",
        ("Características", """- Listado completo de códigos de estado HTTP (1xx, 2xx, 3xx, 4xx y 5xx).
- Agrupacion por categorías con tarjetas individuales para cada código.
- Descripción breve del significado de cada respuesta.
- Interfaz en español con diseño claro y responsive."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Datos de los códigos definidos en JavaScript."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-codigos-http/
├── index.html
├── css/                   # estilos de las tarjetas
├── js/                    # catalogo de códigos y renderizado
└── icon/                  # favicon
```"""),
    ),
    "publico/web-conversor-universal": (
        "Conversor de unidades en el navegador que permite convertir valores entre más de 130 "
        "unidades agrupadas en 14 categorías, con resultados en tiempo real.",
        ("Características", """- 14 categorías disponibles: consumo de combustible, energía, frecuencia, longitud, masa, presión, tamaño de datos, tasa de transmisión de datos, temperatura, tiempo, velocidad, volumen, ángulo plano y área.
- Menú lateral para elegir la categoría y dos listas desplegables para la unidad de origen y la de destino.
- Conversion automática mientras se escribe el valor, sin recargar la página.
- Resultado formateado con dos decimales y separador de miles.
- Datos de conversión declarativos: cada unidad define su factor sobre la unidad base de la categoría."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Tipografia Montserrat (Google Fonts)."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o usa un servidor estático local (por ejemplo, `python -m http.server`).

No requiere instalación ni compilación."""),
        ("Estructura del proyecto", """```
web-conversor-universal/
├── index.html
├── css/                   # estilos de la interfaz
├── js/                    # unidades y lógica de conversión
└── icon/                  # favicon y logo
```"""),
    ),
    "publico/web-convertidor-moneda": (
        "Convertidor de monedas que obtiene las tasas de cambio en tiempo real desde una API "
        "publica y calcula la conversión entre dos divisas.",
        ("Características", """- Selección de la divisa de origen y de la divisa de destino mediante listas desplegables.
- Tasas de cambio actualizadas desde la API pública open.er-api.com (`/v6/latest`).
- Conversion calculada al pulsar el botón correspondiente.
- Resultado mostrado con el importe convertido.
- Interfaz en español con diseño responsive."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- API externa: open.er-api.com para las tasas de cambio."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Selecciona las monedas e indica el importe; la conversión usa las tasas más recientes de la API."""),
        ("Estructura del proyecto", """```
web-convertidor-moneda/
├── index.html
├── css/                   # estilos de la interfaz
├── js/                    # lógica de conversión y consulta a la API
└── icon/                  # favicon
```"""),
    ),
    "publico/web-generador-codigo-qr": (
        "Generador de códigos QR a partir de una URL, mediante la API pública de QRcode Monkey.",
        ("Características", """- Campo de texto para introducir la URL que se quiere codificar.
- Generación del QR llamando a la API de QRcode Monkey (`api.qrcode-monkey.com`) con el tamaño por defecto.
- Inserción de la imagen del código generado en la propia página.
- Validación de entrada con mensaje de error si el campo esta vacío."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- API externa: QRcode Monkey para generar los códigos QR."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Introduce la URL y pulsa el botón para generar el código QR."""),
        ("Estructura del proyecto", """```
web-generador-codigo-qr/
├── index.html
├── css/                   # estilos del generador
├── js/                    # lógica de generación
└── icon/                  # favicon
```"""),
    ),
    "publico/web-generador-contrasena": (
        "Generador de contraseñas seguras y aleatorias al instante, desde el navegador.",
        ("Características", """- Generación de una contraseña aleatoria con un solo clic.
- Contraseñas formadas por combinaciones seguras de caracteres.
- Campo de solo lectura donde se muestra el resultado para copiarlo.
- Mensajes de estado que informan sobre la última acción realizada."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Pulsa el botón Generar para obtener una contraseña nueva."""),
        ("Estructura del proyecto", """```
web-generador-contrasena/
├── index.html
├── css/                   # estilos del generador
├── js/                    # lógica de generación
└── icon/                  # favicon
```"""),
    ),
    "publico/web-generador-crucigramas": (
        "Generador de patrones de crucigramas que crea y descarga plantillas a partir de las "
        "palabras proporcionadas.",
        ("Características", """- Entrada de las palabras que deben componer el crucigrama.
- Generación automática del patron con las casillas negras colocadas correctamente.
- Creación de 100 patrones distintos en una sola acción.
- Descarga de los patrones generados para su uso posterior."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Introduce las palabras y pulsa el botón para generar y descargar los patrones."""),
        ("Estructura del proyecto", """```
web-generador-crucigramas/
├── index.html
├── css/                   # estilos del generador
├── js/                    # algoritmo de colocación de palabras
└── icon/                  # favicon
```"""),
    ),
    "publico/web-gestiona-presupuesto": (
        "Gestor de presupuesto personal en el navegador: registra ingresos y gastos y consulta "
        "el balance neto resultante.",
        ("Características", """- Registro de ingresos y gastos con importe.
- Totales parciales de ingresos y de gastos.
- Cálculo automático del balance neto.
- Interfaz en español con formularios separados para cada tipo de movimiento."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-gestiona-presupuesto/
├── index.html
├── css/                   # estilos de la interfaz
├── js/                    # lógica de registros y balance
└── icon/                  # favicon
```"""),
    ),
    "publico/web-lector-arxiu": (
        "Lector de archivos locales en el navegador, con interfaz en catalán, que muestra el "
        "contenido del archivo seleccionado sin subirlo a ningun servidor.",
        ("Características", """- Selección de un archivo local mediante el selector del navegador.
- Lectura del contenido con la API FileReader del navegador.
- Visualización del texto leido en pantalla.
- Interfaz en catalán (es el idioma de la aplicación).
- Todo el procesamiento ocurre de forma local."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- API FileReader para la lectura de archivos."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Selecciona un archivo de texto y su contenido se mostrara en pantalla."""),
        ("Estructura del proyecto", """```
web-lector-arxiu/
├── index.html
├── css/                   # estilos de la interfaz
├── js/                    # lógica de lectura de archivos
└── icons/                 # iconos
```"""),
    ),
    "publico/web-lexaro": (
        "Tablero de tareas (kanban) en el navegador con columnas por estado, prioridades, "
        "arrastrar y soltar y persistencia local.",
        ("Características", """- Tablero kanban con las columnas To Do, En Progreso, En Revision y Completado.
- Creación de tareas con título y prioridad (alta, media o baja).
- Arrastrar y soltar para mover las tareas entre columnas.
- Filtros por prioridad (Todas, Alta, Media y Baja).
- Edición y eliminación de tareas con confirmación.
- Persistencia de las tareas en `localStorage` para conservarlas entre sesiones."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- API localStorage para la persistencia."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Crea tareas, asignales prioridad y arrastralas entre columnas segun su estado."""),
        ("Estructura del proyecto", """```
web-lexaro/
├── index.html
├── css/                   # estilos del tablero
├── js/                    # lógica del kanban
└── LICENSE
```"""),
    ),
    "publico/web-narcopedia": (
        "Página web informativa que recoge el ranking de los mayores imperios del narcotráfico "
        "de la historia, con fichas de detalle de cada organización.",
        ("Características", """- Listado de las organizaciones más relevantes del narcotráfico.
- Fichas de detalle con información historica de cada organización.
- Navegación entre las secciones Capos y Organizaciones.
- Vistas de listado y de detalle generadas dinámicamente.
- Contenido con fines informativos y documentales."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- Recursos de imagen incluidos en el repositorio."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-narcopedia/
├── index.html
├── assets/                # recursos graficos
├── css/                   # estilos de la página
└── js/                    # datos y lógica de la interfaz
```"""),
    ),
    "publico/web-paises-visitados": (
        "Página web para registrar y consultar los países visitados, organizados por continente, "
        "con buscador y una animación de avión de fondo.",
        ("Características", """- Catálogo de países del mundo agrupados por continente con su código ISO.
- Buscador para localizar un pais por nombre.
- Selección de los países visitados para llevar el registro personal.
- Persistencia de la selección en `localStorage`.
- Animación de avión con estela y nubes de fondo."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas.
- Datos de países y continentes definidos en JavaScript."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Busca y marca los países que has visitado."""),
        ("Estructura del proyecto", """```
web-paises-visitados/
├── index.html
├── css/                   # estilos de la página
├── js/                    # datos de países y animaciones
└── img/                   # recursos graficos
```"""),
    ),
    "publico/web-porcentaje-anual": (
        "Indicador del porcentaje del año transcurrido con barra de progreso, día actual y días "
        "restantes, teniendo en cuenta los años bisiestos.",
        ("Características", """- Cálculo del porcentaje del año transcurrido en tiempo real.
- Barra de progreso visual actualizada automáticamente.
- Indicación del día del año y de los días restantes.
- Gestion correcta de los años bisiestos."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin dependencias externas."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-porcentaje-anual/
├── index.html
├── css/                   # estilos del indicador
├── js/                    # calculo del progreso
└── icon/                  # favicon
```"""),
    ),
    "publico/web-redimensiona-imagen": (
        "Herramienta para redimensionar imagenes en el navegador: se carga una imagen local, se "
        "ajusta su tamaño y se descarga el resultado.",
        ("Características", """- Carga de una imagen local mediante FileReader.
- Redimension de la imagen en un lienzo (canvas) con las nuevas dimensiones.
- Previsualizacion del resultado antes de descargar.
- Descarga de la imagen procesada con un solo clic."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- API FileReader y elemento canvas para el procesado."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Selecciona una imagen y pulsa el botón para descargarla redimensionada."""),
        ("Estructura del proyecto", """```
web-redimensiona-imagen/
├── index.html
├── css/                   # estilos de la herramienta
├── js/                    # lógica de redimensión
└── icon/                  # favicon
```"""),
    ),
    "publico/web-reproductor-musica": (
        "Reproductor de música en el navegador con lista de canciones incluidas y controles de "
        "reproducción.",
        ("Características", """- Listado de canciones con sus carátulas.
- Controles de reproducción: reproducir, pausar, anterior y siguiente.
- Carga de las pistas de audio incluidas en la carpeta `canciones`.
- Avance automático al terminar cada canción."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- Elemento de audio HTML5 con archivos MP3 incluidos."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Elige una canción de la lista y usa los controles para reproducirla."""),
        ("Estructura del proyecto", """```
web-reproductor-musica/
├── index.html
├── css/                   # estilos del reproductor
├── js/                    # lógica de reproducción
├── canciones/             # pistas de audio (MP3)
└── img/                   # carátulas de las canciones
```"""),
    ),
    "publico/web-tests-daw": (
        "Plataforma de tests del ciclo formativo de Desarrollo de Aplicaciones Web (DAW): "
        "cuestionarios de preguntas tipo test organizados por módulos.",
        ("Características", """- Tests agrupados por módulos del ciclo DAW (bases de datos, diseño de interfaces, lenguajes de marcas, programación y sistemas informáticos).
- Preguntas tipo test con selección de respuesta.
- Barra de progreso durante el test.
- Pantalla de resultados al finalizar, con opción de reiniciar.
- Navegación con botones para avanzar entre preguntas."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+).
- Preguntas almacenadas en archivos JSON por modulo."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local.
3. Selecciona una categoría, pulsa Iniciar y responde las preguntas del test."""),
        ("Estructura del proyecto", """```
web-tests-daw/
├── index.html
├── css/                   # estilos de la plataforma
├── js/                    # lógica de los tests
├── json/                  # preguntas por modulo
└── icon/                  # favicon
```"""),
    ),
    "publico/link-in-bio": (
        "Página de enlaces (link in bio) con acceso a las redes sociales del autor.",
        ("Características", """- Enlaces directos a GitHub, LinkedIn, Instagram, Threads, Facebook y TikTok.
- Botones con los iconos de cada red social.
- Perfil con el nombre de usuario de cada plataforma.
- Diseño simple, vertical y responsive para móvil."""),
        ("Tecnologías", """- HTML5 y CSS3, con JavaScript mínimo."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o publica la carpeta en cualquier hosting estático."""),
        ("Estructura del proyecto", """```
link-in-bio/
├── index.html
├── styles.css             # estilos de la página
└── icons/                 # iconos de las redes sociales
```"""),
    ),
    "publico/web-curso-git": (
        "Sitio web estático con un curso de Git: incluye una página por comando con su sintaxis, "
        "opciones y ejemplos, pensado para consulta rápida y aprendizaje.",
        ("Características", """- Más de 30 páginas tematicas, una por comando (init, clone, add, commit, branch, checkout, merge, rebase, stash, log, etc.).
- Sintaxis y opciones principales de cada comando con ejemplos practicos.
- Navegación sencilla entre páginas con cabecera comun.
- Contenido 100 % estático, ideal para consulta offline."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin frameworks."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-curso-git/
├── index.html
├── html/                  # página por comando de Git
├── css/                   # estilos del curso
├── js/                    # lógica de la interfaz
└── icons/                 # iconos
```"""),
    ),
    "publico/web-curso-sql": (
        "Sitio web estático con un curso completo de SQL organizado por temas: desde la "
        "introducción y el DDL hasta consultas avanzadas, incluye una prueba final.",
        ("Características", """- Temario progresivo: introducción, DDL, inserción, consultas, operadores, orden y limites.
- Temas intermedios: agregados, joins, subconsultas, vistas e indices.
- Temas avanzados: transacciones, disparadores (triggers), procedimientos, seguridad y restricciones.
- Prueba final para validar los conocimientos adquiridos.
- Navegación clara entre temas con contenido estático."""),
        ("Tecnologías", """- HTML5, CSS3 y JavaScript (ES6+), sin frameworks."""),
        ("Uso", """1. Clona el repositorio.
2. Abre `index.html` en el navegador o sirve la carpeta con un servidor estático local."""),
        ("Estructura del proyecto", """```
web-curso-sql/
├── index.html
├── html/                  # página por tema del curso
├── css/                   # estilos del curso
├── js/                    # lógica de la interfaz
└── icons/                 # iconos
```"""),
    ),
    "publico/web-clima": (
        "Aplicación web del tiempo (SPA) que muestra el clima actual y el pronóstico de "
        "cualquier localización del mundo, con datos de la API abierta de Open-Meteo.",
        ("Características", """- Búsqueda de ciudades mediante el geocodificador de Open-Meteo.
- Uso de la ubicación del dispositivo (geolocalización).
- Clima actual: condición, sensación termica, viento, humedad, radiación UV, presión y visibilidad.
- Pronóstico horario (gráfica SVG) y pronóstico para los proximos días.
- Ficha de la ubicación: coordenadas, elevación, zona horaria, hora local y población.
- Conversor de unidades y persistencia de la última ubicación consultada.
- Diseño responsive y accesible, con fondo animado y soporte de `prefers-reduced-motion`."""),
        ("Tecnologías", """- React + Vite como stack principal.
- CSS Modules con variables CSS (tokens de diseño).
- Vitest para los tests.
- Tipografías locales con @fontsource.
- Datos meteorologicos de Open-Meteo (geocoding, forecast y air quality)."""),
        ("Instalación y desarrollo", """```bash
npm install       # instala las dependencias
npm run dev       # servidor de desarrollo con HMR
npm run build     # genera la build de producción en dist/
npm run preview   # previsualiza la build de producción
npm run lint      # ejecuta ESLint
npm run test:run  # ejecuta los tests (Vitest)
npm run format    # formatea el código con Prettier
```"""),
        ("Estructura del proyecto", """```
web-clima/
├── index.html
├── vite.config.js
├── public/                # favicon, robots.txt
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── styles/            # tokens y estilos globales
│   ├── pages/             # Home
│   ├── components/        # layout, ui y efectos
│   └── services/          # clientes de Open-Meteo
└── docs/                  # documentación del proyecto
```"""),
    ),
    "publico/lenguajes-programacion": (
        "Repositorio con los apuntes y ejercicios de los lenguajes de programación aprendidos "
        "en distintas instituciones, organizado por lenguaje con su teoría y prácticas.",
        ("Características", """- Material de Java del ciclo DAW impartido en ITIC Barcelona (teoría y ejercicios).
- Material de JavaScript del programa DCS de INFOTEP (teoría y ejercicios).
- Material de Python del programa DCS de INFOTEP (teoría y ejercicios).
- Temarios y guías de referencia incluidas en cada carpeta de lenguaje."""),
        ("Tecnologías", """- Documentación Markdown y recursos de estudio (PDF, HTML).
- Contenido organizado por carpetas por lenguaje e institución."""),
        ("Uso", """1. Clona el repositorio.
2. Navega por la carpeta del lenguaje que quieras consultar (Java, JavaScript o Python).
3. Revisa la teoría en `Teoria` (o `Teoria`) y practica con los ejercicios de la carpeta de ejercicios."""),
        ("Estructura del proyecto", """```
lenguajes-programación/
├── JavaDAWITIC/           # Java (ciclo DAW, ITIC Barcelona)
│   ├── Teoria/
│   └── Exercicis/
├── JavaScriptDCSINFOTEP/  # JavaScript (DCS, INFOTEP)
│   ├── Teoria/
│   └── Ejercicios/
├── PythonDCSINFOTEP/      # Python (DCS, INFOTEP)
│   ├── Teoria/
│   └── Ejercicios/
└── LICENSE
```"""),
    ),
    "publico/login-google": (
        "Aplicación web con Flask que permite iniciar sesión con la cuenta de Google mediante "
        "el flujo OAuth 2.0 y guarda los datos del usuario en una base de datos SQLite.",
        ("Características", """- Inicio de sesión con Google mediante OAuth 2.0 (flujo de código de autorización).
- Descubrimiento dinámico de los endpoints de Google (OpenID Configuration).
- Creación automática del usuario en la base de datos tras el primer acceso.
- Sesiones gestionadas con Flask y Flask-Login.
- Página principal que muestra el perfil del usuario autenticado.
- Cierre de sesión que limpia la sesión local."""),
        ("Tecnologías", """- Python 3 con Flask, Flask-Login y oauthlib.
- Base de datos SQLite con el esquema en `schema.sql`.
- Cliente HTTP requests y pyOpenSSL para el intercambio OAuth."""),
        ("Instalación y uso", """1. Clona el repositorio y crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: .\\venv\\Scripts\\activate
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Crea el archivo `.env` en la raiz con tus credenciales de Google Cloud:

   ```
   GOOGLE_CLIENT_ID=tu_cliente_id_google_cloud_app
   GOOGLE_CLIENT_SECRET=tu_cliente_secret_google_cloud_app
   DATABASE=sqlite_db
   OAUTHLIB_INSECURE_TRANSPORT=1
   ```

4. Inicia la aplicación:

   ```bash
   python app.py
   ```

5. Abre la URL que muestra Flask (por defecto `http://127.0.0.1:5000`) e inicia sesión con Google."""),
        ("Estructura del proyecto", """```
login-google/
├── app.py                 # rutas y lógica de la aplicación
├── config.py              # configuración desde variables de entorno
├── db.py                  # conexión con la base de datos
├── user.py                # modelo de usuario
├── schema.sql             # esquema de la base de datos
├── requirements.txt
├── templates/
└── static/
```"""),
    ),
    "publico/alpha-inventory-flask": (
        "Sistema web de gestión de inventario desarrollado con Flask y MySQL: administra "
        "artículos, suplidores, clientes y marcas, y controla las compras y ventas con sus "
        "movimientos, todo bajo cuentas de usuario independientes.",
        ("Características", """- Cuentas de usuario: registro, inicio y cierre de sesión, perfil con edición, cambio y recuperación de contraseña por correo (SMTP) y eliminación de cuenta.
- Artículos con código, descripción, talla, marca, referencia, ubicación, costo, precio, ITBIS, cantidad, unidad de medida y margen de beneficio.
- Registro, listado y edición de suplidores, clientes y marcas.
- Compras y ventas asociadas a encargados de compras y de ventas.
- Movimientos diarios de compras y de ventas con el costo total y filtros por rango de código de artículo.
- Consulta de movimientos por artículo, tanto en compras como en ventas.
- Separación entre vistas públicas del sitio y vistas de gestión del panel administrativo.
- Manejo de errores y mensajes de confirmación (flash) en la interfaz."""),
        ("Tecnologías", """- Python 3 con Flask (Jinja2, sesiones y mensajes flash).
- MySQL mediante la extensión Flask-MySQL (`flaskext.mysql`).
- Flask-Mail para el envío de correos (recuperación de contraseña).
- HTML5, CSS3 y JavaScript en las plantillas."""),
        ("Instalación y uso", """1. Clona el repositorio y crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: .\\venv\\Scripts\\activate
   ```

2. Instala las dependencias usadas por la aplicación:

   ```bash
   pip install flask flask-mysql flask-mail
   ```

3. Crea la base de datos en MySQL (por ejemplo `alphainventory`) e importa el esquema:

   ```bash
   mysql -u root -p alphainventory < alphainventory.sql
   ```

4. Configura en `app.py` los datos de conexión a MySQL y, si se usa la recuperación de contraseña por correo, los datos SMTP (`MAIL_USERNAME` y `MAIL_PASSWORD`).

5. Inicia la aplicación:

   ```bash
   python app.py
   ```

   Y abre `http://127.0.0.1:5000` en el navegador."""),
        ("Estructura del proyecto", """```
alpha-inventory-flask/
├── app.py                 # rutas y lógica de negocio (Flask)
├── alphainventory.sql     # esquema de la base de datos (MySQL)
├── templates/
│   ├── sitio/             # vistas públicas y de consulta
│   └── admin/             # vistas de gestión administrativa
├── static/                # css, javascript e imagenes
├── manual-de-uso.pdf      # manual del usuario
└── alpha-inventory.pdf    # documentación del sistema
```"""),
    ),
    "publico/alpha-inventory-django": (
        "Sistema web de gestión de inventario desarrollado con Django y MySQL: administra "
        "artículos, suplidores, clientes y marcas, y gestiona las compras y ventas del negocio "
        "con cuentas de usuario independientes.",
        ("Características", """- Cuentas de usuario con registro y activación por correo (enlace con token), inicio y cierre de sesión y recuperación de contraseña.
- Artículos con código, descripción, talla, marca, referencia, ubicación, costo, precio, ITBIS, cantidad, unidad de medida y margen de beneficio.
- Registro, listado, edición y eliminación de suplidores, clientes y marcas.
- Compras y ventas asociadas a encargados de compras y de ventas.
- Consulta y control de movimientos del inventario por usuario.
- Panel de administración de Django para la gestión avanzada de los datos.
- Separación de las vistas de gestión en plantillas propias del sitio."""),
        ("Tecnologías", """- Python 3 con Django (proyecto configurado para Django 4.2+).
- Base de datos MySQL (configurada en `settings.py`).
- HTML5, CSS3 y JavaScript con plantillas Django (Jinja)."""),
        ("Instalación y uso", """1. Clona el repositorio y crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: .\\venv\\Scripts\\activate
   ```

2. Instala Django y el driver de MySQL:

   ```bash
   pip install django mysqlclient
   ```

3. Crea la base de datos `alphainventory` en MySQL e importa el esquema (`alpha_inventory.sql`).

4. Revisa la conexión a la base de datos en `AlphaInventoryDjangoBD/settings.py` (host, usuario y contraseña) y aplica las migraciones:

   ```bash
   python manage.py migrate
   ```

5. Inicia el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

   Y abre la dirección que muestra Django (por defecto `http://127.0.0.1:8000`)."""),
        ("Estructura del proyecto", """```
alpha-inventory-django/
├── manage.py
├── AlphaInventoryDjangoBD/    # proyecto Django (settings, urls)
├── AlphaInventory/            # aplicación principal
│   ├── models.py              # modelos del sistema
│   ├── views.py               # lógica de las vistas
│   ├── admin.py
│   ├── forms.py
│   ├── urls.py
│   ├── migrations/
│   ├── templates/
│   └── static/
├── alpha_inventory.sql        # esquema de la base de datos
├── ManualDeUso.pdf            # manual del usuario
└── alpha-inventory.pdf        # documentación del sistema
```"""),
    ),
    "privado/cursos-infotep-virtual": (
        "Repositorio con las evidencias y los materiales de los cursos virtuales de INFOTEP "
        "completados al 100 %, organizados por curso y unidad.",
        ("Características", """- Curso 'Desarrollando apps' completado al 100 %, con tres unidades.
- Curso 'Introduccion a la Industria 4.0' completado al 100 %.
- Evidencias de cada unidad: foros, prácticas, guías obligatorias, evaluaciones y proyecto final.
- Materiales en diversos formatos (imagenes de foros, documentos, guías de texto y PDF)."""),
        ("Contenido", """```
cursos-infotep-virtual/
├── desarrollando_app_100_c/          # curso Desarrollando apps (100 %)
│   ├── unidad_1_100/
│   ├── unidad_2_100/
│   └── unidad_3_100/                 # incluye proyecto final
└── introduccion_industria_4_0_100_c/ # curso Industria 4.0 (100 %)
    └── introduccion_industria_4_0_100/
```"""),
        ("Estructura del repositorio", """```
cursos-infotep-virtual/
├── desarrollando_app_100_c/          # evidencias del primer curso
└── introduccion_industria_4_0_100_c/ # evidencias del segundo curso
```"""),
    ),
}
