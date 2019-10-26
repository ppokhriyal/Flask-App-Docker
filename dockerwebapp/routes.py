from flask import render_template,url_for,flash,redirect,request,abort,session
from dockerwebapp import app,db,bcrypt,login_manager
from dockerwebapp.forms import LoginForm
from dockerwebapp.models import User
from flask_login import login_user,current_user,logout_user,login_required


#Docker Web App Login Page
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		next_page = request.args.get('next')
		if form.username.data == 'DockerAdmin' and form.password.data == 'dockeradmin':
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check the username and password','danger')
	return render_template('login.html',title='Login',form=form)

#Docker Home Page
@app.route('/home')
@login_required
def home():
	return render_template('home.html',title='Home')