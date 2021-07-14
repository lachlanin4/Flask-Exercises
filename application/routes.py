from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from flask import Flask, render_template, request
from application import app, db
from application.models import Games
from application.models import Task
from application.models import BasicForm, myForm, ShowToDoList
@app.route('/add',methods=['GET','POST'])
def add():
    error=""
    form=ShowToDoList()
    
    if request.method=='POST':
        name=form.name.data
        description=form.description.data
        if len(name)<3 or len(description)<3:
            error='Plese add an appropriate task'
        else:
            
            new_task = Task(name=name,description=description,complete=False)
            db.session.add(new_task)
            db.session.commit() 
            return 'Added the new task!'
    return render_template('addtask.html',form=form,message=error)


@app.route('/', methods=['GET','POST'])
@app.route('/read',methods=['GET','POST'])
def read():
    form=ShowToDoList()
    forms=['']
    all_tasks= Task.query.all()
    tasks_string = ""
    for task in all_tasks:
        tasks_string += "<br>"+ task.name + " " + task.description + " " + str(task.complete)
    return tasks_string
    for task in all_tasks:
        form.name=task.name
        form.description=task.description
        form.status=task.complete
        forms.append(form)

    return render_template('homeTask.html',tasks=forms,form=form)

@app.route('/update',methods=['GET','POST'])
def update():
    error=""
    form=ShowToDoList()
    
    if request.method=='POST':
        
        if len(form.name.data)<3 or Task.query.filter_by(name=form.name.data).first()==False:
            error='Plese search for an existing task'
        else:
            task = Task.query.filter_by(name=form.name.data).first()
            task.description=form.description.data
            db.session.commit() 
            return 'Updated the task!'
    return render_template('addtask.html',form=form,message=error)

@app.route('/status',methods=['GET','POST'])
def status():
    error=""
    form=ShowToDoList()
    
    if request.method=='POST':
        
        if len(form.name.data)<3:
            error='Plese search for an existing task'
        else:
            task = Task.query.filter_by(name=form.name.data).first()
            task.complete=True
            db.session.commit()
            return 'Completed the task'
    return render_template('deleteTask.html',form=form,message=error)


@app.route('/delete',methods=['GET','POST'])
def delete():
    error=""
    form=ShowToDoList()
    
    if request.method=='POST':
        
        if len(form.name.data)<3:
            error='Plese search for an existing task'
        else:
            task = Task.query.filter_by(name=form.name.data).first()
            db.session.delete(task)
            db.session.commit()
            return 'Deleted the task!'
    return render_template('deleteTask.html',form=form,message=error)

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

@app.route('/oldhome', methods=['GET','POST'])
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
