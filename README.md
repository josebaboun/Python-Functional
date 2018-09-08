## Tarea 03

### Lectura del Archivo

Todos los archivos correspondientes a lectura se encuentran en la carpeta `Consultas/Lectura`.
Para los archivos con **header**, se utilizo la función `DictReader` del módulo `csv`.

---
### Comentarios

La carpeta `Consultas/Lecturas/ReviewsDatabase` almacena todos los archivos relacionados al procesamiento de comentarios. De este apartado cabe destacar que el método que se utilizó para contar palabras positivas, negativas y bots fue:

+ Hacer una lista de las palabras clave (ya sea filtrandolas o cargandolas directamente).
+ Separar comentarios por palabras y *limpiar* las palabras (remover símbolos que afecten la lectura de una palabra *(hola, -> hola))*.
+ filtrar comentarios si cumplen con la condición de que la palabra pertenesca a la lista de palabras claves.
+ contar y obtener resultados.

---
### Consultas

Primero, se desempaquetan la lista de consultas y se entrega cada consulta al método unpack.
`unpack` es una funcion recursiva que termina cuando el largo de la consulta es 1, que en este caso va a ser `load_database`. Luego entrega los resultados de la consulta a la consulta siguiente, etc.

la funcion `consultas` es mas larga que lo establecido en el enunciado. Sin embargo si cuenta con la filosofia del enunciado, ya que hace solo una cosa y es asignar una funcion dependiendo de lo solicitado y atrapar un error. la alternativa para hacer la funcion mas corta era dividir la funcion en dos, lo cual (creo yo) atenta con la filosofia ya que hace mas engorrosa la lectura del programa.

---
### Exepciones

Todas las funciones cuentan con un método similar llamado `print_error`. Este método retorna un string con el formato mencionado en el enunciado relativo al error generado.

+ `BadQuerry`: Es utilizada una vez, y su implementacion es muy estandar por lo que no entrare en detalles.

+ `WrongInput`: Este error es chequeado mediante el uso de un decorador llamado `check_params`. debido a que las funciones generan, en su mayoria, listas con filtros, no es necesario chequear que el input se encuentre dentro de un parametro *(Por ejemplo, filter_by_date va a retornar una lista vacia si se ingresa una fecha muy alta o muy baja)*. Es por eso que `check_param` recibe las instancias que deberian tener los argumentos y levanta una excepcion si no cumplen. Notese tambien que no se manejo que se ingresen mas o menos argumentos. Esto debido a que no vi especificamente que se pidiera esto.

+ `MovieError`: Cada vez que se busca revisar un generador de peliculas por un dato, se llama una funcion llamada `check_columns` que levanta un error si alguna columna es igual a *N/A*.
Notese que el error se levanta y la consulta completa levanta un error, cuando se pudo haber saltado la pelicula.

Todas las excepciones se manejan de manera similar en el `main` y en `consultas`.

---
### Testing

El testeo cuenta con archivos propios que fueron subidos a git. Notese que decidi cambiar a mano la ruta de los archivos de lectura en vez de ingresar path como un parámetro (para que sea mas simple).

Para ejecutar el test se deben modificar las siguientes líneas:

+ Consultas/Lectura/actors_database linea 37 a `path = Consultas/Lectura/Testing/actors.csv`
+ Consultas/Lectura/genres_database línea 5 a `path = "Consultas/Lectura/Testing/genres.csv"`
+ Consultas/Lectura/movies_database línea 8 a `path = "Consultas/Lectura/Testing/movies.csv"`
+ Consultas/Lectura/reviews_database línea 9 a `path = "Consultas/Lectura/Testing/reviews.csv"`
+ Consultas/Lectura/reviews_database línea 17 a `path = "Consultas/Lectura/Testing/vocabulary.txt"`
+ Consultas/Lectura/reviews_database línea 25 a `path = "Consultas/Lectura/Testing/words.csv"`

La función `test_MovieError` no es exitosa. no tuve tiempo para corregir esto. defini el test al igual que los otros test donde se levantan errores y si se prueba la funcion con los parametros del test levanta el error, aun así no es exitosa. (puede que solamente pruebe con el wrapper, pero no estoy seguro).

---
### Extras

Se importó `types`, `typing`, y reduce de `functools` por razones lógicas.
También pedir perdón si el codigo esta un poco ilegible o se crearon muchos archivos, trate de hacer el código lo mas limpio posible y seria muy apreciado un feedback respecto a este tema.
