from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash
import datetime
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

techcafeApp = Flask(__name__)
db          = MySQL(techcafeApp)
adminSesion = LoginManager(techcafeApp)

@adminSesion.user_loader
def cargarUsuario():
    return ModelUser.get_by_id(db, id) 

@techcafeApp.route('/')
def home():
    return render_template('home.html')

@techcafeApp.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre'] 
        correo = request.form['correo']
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        fechareg = datetime.datetime.now()
        reUsuario = db.connection.cursor()
        reUsuario.execute("INSERT INTO usuario (nombre, correo, clave, fechareg)VALUES(%s,%s,%s,%s)",(nombre, correo, claveCifrada, fechareg))
        db.connection.commit()
        return render_template('home.html') 
    else: 
        return render_template('signup.html')

@techcafeApp.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None, None)
        usuarioAutenticado = ModelUser.signin(db,usuario)
        if usuarioAutenticado is not None:
            login_user(usuarioAutenticado)
            if usuarioAutenticado.clave:
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template('user.html')
            else:
                return 'Contraseña Incorrecta'
        else:
            return 'Correo no encontrado'        
    else:
        return render_template('signin.html')

@techcafeApp.route('/signout',methods=['GET','POST'])
def signout():
    logout_user() 
    return render_template('home.html')


if __name__ == '__main__':
    techcafeApp.config.from_object(config['development'])
    techcafeApp.run(port=3300)    