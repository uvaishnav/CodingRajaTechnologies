import os
import sys
import gdown 
import zipfile


from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.entity.config_entity import DataIngestionConfig
from wasteDetection.entity.artifacts_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            error_message = "Error occurred while initializing DataIngestion"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
    
    def download_data(self)->str:
        """
        Download data from url
        """
        
        try:
            data_url = self.data_ingestion_config.data_download_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)

            data_file_name = "data.zip"
            zip_file_path = os.path.join(zip_download_dir, data_file_name)

            logging.info(f"Downloading data from url {data_url}")

            file_id = data_url.split("/")[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix + file_id, zip_file_path, quiet=False)

            logging.info(f"Data downloaded at path {zip_file_path}")

            return zip_file_path
        except Exception as e:  
            error_message = "Error occurred while downloading data"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
    
    def extract_zip_file(self, zip_file_path:str)->str:
        """
        Extract zip file
        :param zip_file_path: zip file path
        """
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_dir, exist_ok=True)

            logging.info(f"Extracting zip file from path {zip_file_path}")
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_dir)
            logging.info(f"Zip file extracted at path {feature_store_dir}")
            return feature_store_dir
        except Exception as e:
            error_message = "Error occurred while extracting zip file"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
        
    def ingest_data_ingestion(self)->DataIngestionArtifact:
        """
        Ingest data Ingestion
        """
        try:
            zip_file_path = self.download_data()
            feature_store_dir = self.extract_zip_file(zip_file_path)
            return DataIngestionArtifact(zip_file_path, feature_store_dir)
        except Exception as e:
            error_message = "Error occurred while ingesting data"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())



