from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelProduct import ModelProduct

# Entities:
from models.entities.User import User
from models.entities.Product import Product

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    products = ModelProduct.get_all_products(db)
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            user = User(request.form['email'], request.form['password'])
            logged_user = ModelUser.login(db, user)
            if logged_user != None:
                if logged_user.password:
                    login_user(logged_user)
                    return redirect(url_for('index'))
                else:
                    flash("Contraseña incorrecta...")
                    return render_template('auth/login.html')
            else:
                flash("Email no encontrado...")
                return render_template('auth/login.html')
        else:
            return render_template('auth/login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            # Obtener los datos del formulario de registro
            email = request.form['email']
            password = request.form['password']
            username = email.split('@')[0] # Extraer el nombre de usuario del correo electrónico
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = request.form['age']

            # Verificar si el email ya está registrado
            existing_user = ModelUser.get_by_email(db, email)
            if existing_user:
                flash('El email ya está registrado. Por favor, use otro.', 'error')
                return redirect(url_for('registro'))

            # Crear un nuevo usuario
            new_user = User(email=email, password=password, username=username, 
                            first_name=first_name, last_name=last_name, age=age, id_rol=3)

            ModelUser.create_user(db, new_user)

            flash('¡Registro exitoso! Por favor, inicie sesión.', 'success')
            return redirect(url_for('login'))
        else:
            return render_template('auth/registro.html')

@app.route('/mi_perfil')
def mi_perfil():
    # Verificar si el usuario está autenticado
    if current_user.is_authenticated:
        #user_info = ModelUser.get_by_email(db, current_user.email) NO HACE FALTA
        #print(user_info.get_string_info()) NO HACE FALTA
        return render_template('pages/mi_perfil.html', usuario=current_user)
    else:
        flash('Debes iniciar sesión para ver tu perfil.', 'warning')
        return redirect(url_for('login'))

@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    # Verificar si el usuario está autenticado
    if current_user.is_authenticated:
        if request.method == 'POST':
            # Obtener los datos del formulario de edición de perfil
            email = current_user.email # No se puede editar el email
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = request.form['age']

            # Actualizar el usuario en la base de datos
            ModelUser.update_profile(db, email, first_name, last_name, age)

            flash('¡Perfil actualizado correctamente!', 'success')
            return redirect(url_for('mi_perfil'))
        else:
            # Si la solicitud es GET, renderizar el formulario de edición de perfil
            return render_template('pages/editar_perfil.html')
    else:
        flash('Debes iniciar sesión para poder editar tu perfil.', 'warning')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

@app.route('/añadir_producto', methods=['GET', 'POST'])
def añadirproducto():
    # Verificar si el usuario está autenticado
    if current_user.is_authenticated:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            trueque = request.form['trueque']
            vendedor = ModelUser.get_id(db, current_user.email)
            print(vendedor)
            # Crear un nuevo producto
            new_product = Product(name=name, description=description, trueque=trueque, vendedor=vendedor)

            ModelProduct.create_product(db, new_product)

            flash('¡Añadido exitoso!.', 'success')
            return redirect(url_for('index'))
        return render_template('pages/añadir_producto.html')
    else:
        flash('Debes iniciar sesión para añadir productos.', 'warning')
        return redirect(url_for('login'))


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404
    #return render_template('404.html'), 404 # para mostrar que se equivocó
    #return redirect(url_for('index')) # para redireccionar a la página principal


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
