from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash
import datetime
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

techcafeApp = Flask(__name__)
db          = MySQL(techcafeApp)
#PythonAnywhere
techcafeApp.config.from_object(config['development'])
adminSesion = LoginManager(techcafeApp)

@adminSesion.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id) 

@techcafeApp.route('/')
def home():
    '''if session['NombreU']:
        if session['PerfilU'] == 'A':
            return render_template('admin.html')
        else:          
            return render_template('user.html')'''
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
            session['NombreU'] = usuarioAutenticado.nombre
            session['PrefilU'] = usuarioAutenticado.perfil
            if usuarioAutenticado.clave:
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template('user.html')
            else:
                flash('contraseña incorrecta')
                return redirect(request.url)
        else:
            flash('Usuario Inexistente')
            return redirect(request.url)        
    else:
        return render_template('signin.html')

@techcafeApp.route('/signout',methods=['GET','POST'])
def signout():
    logout_user() 
    return render_template('home.html')

@techcafeApp.route('/sUsuario',methods=['GET','POST'])
def sUsuario():
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuario")
    u = selUsuario.fetchall()
    selUsuario.close()
    return render_template('usuarios.html',usuarios = u)

@techcafeApp.route('/iUsuario',methods=['GET','POST'])
def iUsuario():
    nombre = request.form['nombre'] 
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']

    crearUsuario = db.connection.cursor()
    crearUsuario.execute("INSERT INTO usuario (nombre, correo, clave, fechareg, perfil) VALUES (%s,%s,%s,%s,%s)",(nombre, correo, claveCifrada, fechareg, perfil))
    db.connection.commit()
    flash('Usuario Creado')
    return redirect('/sUsuario')

@techcafeApp.route('/uUsuario/<int:id>',methods=['GET','POST'])
def uUsuario(id):
    nombre = request.form['nombre'] 
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']

    editarUsuario = db.connection.cursor()
    editarUsuario.execute("UPDATE usuario SET nombre=%s, correo=%s, clave=%s, fechareg=%s, perfil=%s WHERE id=%s", (nombre, correo, claveCifrada, fechareg, perfil, id))
    db.connection.commit()
    flash('Usuario Editado')
    return redirect('/sUsuario')

@techcafeApp.route('/dUsuario/<int:id>', methods=['GET', 'POST'])
def dUsuario(id):
    
        eliminarUsuario = db.connection.cursor()
        eliminarUsuario.execute("DELETE FROM usuario WHERE id=%s", (id,))
        db.connection.commit()
        flash('User deleted successfully')
        return redirect('/sUsuario')

@techcafeApp.route('/sProducto', methods=['GET','POST'])
def sProducto():
    selProducto = db.connection.cursor()
    selProducto.execute("SELECT * FROM productos")
    p = selProducto.fetchall()
    selProducto.close()
    return render_template('productos.html',productos = p)

'''if __name__ == '__main__':
    techcafeApp.config.from_object(config['development'])
    techcafeApp.run(port=3300)'''    