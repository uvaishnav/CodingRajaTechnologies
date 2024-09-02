import sys
import os

from wasteDetection.logger import logging
from wasteDetection.exception import AppException

from wasteDetection.components.data_ingestion import DataIngestion
from wasteDetection.components.model_trainer import ModelTrainer

from wasteDetection.entity.config_entity import (
    DataIngestionConfig,
    ModelTrainerConfig
)
from wasteDetection.entity.artifacts_entity import (
    DataIngestionArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        try:
            self.data_ingestion = DataIngestion()
            self.model_trainer_config = ModelTrainerConfig()
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
        
    def start_model_training(self)->ModelTrainerArtifact:
        """
        Start model training process
        """
        try:
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifacts = model_trainer.initiate_model_trainer()

            return model_trainer_artifacts
        except Exception as e:
            error_message = "Error occurred while starting model training"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())      
        
        

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            logging.info("Data Ingestion completed") 
            model_trainer_artifacts = self.start_model_training()
            logging.info("Model Training completed")    
        except Exception as e:
            error_message = "Error occurred while running pipeline"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
        