import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import  Union
import boto3
import joblib
from io import BytesIO
import ast





description = """
# Welcome to GetAround API

The GetAround API allows you to predict the price of a car based on its make, model, year, mileage, and fuel type.

## Usage

### Predict Price

Endpoint: `/predict_price`

- Method: POST
- Description: Predicts the price of a car based on its details.
- Request Body:
    - `make`: Make of the car (string).
    - `model`: Model of the car (string).
    - `mileage`: Mileage of the car (integer).
    - `fuel`: Fuel type of the car (string).
- Response:
    - `prediction`: Predicted price of the car.

## Example

```python
import requests

url = "http://localhost:8000/predict_price"

payload = {
    "make": "Toyota",
    "model": "Camry",
    "mileage": 50000,
    "fuel_type": "Gasoline"
    ...
}

response = requests.post(url, json=payload)
data = response.json()

"""





tags_metadata = [
    
    {
        "name": "Main Endpoint",
        "description": "Complex endpoint that deals with actual data with  **POST** request."
    }

   
]



app = FastAPI(
    title="GetAround API",
    description=description,
    version="0.1",
    contact={
        "name": "ZGetAround API",
        "url": "https://jedha.co",
    },
    openapi_tags=tags_metadata
)






















# Replace with your S3 bucket name
S3_BUCKET_NAME = "netflix-project-bucket"


with open(".env") as my_file:
    file = my_file.read()

AWS_ACCESS_KEY_ID = ast.literal_eval(file)['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = ast.literal_eval(file)['AWS_SECRET_ACCESS_KEY']

# Replace with your AWS access key ID and secret access key
s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name = 'eu-west-3')

region = s3.meta.region_name


model_S3_url = "https://netflix-project-bucket.s3.eu-west-3.amazonaws.com/mlflow/5/5660a104ad3041bcbaa14700607426ed/artifacts/model.pkl"
preprocessor_S3_url = "https://netflix-project-bucket.s3.eu-west-3.amazonaws.com/mlflow/5/a270d8a2f29a4e20bcfff2cd7a0233a8/artifacts/preprocessor.pkl"

# Take only the name of the image
model_s3_key = model_S3_url.split('.com/')[1]
preprocessor_s3_key = preprocessor_S3_url.split('.com/')[1]

 # Load the model directly from S3 to BytesIO object
model_bytes = BytesIO()
preprocessor_bytes = BytesIO()

s3.download_fileobj(S3_BUCKET_NAME, model_s3_key, model_bytes)
s3.download_fileobj(S3_BUCKET_NAME, preprocessor_s3_key, preprocessor_bytes)

# Reset the file object position to the beginning
model_bytes.seek(0)
preprocessor_bytes.seek(0)

# Load the model from the BytesIO object
model = joblib.load(model_bytes)
preprocessor = joblib.load(preprocessor_bytes)

# Defining required input for the prediction endpoint
class Features(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool



@app.get("/")
async def index():

    message = "Hello world! This `/` is the most simple and default endpoint. If you want to learn more, check out documentation of the api at `/docs`"

    return message


@app.post("/predict_price", tags=["Machine Learning"])
async def get_predict(features:Features):
    """
        This Endpoint make price's car prediction based on its 
        the following input:

        {
        "model_key": "Toyota",
        "mileage": 71000,
        "engine_power": 240,
        "fuel": "petrol",
        "paint_color": "blue",
        "car_type": "sedan",
        "private_parking_available": true,
        "has_gps": False,
        "has_air_conditioning": true,
        "automatic_car": true,
        "has_getaround_connect": true,
        "has_speed_regulator": true,
        "winter_tires": true
        }

        Returns:
        - price: Predicted price of the car.

        You need to respect this format in order to not get error.
    """
    features = dict(features)
    input_df = pd.DataFrame(columns=['model_key', 'mileage', 'engine_power', 'fuel', 'paint_color','car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect','has_speed_regulator', 'winter_tires'])
    input_df.loc[0] = list(features.values())

    X = preprocessor.transform(input_df)
    pred = model.predict(X)

    return {"prediction" : pred[0]}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)