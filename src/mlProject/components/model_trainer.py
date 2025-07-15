from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import GradientBoostingClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import f1_score
import pandas as pd
import joblib
from mlProject import logger
from mlProject.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self,config: ModelTrainerConfig):
        self.config = config

    def train(self):
        data = pd.read_csv('artifacts/data_ingestion/Employee.csv')
        data["Tenure"] = 2025 - data["JoiningYear"]  # Add derived feature
        X = data.drop("LeaveOrNot", axis=1)
        y = data["LeaveOrNot"]
        preprocessor = joblib.load('artifacts/data_transformation/preprocessor.pkl')

        # Define stratified k-fold
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        # Define GBC with best parameters
        gbc = GradientBoostingClassifier(
            n_estimators=self.config.n_estimators,
            learning_rate=self.config.learning_rate,
            max_depth=self.config.max_depth,
            random_state=42
        )
        # Define the model
        model = ImbPipeline([
            ('preprocessor',preprocessor),
            ('smote',SMOTE(random_state=42)),
            ('classifier',gbc)
        ])

        model.fit(X,y)

        # Save model
        model_path = "artifacts/model_trainer/model_gbc_tuned.joblib"
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")