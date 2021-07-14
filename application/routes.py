from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from flask import Flask, render_template, request
from application import app, db
from application.models import Games
from application.models import Task
from application.models import BasicForm, myForm
@app.route('/add/<word>')
def add(word):
    #new_game = Games(name="New Game")
    new_task = Task(name=word,complete=False)
    db.session.add(new_task)
    db.session.commit()
    return f"Added new task to database: {word}"

@app.route('/read')
def read():
    #all_games = Games.query.all()
    all_tasks= Task.query.all()
    tasks_string = ""
    for task in all_tasks:
        tasks_string += "<br>"+ task.name + " " + str(task.complete)
    return tasks_string

@app.route('/update/<nameIn>/<update>')
def update(nameIn,update):
    task = Task.query.filter_by(name=nameIn).first()
    task.name = update
    db.session.commit()
    return task.name

@app.route('/status/<taskName>/<status>')
def status(taskName,status):
    task = Task.query.filter_by(name=taskName).first()
    if(status=='complete'):
        task.complete=True
        db.session.commit()
    elif(status=='incomplete'):
        task.complete=False
        db.session.commit()
    return redirect(url_for('read'))


@app.route('/delete/<taskName>')
def delete(taskName):
    task = Task.query.filter_by(name=taskName).first()
    db.session.delete(task)
    db.session.commit()
    return 'Deleted the selected task'

@app.route('/return')
def returnNum():
    total=Games.query.count()
    return str(total)

@app.route('/harry')
def harry():
    return render_template('harry.html')

@app.route('/ben')
def ben():
    return render_template('ben.html')

@app.route('/list')
def list():
    return render_template('list.html',users=["ben", "harry", "bob", "jay", "matt", "bill"])

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def register():
    error=""
    form = BasicForm()

    if request.method=='POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        height=form.height.data
        years=form.years.data
        date=form.date.data
        confirm=form.confirm.data

        if len(first_name) == 0 or len(last_name) == 0:
            error = 'Please supply both first and last name'
        else:
            return f'Thank you {first_name} {last_name}. You are {years} years old and {height}m tall. The selected date is {str(date)} and Language {confirm} '

    return render_template('home.html',form=form,message=error)

@app.route('/register',methods=["GET","POST"])
def postName():
    form=myForm()
    if form.validate_on_submit():
        username = form.username.data
        return render_template('register.html',form=form,username=username)
    else:
        return render_template('register.html',form=form,username="")
        