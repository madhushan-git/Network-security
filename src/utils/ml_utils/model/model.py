from src.constants.training_pipeline import SAVED_MODEL_NAME,MODEL_FILE_NAME

import os
import sys
from src.exceptions.exceptions import NetworkSecurityException
from src.loggings.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_predict = self.model.predict(x_transform)
            return y_predict
        except Exception as e:
             NetworkSecurityException(e,sys)