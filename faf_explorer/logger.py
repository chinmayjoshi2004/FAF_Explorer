"""
FAF Explorer Logging System
Professional logging configuration with multiple handlers and levels
"""

import logging
import logging.handlers
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime


class FAFLogger:
    """Professional logging system for FAF Explorer"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        self._setup_logger()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default logging configuration"""
        return {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "date_format": "%Y-%m-%d %H:%M:%S",
            "file_logging": True,
            "console_logging": True,
            "log_directory": "logs",
            "max_file_size": 10 * 1024 * 1024,  # 10MB
            "backup_count": 5,
            "encoding": "utf-8"
        }

    def _setup_logger(self) -> None:
        """Setup the logging system"""
        # Create logger
        self.logger = logging.getLogger('faf_explorer')
        self.logger.setLevel(getattr(logging, self.config['level'].upper()))

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create formatters
        formatter = logging.Formatter(
            self.config['format'],
            datefmt=self.config['date_format']
        )

        # Console handler
        if self.config['console_logging']:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # File handler with rotation
        if self.config['file_logging']:
            log_dir = Path(self.config['log_directory'])
            log_dir.mkdir(exist_ok=True)

            log_file = log_dir / f"faf_explorer_{datetime.now().strftime('%Y%m%d')}.log"

            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=self.config['max_file_size'],
                backupCount=self.config['backup_count'],
                encoding=self.config['encoding']
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self, name: str = "") -> logging.Logger:
        """Get a logger instance"""
        if name:
            return self.logger.getChild(name)
        return self.logger

    def log_operation_start(self, operation: str, **kwargs) -> None:
        """Log the start of an operation"""
        extra = {"operation": operation, **kwargs}
        self.logger.info(f"Starting operation: {operation}", extra=extra)

    def log_operation_end(self, operation: str, success: bool = True, **kwargs) -> None:
        """Log the end of an operation"""
        status = "completed" if success else "failed"
        level = logging.INFO if success else logging.ERROR
        extra = {"operation": operation, "status": status, **kwargs}
        self.logger.log(level, f"Operation {operation} {status}", extra=extra)

    def log_file_operation(self, operation: str, file_path: str, **kwargs) -> None:
        """Log file operations with path information"""
        extra = {"operation": operation, "file_path": str(file_path), **kwargs}
        self.logger.info(f"File operation: {operation} on {file_path}", extra=extra)

    def log_error(self, error: Exception, operation: str = "", **kwargs) -> None:
        """Log exceptions with context"""
        extra = {"operation": operation, "error_type": type(error).__name__, **kwargs}
        self.logger.error(f"Error in {operation}: {str(error)}", exc_info=True, extra=extra)

    def log_performance(self, operation: str, duration: float, **kwargs) -> None:
        """Log performance metrics"""
        extra = {"operation": operation, "duration": duration, **kwargs}
        self.logger.info(".2f", extra=extra)

    def set_level(self, level: str) -> None:
        """Change logging level"""
        self.logger.setLevel(getattr(logging, level.upper()))
        self.config['level'] = level

    def enable_file_logging(self, enable: bool = True) -> None:
        """Enable or disable file logging"""
        self.config['file_logging'] = enable
        self._setup_logger()  # Recreate handlers

    def enable_console_logging(self, enable: bool = True) -> None:
        """Enable or disable console logging"""
        self.config['console_logging'] = enable
        self._setup_logger()  # Recreate handlers


# Global logger instance
_logger_instance: Optional[FAFLogger] = None


def get_logger(name: str = "") -> logging.Logger:
    """Get the global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = FAFLogger()
    return _logger_instance.get_logger(name)


def setup_logging(config: Optional[Dict[str, Any]] = None) -> FAFLogger:
    """Setup the global logging system"""
    global _logger_instance
    _logger_instance = FAFLogger(config)
    return _logger_instance


def log_function_call(func_name: str, args: tuple = (), kwargs: dict = None) -> None:
    """Decorator helper to log function calls"""
    kwargs = kwargs or {}
    logger = get_logger()
    args_str = ", ".join(repr(arg) for arg in args)
    kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
    params = ", ".join(filter(None, [args_str, kwargs_str]))
    logger.debug(f"Calling {func_name}({params})")


# Context manager for operation logging
class OperationLogger:
    """Context manager for logging operations"""

    def __init__(self, operation: str, **kwargs):
        self.operation = operation
        self.kwargs = kwargs
        self.logger = get_logger()
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.log_operation_start(self.operation, **self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        success = exc_type is None

        if not success and exc_val:
            self.logger.log_error(exc_val, self.operation, **self.kwargs)

        self.logger.log_operation_end(self.operation, success, duration=duration, **self.kwargs)


# Performance monitoring decorator
def log_performance(logger_name: str = ""):
    """Decorator to log function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            logger = get_logger(logger_name)

            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.log_performance(func.__name__, duration)
                return result
            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.error(f"Function {func.__name__} failed after {duration:.2f}s: {e}")
                raise
        return wrapper
    return decorator


# Initialize default logging on import
setup_logging()
