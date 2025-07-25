from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_transformation import DataTransformation
from mlProject import logger
from pathlib import Path

STAGE_NAME = "Data Transformation stage"

class DataTransformationPipeline:
    def __init__(self):
       pass 
        
    def main(self):
        try:
            with open(Path('artifacts/data_validation/status.txt'),'r') as f:
                status = f.read().split(' ')[-1]

            if status == 'True':
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.data_preparation()

            else:
                raise Exception('Your data Schema is not VALID!')
            
        except Exception as e:
            print(e)

if __name__ == '__main__':
    try:
        logger.info(f'>>>> stage {STAGE_NAME} started <<<<<<')
        obj = DataTransformationPipeline()
        obj.main()
        logger.info(f'>>>>> stage {STAGE_NAME} completed <<<< \n\nx============x')
    except Exception as e:
        logger.exception(e)
        raise e