from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

# Load the trained model
model = joblib.load("churn_model.joblib")

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input data model with 20 fields
class InputData(BaseModel):
    account_length: int
    number_vmail_messages: int
    total_day_minutes: float
    total_day_calls: int
    total_eve_minutes: float
    total_eve_calls: int
    total_night_minutes: float
    total_night_calls: int
    total_intl_minutes: float
    total_intl_calls: int
    customer_service_calls: int
    international_plan: int
    voice_mail_plan: int
    state_0: int
    state_1: int
    state_2: int
    state_3: int
    state_4: int
    state_5: int
    state_6: int

@app.post("/predict")
def predict(data: InputData):
    # Create a feature list in the order used during training:
    features = [
        data.account_length,
        data.number_vmail_messages,
        data.total_day_minutes,
        data.total_day_calls,
        data.total_eve_minutes,
        data.total_eve_calls,
        data.total_night_minutes,
        data.total_night_calls,
        data.total_intl_minutes,
        data.total_intl_calls,
        data.customer_service_calls,
        data.international_plan,
        data.voice_mail_plan,
        data.state_0,
        data.state_1,
        data.state_2,
        data.state_3,
        data.state_4,
        data.state_5,
        data.state_6,
    ]
    X = np.array(features).reshape(1, -1)
    prediction = model.predict(X)[0]
    result = "Customer Will Churn" if prediction == 1 else "Customer Will Not Churn"
    return {"prediction": result}
