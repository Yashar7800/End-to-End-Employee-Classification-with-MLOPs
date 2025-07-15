# The same variables from the config.yaml is here like root_dir, source_url, local_data_file, unzip_dir
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
  
    root_dir: Path
    source_URL: str
    local_data_file: Path 
    unzip_dir: Path 


@dataclass(frozen=True)
class DataValidationConfig:
  
    root_dir: Path
    unzip_data_dir: Path
    STATUS_FILE: str
    all_schema: dict

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    preprocessor_path: Path
    model_path: Path
    n_estimators: float
    learning_rate: int
    max_depth: int   # will define parameters in params.yaml
    target_column: str  # will get target column from schema.yaml


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    data_path: Path
    preprocessor_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str