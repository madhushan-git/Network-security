from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.exceptions.exceptions import NetworkSecurityException
from src.loggings.logger import logging
from src.constants.training_pipeline import SCHEMA_FILE_PATH
from src.utils.main_utils.utils import read_yaml_file, write_yaml_file, read_data
from scipy.stats import ks_2samp
import pandas as pd
import os,sys

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    def validate_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_column = len(self._schema_config["columns"])
            logging.info(f"Required number of column:{number_of_column}")
            logging.info(f"Data frame has column:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_column:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_numerical_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            df_col_normalized = {col.strip().lower() for col in dataframe.columns}
            yaml_col_normalized = {col.strip().lower() for col in self._schema_config["numerical_columns"]}
            if df_col_normalized == yaml_col_normalized:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold = 0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_distribution_same_or_not = ks_2samp(d1,d2)
                if threshold <= is_sample_distribution_same_or_not.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "P_value":float(is_sample_distribution_same_or_not.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## Read the data from train and test
            train_dataframe = read_data(train_file_path)
            test_dataframe = read_data(test_file_path)

            # Validate nu of columns
            status = self.validate_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataset does not contain all columns. \n"
            status = self.validate_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataset does not contain all columns. \n"

            # Validate numerical columns
            status = self.validate_numerical_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataset does not have the same numerical columns. \n"
            status = self.validate_numerical_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataset does not have the same numerical columns. \n"

            # lets check data drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
