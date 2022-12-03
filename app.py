from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sl = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sl} - {self.title}"


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route("/", methods=['GET', 'POST'])
def todo():
    if request.method=='POST':
        # print("post")
        # print(request.form['title'])
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    # todo = Todo(title="First Todo", desc="Start investing in Stock market")
    # db.session.add(todo)
    # db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/update/<int:sl>", methods=['GET', 'POST'])
def update(sl):
    if request.method=='POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo.query.filter_by(sl=sl).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sl=sl).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sl>")
def delete(sl):
    todo = Todo.query.filter_by(sl=sl).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>This is product page</p>"

@app.route("/products")
def products():
    return "<p>This is product page</p>"

if __name__ == "__main__":
    app.run(debug=True, port=8000)