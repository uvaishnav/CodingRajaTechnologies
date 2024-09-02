import sys
import os

from wasteDetection.logger import logging
from wasteDetection.exception import AppException

from wasteDetection.components.data_ingestion import DataIngestion
from wasteDetection.entity.config_entity import DataIngestionConfig
from wasteDetection.entity.artifacts_entity import DataIngestionArtifact

class TrainingPipeline:
    def __init__(self):
        try:
            self.data_ingestion = DataIngestion()
        except Exception as e:
            error_message = "Error occurred while initializing TrainingPipeline"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        """
        Start data ingestion process
        """
        try:
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(
                data_ingestion_config=DataIngestionConfig()
            )
            data_ingestioin_artifacts = data_ingestion.ingest_data_ingestion()
            logging.info("Data ingestion completed")

            return data_ingestioin_artifacts
        except Exception as e:
            error_message = "Error occurred while starting data ingestion"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
        

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            logging.info("Data Ingestion completed")    
        except Exception as e:
            error_message = "Error occurred while running pipeline"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
        