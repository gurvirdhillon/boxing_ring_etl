import sys
import os
import pandas as pd
import subprocess
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.env_config import setup_env
from src.extract.extract import extract_data
from src.utils.logging_utils import setup_logger
from src.transform.clean_boxing_data import boxer_dataset_transformation, fighter_dataset_transformation
from src.load.load import load_fight_dataset

logger = setup_logger("RUN_APP")


def start_streamlit():
    project_root = Path(__file__).resolve().parents[1]
    streamlit_path = project_root / "src" / "streamlit" / "app.py"

    if not streamlit_path.exists():
        logger.error(f"Streamlit app not found at {streamlit_path}")
        return None

    process = subprocess.Popen(
        ["streamlit", "run", str(streamlit_path)],
        stdout=None,
        stderr=None
    )
    logger.info("Streamlit available at launch at http://localhost:8501")
    return process

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_app.py <dev|test|prod>")
        sys.exit(1)
    env = sys.argv[1]
    setup_env(env)
    logger.info(f"ETL pipeline starting in {env} environment...")

    logger.info("Starting EXTRACT stage...")
    df_raw = extract_data()
    logger.info(f"Data successfully loaded")
    logger.info(f"Starting Transformation...")
    df_clean = boxer_dataset_transformation(df_raw.copy())
    output_path = os.path.join("data", "processed", "boxing_match.csv")
    df_clean.to_csv(output_path, index=False)
    logger.info(f"Match dataset cleaned and saved to {output_path}")
    fighter_file = os.path.join("data", "processed", "fighters.csv")
    if os.path.exists(fighter_file):
        logger.info("Starting FIGHTER DATA transformation...")
        df_fighter = pd.read_csv(fighter_file)
        df_fighter_clean = fighter_dataset_transformation(df_fighter.copy())
        fighter_output = os.path.join("data", "processed", "fighters_clean.csv")
        df_fighter_clean.to_csv(fighter_output, index=False)
        logger.info(f"Fighter dataset cleaned and saved to {fighter_output}")
    else:
        logger.warning(f"Fighter dataset not found at {fighter_file}. Skipping fighter transformation.")

    logger.info("Transform complete")
    
    logger.info("Load Process Underway...")
    df = load_fight_dataset()
    df.head()
    
    
    start_streamlit()
    logger.info("ETL complete. Streamlit is running.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Interruption. Shutting off. Goodbye.")

if __name__ == "__main__":
    main()
