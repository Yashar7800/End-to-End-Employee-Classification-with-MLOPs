from mlProject import logger
from mlProject.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from mlProject.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from mlProject.pipeline.stage_03_data_transformation import DataTransformationPipeline
logger.info('welcome to the custom logging')

STAGE_NAME = "Data Ingestion Stage"

try:
        
    logger.info(f"----->> stage {STAGE_NAME} started <<-----")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f"----->> stage {STAGE_NAME} completed <<----- \n\n")

except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = 'Data Validation Stage'

try:
        
    logger.info(f"----->>>> stage {STAGE_NAME} started <<<<-----")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f"----->>>> stage {STAGE_NAME} completed <<<<----- \n\n")

except Exception as e:
        
        logger.exception(e)
        raise e

STAGE_NAME = 'Data Transformation Stage'

try:
     
    logger.info(f'----->>>>>> stage {STAGE_NAME} started <<<<<<-----')
    data_transformation = DataTransformationPipeline()
    data_transformation.main()
    logger.info(f'----->>>>>> stage {STAGE_NAME} completed <<<<<<----- \n\n')

except Exception as e:
     raise e

