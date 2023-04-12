import logging
from logging.handlers import RotatingFileHandler
# from flask import Flask

# app = Flask(__name__)

# Configure logging
log_filename = 'app.log'  # Update with the desired log file name
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 10  # Number of backup log files to keep

# Create a rotating file handler to log to a file
file_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count)
file_handler.setLevel(logging.DEBUG)  # Set the log level (e.g., DEBUG, INFO, ERROR)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# app.logger.addHandler(file_handler)

# # Set the logging level for Flask app.logger
# app.logger.setLevel(logging.DEBUG)  # Set the log level (e.g., DEBUG, INFO, ERROR)



# # Log a message with the DEBUG level
# app.logger.debug('This is a debug message')

# # Log a message with the INFO level
# app.logger.info('This is an info message')

# # Log a message with the ERROR level
# app.logger.error('This is an error message')
