from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os



app = Flask(__name__)

# Use the environment variable for deployment, or fall back to a local SQLite/Postgres URL for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'Render_DATABASE_URI', 
    'postgresql://postgres:mrinalDB@localhost:7996/jacksJournals'  # This is your local development fallback
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# @app.shell_context_processor
# def make_shell_context():
#     # This automatically loads these variables when you run 'flask shell'
#     # return {'db': db, 'User': User, 'app': app}
#     return {'app': app, 'db': db}


class User(db.Model):
    # Define the table name (optional, but good practice)
    __tablename__ = 'users'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # A simple string representation for debugging
    def __repr__(self):
        return f'User {self.username}'
    

class Task(db.Model):
    # Define the table name (optional, but good practice)
    # __tablename__ = 'jacksTasks'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method=='POST':
        title = request.form['fTitle']
        desc = request.form['fDescription']
        task = Task(title=title, description=desc)
        db.session.add(task)
        db.session.commit()
        
    tasks = Task.query.all() 
    return render_template('index.html', allTasks=tasks)
    


@app.route('/show')
def products():
    tasks = Task.query.all()
    print(tasks)
    return 'this is products page'

@app.route('/update/<int:taskId>', methods=['GET', 'POST'])
def updateTask(taskId):

    if request.method == 'POST':
        title=request.form['fTitle']
        desc=request.form['fDescription']
        uTask=Task.query.filter_by(id=taskId).first()
        uTask.title=title
        uTask.description=desc
        # db.session.add(uTask)
        db.session.commit()
        return redirect("/")

    thisTask=Task.query.filter_by(id=taskId).first()
    return render_template('update.html', thisTask=thisTask)


@app.route('/delete/<int:taskId>')
def deleteTask(taskId):

    thisTask=Task.query.filter_by(id=taskId).first()
    db.session.delete(thisTask)
    db.session.commit()
    return redirect("/")
















if __name__ == "__main__":
    app.run(debug = True, port = 3000)