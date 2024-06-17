# Partimos de una imagen base de Python https://hub.docker.com/_/python , de la misma
FROM python:3.10-slim
LABEL authors="facundolucianna"

# Agregamos requirement.txt (de lugar físico donde lo tenemos a la imagen)al contenedor e instalamos los requerimientos. 
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copiamos lo que esta en esta carpeta a app del contenedor. Creamos una carpeta. Esta carpeta no está en la imagen.
COPY . /app 
# Establecemos como la carpeta de trabajo a app. Nos paramos en esa carpeta com carpeta de trabajo.
WORKDIR /app

# Definimos un punto de entrada a la imagen. Vamos a ejecutar python. Tenemos un punto de entrada ahora y luego el comando para ejecutar.
ENTRYPOINT ["python"]
CMD ["app.py"]