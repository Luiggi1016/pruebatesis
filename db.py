from flask import jsonify
import psycopg2
import csv
import os


def getUsuarios():
    connection = psycopg2.connect(
        dbname='tesisdietas',
        user='postgres',
        password='mmundaca',
    )
    connection.autocommit = True
    cursor = connection.cursor()
    query = "select u.idusuario, u.usuario, u.contraseña,tu.nombre as tiponombre from usuario u inner join tipousuario tu on tu.idtipo=u.idtipousuario where tu.nombre !='administrador';"
    try:
        cursor.execute(query)
        users=cursor.fetchall()
        return users
    except Exception as e:
        print(e)

def getPacientes():
    connection = psycopg2.connect(
        dbname='tesisdietas',
        user='postgres',
        password='mmundaca',
    )
    connection.autocommit = True
    cursor = connection.cursor()
    query = "SELECT idpaciente, CONCAT(nombres, ' ', apellidos) AS nombre_completo, DATE_PART('year', AGE(fechanacimiento)) AS edad, correo FROM paciente;"
    try:
        cursor.execute(query)
        pacientes=cursor.fetchall()
        return pacientes
    except Exception as e:
        print(e)
def getAlimentos():
    alimentos = []
    nombres_unicos = set()
    
    with open('C:/Users/Bienvenido/Desktop/sistemaAdmin/nuevo.csv', newline='') as file:
        csv_data = csv.reader(file, delimiter=';')
        next(csv_data)
        
        for fila in csv_data:
            nombre_alimento = fila[1]
            
            if nombre_alimento not in nombres_unicos:
                fila[0] = fila[0]
                fila[1] = fila[1]
                fila[2] = fila[2]
                fila[3] = fila[3]
                fila[4] = fila[4]
                fila[5] = fila[5]

                alimentos.append(fila)
                nombres_unicos.add(nombre_alimento)
        
    return alimentos

def borrarUsuario(user_id):
    connection = psycopg2.connect(
        dbname='tesisdietas',
        user='postgres',
        password='mmundaca',
    )
    connection.autocommit = True
    cursor = connection.cursor()
    query = "DELETE FROM usuario WHERE idusuario = %s"
    try:
        cursor.execute(query, (user_id,))
        response = {'message': 'Usuario eliminado exitosamente'}
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {'message': 'Error al eliminar el usuario'}
        return jsonify(response), 500
    
def borrarPaciente(paciente_id):
    connection = psycopg2.connect(
        dbname='tesisdietas',
        user='postgres',
        password='mmundaca',
    )
    connection.autocommit = True
    cursor = connection.cursor()
    query = "DELETE FROM paciente WHERE idpaciente = %s"
    try:
        cursor.execute(query, (paciente_id,))
        response = {'message': 'Paciente eliminado exitosamente'}
        return jsonify(response)
    except Exception as e:
        print(e)
        response = {'message': 'Error al eliminar el paciente'}
        return jsonify(response), 500

def borrarAlimento(alimento_id):
    ruta_archivo = 'C:/Users/Bienvenido/Desktop/sistemaAdmin/nuevo.csv'
    ruta_temporal = 'C:/Users/Bienvenido/Desktop/sistemaAdmin/nuevo_temp.csv'
    try:
        with open(ruta_archivo, 'r', newline='') as file_in, \
            open(ruta_temporal, 'w', newline='') as file_out:            
            csv_reader = csv.reader(file_in, delimiter=';')
            csv_writer = csv.writer(file_out, delimiter=';')
            for fila in csv_reader:
                id_actual = fila[0]
                if id_actual == alimento_id:
                    continue 
                else:
                    csv_writer.writerow(fila)  
        os.remove(ruta_archivo)
        os.rename(ruta_temporal, ruta_archivo)
    except Exception as e:
        print(e)
        response = {'message': 'Error al eliminar el almuerzo'}
        return jsonify(response), 500
    
def agregarAlimento(nombre,carbohidratos,proteinas,lipidos,etiqueta):
    ruta_archivo = 'C:/Users/Bienvenido/Desktop/sistemaAdmin/nuevo.csv'
    try:
        ultimo_id = None

        with open(ruta_archivo, newline='') as file:
            csv_data = csv.reader(file, delimiter=';')
            for fila in csv_data:
                ultimo_id = fila[0]  # El ID se encuentra en la primera columna

        # Generar el nuevo ID consecutivo
        if ultimo_id is not None:
            nuevo_id = str(int(ultimo_id) + 1)
        else:
            nuevo_id = "1"  

        # Agregar la nueva fila al archivo CSV
        nueva_fila = [nuevo_id,nombre, carbohidratos, proteinas, lipidos, etiqueta]

        with open(ruta_archivo, 'a', newline='') as file:
            csv_writer = csv.writer(file, delimiter=';')
            csv_writer.writerow(nueva_fila)
    except Exception as e:
        print(e)
        response = {'message': 'Error al agregar el nuevo almuerzo'}
        return jsonify(response), 500
    
def editarAlimento(idalimento,nombre,carbohidratos,proteinas,lipidos,etiqueta):
    ruta_archivo = 'C:/Users/Bienvenido/Desktop/sistemaAdmin/nuevo.csv'
    try:
        filas_actualizadas = []

        with open(ruta_archivo, newline='') as file:
            csv_data = csv.reader(file, delimiter=';')
            for fila in csv_data:
                if fila[0] == idalimento:  # Verificar si el ID coincide
                    # Actualizar los datos de la fila
                    fila[1] = nombre
                    fila[2] = carbohidratos
                    fila[3] = proteinas
                    fila[4] = lipidos
                    fila[5] = etiqueta
                filas_actualizadas.append(fila)

        # Escribir las filas actualizadas en el archivo CSV
        with open(ruta_archivo, 'w', newline='') as file:
            csv_writer = csv.writer(file, delimiter=';')
            csv_writer.writerows(filas_actualizadas)
    except Exception as e:
        print(e)
        response = {'message': 'Error al agregar el nuevo almuerzo'}
        return jsonify(response), 500
#Funcionalidad
