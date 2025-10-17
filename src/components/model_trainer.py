import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import (AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor)
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from src.utils import evaluate_models
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info("Data Split")
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
                
            )
            models = {
                "DecisionTree":DecisionTreeRegressor(),
                "LinearRegressor": LinearRegression(),
                "KNeirestREgressor":KNeighborsRegressor(),
                "CatBoostRegressor":CatBoostRegressor(verbose=False),
                "AdaboostRegressor":AdaBoostRegressor(), 
                "GradientBoostRegressor": GradientBoostingRegressor(),
                "RandomForestRegressor":RandomForestRegressor(),
                "XGBRegressor":XGBRegressor()
            }
            model_report: dict= evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test, y_test=y_test, models=models)
            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException("No best model Found")
            logging.info("Done with the model things")
            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                        obj = best_model)
            predicted = best_model.predict(X_test)
            r2_sqaure = r2_score(y_test, predicted)
            return r2_sqaure
        except Exception as e:
            raise CustomException(e,sys)