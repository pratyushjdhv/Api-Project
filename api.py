from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite3"
db = SQLAlchemy(app)

class todo_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)

class todo_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'), nullable=False)
    todolist = db.relationship('todo_list', backref=db.backref('tasks', lazy=True))

with app.app_context():
    db.create_all()

class create_todo(Resource):
    def post(self):
        data = request.get_json()
        title = data['title']
        tasks = data['task']
        
        if not title.strip():
            return jsonify({"message": "Title cannot be empty"}), 400
        if not tasks:
            return jsonify({"message": "Task cannot be empty"}), 400

        todo = todo_list.query.filter_by(title=title).first()
        if not todo:
            new_todo = todo_list(title=title)
            db.session.add(new_todo)
            db.session.flush()  # Flush the session to temp save and get the id
            
            for task in tasks:
                new_task = todo_task(task=task, list_id=new_todo.id)
                db.session.add(new_task)
            db.session.commit()
            return jsonify({"message": "Todo-list created"})
        else:
            for task in tasks:
                new_task = todo_task(task=task, list_id=todo.id)
                db.session.add(new_task)
            db.session.commit()
            return jsonify({"message": "todo_task added to existing Todo-list"})

    def put(self, task_id):
        data = request.get_json()
        tasks = data['task']
        new_task = todo_task.query.filter_by(id=task_id).first()
        if not new_task:
            return jsonify({"message": "Task not found"})
        for task in tasks:
            new_task.task = task
        db.session.commit()
        return jsonify({"message": "Task updated"}) 


class delete_todolist(Resource):
    def delete(self, list_id):
        todo = todo_list.query.filter_by(id=list_id).first()
        taskk = todo_task.query.filter_by(list_id=list_id).all()
        print(todo)
        print(taskk)
        if not todo:
            return jsonify({"message": "Todo-list not found"})
        db.session.delete(todo)
        for task in taskk:
            db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Todo-list deleted"})

        


class print_todo(Resource):
    def get(self, task_id=None):
        if task_id:
            todos = todo_task.query.filter_by(list_id=task_id).all()
            listt = []
            for todo in todos:
                listt.append(todo.task)
            return jsonify({"tasks": listt})
        else:
            todos = todo_list.query.all()
            all_task = []
            for todo in todos:
                tasks = todo_task.query.filter_by(list_id=todo.id).all()
                temp_list = [task.task for task in tasks]
                all_task.append({"title": todo.title, "tasks": temp_list})
            return jsonify({"tasks": all_task})
        

api.add_resource(create_todo, '/todo' , '/todo/<int:task_id>')
api.add_resource(delete_todolist, '/todo/list/<int:list_id>')
api.add_resource(print_todo, '/todo/task', '/todo/task/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)