# -*- coding: utf-8 -*-
from flask import *
from flask import session as login_session
from sqlalchemy.exc import IntegrityError
from model import *
from werkzeug.utils import secure_filename
import json, ast
import datetime
import os
from forms import ContactForm
import pyperclip
#Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Flask Mail
from flask_mail import Message, Mail

mail = Mail()

UPLOAD_FOLDER = 'static/productsImages'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'boomboompass.game@gmail.com'
app.config["MAIL_PASSWORD"] = 'Qloai1107'



mail.init_app(app)

# LOCAL
engine = create_engine('sqlite:///database.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

# FIREBASE
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'boom-boom-pass-website',
})

db = firestore.client()

doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})
  
doc_ref = db.collection(u'users').document(u'aturing')
doc_ref.set({
    u'first': u'Alan',
    u'middle': u'Mathison',
    u'last': u'Turing',
    u'born': 1912
})
snippets.py


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/',methods=['GET','POST'])
@app.route('/bbp', methods=['GET','POST'])
def betaSignup():
	form = ContactForm()

	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']

		form.name=name
		form.email=email
		form.message="Good Luck!"

		# if form.name != "" and form.email!= "" and form.message != "":
		# 	msg = Message("Beta Signup!", sender='BBP.Beta@gmail.com', recipients=['boomboompass.game@gmail.com'])
		# 	msg.body = """
		# 	Registered: %s <%s>
		# 	%s
		# 	""" % (form.name, form.email, form.message)
		# 	mail.send(msg)
		# 	print("message sent")

		EmailObject = Emails(name=name,email=email)
		session.add(EmailObject)
		session.commit()
	
	return render_template('index.html', form=form)

@app.route('/bugs', methods=['GET','POST'])
def bugReporting():
	form = ContactForm()

	if request.method == 'POST':
		form.name = request.form['name']
		form.email = request.form['email']
		form.message = request.form['message']

		if form.name != "" and form.email!= "" and form.message != "":
			msg = Message("Bug Report", sender='NoReply_BBP_Bugs@gmail.com', recipients=['boomboompass.game@gmail.com'])
			msg.body = """
			From: %s <%s>
			Message: %s
			""" % (form.name, form.email, form.message)
			mail.send(msg)
			print("message sent")

			return render_template('bugReport.html',done=True)
	
	return render_template('bugReport.html')

@app.route('/admin',methods=['GET','POST'])
def adminSignin():
	if 'idAdmin' in login_session:
		admin = session.query(Admin).filter_by(id=login_session['idAdmin']).one()
		return redirect(url_for('admin'))

	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"]
		
		adminCheck=session.query(Admin).filter_by(username=username).first()

		if(adminCheck != None and adminCheck.password==password):
			# Logged in successfully
			login_session['idAdmin'] = adminCheck.id
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('adminSignin'))
	else:
		return render_template('adminSignin.html')

@app.route('/admin-panel-secret-login', methods=['GET','POST'])
def admin():
	if 'idAdmin' in login_session:
		emails = session.query(Emails).all()

		return render_template('admin.html' , emails=emails)
	else:
		return redirect(url_for('adminSignin'))

@app.route('/deleteEmail/<id>', methods=['GET','POST'])
def deleteEmail(id):
	if 'idAdmin' in login_session:
		email = session.query(Emails).filter_by(id=id).first()

		session.delete(email)
		session.commit()

	return redirect(url_for('admin'))	

@app.route('/copyEmails',methods=['GET','POST'])
def copyEmails():
	if 'idAdmin' in login_session:
		emails = session.query(Emails).all()

		emailsList=[]
		for email in emails:
			emailsList.append(str(email.email))

		emailsToCopy = ",".join(emailsList)

		pyperclip.copy(emailsToCopy)

		return redirect(url_for('admin'))
	else:
		return redirect(url_for('adminSignin'))

@app.route('/logout', methods=['GET','POST'])
def logout():
	if 'idAdmin' in login_session:
		del login_session['idAdmin']
	return redirect(url_for('adminSignin'))


if __name__ == '__main__':
	app.run(debug=True)
