from flask import Flask, render_template, url_for, redirect, request, flash, Blueprint, jsonify, session 
from psycopg2.extras import RealDictCursor, DictCursor
import os
import uuid
import psycopg2
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from Models.ModelUser import ModuleUser
from Models.entities.user import User


app = Flask(__name__)


@app.route("/home")
@app.route("/")
def root():
    return "Hola"


#-------------APARTADO LOGIN---------------------------#
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    return render_template('login.html')

@app.route('/loguear', methods=['POST'])
def loguear():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        print(f"Datos recibidos: correo={correo}, password={password}")

        if not correo or not password:
            print("Correo o contraseña vacíos.")
            flash('Correo y/o contraseña incorrectos.')
            return redirect(url_for('login'))
        
        loged_user = ModuleUser.login(get_db_connection(), correo, password)
        
        print(f"Loged_user: {loged_user}")
        if loged_user:
            login_user(loged_user)
            session['flash_message_shown'] = False  # Restablece el estado del mensaje flash

        if loged_user:
            login_user(loged_user)
            return redirect(url_for('index'))  
        else:
            flash('Correo y/o contraseña incorrectos.')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('flash_message_shown', None) 
    return redirect(url_for('index'))







if __name__ == "__main__":
    app.run(port=8080, debug=True, host="0.0.0.0")



