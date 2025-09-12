import logging
from config import load_config
from alarm_engine import AlarmEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting TESTPROJ application...")
    config = load_config()
    if config is None:
        logging.error("Failed to load configuration. Exiting.")
        return

    engine = AlarmEngine(config)
    engine.run()

if __name__ == "__main__":
    main()
