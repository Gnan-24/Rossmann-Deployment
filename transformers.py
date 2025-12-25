import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["Date"] = pd.to_datetime(X["Date"])
        X["Day"] = X["Date"].dt.day
        X["Month"] = X["Date"].dt.month
        X["Year"] = X["Date"].dt.year
        X["WeekOfYear"] = X["Date"].dt.isocalendar().week.astype(int)
        return X.drop(columns=["Date"])
