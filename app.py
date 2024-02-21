from flask import Flask, flash, redirect, render_template, request, session, url_for
import mysql
import mysql.connector
from cnx import DB_CONFIG
from PIL import Image

from prediction import predict_coffe, predict_corn, predict_rice, predict_tomato



app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

#Inicio Aplicacion
@app.route('/')
def index():
    return render_template('index.html')

#Redirección Login
@app.route('/login')
def login():
    return render_template('login.html')

#Redireccion Account
@app.route('/create_account')
def create_account():
    return render_template('account.html')


#Redireccion Menu
@app.route('/menu')
def menu():
    user_id = session.get('user_id')
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    phone = session.get('phone')
    email = session.get('email')
    password = session.get('password')

    return render_template('free/principal_free.html',user_id=user_id,first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)

#Redireccion Generator Coffe
@app.route('/generator_coffe')
def generator_coffe():
    return render_template('free/ia_coffe.html')

#Redireccion Generator Tomato
@app.route('/generator_tomato')
def generator_tomato():
    return render_template('free/ia_tomato.html')

#Redireccion Generator Corn
@app.route('/generator_corn')
def generator_corn():
    return render_template('free/ia_corn.html')

#Redireccion Generator Rice
@app.route('/generator_rice')
def generator_rice():
    return render_template('free/ia_rice.html')


#Funcion Crear Usuario
@app.route('/save_profile', methods=['POST'])
def save_profile():
    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        new_accountt(first_name, last_name, phone, email, password)
        return redirect(url_for('login'))

#Funcion Nueva Cuenta
def new_accountt(first_name, last_name, phone, email, password):
    try:
        # Establecer la conexión a la base de datos utilizando DB_CONFIG
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Llamar a un procedimiento almacenado para insertar los datos del cliente
        cursor.callproc(
            'new_account', [first_name, last_name, phone, email, password])

        conn.commit()
        cursor.close()
        conn.close()

        print("Nuevo usuario creado exitosamente.")

    except Exception as e:
        # Imprimir el error en la consola
        print(f"Error en new_accountt: {str(e)}")

#Funcion Login - Inicio de Sesion
@app.route('/loginUser', methods=['POST'])
def loginUser():
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.form.get('user_name')
        password = request.form.get('user_password')

        print("Intento de inicio de sesión con correo electrónico:", email)  # Mensaje de depuración

        # Validar el acceso del usuario
        user_info = validar_acceso(email, password)
        print("Resultado de la validación de acceso:", user_info)  # Mensaje de depuración

        if user_info is not None:
            user_id, first_name, last_name, phone, email, password= user_info

            session['user_id'] = user_id
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['phone'] = phone
            session['email'] = email
            session['password'] = password

            return redirect(url_for('menu'))

        else:
            flash(
                'Usuario o contraseña incorrectos. Por favor, intenta nuevamente.', 'error')
            return redirect(url_for('login'))

#Funcion Validar Acceso
def validar_acceso(email, password):
    try:
        # Configura la conexión a la base de datos
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT user_id, first_name, last_name, phone, email, password FROM user WHERE email = %s and password = %s"
        print("Ejecutando consulta SQL:", query)  # Mensaje de depuración
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        print("Resultado de la consulta:", result)  # Mensaje de depuración
        if result:
            return result[0], result[1], result[2], result[3], result[4], result[5]
        return None
    except mysql.connector.Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


@app.route('/prediction_coffe', methods=['GET', 'POST'])
def prediction_coffe():
    result = None
    
    if request.method == 'POST':
        # Verificar si se cargó una imagen
        if 'file' not in request.files:
            return render_template('free/ia_coffe.html', result='No se cargó una imagen.')

        uploaded_image = request.files['file']

        # Verificar si se seleccionó un archivo
        if uploaded_image.filename == '':
            return render_template('free/ia_coffe.html', result='No se seleccionó un archivo.')

        # Verificar si la extensión del archivo es válida (puedes ajustar las extensiones según tus necesidades)
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        if '.' not in uploaded_image.filename or uploaded_image.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return render_template('free/ia_coffe.html', result='Formato de archivo no válido. Use imágenes JPG o PNG.')

        # Leer la imagen cargada
        image = Image.open(uploaded_image)

        # Realizar la predicción
        predicted_disease = predict_coffe(image)

        # Preparar el resultado para mostrar en la página
        result = f"{predicted_disease}"

    return render_template('free/ia_coffe.html', result=result)


@app.route('/prediction_tomato', methods=['GET', 'POST'])
def prediction_tomato():
    result = None
    
    if request.method == 'POST':
        # Verificar si se cargó una imagen
        if 'file' not in request.files:
            return render_template('free/ia_tomato.html', result='No se cargó una imagen.')

        uploaded_image = request.files['file']

        # Verificar si se seleccionó un archivo
        if uploaded_image.filename == '':
            return render_template('free/ia_tomato.html', result='No se seleccionó un archivo.')

        # Verificar si la extensión del archivo es válida (puedes ajustar las extensiones según tus necesidades)
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        if '.' not in uploaded_image.filename or uploaded_image.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return render_template('free/ia_tomato.html', result='Formato de archivo no válido. Use imágenes JPG o PNG.')

        # Leer la imagen cargada
        image = Image.open(uploaded_image)

        # Realizar la predicción
        predicted_disease = predict_tomato(image)

        # Preparar el resultado para mostrar en la página
        result = f"{predicted_disease}"

    return render_template('free/ia_tomato.html', result=result)

@app.route('/prediction_corn', methods=['GET', 'POST'])
def prediction_corn():
    result = None
    
    if request.method == 'POST':
        # Verificar si se cargó una imagen
        if 'file' not in request.files:
            return render_template('free/ia_corn.html', result='No se cargó una imagen.')

        uploaded_image = request.files['file']

        # Verificar si se seleccionó un archivo
        if uploaded_image.filename == '':
            return render_template('free/ia_corn.html', result='No se seleccionó un archivo.')

        # Verificar si la extensión del archivo es válida (puedes ajustar las extensiones según tus necesidades)
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        if '.' not in uploaded_image.filename or uploaded_image.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return render_template('free/ia_corn.html', result='Formato de archivo no válido. Use imágenes JPG o PNG.')

        # Leer la imagen cargada
        image = Image.open(uploaded_image)

        # Realizar la predicción
        predicted_disease = predict_corn(image)

        # Preparar el resultado para mostrar en la página
        result = f"{predicted_disease}"

    return render_template('free/ia_corn.html', result=result)


@app.route('/prediction_rice', methods=['GET', 'POST'])
def prediction_rice():
    result = None
    
    if request.method == 'POST':
        # Verificar si se cargó una imagen
        if 'file' not in request.files:
            return render_template('free/ia_rice.html', result='No se cargó una imagen.')

        uploaded_image = request.files['file']

        # Verificar si se seleccionó un archivo
        if uploaded_image.filename == '':
            return render_template('free/ia_rice.html', result='No se seleccionó un archivo.')

        # Verificar si la extensión del archivo es válida (puedes ajustar las extensiones según tus necesidades)
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        if '.' not in uploaded_image.filename or uploaded_image.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return render_template('free/ia_rice.html', result='Formato de archivo no válido. Use imágenes JPG o PNG.')

        # Leer la imagen cargada
        image = Image.open(uploaded_image)

        # Realizar la predicción
        predicted_disease = predict_rice(image)

        # Preparar el resultado para mostrar en la página
        result = f"{predicted_disease}"

    return render_template('free/ia_rice.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
