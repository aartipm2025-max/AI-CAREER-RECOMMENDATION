import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset paths
DEGREES_DATASET_PATH = os.path.join(BASE_DIR, "datasets", "degrees_dataset.csv")
SALARY_DATASET_PATH = os.path.join(BASE_DIR, "datasets", "salary_dataset.csv")
DEMAND_DATASET_PATH = os.path.join(BASE_DIR, "datasets", "demand_dataset.csv")
SKILLS_DATASET_PATH = os.path.join(BASE_DIR, "datasets", "career_skills_dataset.csv")
PATHS_DATASET_PATH = os.path.join(BASE_DIR, "datasets", "degree_career_paths.csv")
TRENDS_DATASET_PATH = os.path.join(BASE_DIR, "datasets", "domain_industry_trends.csv")

# LLM Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Ranking Weights
WEIGHT_SALARY = 0.5
WEIGHT_DEMAND_GROWTH = 0.3
WEIGHT_HIRING_VOLUME = 0.2

# Streams
VALID_STREAMS = ["Science", "Commerce", "Arts"]
