from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Initialize Flask application
app = Flask(__name__)

# Initialize database as SQLite for the todos using SQLAlchemy

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create the columns for the Todos database
class Todo(db.Model):

    # Initialize the types and set the id as the primary query key
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Routing code for the index page
@app.route("/")
def home():

    # Query all the todos from the database
    todo_list = Todo.query.all()

    # Render the index HTML and the todos
    return render_template("base.html", todo_list=todo_list)

# Routing code for the add page
@app.route("/add", methods=["POST"])
def add():

    # Get the todo task name
    title = request.form.get("title")

    # If todo is not empty string, add it to the todo task list via database
    if (title != ''):
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)

        # Commit the changes to the database
        db.session.commit()
    
    # Return to the index page
    return redirect(url_for("home"))

# Routing code for the update page for each todo task
@app.route("/update/<int:todo_id>")
def update(todo_id):

    # Find the first todo that has the same id as the query id
    todo = Todo.query.filter_by(id=todo_id).first()

    # Reverse the completion status of the todo
    todo.complete = not todo.complete

    # Commit the changes to the database
    db.session.commit()

    # Return to the index page
    return redirect(url_for("home"))

# Routing code for the delete page for each todo task
@app.route("/delete/<int:todo_id>")
def delete(todo_id):

    # Find the first todo that has the same id as the query id
    todo = Todo.query.filter_by(id=todo_id).first()

    # Delete the todo from the todo list
    db.session.delete(todo)

    # Commit the changes to the database
    db.session.commit()

    # Return to the index page
    return redirect(url_for("home"))

# Main/default method to run the application and create the database
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)