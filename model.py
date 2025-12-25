import joblib
import pandas as pd

# IMPORTANT: make sure custom transformer is imported
from transformers import DateFeatureExtractor

# Load pipeline ONCE
pipeline = joblib.load("rossmann_pipeline.pkl")


def predict_sales(input_dict: dict) -> int:
    """
    Takes raw input as dictionary
    Returns predicted sales as int
    """

    df = pd.DataFrame([input_dict])
    prediction = pipeline.predict(df)[0]
    return int(prediction)
