from src.components.data_ingestion import DataIngestion
from src.exceptions.exceptions import NetworkSecurityException
from src.loggings.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=="__main__":
    try:
        data_ingestion = DataIngestion(DataIngestionConfig(TrainingPipelineConfig()))
        logging.info ("Initiate the data Ingestion")
        dataingestionartifact = data_ingestion.initiate_date_ingestion()
        print(dataingestionartifact)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)