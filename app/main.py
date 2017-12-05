import json
import uuid
from app import webapp
import app.db_util
import app.login
from app.lambda_lib import invoke_render
from operator import itemgetter
from flask import session, request, render_template, redirect, url_for

@webapp.route('/')
def main():
    return redirect(url_for('index'))

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
            return render_template("login.html", message="Your username/password is wrong. Please try again.")
             
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
            return render_template("register.html", message="Username not available. Please try another username.") 
        
@webapp.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    #TODO:get past user request
    result=sorted(app.db_util.get_user_requests(session['username']), key=itemgetter('timestamp'), reverse=True)
    
    return render_template("dashboard.html",page = 'dashboard', username=session['username'],requests=result)

@webapp.route("/public")
def public_images():
    if 'username' not in session:
        return redirect(url_for('index'))

    #TODO:get past user request
    result=sorted(app.db_util.get_public_request(), key=itemgetter('timestamp'), reverse=True)
    
    return render_template("public.html",page ='public', username=session['username'],requests=result)


@webapp.route("/updateOwnership/", methods=['GET'])
def updateOwnership():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    image_id = request.args.get('image_id')
    ownership = request.args.get('ownership')
    print(ownership)
    result = app.db_util.update_request(session['username'], image_id, ownership)
       
    return redirect(url_for('image', image_id= image_id, page = 'dashboard'))

@webapp.route("/showImage/", methods=['GET'])
def showImage():
    image_id = request.args.get('image_id')
    page = request.args.get('page')
   
    if not image_id:
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('image', page = page, image_id=image_id))

@webapp.route("/image")
def image():

    if 'username' not in session:
        return redirect(url_for('index'))
    
    image_id = request.args.get('image_id')
    page = request.args.get('page')
    
    result = app.db_util.get_image_entities(image_id)
    entities = ''
    if result and 'entities' in result:
        entities = sorted(result['entities'], key=itemgetter('type'))
    
    return render_template('image.html', page = page, image_id=image_id, result = result, entities=entities)


@webapp.route("/delete/<image_id>")
def delete(image_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    print(image_id)
    print(session['username'])
    
    result=app.db_util.delete_request(session['username'], image_id)
    
    return redirect(url_for('dashboard'))


@webapp.route("/form", methods=["GET", "POST"])
def form():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template("form.html", page = 'form')
    else:
        entities = request.form['output_json']
        
        entities=str(entities)
        d={
            'id': str(uuid.uuid4())[:18] +".png",
            "entities":json.loads(entities)   
        }
        
        ownership = 'private'
        #insert pending request to db
        app.db_util.insert_pending_user_request(session['username'],d['id'], d['entities'], ownership)
        #invoke lambda function
        invoke_render(d)
        
        return redirect(url_for('dashboard'))
    
@webapp.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@webapp.route("/request",methods=["GET",'POST'])
def render_request():
    return "To be implemented"