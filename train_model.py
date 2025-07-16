import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Sample training data
data = {
    'text': [
        "I feel hopeless and overwhelmed",
        "I'm okay",
        "Farming is stressful again",
        "I’m happy and excited about the harvest"
    ],
    'label': ['negative', 'neutral', 'negative', 'positive']
}

df = pd.DataFrame(data)

# Build ML pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# Train the model
pipeline.fit(df['text'], df['label'])

# Get absolute path to current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure 'model' directory exists
model_dir = os.path.join(BASE_DIR, "model")
os.makedirs(model_dir, exist_ok=True)

# Save model to the correct location
model_path = os.path.join(model_dir, "sentiment_model.pkl")
joblib.dump(pipeline, model_path)

print(f"✅ Model successfully saved at: {model_path}")
