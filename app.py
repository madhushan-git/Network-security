from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.exceptions.exceptions import NetworkSecurityException
from src.loggings.logger import logging
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=="__main__":
    try:
        data_ingestion = DataIngestion(DataIngestionConfig(TrainingPipelineConfig()))
        logging.info ("Initiate the data Ingestion")
        dataingestionartifact = data_ingestion.initiate_date_ingestion()
        print(dataingestionartifact)
        logging.info("Data ingestion initiated")
        data_validation = DataValidation(data_ingestion_artifact=dataingestionartifact, data_validation_config=DataValidationConfig(training_pipeline_config=TrainingPipelineConfig()))
        logging.info("Data validation initiate")
        datavalidationartifact = data_validation.initiate_data_validation()
        print(datavalidationartifact)
        logging.info("Data validation initiated")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)