import json
import os
import logging
from logging.handlers import RotatingFileHandler
import yaml

class JsonEncoder(json.JSONEncoder):
    
    def default(self, obj):
        
        if isinstance(obj, set):
            return list(obj)
        
        return json.JSONEncoder.default(self, obj)
    
class JsonLoader:

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    @staticmethod
    def save(file_path, data):
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file)


class CsvService:
    """handle csv function"""
    @staticmethod
    def is_csv_file(file_path: str) -> bool:
        """determine csv file"""
        _, file_ext = os.path.splitext(file_path)

        return file_ext.lower() == '.csv'

class Logger:
    # Load logger configuration from a YAML file
    with open('./utils/logger_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    loggers = {}
    @classmethod
    def setup_logger(cls, name=None):

        if name in cls.loggers:
            return cls.loggers[name]

        """Set up and return a logger with the name provided."""
        if name:
            log_config = cls.config.get(name, {})
            if not log_config:
                raise ValueError(f"No logger configuration found for '{name}'")
        else:
            log_config = cls.config.get('info', {})

        log_file = log_config.get('log_file', 'default.log')
        level = log_config.get('level', logging.INFO)
        format = log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s')
        
        formatter = logging.Formatter(format)
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=log_config.get('maxBytes', 1024 * 1024 * 100), 
            backupCount=log_config.get('backupCount', 20)
        )
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if not logger.handlers:
            logger.addHandler(handler)

        # Store the configured logger in the dictionary
        cls.loggers[name] = logger

        return logger
    
    #TODO: migration to cloud watch
    # import watchtower
    # def setup_logger(cls, name):
    #     logger = logging.getLogger(name)
    #     logger.setLevel(logging.INFO)

    #     # Create a CloudWatch handler
    #     cw_handler = watchtower.CloudWatchLogHandler()
    #     logger.addHandler(cw_handler)

    #     return logger