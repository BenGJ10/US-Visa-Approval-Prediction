import sys

from usvisa.logger.logger import logging
from usvisa.exception.exception import UsVisaException
from usvisa.entity.s3_estimator import UsVisaEstimator
from usvisa.cloud.aws_storage import SimpleStorageService
from usvisa.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact
from usvisa.entity.config_entity import ModelPusherConfig

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = UsVisaEstimator(bucket_name = self.model_pusher_config.bucket_name,
                                                model_path = self.model_pusher_config.s3_model_key_path)
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            self.usvisa_estimator.save_model(from_file = self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(bucket_name = self.model_pusher_config.bucket_name,
                                                        s3_model_path = self.model_pusher_config.s3_model_key_path)
            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            return model_pusher_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)