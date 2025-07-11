# Next we need to read the Yaml file.then we will write some functions in the constants folder. we define that 3 functionto read the yaml files.
# after that we will import functions like read_yaml, create_directories from utils.common

from mlProject.constants import *
from mlProject.utils.common import read_yaml, create_directories
from mlProject.entity.config_entity import DataIngestionConfig

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