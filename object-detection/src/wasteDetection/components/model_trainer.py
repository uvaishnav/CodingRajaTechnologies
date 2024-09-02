import os
import sys
import yaml

from wasteDetection.utils.common import read_yaml

from wasteDetection.logger import logging
from wasteDetection.exception import AppException

from wasteDetection.entity.config_entity import ModelTrainerConfig
from wasteDetection.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(self, model_trainer_config = ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self):
        try:
            logging.info("Initiating model training")
            with open(self.model_trainer_config.model_data_path, 'r') as file:
                num_classes = str(yaml.safe_load(file)['nc'])
            
            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            logging.info(f"Using {model_config_file_name} for detecting waste")

            config = read_yaml(f"yolov5/models/{model_config_file_name}.yaml")

            config['nc'] = int(num_classes)

            with open(f"yolov5/models/{model_config_file_name}.yaml", 'w') as file:
                yaml.dump(config, file)
            
            # Training Command
            logging.info("Started Model training")
            os.system(f"cd yolov5/ && python train.py --img 416 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.num_epochs} --data ../{self.model_trainer_config.model_data_path} --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results  --cache")
            logging.info("Model training completed")

            os.system("cp yolov5/runs/train/yolov5s_results/weights/best.pt yolov5/")
            
            os.makedirs(self.model_trainer_config.model_training_dir, exist_ok=True)

            os.system(f"cp yolov5/runs/train/yolov5s_results/weights/best.pt {self.model_trainer_config.model_training_dir}/")

            logging.info("Model training artifacts saved")

            model_trainer_artifacts = ModelTrainerArtifact(
                trained_model_path=self.model_trainer_config.model_training_dir
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifacts}")

            return model_trainer_artifacts
        except Exception as e:
            error_message = "Error occurred while training model"
            logging.error(error_message, exc_info=True)
            raise AppException(error_message, error_detail=sys.exc_info())
        

