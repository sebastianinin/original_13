FROM python:3.7.4

WORKDIR /app

# Instala las dependencias necesarias, incluyendo gdown
RUN pip install --no-cache-dir gdown

# Descarga y descomprime el archivo
RUN gdown --id 1_sRMeV_jdECnAb51e6fUke79F3x0JzcJ --output ratings.zip \
    && unzip ratings.zip \
    && rm ratings.zip  # Opcional: Elimina el archivo ZIP si ya no lo necesitas

# Copia el resto de los archivos de la aplicación
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para ejecutar tu aplicación
CMD ["python", "app.py"]
