import random
import fastapi

app = fastapi.FastAPI()


class MLModel: 
    @staticmethod #Decorador de que se debe ejecutar cuando se ejecute la API.
    def predict(size, height, weight, number_of_whiskers):
        value = random.randint(0, 1) #Generamos un entero entre 0 y 1
        output = "Dog"
        if value == 0: # Si es cero lo ponemos en gato
            output = "Cat"
        # Placeholder prediction logic
        return {"prediction": output}


# Create an instance of the placeholder model
ml_model = MLModel()

# Endpoint to make predictions
@app.post("/predict/") #Nombre del endpoint
async def predict(size: float, height: float, weight: float, number_of_whiskers: int): #tipos de datos que deben entrar
    prediction = ml_model.predict(size, height, weight, number_of_whiskers) #dentro de la instancia del modelo usamos el método predict
    return prediction #nos da una diccionario
