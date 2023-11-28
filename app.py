from flask import Flask, render_template, request
import csv
import math
import time
import numpy as np

app = Flask(__name__)
app = Flask(__name__, template_folder='templates', static_folder='static')

def extraer_datos_usuarios(archivo_csv):
    datos_usuarios = {}
    with open(archivo_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = int(row['userId'])
            movie_id = row['movieId']
            rating = float(row['rating'])
            if user_id not in datos_usuarios:
                datos_usuarios[user_id] = {}
            datos_usuarios[user_id][movie_id] = rating
    return datos_usuarios

def calcular_distancia_euclidiana(datos_1, datos_2):
    claves_comunes = set(datos_1.keys()) & set(datos_2.keys())
    valores_1 = np.array([datos_1[clave] for clave in claves_comunes])
    valores_2 = np.array([datos_2[clave] for clave in claves_comunes])
    distancia = np.linalg.norm(valores_1 - valores_2)
    return distancia

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_time = time.time()  # Registro del tiempo de inicio

        user_id_buscado = int(request.form['user_id'])
        archivo_csv = 'ratings.csv'
        datos_usuarios = extraer_datos_usuarios(archivo_csv)
        datos_usuario_buscado = datos_usuarios[user_id_buscado]
        distancias_no_nulas = {}

        for user_id, datos_usuario in datos_usuarios.items():
            if user_id != user_id_buscado:
                distancia_euclidiana = calcular_distancia_euclidiana(datos_usuario_buscado, datos_usuario)
                if distancia_euclidiana != 0:
                    distancias_no_nulas[user_id] = distancia_euclidiana

        distancias_ordenadas = sorted(distancias_no_nulas.items(), key=lambda x: x[1])
        resultados = []

        for (user_id, distancia) in distancias_ordenadas[:3]:
            movie_ids_compartidos = set(datos_usuario_buscado.keys()) & set(datos_usuarios[user_id].keys())
            movie_info = []
            for movie_id in movie_ids_compartidos:
                calificacion_usuario_buscado = datos_usuario_buscado[movie_id]
                calificacion_usuario_otro = datos_usuarios[user_id][movie_id]
                movie_info.append({
                    'movie_id': movie_id,
                    'calificacion_usuario_buscado': calificacion_usuario_buscado,
                    'calificacion_usuario_otro': calificacion_usuario_otro
                })

            resultados.append({
                'user_id': user_id,
                'distancia': distancia,
                'movie_info': movie_info
            })

        end_time = time.time()  # Registro del tiempo de finalización
        elapsed_time = end_time - start_time  # Cálculo del tiempo transcurrido
        print(f'Tiempo de ejecución: {elapsed_time} segundos')

        return render_template('index.html', resultados=resultados)



    return render_template('index.html', resultados=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

