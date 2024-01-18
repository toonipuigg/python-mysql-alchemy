# The code `from flask import Flask` imports the Flask class from the Flask module, which is a web
# framework for Python.
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# The code `app = Flask(__name__)` creates a Flask application object. The `__name__` argument is a
# special Python variable that represents the name of the current module. This is necessary for Flask
# to know where to look for resources such as templates and static files.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:27112003T@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# The code `app.app_context().push()` creates an application context for the Flask application. This
# is necessary for the application to access resources such as the database.
app.app_context().push()
db = SQLAlchemy(app)
ma = Marshmallow(app)

# The above class defines a Task model with id, title, and description attributes, and an initializer
# method.
#Creamos el modelo para acceder 
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
        
# The `db.create_all()` function is used to create all the database tables defined in the models. It
# creates the tables based on the models defined in the code.

##Lee todas las clases que sean db.Models.
##Crea todas las tablas que tengamos definidas como en este caso Task
db.create_all()

#Creamos un esquema para interactuar de forma facil con nuestros modelos
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

##Definimos las rutas de nuestra API Request

@app.route('/tasks', methods=['POST'])
def create_task():
    
    #print(request.json)
    title = request.json['title']
    description = request.json['description']

    #Llamamos al constructor de Task para crear una nueva tarea
    new_task = Task(title, description)
    print("Tarea creada con exito")
        
    ##Almacenamos os datos en la base de datis
    db.session.add(new_task)
    db.session.commit()
    print("Almacenamiento en la base de datos --> OK!")
    return task_schema.jsonify(new_task)

#Ruta READ ALL tasks - GET
@app.route('/tasks', methods=['GET'])
def get_tasks():
    #Nos devuelve todas las tareas
    all_tasks = Task.query.all()
    #Lista con los datos
    result = task_schema.dump(all_tasks)
    #Convertimos en JSON los resultados del select de la base de datos por el ORM
    return jsonify(result)

##Ruta READ Single Task - GET
@app.route('/task/<id>', methods = ['GET'])
def get_task(id):
    task = Task.query.get(id)
    
    return task_schema.jsonify(task)

#Ruta UPDATE Task - PUT
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.session.get(Task, id)
    title = request.json['title']
    description = request.json['description']
    
    task.title = title
    task.description = description
    
    db.session.commit()
    
    return task_schema.jsonify(task)

##Ruta DELETE Task - DELETE
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.session.get(Task, id)
    
    db.session.delete(task)
    db.session.commit()
    
    return task_schema.jsonify(task)

## Ruta de landing Page - Pagina de Inicio /
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : 'Welcome to my first API with Python Flask and MySQL'})

#Ruta Delete ALL tasks - DELETE
@app.route('/tasks/delete', methods=['DELETE'])
def delete_tasks():
    db.session.query(Task).delete()
    db.session.commit()
    
    return jsonify({"message":"All tasks deleted!!!"})

if __name__ == "__main__":
    app.run(debug=True)