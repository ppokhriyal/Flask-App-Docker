import docker
from cpuinfo import get_cpu_info
from psutil import virtual_memory
from flask import render_template, url_for, flash, redirect, request, abort, session
from dockerwebapp import app, db, bcrypt, login_manager
from dockerwebapp.forms import LoginForm,ChangePasswordForm
from dockerwebapp.models import User
#from dockerwebapp.dockerinfo import dockerinfo ,cpu,ram,container_count,image_count,volume_count,docker_container,docker_image,docker_volume,docker_network
from flask_login import login_user, current_user, logout_user, login_required



def docker_refresh():

	#System Information
	#Get CPU information
	cpu = get_cpu_info()
	#Get Memory Information
	mem = virtual_memory()
	ram = mem.total / 1024 / 1024 / 1024

	#Connect to Docker Socket
	apiclient = docker.APIClient(base_url='unix://var/run/docker.sock')
	client = docker.from_env()

	#APIClient Informations [Low Level API]
	dockerinfo = apiclient.version()
	container_count = len(apiclient.containers(all=True))
	image_count = len(apiclient.images(all=True))
	docker_container = apiclient.containers(all=True)
	docker_image = apiclient.images(all=True)
	docker_volume = apiclient.volumes()
	docker_network = apiclient.networks()
	#High Level API
	volume_count = len(client.volumes.list())

	return[apiclient,client,dockerinfo,container_count,image_count,docker_container,docker_image,docker_volume,docker_network,volume_count,cpu,ram]



#Docker Home Page
@app.route('/home')
@login_required
def home():

	dock_func_list=docker_refresh()

	return render_template('home.html',title='Home',dockerinfo=dock_func_list[2],cpu=dock_func_list[10],ram=dock_func_list[11],container_count=dock_func_list[3],
		image_count=dock_func_list[4],volume_count=dock_func_list[9],network_count=len(dock_func_list[8]))

#Docker Web App Login Page
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check the username and password','danger')
	return render_template('login.html',title='Login',form=form)

#Change Password
@app.route('/change_password',methods=['GET','POST'])
@login_required
def changepassword():
	form = ChangePasswordForm()
	user = User.query.get(1)
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f"Your DockerAdmin password has been changed",'success')
	return render_template('change_password.html',form=form,title='Change Password')

#Docker Containers
@app.route('/containers',methods=['GET','POST'])
@login_required
def containers():
	dock_func_list = docker_refresh()
	return render_template('containers.html',title='Containers',container_count=dock_func_list[3],docker_container=dock_func_list[5])	

#Docker Images
@app.route('/images',methods=['GET','POST'])
@login_required
def images():
	dock_func_list = docker_refresh()
	return render_template('images.html',title='Images',image_count=dock_func_list[4],docker_image=dock_func_list[6])

#Remove Docker Images
@app.route('/images/delete/<string:image_id>',methods=['GET','POST'])
@login_required
def delete_image(image_id):

	dock_func_list = docker_refresh()
	dock_func_list[0].remove_image(image_id)	
	dock_func_list = docker_refresh()
	
	return render_template('images.html',title='Images',image_count=dock_func_list[4],docker_image=dock_func_list[6])




#Docker Volumes
@app.route('/volumes',methods=['GET','POST'])
@login_required
def volumes():
	dock_func_list=docker_refresh()
	return render_template('volumes.html',title='Volumes',volume_count=dock_func_list[9],docker_volume=dock_func_list[7])

#Docker Networks
@app.route('/networks',methods=['GET','POST'])
@login_required
def networks():
	dock_func_list=docker_refresh()
	return render_template('networks.html',title='Networks',docker_network=dock_func_list[8],network_count=len(dock_func_list[8]))

#Logout
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


