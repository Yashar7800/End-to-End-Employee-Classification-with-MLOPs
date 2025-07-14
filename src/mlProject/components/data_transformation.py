import os
from mlProject import logger
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
import joblib
import pandas as pd
from mlProject.entity.config_entity import DataTransformationConfig
from pathlib import Path

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def data_preparation(self):
        data = pd.read_csv(self.config.data_path)
        data['Tenure'] = 2025 - data['JoiningYear']

        X = data.drop("LeaveOrNot", axis=1)
        y = data["LeaveOrNot"]

        logger.info("splitting the data into dependet and independent variables")
        logger.info(X.shape)
        logger.info(y.shape)

        print(X.shape)
        print(y.shape)

        # Define preprocessor
        categorical_nominal = ["City", "Gender", "EverBenched"]
        categorical_ordinal = ["Education"]
        numerical_cols = ["JoiningYear", "PaymentTier", "Age", "ExperienceInCurrentDomain", "Tenure"]
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat_nominal", OneHotEncoder(handle_unknown="ignore"), categorical_nominal),
                ("cat_ordinal", OrdinalEncoder(categories=[["Bachelors", "Masters", "PHD"]]), categorical_ordinal),
                ("num", "passthrough", numerical_cols)
            ]
        )

        # Fit preprocessor (to be used in training)
        preprocessor.fit(X)

        # Save preprocessor
        joblib.dump(preprocessor, os.path.join(self.config.root_dir,'preprocessor.pkl'))
        logger.info("the Preprocessor is saved successfully! ")

    
