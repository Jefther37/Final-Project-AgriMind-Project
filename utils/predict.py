import joblib
import os

# Load the trained model from the 'model' directory
model_path = os.path.join(os.path.dirname(__file__), "../model/sentiment_model.pkl")
model = joblib.load(model_path)

def predict_mood(text):
    return model.predict([text])[0]
