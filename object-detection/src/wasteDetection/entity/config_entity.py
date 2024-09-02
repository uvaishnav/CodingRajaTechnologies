import os
from dataclasses import dataclass
from datetime import datetime

from wasteDetection.constants.training_pipeline import *

@dataclass
class TrainingPipelineConfig:
    artifacts_dir: str = ARTIFACTS_DIR

training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig() 

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR
    )

    data_download_url: str = DATA_DOWNLOAD_URL


@dataclass
class ModelTrainerConfig:
    model_training_dir = os.path.join(
        training_pipeline_config.artifacts_dir, MODEL_TRAINER_DIR_NAME
    )

    weight_name = MODEL_TRAINER_PRETRAINED_WEIGHT_NAME
    num_epochs = MODEL_TRAINER_NO_EPOCHS
    batch_size = MODEL_TRAINER_BATCH_SIZE

    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
    )
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR
    ) 
    model_data_path = os.path.join(feature_store_file_path, MODEL_YAML_PATH)