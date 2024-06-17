# Creamos un archivo de python
FROM python:3.10-slim

# La dirección 
WORKDIR /app

# Install python requirements
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# Copy App
COPY /app .

# Expose streamlit port, streamlit es una librería para hacer dashboard. Vamos a poder acceder al front con este puerto.
EXPOSE 8501

# Run the command on container startup. Le tenes que dar todas las instrucciones a streamlit, se ejecut y se abre app.py. 
ENTRYPOINT ["streamlit", "run", "./app.py"]
