from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from flask_mail import Mail, Message
from flask import send_file
from io import BytesIO
from werkzeug.security import generate_password_hash
import datetime
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

techcafeApp = Flask(__name__)
#PythonAnywhere
techcafeApp.config.from_object(config['development'])
techcafeApp.config.from_object(config['mail'])
db          = MySQL(techcafeApp)
mail        = Mail(techcafeApp)

adminSesion = LoginManager(techcafeApp)

@adminSesion.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id) 

@techcafeApp.route('/')
def home():
    return render_template('home.html')


@techcafeApp.route('/admin')
def admin():
    return render_template('admin.html')

@techcafeApp.route('/user')
def user():
    productos = obtener_productos()
    return render_template('user.html', productos=productos)


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
        msg = Message(subject='Bienvenido a Techcafe', recipients=[correo])
        msg.body = 'Este es un correo con una imagen adjunta'
        with open('static/img/011.png', 'rb') as f:
            img_data = f.read()
            msg.attach('011.png', 'image/png', img_data)
        msg.html = render_template('mail.html', nombre=nombre)
        mail.send(msg)
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
                flash('Contraseña incorrecta')
                return redirect(request.url)
        else:
            flash('Usuario inexistente')
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
    return render_template('usuarios.html', usuarios=u)

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
    flash('Usuario eliminado exitosamente')
    return redirect('/sUsuario')

@techcafeApp.route('/sProducto', methods=['GET','POST'])
def sProducto():
    selProducto = db.connection.cursor()
    selProducto.execute("SELECT * FROM productos")
    p = selProducto.fetchall()
    selProducto.close()
    return render_template('productos.html', productos=p)

@techcafeApp.route('/iProducto', methods=['POST'])
def iProducto():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    categoria = request.form['categorias']
    existencias = request.form['existencias']

    # Verifica si se subió una imagen
    imagen = request.files.get('imagen')  # Este es el archivo de la imagen
    
    if imagen:
        # Guardar la imagen en la carpeta static/img
        imagen_filename = imagen.filename
        imagen_path = f"static/img/{imagen_filename}"
        imagen.save(imagen_path)
    else:
        imagen_filename = None  # No se subió ninguna imagen

    cursor = db.connection.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, precio, categoria, existencias, imagen)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, descripcion, precio, categoria, existencias, imagen_filename))
    db.connection.commit()
    flash('Producto agregado exitosamente.')
    return redirect('/sProducto')

@techcafeApp.route('/uProducto/<int:id>', methods=['POST'])
def uProducto(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    categoria = request.form['categorias']
    existencias = request.form['existencias']

    # Verifica si se subió una nueva imagen
    imagen = request.files.get('imagen')
    
    cursor = db.connection.cursor()
    
    if imagen:
        # Guardar la imagen en la carpeta static/img
        imagen_filename = imagen.filename
        imagen_path = f"static/img/{imagen_filename}"
        imagen.save(imagen_path)
    else:
        # Si no se subió una nueva imagen, mantén la imagen existente
        cursor.execute("SELECT imagen FROM productos WHERE id_producto = %s", (id,))
        imagen_filename = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE productos
        SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, existencias = %s, imagen = %s
        WHERE id_producto = %s
    """, (nombre, descripcion, precio, categoria, existencias, imagen_filename, id))
    db.connection.commit()
    flash('Producto actualizado exitosamente.')
    return redirect('/sProducto')


@techcafeApp.route('/dProducto/<int:id>', methods=['POST'])
def dProducto(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    db.connection.commit()
    flash('Producto eliminado exitosamente.')
    return redirect('/sProducto')

if __name__ == '__main__':
    techcafeApp.config.from_object(config['development'])
    techcafeApp.run(port=3300)
