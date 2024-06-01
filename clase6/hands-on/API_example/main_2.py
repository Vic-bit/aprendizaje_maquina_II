import random
import fastapi
from pydantic import BaseModel #Hace un control de tipo de datos, cosa que no pasaba con el Main 1

app = fastapi.FastAPI()


class InputFeatures(BaseModel):
    size: float
    height: float
    weight: float
    number_of_whiskers: int


class OutputPrediction(BaseModel):
    prediction: str


class MLModel: # Vamos a crear la clase del modelo
    @staticmethod
    def predict(size, height, weight, number_of_whiskers):
        value = random.randint(0, 1)
        output = "Dog"
        if value == 0:
            output = "Cat"
        # Placeholder prediction logic
        return OutputPrediction(prediction=output)


# Create an instance of the placeholder model
ml_model = MLModel()

# Endpoint to make predictions
@app.post("/predict/") #Igual que antes
async def predict(features: InputFeatures) -> OutputPrediction: #La salida es lo que no da la calse salida
    prediction = ml_model.predict(features.size, features.height, features.weight, features.number_of_whiskers)
    return prediction
