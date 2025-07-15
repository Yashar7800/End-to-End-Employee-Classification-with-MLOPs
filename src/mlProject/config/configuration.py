# Next we need to read the Yaml file.then we will write some functions in the constants folder. we define that 3 functionto read the yaml files.
# after that we will import functions like read_yaml, create_directories from utils.common

from mlProject.constants import *
from mlProject.utils.common import read_yaml, create_directories, save_json
from mlProject.entity.config_entity import (DataIngestionConfig, DataValidationConfig,DataTransformationConfig,
                                            ModelTrainerConfig, ModelEvaluationConfig)
from pathlib import Path

class ConfigurationManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,  # these variables like CONFIG_FILE_PATH has come from the constants folder
                 params_filepath = PARAMS_FILE_PATH,
                 schema_filepaht = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepaht)

        create_directories([self.config.artifacts_root]) # here we are creating th artifacts folder | the artifacts_root has come from config.yaml

    def get_data_ingestion_config(self) -> DataIngestionConfig:  # here we have defined our written type
        config = self.config.data_ingestion

        create_directories([config.root_dir])   # the root_dir has come from config.yaml

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file= config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config
    

# Updating configuration manager in src config
# Next we need to read the Yaml file.then we will write some functions in the constants folder. we define that 3 functionto read the yaml files.
# after that we will import functions like read_yaml, create_directories from utils.common

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            unzip_data_dir = config.unzip_data_dir,
            root_dir = config.root_dir,
            STATUS_FILE= config.STATUS_FILE,
            all_schema= schema

        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path
        )

        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.GradientBoostingClassifier
        schema = self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path= config.data_path,
            preprocessor_path= config.preprocessor_path,
            model_path= config.model_path,
            n_estimators= params.n_estimators,
            learning_rate= params.learning_rate,
            max_depth= params.max_depth,
            target_column= schema.name
        )

        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params.GradientBoostingClassifier
        schema = self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir = config.root_dir,
            data_path = config.data_path,
            preprocessor_path= config.preprocessor_path,
            model_path = config.model_path,
            all_params = params,
            metric_file_name = config.metric_file_name,
            target_column = schema.name,
            mlflow_uri = "https://dagshub.com/Yashar7800/End-to-End-Employee-Classification-with-MLOPs.mlflow"
        )

        return model_evaluation_config