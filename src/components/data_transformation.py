from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from src.exceptions.exceptions import NetworkSecurityException
from src.loggings.logger import logging
from src.utils.main_utils.utils import save_numpy_array_data,save_object, read_data
from src.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
import pandas as pd
import os,sys
import numpy as np

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransformationn:
    def __init__(self, data_validation_artifact:DataValidationArtifact, 
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info("Entered get_data_trnasformer_object method of Trnasformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline = Pipeline(steps=[("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered data_transformation_method in DataTransformation")
        try:
            train_file_path = self.data_validation_artifact.valid_train_file_path
            test_file_path = self.data_validation_artifact.valid_test_file_path
            logging.info("Starting data transformation")
            train_df = read_data(train_file_path)
            test_df = read_data(test_file_path)
            
            ## training dataframe
            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            ## training dataframe
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_features_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_features_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_features_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)

            # Preparing artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transfformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
