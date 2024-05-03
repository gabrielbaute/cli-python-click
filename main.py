import click

# Agrupador
@click.group()
def mycommands():
    pass

# Función de prueba, creamos un "echo" y lo convertimos en un comando.
@click.command()
@click.option("--name", prompt="Enter your name", help="The name of the user")
def hello(name):
    click.echo(f"Hello {name}!")

# Array con los valores de las prioridades que requerimos para el argumento de add_todo
PRIORITIES = {
    "o": "Optional",
    "l": "Low",
    "m": "Medium",
    "h": "Hight",
    "c": "Crucial"
}

"""
Comando que crea el archivo (nos permite crear tantos como queramos),
y a su vez registra las tareas nuevas, sus descripciones y sus 
diferentes grados de prioridad
"""
@click.command()
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="m")
@click.argument("todofile", type=click.Path(exists=False), required=0)
@click.option("-n", "--name", prompt="Enter the todo name ", help="The name of the todo item")
@click.option("-d", "--description", prompt="Describe the todo ", help="The description of the todo item")
def add_todo(name, description, priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "a+") as f:
        f.write(f"{name}: {description} [Priority: {PRIORITIES[priority]}]\n")

# Comando para borrar tareas del archivo de registro.
@click.command()
@click.argument("idx", type=int, required=1)
def delete(idx):
    with open("mytodos.txt", "r") as f:
        todo_list = f.read().splitlines()
        todo_list.pop(idx)
    with open("mytodos.txt", "w") as f:
        f.write("\n".join(todo_list))
        f.write('\n')
        
# Comando para que nos muestre las tareas registradas en un determinado documento.
@click.command()
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys))
@click.argument("todofile", type=click.Path(exists=True), required=0)
def list_todo(priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "r") as f:
        todo_list = f.read().splitlines()
    if priority is None:
        for idx, todo in enumerate(todo_list):
            print(f"({idx}) - {todo}")
    else:
        for idx, todo in enumerate(todo_list):
            if f"[Priority: {PRIORITIES[priority]}]" in todo:
                print(f"({idx}) - {todo}")

# Rama final del nesting, o agrupado de comandos.
mycommands.add_command(hello)
mycommands.add_command(add_todo)
mycommands.add_command(delete)
mycommands.add_command(list_todo)

# Permite mostrar la aplicación por consola.
if __name__ == "__main__":
    mycommands()