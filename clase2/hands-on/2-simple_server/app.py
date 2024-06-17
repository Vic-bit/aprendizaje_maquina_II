from flask import Flask
import os

# Se crea el objeto app para la API.
app = Flask(__name__)

# Se crea una app.
@app.route("/") #La ruta es cero
def hello():
    return "Hola mundo!!!"

# Va a estar corriendo en el localhost.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # Generamos una variable ambiente que se llama PORT 8000.
    app.run(debug=True, host='0.0.0.0', port=port) #Ejecuta la app y la puedo ver en el buscador. Le estoy haciendo 
                                                   #una consulta a la API que está en el contenedor de mi máquina. 