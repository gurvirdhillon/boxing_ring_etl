import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.env_config import setup_env
from src.extract.extract import extract_data
from src.utils.logging_utils import setup_logger

logger = setup_logger("RUN_APP")

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_app.py <dev|test|prod>")
        sys.exit(1)
    env = sys.argv[1]
    setup_env(env)
    logger.info(f"ETL pipeline starting in {env} environment...")

    logger.info("\n🔹 Starting EXTRACT stage...")
    df_raw = extract_data()
    logger.info(f"Data successfully loaded")
    return df_raw
if __name__ == "__main__":
    main()
