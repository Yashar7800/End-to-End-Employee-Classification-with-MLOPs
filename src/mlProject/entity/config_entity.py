# The same variables from the config.yaml is here like root_dir, source_url, local_data_file, unzip_dir
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
  
    root_dir: Path
    source_URL: Path
    local_data_file: Path 
    unzip_dir: Path 