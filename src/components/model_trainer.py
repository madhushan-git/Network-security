import os
import sys

from src.exceptions.exceptions import NetworkSecurityException
from src.loggings.logger import logging

from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.utils.main_utils.utils import load_numpy_array_data,save_object, load_object, evaluate_models
from src.utils.ml_utils.metric.metric import classification_metric
from src.utils.ml_utils.model.model import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkModel(e,sys)
        
    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params = {
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }            
            }
            model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models,param=params)
            best_model_score = max(v["test_model_score"] for v in model_report.values())
            best_model_name = max(model_report, key=lambda k: model_report[k]["test_model_score"])
            best_model = models[best_model_name]

            y_train_pred = best_model.predict(X_train)
            classification_train_metric = classification_metric(y_train, y_train_pred)

            ## Track the mlflow


            y_test_pred = best_model.predict(X_test)
            classification_test_metric = classification_metric(y_test, y_test_pred)

            preprocessor = load_object(self.data_transformation_artifact.transfformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_dir)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor,best_model)

            save_object(self.model_trainer_config.trained_model_dir, obj=NetworkModel)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_modelTrainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model = self.train_model(x_train,y_train, x_test,y_test)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

