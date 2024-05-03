# CLI en Python con Click

Desarrollo de una interfaz por línea de comando (CLI, por sus siglas en inglés) en Python mediante la librería Click.

Partimos del tutorial [Professional CLI Applications with Click](https://youtu.be/vm9tOamPkeQ) de [@NeuralNine](https://github.com/NeuralNine). A su vez, se recomienda estudiar la [Documentaciónb oficial de Click](https://click.palletsprojects.com/en/8.1.x/#documentation).

## Conceptos básicos

Click es un package de Python que sirve para crear CLI's mediante decoradores (para las dudas, pueden consultar el siguiente [artículo](https://codigofacilito.com/articulos/decoradores-python, "Decoradores en Python")).

Las primeras línea de código del programa están destinadas a servir de ejemplo:

```python
@click.command()
@click.option("--name", prompt="Enter your name", help="The name of the user")
def hello(name):
    click.echo(f"Hello {name}!")
```

Esta función solo le pide su nombre al usuario por consola y devuelve un saludo personalizado. La sintaxis explicada sería más o menos: `@click.command()` es un decorador de click que llama a la función *command* que convertirá a la función que hemos definido abajo en *fdef* en un comando de click. El decorador `@click.option()` nos permite manipular los parámetros o argumentos de esa función (aunque el término *argumento* recibe un peso especial en click, así que lo evitaremos en este contexto para no evitar confusiones). En concreto, convierte los parámetros de la función en la orden de nuestro comando o en una opción de ella.

Es en este punto en donde entran los *arguments*(`@click.argument()`), el cual es otra clase de parámetros que nos permite pasar datos como argumentos para la función que queremos convertir en comando sin que, como en el caso de *option*. Es en el siguiente bloque de código en donde empleamos ambas clases de parámetros:

```python
@click.command()
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="m")
@click.argument("todofile", type=click.Path(exists=False), required=0)
@click.option("-n", "--name", prompt="Enter the todo name ", help="The name of the todo item")
@click.option("-d", "--description", prompt="Describe the todo ", help="The description of the todo item")
def add_todo(name, description, priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "a+") as f:
        f.write(f"{name}: {description} [Priority: {PRIORITIES[priority]}]\n")
```

El orden es elemental, por ello el decorador de `@click.command()` va en primer lugar, afectando a todo el bloque. Los parámetros se pasan en orden secuencial. Al seleccionar primero los argumentos (que están repartidos en bloque dentro de los parámetros de la función `add_todo()`), empezamos por el primero de ellos, que es *priority*, y luego seguimos con *todofile*, y pasa lo mismo al saltar a las *options*, se empieza con *name* y luego con *description*.

Cada parámetro que va a recibir el comando definido en `def add_todo` con el decorador debe estar especificado en una de sus dos clases (es decir, *option* o *argument*).

En concreto, el comando `add_todo` nos permite agregar una acción a la lista de tareas, y a su vez, nos guarda esa información en un archivo .txt del cual podemos escoger el nombre. Y si no le asignamos un nombre al archivo (mediante el parámetro `--name`), `main.py` le asignará el nombre *mytodos.txt* por defecto. De hecho, hemos configurado que esa sea la opción por defecto, incluso que exista una opción por defecto. Porque también hemos podido construir el archivo nosotros mismos y colocarlo como indispensable. Para ello sólo teníamos que situarnos en la línea:

```python
@click.argument("todofile", type=click.Path(exists=False), required=0)
```

Una vez allí, bastaba con asignar en `type=click.Path(exists=False)` el valor *True* en lugar de *False* al final del argumento. También pudimos no haber creado ese documento como intocable e indispensable, pero sí exigir al usuario que creara el documento, asignando al final `requiered=1`, para que el suministrar el nombre del archivo sea una acción obligatoria.

## Algunos recursos:

* [Click Argument en la documentación oficial](https://click.palletsprojects.com/en/8.1.x/api/#click.argument)
* [Click Option en la documentación oficial](https://click.palletsprojects.com/en/8.1.x/api/#click.option)
* [Decoradores en la documentación oficial de Click](https://click.palletsprojects.com/en/8.1.x/api/#decorators)
* [Agrupar comandos (nesting)](https://click.palletsprojects.com/en/8.1.x/quickstart/#nesting-commands)