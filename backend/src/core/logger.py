"""Structured logging configuration"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


def setup_logger(
    name: str = "news_aggregator",
    level: str = "INFO",
    log_file: str = None
) -> logging.Logger:
    """
    Set up structured logger with JSON formatting
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    return logger


class LogContext:
    """Context manager for adding extra fields to logs"""
    
    def __init__(self, logger: logging.Logger, **kwargs):
        self.logger = logger
        self.extra_fields = kwargs
        self.old_factory = None
    
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            record.extra_fields = self.extra_fields
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)


# Default logger instance
logger = setup_logger()
