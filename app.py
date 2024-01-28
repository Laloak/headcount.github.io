from flask import Flask, render_template, request, redirect, flash
import csv

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto con una clave secreta segura

# Ruta principal
@app.route('/')
def index():
    return render_template('home.html')

# Función para verificar si un nombre ya existe en el CSV
def nombre_existe(nombre, csv_file):
    with open(csv_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Saltar la primera fila (encabezados)
        for row in csvreader:
            if row[1] == nombre:
                return True
    return False

# Ruta para manejar el formulario y guardar en CSV
@app.route('/guardar', methods=['POST'])
def guardar():
    opciones = []
    nombres = []

    # Validar que todas las casillas no estén en blanco y el nombre no exista
    for i in range(1, 11):
        opcion = request.form.get(f'opcion_{i}')
        nombre = request.form.get(f'nombre_{i}')

        # Verificar si alguna casilla está en blanco
        if not opcion or not nombre:
            flash("Error: Todas las casillas deben ser completadas.", 'error')
            return redirect('/')

        # Verificar si el nombre ya existe en el archivo CSV
        if nombre_existe(nombre, 'datos.csv'):
            flash(f"Error: El nombre '{nombre}' ya existe en el archivo.", 'error')
            return redirect('/')

        opciones.append(opcion)
        nombres.append(nombre)

    # Guardar en archivo CSV (modo append 'a')
    with open('datos.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Si el archivo está vacío, escribir encabezados
            csvwriter.writerow(['Opción', 'Nombre'])
        for i in range(10):
            csvwriter.writerow([opciones[i], nombres[i]])

    flash("Datos guardados con éxito.", 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)



