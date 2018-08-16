# -*- coding: utf-8 -*-
from flask import *
from flask import session as login_session
from sqlalchemy.exc import IntegrityError
from model import *
from werkzeug.utils import secure_filename
import json, ast
import datetime
import os

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
app.config["MAIL_USERNAME"] = 'topperfum1@gmail.com'
app.config["MAIL_PASSWORD"] = 'Blackisblack212'

mail.init_app(app)

# LOCAL
engine = create_engine('sqlite:///database.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/',methods=['GET','POST'])
@app.route('/bbp', methods=['GET','POST'])
def betaSignup():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']

		EmailObject = Emails(name=name,email=email)
		session.add(EmailObject)
		session.commit()
	
	return render_template('index.html')



if __name__ == '__main__':
	app.run(debug=True)
