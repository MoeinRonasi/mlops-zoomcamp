# In this file we train 5 different ML models and log their parameters, metrics, and artifacts using MLflow Autolog.
# The dataset we use is the nyc taxi fare dataset, which contains information about taxi trips in New York City, including the pickup and dropoff locations, the fare amount, and other relevant features.
# We use the data for january 2021 as training data and the data for february 2021 as test data. We train the following models:

# 1. Random Forest Regressor
# 2. Gradient Boosting Regressor
# 3. Extra Trees Regressor
# 4. LinearSVC

#Import the necessary libraries
import mlflow
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
import xgboost as xgb
from sklearn.svm import LinearSVR
import pickle
from sklearn.metrics import root_mean_squared_error

# Preprocess the data
# Define a function to read the parquet files and preprocess the data
def read_dataframe(filename):
    df = pd.read_parquet(filename)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    return df
# Load the training and test data
train_data_path = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet'
val_data_path = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-02.parquet'
df_train = read_dataframe(train_data_path)
df_val = read_dataframe(val_data_path)

# Prepare the data for training and validation.
# NOTE (Option A - memory fix): We deliberately do NOT build the combined
# 'PU_DO' feature here. Combining pickup+dropoff created ~13,200 one-hot columns,
# which densified to ~7.8 GB and got the process OOM-killed on this 5 GB Codespace.
# Using the two location IDs SEPARATELY keeps cardinality to a few hundred columns.
categorical = ['PULocationID', 'DOLocationID']
numerical = ['trip_distance']

# Create the DictVectorizer and transform the training and validation data
dv = DictVectorizer()
train_dicts = df_train[categorical + numerical].to_dict(orient='records')
X_train = dv.fit_transform(train_dicts)
val_dicts = df_val[categorical + numerical].to_dict(orient='records')
X_val = dv.transform(val_dicts)
target = 'duration'
y_train = df_train[target].values
y_val = df_val[target].values

# Save the preprocessor to use it later in the inference pipeline
with open("models/preprocessor.b", "wb") as f:
    pickle.dump(dv, f)

# Enable autologging
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nyc-taxi-experiment")
mlflow.autolog()
# Train and evaluate the models

# Resource-friendly settings: this Codespace has only ~5GB free RAM and 2 cores.
# The PU_DO one-hot feature matrix is very wide, and default tree ensembles
# (many deep trees, parallel jobs that copy the matrix) exhaust memory and the
# OS kills the process (exit 143 / SIGTERM). We constrain each model to fit.
model_params = {
    RandomForestRegressor: {"n_estimators": 30, "max_depth": 15, "n_jobs": 1, "random_state": 42},
    GradientBoostingRegressor: {"n_estimators": 30, "max_depth": 5, "random_state": 42},
    ExtraTreesRegressor: {"n_estimators": 30, "max_depth": 15, "n_jobs": 1, "random_state": 42},
    LinearSVR: {"max_iter": 1000, "random_state": 42},
    xgb.XGBRegressor: {"n_estimators": 30, "max_depth": 5, "random_state": 42, "n_jobs": 1},
}

for model_class in (GradientBoostingRegressor, xgb.XGBRegressor,ExtraTreesRegressor, RandomForestRegressor, LinearSVR):

    with mlflow.start_run():

        mlflow.log_param("train-data-path", "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet")
        mlflow.log_param("valid-data-path", "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-02.parquet")
        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")

        mlmodel = model_class(**model_params[model_class])
        mlmodel.fit(X_train, y_train)

        y_pred = mlmodel.predict(X_val)
        rmse = root_mean_squared_error(y_val, y_pred)
        mlflow.log_metric("rmse", rmse)
        


