from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_ingestion import DataIngestion
from mlProject import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        
        config = ConfigurationManager() # configuration manager
        data_ingestion_config = config.get_data_ingestion_config() # configuration manager
        data_ingestion = DataIngestion(config=data_ingestion_config) # components
        data_ingestion.download_file() # components
        data_ingestion.extract_zip_file() # components

        
if __name__ == '__main__':
    try:
        logger.info(f"----->> stage {STAGE_NAME} started <<-----")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f"----->> stage {STAGE_NAME} completed <<----- \n\n")

    except Exception as e:
        logger.exception(e)
        raise e
    
