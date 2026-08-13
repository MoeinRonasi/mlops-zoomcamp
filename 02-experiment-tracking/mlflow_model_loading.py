# Load the MLflow model from experiment tracking and use it for inference on new data.
import mlflow
import pickle

# Point MLflow at the same SQLite backend the models were logged to.
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Load the best model and use it for inference
best_model_id = "m-640fa8799d2e43069e45ddcbd1d06152"

# MLflow 3 logged-model URI is just models:/<model_id> (NO /version suffix).
# The /version form (models:/<name>/<version>) is only for REGISTERED models.
best_model_uri = f"models:/{best_model_id}"
best_model = mlflow.sklearn.load_model(best_model_uri)

# Use the best model for inference on new data
new_data = [
    {"PULocationID": "130", "DOLocationID": "205", "trip_distance": 5.0},
    {"PULocationID": "205", "DOLocationID": "130", "trip_distance": 3.0},
]

# Load the preprocessor
with open("models/preprocessor.b", "rb") as f:
    dv = pickle.load(f)
new_data_transformed = dv.transform(new_data)

# Make predictions
predictions = best_model.predict(new_data_transformed)
print(predictions)