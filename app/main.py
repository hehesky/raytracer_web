
import json, uuid
from app import webapp
import app.db_util
import app.login
from app.lambda_lib import invoke_render

from flask import session, request, render_template, redirect, url_for

@webapp.route('/')
@webapp.route('/index')
def index():
    if 'username' not in session:
        return render_template("index.html")
    else:
        return redirect(url_for('dashboard'))

@webapp.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username=request.form['username']
        password=request.form['password']
 
        result=app.login.login(username,password)
        if result is True:
            session['username']=username
            return redirect(url_for('dashboard'))
        else:
            return render_template("login_fail.html")
             
@webapp.route('/register',methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username=request.form['username']
        password=request.form['password']
 
        if app.login.register(username,password) is True:
            session['username']=username
            return redirect(url_for('dashboard'))
        else:
            return "Username not available"
        
@webapp.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    #TODO:get past user request
    result=app.db_util.get_user_requests(session['username'])
    
    return render_template("dashboard.html",username=session['username'],result=str(result))

@webapp.route("/form", methods=["GET", "POST"])
def form():
    if request.method == 'GET':
        return render_template("form.html")
    else:
        entities = request.form['output_json']
        
        entities=str(entities)
        d={
            'id': str(uuid.uuid4())[:18] +".png",
            "entities":json.loads(entities)   
        }
        #insert pending request to db
        app.db_util.insert_pending_user_request(session['username'],d['id'])
        #invoke lambda function
        app.lambda_lib.invoke_render(d)

        return redirect(url_for('dashboard'))
    
@webapp.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@webapp.route("/request",methods=["GET",'POST'])
def render_request():
    return "To be implemented"