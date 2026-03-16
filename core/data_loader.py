import pandas as pd
import os
from core.config import (
    DEGREES_DATASET_PATH, 
    SALARY_DATASET_PATH, 
    DEMAND_DATASET_PATH,
    SKILLS_DATASET_PATH,
    PATHS_DATASET_PATH,
    TRENDS_DATASET_PATH
)

class DataValidationError(Exception):
    pass

def validate_dataframe(df, required_columns, table_name):
    """Checks if required columns are present in the dataframe."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise DataValidationError(f"Missing columns in {table_name}: {', '.join(missing)}")
    return True

def load_csv(path, required_columns, table_name):
    """Generic CSV loader with validation."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{table_name} not found at {path}")
    df = pd.read_csv(path)
    validate_dataframe(df, required_columns, table_name)
    return df

def load_degrees():
    return load_csv(DEGREES_DATASET_PATH, ["stream", "degree", "domain", "industry"], "degrees_dataset.csv")

def load_salary():
    return load_csv(SALARY_DATASET_PATH, ["degree", "median_salary_lpa", "salary_range_lpa", "source"], "salary_dataset.csv")

def load_demand():
    return load_csv(DEMAND_DATASET_PATH, ["domain", "demand_growth_percent", "hiring_volume_score", "evidence", "primary_source"], "demand_dataset.csv")

def load_skills():
    return load_csv(SKILLS_DATASET_PATH, ["degree", "top_job_roles", "top_skills"], "career_skills_dataset.csv")

def load_paths():
    return load_csv(PATHS_DATASET_PATH, ["degree", "career_path"], "degree_career_paths.csv")

def load_trends():
    return load_csv(TRENDS_DATASET_PATH, ["domain", "industry_growth_projection", "automation_risk", "emerging_skills"], "domain_industry_trends.csv")

def load_all_datasets():
    """Loads and returns all datasets as a dictionary of dataframes."""
    return {
        "degrees": load_degrees(),
        "salary": load_salary(),
        "demand": load_demand(),
        "skills": load_skills(),
        "paths": load_paths(),
        "trends": load_trends()
    }
