import sys

from wasteDetection.logger import logging
from wasteDetection.exception import AppException

from wasteDetection.pipeline.training_pipeline import TrainingPipeline

obj = TrainingPipeline()
obj.run_pipeline()

