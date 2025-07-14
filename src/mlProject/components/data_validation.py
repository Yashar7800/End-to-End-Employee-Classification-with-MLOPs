# Updating the components
import pandas as pd
from mlProject.entity.config_entity import DataValidationConfig
import os
from mlProject import logger


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            # Read the CSV file
            data = pd.read_csv(self.config.unzip_data_dir)
            
            # Get columns from CSV and schema
            all_cols = set(data.columns)
            schema_cols = set(self.config.all_schema.keys())
            
            # Check if columns match exactly
            validation_status = (all_cols == schema_cols)
            
            # If columns match, check data types
            if validation_status:
                for col in all_cols:
                    expected_dtype = self.config.all_schema[col]
                    actual_dtype = data.dtypes[col].name
                    if actual_dtype != expected_dtype:
                        validation_status = False
                        break
            
            # Write validation status to file
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")
            
            return validation_status
        
        except Exception as e:
            raise e
            
