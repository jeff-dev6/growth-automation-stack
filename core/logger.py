import logging
import os
from datetime import datetime

def get_logger(module_name):
    """
    Creates the logger that writes to both the 
    terminal and a permanent log file.

    """

    # Ensure the 'logs' directory exists at the project root.
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.mkdirs(logs_dir)

    # Initialize the logger for the specific module
    logger = logging.getLogger(module_name)
    logger.setlevel(logging.INFO)

    # Format how the logs are viewed.
    # File format: Detailed for debugging (Date - Name - Level - Message)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console format: Clean for in real-time viewing
    console_format = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')

    # Create the Handlers (Where the logs go)

    # File Handler: Appends logs to 'logs/growth-automation-stack.log'
    file_handler = logging.FileHandler(logs_dir, "growth-automation-stack.logs")
    file_handler.setFormatter(file_format)

    # Console Handler: Prints logs to the VS Code terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_format)

    # Add Handlers to the logger (Only if they aren't already there)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger



