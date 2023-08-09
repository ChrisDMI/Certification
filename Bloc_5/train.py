import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import  GridSearchCV

import mlflow
import time
import joblib


print('Start running train.py')

# Set your variables for your environment
EXPERIMENT_NAME="GetAround"

# Set tracking URI to your Heroku application
mlflow.set_tracking_uri(os.environ["APP_URI"])

# Set experiment's info 
mlflow.set_experiment(EXPERIMENT_NAME)


# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Call mlflow autolog
mlflow.sklearn.autolog()

# Time execution
start_time = time.time()


# Log metric with MLflow
with mlflow.start_run(experiment_id = experiment.experiment_id):
    


    data_ml = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")
    data_ml.drop('Unnamed: 0', axis=1, inplace=True)

    target = 'rental_price_per_day'

    print("Separating labels from features...")
    Y = data_ml[target]
    X = data_ml.drop(target, axis=1)
    print("...Done!")




    print('Dividing into train and test sets...')
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    print('... Done!')


    print('Detecting numerical and categorical features...')
    numerical_features = []
    categorical_features = []
    for i,t in X.dtypes.items():
        if ('float' in str(t)) or ('int' in str(t)) :
            numerical_features.append(i)
        else :
            categorical_features.append(i)

    print('Found numerical features ', numerical_features)
    print('Found categorical features ', categorical_features)

    print('... Done!')





    print('Transforming numerical and categorical features...')
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(drop='first')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)
    print('... Done!')





    # Define the GradientBoostingRegressor model
    model = GradientBoostingRegressor()


    # Define the parameter grid
    params = {
        'n_estimators': [50, 100, 150, 200],        # Number of boosting stages to perform
        'learning_rate': [0.1, 0.01],     # Learning rate
        'max_depth': [None, 3, 5],                  # Maximum depth of individual regression estimators
        'min_samples_split': [2, 3, 5],         # Minimum number of samples required to split an internal node
        'min_samples_leaf': [2, 4, 6],           # Minimum number of samples required to be at a leaf node
    }
    # Perform grid search using 5-fold cross-validation
    gridsearch = GridSearchCV(estimator=model, param_grid=params, n_jobs=-1, cv=5, scoring='r2')

    # Fit the grid search to the data
    gridsearch.fit(X_train, Y_train)

    # Print the best parameters and best score and std
    print("Best mean test score: %f , and best std test score: %f best using %s" % (gridsearch.best_score_, gridsearch.cv_results_['std_test_score'][gridsearch.best_index_], gridsearch.best_params_))



    n_estimators = gridsearch.best_params_['n_estimators']
    learning_rate = gridsearch.best_params_['learning_rate']
    max_depth = gridsearch.best_params_['max_depth']
    min_samples_leaf = gridsearch.best_params_['min_samples_leaf']
    min_samples_split = gridsearch.best_params_['min_samples_split']

    print("Best params : ", gridsearch.best_params_)

    # Train the model with the best parameters
    print("Train model...")
    GB_Regressor = GradientBoostingRegressor(n_estimators= n_estimators, 
                                            learning_rate= learning_rate, 
                                            max_depth= max_depth, 
                                            min_samples_leaf= min_samples_leaf, 
                                            min_samples_split= min_samples_split)
    GB_Regressor.fit(X_train, Y_train)
    print("...Done.")


    # Save the model as a file
    model_file = "./model.pkl"
    joblib.dump(GB_Regressor, model_file)

    preprocessor_file = "./preprocessor.pkl"
    joblib.dump(preprocessor, preprocessor_file)

    # Log parameters and best score
    mlflow.log_metric('best_score', gridsearch.best_score_)
    mlflow.log_params(gridsearch.best_params_)

    # Log the model file and preprocessor as an artifact
    mlflow.log_artifact(model_file)
    mlflow.log_artifact(preprocessor_file)


    print('End running train.py')
    print(f"---Total training time: {time.time()-start_time}")
