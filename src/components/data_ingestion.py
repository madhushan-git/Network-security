import pymongo.mongo_client
from src.exceptions.exceptions import NetworkSecurityException
from src.loggings.logger import logging

## Configuration of the data ingestion config

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
            logging.info("initiated data ingestion attributes")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            logging.info("logged to the export_collection_as_dataframe")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            logging.info("Mongo client is initiated")
            collection = self.mongo_client[database_name][collection_name]
            logging.info("collection is initiated")
            df = pd.DataFrame(list(collection.find()))
            logging.info("Dataframe is initiated")
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)

            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            logging.info("logged to the export_data_into_feature_store")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_date_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            logging.info("export_collection_as_dataframe done")
            dataframe=self.export_data_into_feature_store(dataframe)
            logging.info("export_data_into_feature_store done")
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)