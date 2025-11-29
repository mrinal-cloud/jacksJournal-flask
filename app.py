from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys




app = Flask(__name__)

# Use the environment variable for deployment, or fall back to a local SQLite/Postgres URL for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('Render_DATABASE_URI', 'postgresql://postgres:mrinalDB@localhost:7996/jacksJournals') 
# The second is your local development fallback

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- TEMPORARY DATABASE SETUP BLOCK ---

# Check if the script was run with the special 'db_init' argument
# if 'db_init' in sys.argv:
#     with app.app_context():
#         print("Running one-time database setup (db.create_all())...")
#         db.create_all()
#         print("Database setup complete. Exiting script.")
#         # Exit with success code 0 so the deployment doesn't get stuck
#         sys.exit(0)
# --- END TEMPORARY BLOCK ---

@app.shell_context_processor
def make_shell_context():
    # This automatically loads these variables when you run 'flask shell'
    # return {'db': db, 'User': User, 'app': app}
    return {'app': app, 'db': db}


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
    category = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"


# This ensures tables are created/present on EVERY startup
# ----------------------------------------------------
with app.app_context():
    # This call attempts to create tables that don't exist. 
    # It does nothing if the tables are already present.
    db.create_all()


@app.route('/')
def home(): 
    tasks = Task.query.all()
    return render_template('home.html', allTasks=tasks)   

@app.route('/show', methods=['GET', 'POST'])
def showAll():
    if request.method=='POST':
        title = request.form['fTitle']
        desc = request.form['fDescription']
        catg = request.form['fCategory']
        task = Task(title=title, description=desc, category=catg)
        db.session.add(task)
        db.session.commit()
        
    tasks = Task.query.all() 
    return render_template('journals.html', allTasks=tasks)    

@app.route('/update/<int:taskId>', methods=['GET', 'POST'])
def updateTask(taskId):

    if request.method == 'POST':
        title=request.form['fTitle']
        desc=request.form['fDescription']
        catg=request.form['fCategory']

        uTask=Task.query.filter_by(id=taskId).first()
        uTask.title=title
        uTask.description=desc
        uTask.category=catg
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



@app.route('/show/<int:taskId>')
def showThis(taskId):
    thisTask=Task.query.filter_by(id=taskId).first()
   
    return render_template('details.html', Task=thisTask)    












if __name__ == "__main__":
    app.run(debug = True, port = 3000)
